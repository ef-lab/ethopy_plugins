# Multimodal stimuli in EthoPy

This guide explains how to use multiple stimuli in EthoPy. This plugin builds on the grating.py stimulus provided with the default EthoPy installation, and adds an auditory stimulus. The setup involves four main components:

1. `tones.py` - The auditory stimulus plugin
2. `tones_grating.py` - The auditory/visual stimuli plugin
2. `tones_test.py` - The task configuration for auditory 2AFC experiments
3. `tones_grating_test.py` - The task configuration for audiovisual 2AFC experiments

## Setup Instructions

Follow steps 1-4 in [Plugin Installation](https://github.com/ef-lab/ethopy_plugins). 

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
1. `__init__()` - Tone stimulus uses the `Tones` condition table, storing parameters for `required_fields` and the `default` key.
2. `start`      - Validates whether the click frequency can be implemented given the `tone_duration`, invokes the parent class's `start()` method, begins sound playback.
3. `present`    - Checks if the auditory stimulus duration has elapsed; if so, calls the `stop()` method.
4. `stop`       - Stops the sound and logs the stop event
5. `exit`       - Stops the sound


### 2. AudioVisual Stimulus (`tones_grating.py`)

The tones_grating.py implements a multimodal stimulus consititng of a grating and an ultasound stimulus by inherit the Grating the methods.
```python
from ethopy.stimuli.grating import Grating
```
the tones plugin inherits the Grating methods. 


```python
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

### Task Configurations (`tones_test.py` & `tones_grating_test.py`)

The task configuration file sets up the experiment parameters and stimulus conditions.

## Running the Experiment

1. **Start EthoPy with the task**:

```bash
ethopy -p ~/.ethopy/tasks/tones_test.py
```

or

```bash
ethopy -p ~/.ethopy/tasks/tones_grating_test.py
```

## Database Tables

### 1. Tones Table

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `stim_hash` | varchar(24) | Stimulus hash | - |
| `tones_duration` | int | Duration of tone stimulus presenation (ms) | 1000 |
| `tone_frequency` | int | Frequency of the tone (Hz) | 40500 |
| `tone_volume` | int | Amplitude of the tone stimulus (0-100 range) | 30 |
| `tone_pulse_freq` | float | Frequency of the clicks (Hz) | 100 |

### 2. Grating Table

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `stim_hash` | varchar(24) | Stimulus hash | - |
| `theta` | int | Grating, in degrees (0-360) | 90 |
| `spatial_freq` | float | cycles/deg | 0.05 |
| `phase` | float | initial phase in rad | 0.0 |
| `contrast` | int | 0-100 Michelson contrast| 80 |
| `square` | int | square flag | 0 |
| `temporal_freq` | float | cycles/sec | 0.0 |
| `flatness_correction` | int | 1 correct for flatness of monitor, 0 do not | 1 |
| `duration` | int | grating duration | 5000 |

## Best Practices

**Task Configuration**
- Use descriptive condition names
- Document parameter choices
- Test configurations before experiments

## Additional Resources

1. **Documentation**
- [EthoPy Documentation](https://ef-lab.github.io/ethopy_package/)
- [DataJoint Documentation](https://docs.datajoint.org/)

2. **Source Code**
- [EthoPy GitHub Repository](https://github.com/ef-lab/ethopy_package)
- [Example Configurations](https://github.com/ef-lab/ethopy_package/tree/main/src/ethopy/task)

3. **Support**
- [Issue Tracker](https://github.com/ef-lab/ethopy_package/issues)
- [Contributing Guidelines](https://github.com/ef-lab/ethopy_package/blob/main/CONTRIBUTING.md)

