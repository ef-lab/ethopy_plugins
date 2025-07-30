# Multimodal stimuli in EthoPy

This guide explains how to use multiple stimuli in EthoPy. This plugin builds on the grating.py stimulus provided with the default EthoPy installation, and adds an auditory stimulus. The setup involves four main components:

1. `tones.py` - The stimulus plugin
2. `tones_grating.py` - The stimulus plugin
3. `tones_test.py` - The task configuration
4. `tones_grating_test.py` - The task configuration

## Setup Instructions

Follow steps 1-8 in [Plugin Installation](https://github.com/ef-lab/ethopy_plugins). 

### Installation of required packages

No other packages are required

## Plugin Components

### 1. Auditory Stimulus (`tones.py`)

The tones.py implements pulses ('clicks') of an ultasound stimulus. It further sets the colors of an screen to indicate state transitons (pretrial, trial, ready for response, reward, punish).

```python
# Example usage in task configuration
from ethopy.stimuli.tones import Tones

# Key parameters
params = {
    'tone_duration': 1000,      # Duration of tone stimulus presenation (ms)
    'tone_frequency': 40000,    # Frequency of the tone (Hz)
    'tone_pulse_freq': 100,     # Frequency of the clicks (Hz)
    'tone_volume': 50,          # Amplitude of the tone stimulus (0-100 range) 
}
```
Note: Tone volume is set by adjusting the duty cycle of the tone speaker, and thus is set within the 0-100 (%) range. Use a receiver to monitor the corresponding tone levels in dB.

#### Methods:
1. `__init__()` - Tone stimulus uses the `Tones` condition table, storing parameters for `required_fields` and the `default` key. <!-- Is it usefull? -->
2. `start`      - Validates whether the click frequency can be implemented given the `tone_duration`, invokes the parent class's `start()` method, begins sound playback.
3. `present`    - Checks if the auditory stimulus duration has elapsed; if so, calls the `stop()` method.
4. `stop`       - Stops the sound and logs the stop event
5. `exit`       - Stops the sound


### 2. AudioVisual Stimulus (`tones_grating.py`)

The tones_grating.py implements a multimodal stimulus consititng of a grating and an ultasound stimulus by importing the tones plugin inherits the Grating the methods.
 
```python
# Example usage in stimulus plugin
from ethopy.stimuli.grating import Grating

# Example usage in task configuration
from ethopy.stimuli.tones_grating import TonesGrating

# Key parameters
params = {
    'tone_duration': 1000,      # Duration of tone stimulus presenation (ms)
    'tone_frequency': 40000,    # Frequency of the tone (Hz)
    'tone_pulse_freq': 100,     # Frequency of the clicks (Hz)
    'tone_volume': 50,          # Amplitude of the tone stimulus (0-100 range) 
    'theta'      : 0            # Grating, in degrees (0-360)
    'spatial_freq' : 0.05       # cycles/deg
    'phase'   : 0               # initial phase in rad
    'contrast ' : 80            # 0-100 Michelson contrast
    'square' : 0                # square flag
    'temporal_freq' : 0         # cycles/sec
    'flatness_correction' : 1   # 1 correct for flatness of monitor, 0 do not
    'duration'  : 1000          # grating duration    
}
```

#### Methods:
1. `__init__()` - Uses both the 'Tones' and 'Grating' condition tables <!-- Is it usefull? -->
2. `start`      - Sets the grating and sound operation flags to `true`. Starts the sound, and initiates the grating presentation via `super().start()`
3. `present`    - Checks whether the auditory stimulus duration has elapsed and presents the grating stimulus.
4. `stop`       - Ensures the sound is stopped and logs the stop event
5. `ready_stim` - Fills the screen with a color if the grating stimulus has finished 


### 3. Task Configurations (`tones_test.py` & `tones_grating_test.py`)

The task configuration files set up the experiment parameters and stimulus conditions. You need to specify the task path, create it if doesn't exist and add the configuration file, e.g. `~/.ethopy/tasks/task_configuration_name` 

## Running the Experiment

1. **Start EthoPy with the task**:

```bash
ethopy -p ~/.ethopy/tasks/tones_test.py 
# or
ethopy -p ~/.ethopy/tasks/tones_grating_test.py
```


2. **Monitor the experiment**:
- Check the Control table for experiment status
- Monitor behavioral data in the database
- View log files for detailed information

## Database Tables

### 1. Tones Tables
- `Tones`
- `Tones.tones_duration`
- `Tones.tone_frequency`
- `Tones.tone_pulse_freq`
- `Tones.tone_volume`

### 2. Grating Tables
- `Grating`
- `Grating.theta`
- `Grating.spatial_freq`
- `Grating.phase`
- `Grating.contrast`
- `Grating.temporal_freq`
- `Grating.flatness_correction`
- `Grating.duration`