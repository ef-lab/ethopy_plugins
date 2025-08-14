# BpodPorts Interface for EthoPy

## Overview

The `BpodPorts` interface integrates Bpod behavioral hardware with the EthoPy experimental framework. It provides real-time event detection, liquid reward delivery, and while maintaining compatibility with EthoPy's database-driven configuration system.

## System Requirements

- **Python**: tested with Python 3.8
- **Hardware**: Bpod State Machine r0.5.1
- **Firmware**: Bpod StateMachine Firmware v22
- **Dependencies**: pybpod-api, ethopy

## Hardware Setup Guide

### Step 1: Bpod Firmware Installation

Before using the BpodPorts interface, you must install the correct firmware on your Bpod device.

#### Required Firmware
- **Version**: StateMachine Firmware v22 for Bpod r0.5
- **Source**: https://github.com/sanworks/Bpod_StateMachine_Firmware/tree/v23/Preconfigured/v22/StateMachine-Bpod0_5

#### Installation Steps

1. **Download the firmware**:
   ```bash
   git clone https://github.com/sanworks/Bpod_StateMachine_Firmware.git
   cd Bpod_StateMachine_Firmware/Preconfigured/v22/StateMachine-Bpod0_5/
   ```

2. **Install Arduino IDE** (if not already installed):
   - Download from: https://www.arduino.cc/en/software

3. **Upload firmware to Bpod**:
   - Connect Bpod to computer via **USB port labeled "PROGRAM"** or **"USB1"**
   - Open `StateMachine-Bpod0_5.ino` in Arduino IDE
   - Select correct board type:
     - **Bpod r0.5**: Arduino Uno/Nano
   - Select correct COM port for programming
   - Click **Upload** button
   - Wait for "Upload Complete" message
   - more details [here](https://sites.google.com/site/bpoddocumentation/firmware-update/state-machine?authuser=0)

4. **Switch USB ports for operation**:
   - **Disconnect** from programming USB port
   - **Connect** to the **serial communication USB port**
   - This port will be used for all subsequent communication

### Step 2: Serial Port Detection

After firmware installation, identify the serial communication port:

```bash
# List all available serial ports
ls /dev/tty*

# Look for devices like:
# /dev/ttyACM0, /dev/ttyACM1  (Arduino/USB-CDC devices)
# /dev/ttyUSB0, /dev/ttyUSB1  (USB-serial adapters)

# Check USB device information
lsusb

# Monitor port changes when plugging/unplugging Bpod
dmesg | grep tty  # Watch for new device messages
```

### Step 3: Permissions Setup

Grant your user access to serial ports:

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Logout and login for group changes to take effect
```

## Software Integration

### Step 4: Install Dependencies

Install the required Python packages:

```bash
# Install pybpod-api
pip install pybpod-api

# Install EthoPy (if not already installed)
pip install ethopy

# Install additional dependencies
pip install pyserial numpy
```

### Step 5: Test Basic Connection

Verify that your Bpod device communicates correctly:

```python
# Test basic pybpod connection
from pybpodapi.bpod import Bpod

try:
    # Replace with your serial port
    bpod = Bpod(serial_port='/dev/ttyACM0')
    
    print(f"✅ Connected to Bpod on {bpod.serial_port}")
    print(f"📊 Firmware version: {bpod.hardware.firmware_version}")
    print(f"🔧 Hardware info: {bpod.hardware}")
    
    bpod.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("Check:")
    print("- Serial port path is correct")
    print("- Bpod firmware is installed")
    print("- USB cable is connected to communication port")
    print("- User permissions for serial port")
    print("- Try pressing in arduino the RESET button near the USB port and reconnect")
```

## Features

- **Non-blocking event detection** - Background monitoring of all Bpod inputs
- **Real-time processing** - Events processed immediately via `loop_handler()`
- **Liquid reward delivery** - Automated valve control with calibration support
- **Multi-port support** - Handles behavior ports and wire connections
- **Thread-safe operations** - Prevents state machine conflicts
- **No user_settings.py required** - Configuration via environment variables or EthoPy config


## Code Architecture Deep Dive

### 1. Bpod State Machine System

The BpodPorts interface uses Bpod's finite state machine architecture for both event monitoring. Understanding this system is crucial for behavioral experiments.

#### Bpod State Machine

**1. Monitoring Mode (Background Thread)**
```python
def _monitoring_loop(self):
    """Continuous background monitoring"""
    sma = StateMachine(self)
    
    # Create looping state that captures ALL events
    sma.add_state(
        state_name="Monitor",
        state_timer=0.1,  # 0.1-second cycles
        state_change_conditions={
            EventName.Tup: "Monitor",        # Loop back on timeout
            EventName.Port1In: "Monitor",    # Loop back on Port1 entry
            EventName.Port1Out: "Monitor",   # Loop back on Port1 exit
            EventName.Port2In: "Monitor",    # Loop back on Port2 entry
            # ... all other ports and events ...
        },
        output_actions=[]  # No hardware actions, just monitoring
    )
    
    # This runs continuously, calling loop_handler() for each event
    self.send_state_machine(sma)
    self.run_state_machine(sma)
```

**2. Action Mode (Liquid Delivery)**
```python
def _deliver_liquid(self, port: int, duration: float):
    """Dedicated state machine for valve control"""
    sma = StateMachine(self)
    
    # Simple state: open valve, wait, then exit
    sma.add_state(
        state_name="DeliverReward",
        state_timer=(duration / 1000.0),  # Convert ms to seconds
        state_change_conditions={
            EventName.Tup: "exit"  # Exit when timer expires
        },
        output_actions=[("Valve", port)]  # Open valve for specified port
    )
    
    # Run once and exit
    self.send_state_machine(sma)
    self.run_state_machine(sma)
```

### 2. Event Detection Mechanism

#### Hardware Event Types

**Behavior Ports (Lick Detection)**
- **Port1In, Port2In, ..., Port8In**: Beam break or sensor activation (animal enters)
- **Port1Out, Port2Out, ..., Port8Out**: Beam restoration (animal exits)
- **Physical Setup**: Infrared beam or capacitive sensor at port entrance


#### Real-time Event Processing Flow

```python
def loop_handler(self):
    """Called by Bpod during state machine execution"""
    
    # 1. Check if new events occurred in current trial
    current_trial = self.session.current_trial
    current_event_count = len(current_trial.events_occurrences)
    
    if current_event_count > self._last_event_count:
        # 2. Get only NEW events since last check
        new_events = current_trial.events_occurrences[self._last_event_count:]
        
        # 3. Process each event immediately
        for event_obj in new_events:
            self._process_realtime_event(event_obj)
        
        # 4. Update counter for next iteration
        self._last_event_count = current_event_count
```

### 3. Port Activation Logic

#### Lick Port Detection
```python
def _handle_lick_event(self, port_num: int, timestamp: float):
    """
    Handle lick port activation.

    Args:
        port_num: Port number that was activated
        timestamp: Event timestamp
    """
    # Find matching port in configuration
    lick_port = None
    for port in self.ports:
        if port.type == "Lick" and port.port == port_num:
            lick_port = port
            break

    if lick_port:
        self.response = lick_port
        self.resp_tmst = self.logger.logger_timer.elapsed_time()

        # Log activity through EthoPy behavior system
        if hasattr(self, "beh") and self.beh:
            self.beh.log_activity(
                {
                    **lick_port.__dict__,
                    "time": self.resp_tmst,
                    "bpod_timestamp": timestamp,
                }
            )

        log.debug(f"🐭 Lick detected on port {port_num}")

```

#### Proximity Sensor Logic
```python
def _handle_proximity_event(self, sensor_num: int, active: bool, timestamp: float):
    """
    Handle proximity sensor activation.

    Args:
        sensor_num: Sensor number
        active: True if sensor activated, False if deactivated
        timestamp: Event timestamp
    """
    # Find matching proximity port
    prox_port = None
    for port in self.ports:
        if port.type == "Proximity" and port.port == sensor_num:
            prox_port = port
            break

    if prox_port:
        if active and not self.ready:
            # Animal entered position
            self.timer_ready.start()
            self.ready = True
            self.position = prox_port
            self.position_tmst = self.beh.log_activity(
                {
                    **prox_port.__dict__,
                    "in_position": 1,
                    "bpod_timestamp": timestamp,
                }
            )
            log.debug(f"🐭 Animal in position (sensor {sensor_num})")

        elif not active and self.ready:
            # Animal left position
            self.ready = False
            tmst = self.beh.log_activity(
                {
                    **prox_port.__dict__,
                    "in_position": 0,
                    "bpod_timestamp": timestamp,
                }
            )
            self.position_dur = tmst - self.position_tmst
            log.debug(f"🐭 Animal left position (sensor {sensor_num})")

```

### 4. Valve Control System

#### Hardware Setup
- **Solenoid Valves**: Electronically controlled liquid dispensers
- **Port Mapping**: Each reward port connects to a specific valve number
- **Timing Critical**: Precise duration control for accurate volumes

#### Valve Operation Flow
```python
def give_liquid(self, port: int, duration: Optional[float] = None):
    """Public interface for liquid delivery"""
    
    # 1. Get calibrated duration if not specified
    if not duration:
        duration = self.duration.get(port, 50)  # Default 50ms
    
    # 2. Execute in thread pool to avoid blocking main experiment
    self.thread.submit(self._deliver_liquid, port, duration)

def _deliver_liquid(self, port: int, duration: float):
    """Thread-safe valve control implementation"""
    
    # 1. CRITICAL: Pause monitoring to prevent state machine conflicts
    self.pause_monitoring()
    
    try:
        # 2. Acquire exclusive lock for state machine
        with self._state_machine_lock:
            
            # 3. Create dedicated liquid delivery state machine
            sma = StateMachine(self)
            sma.add_state(
                state_name="DeliverReward",
                state_timer=(duration / 1000.0),  # Convert ms to seconds
                state_change_conditions={
                    EventName.Tup: "exit"  # Exit when timer expires
                },
                output_actions=[("Valve", port)]  # Hardware command: open valve
            )
            
            # 4. Execute valve control
            self.send_state_machine(sma)  # Upload to Bpod hardware
            self.run_state_machine(sma)   # Execute on hardware
            
            # 5. Valve automatically closes when state exits
            
    finally:
        # 6. ALWAYS resume monitoring, even if error occurred
        self.resume_monitoring()

def give_liquid(self, port: int, duration: Optional[float] = None):
    """
    Deliver liquid reward through specified port.

    Args:
        port: Port number for delivery
        duration: Duration in milliseconds (uses calibrated value if None)
    """
    # 1. Execute in thread pool to avoid blocking main experiment
    self.thread.submit(self._deliver_liquid, port, duration)

def _deliver_liquid(self, port: int, duration: float):
    """
    Internal method to deliver liquid reward.

    Args:
        port: Port number
        duration: Duration in milliseconds
    """
    # Validate inputs
    if not port or not isinstance(port, int):
        log.error(f"Invalid port for liquid delivery: {port}")
        return

    # 1. CRITICAL: Pause monitoring to prevent state machine conflicts
    self.pause_monitoring()

    try:
        # Wait for monitoring to actually pause and acquire lock
        with self._state_machine_lock:
            # Create liquid delivery state machine
            sma = StateMachine(self)

            # Add liquid delivery state
            sma.add_state(
                state_name="DeliverReward",
                # Convert to seconds, default 50ms
                state_timer=(duration / 1000.0) if duration else 0.050,
                state_change_conditions={EventName.Tup: "exit"},
                output_actions=[("Valve", port)] if port else [
                ],  # Open valve
            )

            # Send and run with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.send_state_machine(sma)
                    self.run_state_machine(sma)
                    log.info(f"Delivered {duration}ms liquid on port {port}")
                    break  # Success, exit retry loop
                except Exception as retry_e:
                    if attempt < max_retries - 1:
                        log.warning(f"Retry {attempt + 1}/{max_retries} for liquid delivery: {retry_e}")
                        time.sleep(0.1)  # Brief delay before retry
                    else:
                        raise  # Re-raise on final attempt

    except Exception as e:
        log.error(f"Error delivering liquid reward: {e}")
    finally:
        # Always resume monitoring
        self.resume_monitoring()

```

### 5. Non-Blocking Threading Architecture

**Background Monitoring Thread**
```python
def _monitoring_loop(self):
    """Daemon thread - runs continuously until program exits"""
    while self.is_monitoring:
        # This thread NEVER blocks the main experiment
        try:
            # Run monitoring state machine
            with self._state_machine_lock:
                sma = StateMachine(self)
                # ... setup monitoring state
                self.run_state_machine(sma)  # Calls loop_handler() automatically
                
        except Exception as e:
            log.error(f"Monitoring error: {e}")
            time.sleep(0.5)  # Brief pause, then retry
```


#### Thread Synchronization

**Critical Section Protection:**
```python
# Only ONE thread can use Bpod state machine at a time
self._state_machine_lock = threading.Lock()

def _deliver_liquid(self, port, duration):
    # Prevent monitoring thread from interfering
    self.pause_monitoring()  # Signal monitoring to pause
    
    try:
        with self._state_machine_lock:  # Exclusive access
            # Safe to use state machine here
            sma = StateMachine(self)
            # ... valve control logic
    finally:
        self.resume_monitoring()  # Always resume
```

#### Benefits of This Architecture

1. **Real-time Responsiveness**: Events detected with ms latency
2. **Non-blocking Operations**: Experiment never freezes waiting for hardware
3. **Concurrent Processing**: Multiple stimuli can be delivered simultaneously
4. **Robust Error Handling**: One thread failure doesn't crash entire system

This threading model is essential for behavioral experiments where timing precision and responsiveness are critical for valid scientific data collection.

## Hardware Configuration

### Bpod Variable Definitions

The interface automatically configures the following pybpod-api variables:

#### Essential Hardware Settings
| Variable | Purpose | Default | Environment Variable |
|----------|---------|---------|----------------------|
| `PYBPOD_SERIAL_PORT` | Serial port path (e.g., `/dev/ttyACM0`) | `"/dev/ttyACM0"` | `PYBPOD_SERIAL_PORT` |
| `BPOD_BNC_PORTS_ENABLED` | Which BNC connectors are active | `[True, True]` | `BPOD_BNC_PORTS_ENABLED` |
| `BPOD_WIRED_PORTS_ENABLED` | Which wire inputs are active | `[True, True]` | `BPOD_WIRED_PORTS_ENABLED` |
| `BPOD_BEHAVIOR_PORTS_ENABLED` | Which behavior ports are active | `[True, True, True, True, True, True, True, True]` | `BPOD_BEHAVIOR_PORTS_ENABLED` |

#### Communication Settings
| Variable | Purpose | Default | Environment Variable |
|----------|---------|---------|----------------------|
| `PYBPOD_BAUDRATE` | Serial communication speed | `1312500` | `PYBPOD_BAUDRATE` |

#### Logging Settings
| Variable | Purpose | Default | Environment Variable |
|----------|---------|---------|----------------------|
| `PYBPOD_API_LOG_LEVEL` | Logging verbosity | `"INFO"` | `PYBPOD_API_LOG_LEVEL` |
| `PYBPOD_API_LOG_FILE` | Log file name | `"pybpod-api.log"` | `PYBPOD_API_LOG_FILE` |

### Port Types and Functions

#### Behavior Ports (1-8)
- **Purpose**: Nose poke detection, lick sensors
- **Events**: `Port1In`, `Port1Out`, `Port2In`, `Port2Out`, etc.
- **Usage**: Animal interaction monitoring

#### Wire Ports (1-4)
- **Purpose**: Direct digital I/O
- **Events**: `Wire1High`, `Wire1Low`, `Wire2High`, `Wire2Low`
- **Usage**: Custom digital sensors, triggers

## Configuration Methods

### Method 1: Environment Variables (Example)

```bash
# Essential configuration
export PYBPOD_SERIAL_PORT="/dev/ttyACM0"

# Optional: Enable specific ports
export BPOD_BNC_PORTS_ENABLED="[True, True]"
export BPOD_BEHAVIOR_PORTS_ENABLED="[True, True, True, False, False, False, False, False]"

# Optional: Logging
export PYBPOD_API_LOG_LEVEL="DEBUG"

# Run your experiment
```

### Method 2: EthoPy Configuration

Add to your `local_conf.json`:

```json
{
  "PYBPOD_SERIAL_PORT": "/dev/ttyACM0",
  "Channels": {
    "Lick": {1: 1, 2: 2, 3: 3},
    "Liquid": {1: 1, 2: 2},
    "Proximity": {1: 1},
    "Sound": {1: 1},
    "Sync": {"out": 1, "in": 2}
  },
  "PYBPOD_API_LOG_LEVEL": "INFO"
}
```

## Database Integration

### Required Database Tables

The `BpodPorts` interface integrates with EthoPy's database configuration system. Add the following to your database:

#### 1. SetupConfiguration Table

First, add BpodPorts as an available interface option in your EthoPy database:

```python
from ethopy.core.interface import SetupConfiguration

# Check existing interfaces
existing_interfaces = SetupConfiguration.fetch()
print("Current interfaces:", existing_interfaces)

# Add BpodPorts interface (choose an unused setup_conf_idx)
setup_conf_idx = 1  # Choose your setup configuration ID

# Insert the BpodPorts interface configuration
SetupConfiguration.insert1([
    setup_conf_idx,                              # Setup configuration index  
    'BpodPorts',                                # Interface class name
    'Bpod Hardware Interface for EthoPy'        # Description
])

print(f"✅ Added BpodPorts interface with setup_conf_idx = {setup_conf_idx}")
```

**Important Notes:**
- Choose a unique `setup_conf_idx` that's not already in use
- The interface name must match the class name exactly: `'BpodPorts'`
- This makes BpodPorts available for experiments using `setup_conf_idx = 1`

#### 2. SetupConfiguration.Port Table

Define your hardware ports:

```python
# Example port configuration
ports_config = [
    # [port, type, setup_conf_idx, ready, response, reward, invert, description]
    [1, 'Lick', setup_conf_idx, 0, 1, 1, 0, 'Left lick port with reward'],
    [2, 'Lick', setup_conf_idx, 0, 1, 1, 0, 'Right lick port with reward'],
    [3, 'Proximity', setup_conf_idx, 1, 0, 0, 0, 'Animal position sensor'],
]

for port_config in ports_config:
    SetupConfiguration.Port.insert1(port_config)
```

#### 3. PortCalibration.Liquid Table

**⚠️ IMPORTANT: Calibration is Required Before Use**

Before running experiments, you **must calibrate each liquid reward port**. This determines how long valves need to be open to deliver specific volumes of liquid.
```python
ethopy -p your_path/bpod_calibration.py --log-console
```

## Troubleshooting

### Common Issues

#### Serial Port Connection Issues

**Problem**: Cannot connect to Bpod device

**Detailed Diagnosis**:

1. **Find available serial ports**:
   ```bash
   # List all serial devices
   ls /dev/tty* | grep -E "(ACM|USB)"
   
   # Watch for new devices when plugging in Bpod
   # Terminal 1: Run this first
   ls /dev/tty* > before.txt
   # Plug in Bpod
   # Terminal 2: Compare
   ls /dev/tty* > after.txt
   diff before.txt after.txt
   ```

2. **Test port accessibility**:
   ```bash
   # Test if port exists and is accessible
   if [ -e "/dev/ttyACM0" ]; then
       echo "✅ Port exists"
       if [ -r "/dev/ttyACM0" ] && [ -w "/dev/ttyACM0" ]; then
           echo "✅ Port accessible"
       else
           echo "❌ Permission denied - run: sudo chmod 666 /dev/ttyACM0"
       fi
   else
       echo "❌ Port not found"
   fi
   ```

3. **Check USB connection**:
   ```bash
   # Monitor USB events
   dmesg | tail -20 | grep -i "usb\|tty\|cdc"
   
   # Look for messages like:
   # "cdc_acm 1-1.2:1.0: ttyACM0: USB ACM device"
   # "USB disconnect"
   ```

4. **Reset Arduino/Bpod if communication fails**:
   ```bash
   # If you get connection errors, try hardware reset
   # 1. Locate the small RESET button near the USB port on the Bpod/Arduino
   # 2. Press and release the RESET button
   # 3. Wait 2-3 seconds for device to restart
   # 4. Try connection again
   
   # You should see the device reconnect in dmesg:
   dmesg | tail -5
   # Look for: "USB disconnect" followed by "cdc_acm: ttyACM0: USB ACM device"
   ```

5. **Set correct port environment variable**:
   ```bash
   # Set port environment variable
   export PYBPOD_SERIAL_PORT="/dev/ttyACM0"  # or your detected port
   
   # Make permanent
   echo 'export PYBPOD_SERIAL_PORT="/dev/ttyACM0"' >> ~/.bashrc
   source ~/.bashrc
   ```

#### Permission Issues
```bash
# Add user to dialout group (Linux)
sudo usermod -a -G dialout $USER
# Logout and login again
```

#### State Machine Conflicts
- **Error**: "The last state machine sent was not acknowledged"
- **Solution**: The interface automatically handles this with pause/resume mechanism
- **Check**: Ensure only one BpodPorts instance is running

### Logging and Debugging

Enable debug logging:
```bash
export PYBPOD_API_LOG_LEVEL="DEBUG"
```

## Hardware Compatibility

### Supported Bpod Models
- Bpod State Machine r0.5-1.0
- Bpod State Machine r2.0+
- Finite State Machine r1.0+

### Firmware Requirements
- Firmware version 22+ recommended
- Backwards compatible with firmware 13+

### Port Specifications
- **Behavior Ports**: 8 ports, 3.3V logic
- **BNC Ports**: 2 ports, TTL compatible  
- **Wire Ports**: 4 ports, 3.3V logic
- **Valves**: Supports up to 8 solenoid valves

---

## Quick Setup Checklist

### Hardware Setup
- [ ] **Download Bpod firmware v22**: From [GitHub repository](https://github.com/sanworks/Bpod_StateMachine_Firmware/tree/v23/Preconfigured/v22/StateMachine-Bpod0_5)
- [ ] **Install Arduino IDE**: Download from [arduino.cc](https://www.arduino.cc/en/software)
- [ ] **Upload firmware**: Connect to programming USB port and upload `StateMachine-Bpod0_5.ino`
- [ ] **Switch USB ports**: Disconnect from programming port, connect to communication port
- [ ] **Find serial port**: Use `ls /dev/tty*` to detect available ports
- [ ] **Set permissions**: `sudo usermod -a -G dialout $USER`

### Software Setup  
- [ ] **Install dependencies**: `pip install pybpod-api ethopy pyserial numpy`
- [ ] **Set serial port**: `export PYBPOD_SERIAL_PORT="/dev/ttyACM0"` (or your port)
- [ ] **Test connection**: Run basic connection test script
- [ ] **Verify Python 3.8+**: `python --version`

### Database Setup
- [ ] **Add BpodPorts interface**: Insert into `SetupConfiguration` table
- [ ] **Configure ports**: Add entries to `SetupConfiguration.Port` table
- [ ] **Calibrate liquid delivery**
- [ ] **Test EthoPy integration**: `python -c "from ethopy.interfaces.BpodPorts import BpodPorts; print('✅ Import successful')"`


---

## Files and Components

### event_detect.py - Standalone Hardware Testing

**Purpose**: Independent Bpod hardware validation tool that works without EthoPy integration.

The `event_detect.py` file provides a standalone testing utility to verify your Bpod hardware is working correctly before attempting EthoPy integration. This is especially useful for:

- **Initial hardware validation** - Test Bpod connection and event detection
- **Troubleshooting** - Isolate hardware issues from EthoPy configuration problems  
- **Quick testing** - Verify port functionality without database setup

#### Key Features

- **No EthoPy dependencies** - Works with just pybpod-api
- **Real-time event monitoring** - Uses `loop_handler()` for immediate event processing
- **Standalone operation** - No database or configuration files required
- **Console output** - Live event display for immediate feedback

#### Usage Example

```bash
# Test your Bpod hardware independently
cd Bpod/
python event_detect.py
```

The script will:
1. Connect to your Bpod device (using settings from `user_settings.py`)
2. Start real-time monitoring for 30 seconds
3. Display any port events (licks, beam breaks, etc.) in the console
4. Demonstrate custom event callback functionality

#### Code Structure

```python
class RealTimeBpodMonitor(Bpod):
    """Real-time event monitor using loop_handler()"""
    
    def loop_handler(self):
        """Called continuously during state machine execution"""
        # Processes events immediately as they occur
        
    def start_monitoring(self, duration=None):
        """Start monitoring with configurable duration"""
        # Creates state machine that loops on all port events
```

**Recommended Testing Workflow:**
1. Run `event_detect.py` first to verify hardware connectivity
2. Test each port by triggering sensors/licks while monitoring
3. Once hardware validation passes, proceed to EthoPy integration

### tasks/ - EthoPy Experiment Examples

The `tasks/` folder contains example experiments that demonstrate full EthoPy integration with the BpodPorts interface.

#### bpod_calibration.py

**Purpose**: Liquid reward system calibration for accurate volume delivery.

This calibration experiment is **required before running behavioral experiments** to ensure accurate liquid rewards. It determines the valve opening duration needed to deliver specific volumes.

**Key Parameters:**
- `duration`: List of valve opening times to test (ms)
- `ports`: Which reward ports to calibrate 
- `pulsenum`: Number of pulses per duration
- `pulse_interval`: Time between pulses (ms)
- `setup_conf_idx`: **Required** - Your BpodPorts configuration index

**Usage:**
```bash
# Calibrate your liquid reward system
ethopy -p Bpod/tasks/bpod_calibration.py --log-console
```

**Configuration Validation:**
The script includes user-friendly validation that prompts you to define `setup_conf_idx` if not configured:

```
⚠️  CONFIGURATION REQUIRED
Please define 'setup_conf_idx' in session_params
This should be the index of your BpodPorts setup configuration
Example: "setup_conf_idx": 0
```

#### grating_test.py

**Purpose**: Complete behavioral experiment example - Orientation discrimination task.

This file demonstrates a full EthoPy behavioral experiment using:
- **Visual stimuli**: Grating patterns with configurable orientation
- **Multiple ports**: Left/right choice paradigm  
- **Staircase protocol**: Adaptive difficulty adjustment
- **Reward delivery**: Liquid rewards for correct responses

**Key Components:**
- `session_params`: Maximum/minimum rewards and hardware configuration
- `key`: Stimulus parameters (contrast, spatial frequency, duration)
- `conditions`: Generated stimulus-response mappings for each port
- `block`: Staircase difficulty adjustment parameters

**Hardware Requirements:**
- 2 lick ports for left/right responses
- Liquid reward valves connected to each port
- Visual stimulus display system

**Usage:**
```bash
# Run orientation discrimination experiment  
ethopy -p Bpod/tasks/grating_test.py --log-console
```

### user_settings.py - Pybpod API Configuration

**Purpose**: Low-level configuration file for pybpod-api hardware settings.

This file configures the underlying pybpod-api library used by both `event_detect.py` and the EthoPy `BpodPorts` interface.

#### Key Settings

**Hardware Connection:**
```python
PYBPOD_SERIAL_PORT = '/dev/ttyACM0'  # Your Bpod's serial port
```

**Port Configuration:**
```python
BPOD_BNC_PORTS_ENABLED = [True, True]           # BNC connector ports
BPOD_WIRED_PORTS_ENABLED = [True, True]         # Wire input ports  
BPOD_BEHAVIOR_PORTS_ENABLED = [True, True, True, False, False, False, False, False]  # Which behavior ports active
```

**Logging:**
```python
PYBPOD_API_LOG_LEVEL = logging.DEBUG    # Verbosity level
PYBPOD_API_LOG_FILE = 'pybpod-api.log'  # Log file location
```

#### Usage Notes

- **Auto-loaded**: pyBpod automatically import these settings 
- **Port optimization**: Disable unused ports to improve performance
- **Serial port**: Must match your actual Bpod device port (find with `ls /dev/tty*`)

---

For additional support, see the [pybpod-api documentation](https://pybpod-api.readthedocs.io/) and [EthoPy documentation](https://ethopy.readthedocs.io/).