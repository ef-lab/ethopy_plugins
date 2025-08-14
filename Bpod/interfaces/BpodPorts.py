"""
Bpod Interface for EthoPy
=========================

This interface adapts the Bpod hardware system for use with EthoPy experiments.
It provides non-blocking event detection and integrates with EthoPy's interface system.

This interface runs event detection in a background thread while allowing the main experiment to continue.

Features:
- Real-time event detection for all Bpod ports
- Non-blocking operation compatible with EthoPy experiment flow
- Event logging through EthoPy's behavior tracking system
- Support for liquid rewards, proximity detection, and general I/O
- Configurable through EthoPy's setup configuration system
"""

import logging
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, Tuple

from ethopy import local_conf
from ethopy.core.interface import Interface, Port

try:
    from pybpodapi import settings as pybpod_settings
    from pybpodapi.bpod import Bpod
    from pybpodapi.bpod.hardware.events import EventName
    from pybpodapi.state_machine import StateMachine

    IMPORT_BPOD = True
except ImportError:
    IMPORT_BPOD = False

log = logging.getLogger(__name__)


class BpodPorts(Interface, Bpod):
    """
    Bpod hardware interface for EthoPy experiments.

    This class extends the base Interface to work with Bpod hardware,
    providing non-blocking event detection and stimulus delivery.
    """

    def __init__(self, **kwargs):
        """
        Initialize Bpod interface.

        Args:
            **kwargs: Arguments passed to base Interface class

        Raises:
            ImportError: If pybpod-api packages are not available
        """
        if not globals()["IMPORT_BPOD"]:
            raise ImportError(
                "Could not import Bpod packages (pybpodapi)! "
                "Install with: pip install pybpod-api"
            )

        # Configure pybpod settings before initialization
        self._configure_pybpod_settings()

        # Initialize both parent classes - Interface first for experiment setup
        Interface.__init__(self, **kwargs)
        Bpod.__init__(self)

        # Log connection info if Bpod initialized successfully
        if hasattr(self, "serial_port"):
            log.info(f"Connected to Bpod on {self.serial_port}")
        if hasattr(self, "hardware") and self.hardware:
            log.info(f"Hardware: {self.hardware.firmware_version} firmware")
        else:
            log.warning("Bpod hardware not fully initialized")

        # Event detection setup
        self.is_monitoring = False
        self.monitor_thread = None
        self._last_event_count = 0

        # State machine synchronization
        self._state_machine_lock = threading.Lock()
        self._monitoring_paused = False

        self.ready = False
        self.response = None
        self.resp_tmst = None
        self.position = None
        self.position_tmst = None

        # Thread pool for stimulus delivery
        self.thread = ThreadPoolExecutor(max_workers=4)

        # Start background event monitoring
        self.start_monitoring()

    def _configure_pybpod_settings(self):
        """
        Configure pybpod module settings using environment variables and EthoPy config.
        This eliminates the need for a separate user_settings.py file.
        """
        try:
            # 🔌 ESSENTIAL: Serial port configuration
            serial_port = (
                os.environ.get("PYBPOD_SERIAL_PORT")  # Environment variable
                or local_conf.get("PYBPOD_SERIAL_PORT", None)  # EthoPy config
                or "/dev/ttyACM0"  # Default for Linux
            )
            pybpod_settings.PYBPOD_SERIAL_PORT = serial_port
            log.info(f"🔌 Bpod serial port: {serial_port}")

            # 🎯 PORT ENABLEMENT: Which hardware ports are active
            # BNC ports (typically 2): for external triggers, sync signals
            bnc_ports = os.environ.get("BPOD_BNC_PORTS_ENABLED", "[True, True]")
            pybpod_settings.BPOD_BNC_PORTS_ENABLED = (
                eval(bnc_ports) if isinstance(bnc_ports, str) else bnc_ports
            )

            # Wire ports (typically 2-4): for direct digital I/O
            wire_ports = os.environ.get("BPOD_WIRED_PORTS_ENABLED", "[True, True]")
            pybpod_settings.BPOD_WIRED_PORTS_ENABLED = (
                eval(wire_ports) if isinstance(wire_ports, str) else wire_ports
            )

            # Behavior ports (typically 8): for nose pokes, lick detection
            behavior_ports = os.environ.get(
                "BPOD_BEHAVIOR_PORTS_ENABLED",
                "[True, True, True, True, True, True, True, True]",
            )
            pybpod_settings.BPOD_BEHAVIOR_PORTS_ENABLED = (
                eval(behavior_ports)
                if isinstance(behavior_ports, str)
                else behavior_ports
            )

            # ⚙️ COMMUNICATION: Serial communication settings
            pybpod_settings.PYBPOD_BAUDRATE = int(
                os.environ.get("PYBPOD_BAUDRATE", "1312500")
            )  # Fast, reliable
            pybpod_settings.PYBPOD_SYNC_CHANNEL = int(
                os.environ.get("PYBPOD_SYNC_CHANNEL", "255")
            )  # Default sync
            pybpod_settings.PYBPOD_SYNC_MODE = int(
                os.environ.get("PYBPOD_SYNC_MODE", "1")
            )  # Standard mode

            # 📊 LOGGING: API logging configuration
            log_level = os.environ.get("PYBPOD_API_LOG_LEVEL", "INFO")
            pybpod_settings.PYBPOD_API_LOG_LEVEL = getattr(
                logging, log_level.upper(), logging.INFO
            )
            pybpod_settings.PYBPOD_API_LOG_FILE = os.environ.get(
                "PYBPOD_API_LOG_FILE", "pybpod-api.log"
            )

            # 🗂️ SESSION: Experiment metadata (optional)
            pybpod_settings.PYBPOD_PROTOCOL = os.environ.get(
                "PYBPOD_PROTOCOL", "EthoPy-Bpod"
            )
            pybpod_settings.PYBPOD_CREATOR = os.environ.get("PYBPOD_CREATOR", "EthoPy")
            pybpod_settings.PYBPOD_PROJECT = os.environ.get(
                "PYBPOD_PROJECT", "Behavioral-Experiment"
            )

            log.info("✅ Pybpod settings configured successfully")
            log.debug(
                f"   - BNC ports enabled: {pybpod_settings.BPOD_BNC_PORTS_ENABLED}"
            )
            log.debug(
                f"   - Wire ports enabled: {pybpod_settings.BPOD_WIRED_PORTS_ENABLED}"
            )
            log.debug(
                f"   - Behavior ports enabled: {pybpod_settings.BPOD_BEHAVIOR_PORTS_ENABLED}"
            )

        except Exception as e:
            log.warning(f"⚠️ Error configuring pybpod settings: {e}")
            log.info("Using pybpod default settings")

    def start_monitoring(self):
        """Start background event monitoring - non-blocking!"""
        if self.is_monitoring:
            log.warning("⚠️  Already monitoring events!")
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True, name="BpodEventMonitor"
        )
        self.monitor_thread.start()
        log.info("Background Bpod event monitoring started!")

    def _monitoring_loop(self):
        """Background monitoring loop that runs continuously"""
        while self.is_monitoring:
            try:
                # Check if monitoring is paused (for liquid delivery)
                if self._monitoring_paused:
                    log.debug("Bpod monitoring is paused")
                    time.sleep(0.1)
                    continue

                self._last_event_count = 0  # Reset for each cycle

                # Acquire lock before sending state machine
                with self._state_machine_lock:
                    if self._monitoring_paused:  # Double-check after acquiring lock
                        continue

                    # Create state machine for event monitoring
                    sma = StateMachine(self)

                    # Create a monitoring state that loops back on all events
                    sma.add_state(
                        state_name="Monitor",
                        state_timer=0.2,  # 2 second cycles
                        state_change_conditions={
                            EventName.Tup: "Monitor",  # Loop back on timeout
                            # Port events
                            EventName.Port1In: "Monitor",
                            EventName.Port1Out: "Monitor",
                            EventName.Port2In: "Monitor",
                            EventName.Port2Out: "Monitor",
                            EventName.Port3In: "Monitor",
                            EventName.Port3Out: "Monitor",
                            EventName.Port4In: "Monitor",
                            EventName.Port4Out: "Monitor",
                            EventName.Port5In: "Monitor",
                            EventName.Port5Out: "Monitor",
                            EventName.Port6In: "Monitor",
                            EventName.Port6Out: "Monitor",
                            EventName.Port7In: "Monitor",
                            EventName.Port7Out: "Monitor",
                            EventName.Port8In: "Monitor",
                            EventName.Port8Out: "Monitor",
                            # # BNC events
                            # EventName.BNC1High: "Monitor",
                            # EventName.BNC1Low: "Monitor",
                            # EventName.BNC2High: "Monitor",
                            # EventName.BNC2Low: "Monitor",
                            # # Wire events
                            # EventName.Wire1High: "Monitor",
                            # EventName.Wire1Low: "Monitor",
                            # EventName.Wire2High: "Monitor",
                            # EventName.Wire2Low: "Monitor",
                        },
                        output_actions=[],
                    )

                    # Run state machine (this calls our loop_handler automatically)
                    self.send_state_machine(sma)
                    self.run_state_machine(sma)

            except Exception as e:
                log.error(f"Error in Bpod monitoring loop: {e}")
                time.sleep(0.5)  # Brief pause before retry

    def loop_handler(self):
        """
        Real-time event capture during state machine execution.
        This method is called by Bpod during state machine execution.
        """
        if not self.is_monitoring:
            return

        # Check for new events in current trial
        if hasattr(self.session, "current_trial") and self.session.current_trial:
            current_trial = self.session.current_trial
            current_event_count = len(current_trial.events_occurrences)

            if current_event_count > self._last_event_count:
                # Process new events
                new_events = current_trial.events_occurrences[self._last_event_count :]

                for event_obj in new_events:
                    self._process_realtime_event(event_obj)

                self._last_event_count = current_event_count

    def _process_realtime_event(self, event_obj):
        """
        Process a single event immediately as it occurs.

        Args:
            event_obj: EventOccurrence object from Bpod
        """
        try:
            event_name = str(event_obj.event_name)

            # Skip timer events
            if "Tup" in event_name or "Timer" in event_name:
                return

            timestamp = time.time()

            # Process event based on type for EthoPy integration
            self._handle_ethopy_event(event_name, timestamp)

            log.debug(f"Bpod event: {event_name} at {timestamp:.3f}")

        except Exception as e:
            log.error(f"Error processing Bpod event: {e}")

    def _handle_ethopy_event(self, event_name: str, timestamp: float):
        """
        Convert Bpod events to EthoPy port activations.

        Args:
            event_name: Name of the Bpod event
            timestamp: Event timestamp
        """
        # Validate inputs
        if not event_name:
            log.warning("Empty event name received")
            return

        try:
            # Parse event name (e.g., "Port1In", "Port2Out", "BNC1High")
            if event_name.startswith("Port") and (
                "In" in event_name or "Out" in event_name
            ):
                # Extract port number
                port_num = int(event_name[4])  # Port1In -> 1

                # Find the port configuration to determine type
                port_config = next((p for p in self.ports if p.port == port_num), None)
                if port_config:
                    if port_config.type == "Lick" and "In" in event_name:
                        self._handle_lick_event(port_num, timestamp)
                    elif port_config.type == "Proximity":
                        # IN = entering position (active), OUT = leaving position (inactive)
                        self._handle_proximity_event(
                            port_num, "In" in event_name, timestamp
                        )

        except Exception as e:
            log.error(f"Error handling EthoPy event {event_name}: {e}")

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

    def pause_monitoring(self):
        """Temporarily pause monitoring for state machine operations"""
        self._monitoring_paused = True
        log.debug("Bpod monitoring paused")

    def resume_monitoring(self):
        """Resume monitoring after state machine operations"""
        self._monitoring_paused = False
        log.debug("Bpod monitoring resumed")

    def stop_monitoring(self):
        """Stop background event monitoring"""
        self.is_monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=3.0)
        log.info("Bpod event monitoring stopped")

    def give_liquid(self, port: int, duration: Optional[float] = None):
        """
        Deliver liquid reward through specified port.

        Args:
            port: Port number for delivery
            duration: Duration in milliseconds (uses calibrated value if None)
        """

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

        # Pause monitoring to avoid state machine conflicts
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
                    output_actions=[("Valve", port)] if port else [],  # Open valve
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
                            log.warning(
                                f"Retry {attempt + 1}/{max_retries} for liquid delivery: {retry_e}"
                            )
                            time.sleep(0.1)  # Brief delay before retry
                        else:
                            raise  # Re-raise on final attempt

        except Exception as e:
            log.error(f"Error delivering liquid reward: {e}")
        finally:
            # Always resume monitoring
            self.resume_monitoring()

    def in_position(self, port: int = 0) -> Tuple[Port, float, float]:
        """
        Check if subject is in position.

        Args:
            port: Specific port to check (0 = check all)

        Returns:
            Tuple of (position_port, position_duration, position_timestamp)
        """
        # Return current position state
        position_dur = (
            self.timer_ready.elapsed_time() if self.ready else self.position_dur
        )
        return self.position, position_dur, self.position_tmst

    def off_proximity(self) -> bool:
        """
        Check if all proximity ports are not activated.

        Returns:
            True if all proximity ports are inactive
        """
        return self.position.type != "Proximity"

    def set_operation_status(self, operation_status: bool):
        """
        Set operation status.

        Args:
            operation_status: Status to set
        """
        # Could trigger status LED or other indicators via Bpod
        log.info(f"Operation status: {'ON' if operation_status else 'OFF'}")

    def cleanup(self):
        """Clean up Bpod resources"""
        try:
            self.stop_monitoring()

            # Close Bpod connection
            self.close()

            # Shutdown thread pool
            self.thread.shutdown(wait=True)

            log.info("Bpod interface cleaned up successfully")

        except Exception as e:
            log.error(f"Error during Bpod cleanup: {e}")

    def load_calibration(self):
        """Load port calibration data from database"""
        # Use parent class calibration loading
        super().load_calibration()
        log.info("Bpod calibration data loaded")

    def calc_pulse_dur(self, reward_amount: float) -> Dict[int, float]:
        """
        Calculate pulse duration for desired reward amount.

        Args:
            reward_amount: Desired reward in microliters

        Returns:
            Dictionary of actual reward amounts by port
        """
        # Use parent class calculation or provide Bpod-specific implementation
        return super().calc_pulse_dur(reward_amount)
