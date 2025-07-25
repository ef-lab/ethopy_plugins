# Multimodal stimuli in EthoPy

This guide explains how to use multiple stimuli in EthoPy. This plugin builds on the grating.py stimulus provided with the default EthoPy installation, and adds an auditory stimulus. The setup involves two main components:

1. `tones.py` - The auditory stimulus plugin
2. `tones_grating.py` - The auditory/visual stimuli plugin
2. `tones_test.py` - The task configuration for auditory 2AFC experiments
3. `tones_grating_test.py` - The task configuration for audiovisual 2AFC experiments

### Plugin Installation
For installation, follow the instructions provided [here](https://ef-lab.github.io/ethopy_package/plugin/). 

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
1. '__init__()' - Tone stimulus uses the 'Tones' condition table, where the used parameters for the required_fields and default key are stored 
2. `start`      - It checks if the frequency of the clicks can be implemented given the tone_duration, it calls the parent class's start method and it starts the sound 
3. `present`    - Checks if the auditory stimulus duration has elapsed. If the time has elapsed it calls the stop method
4. `stop`       - Stops the sound and logs the stop event 
5. `exit`       - Stops the sound


### 2. AudioVisual Stimulus (`tones_grating.py`)

The tones_Grating.py implements a multimodal stimulus consititng of a grating and an ultasound stimulus. 
By importing 
```python
from ethopy.stimuli.grating import Grating
```
the tones plugin inherits the Grating the methods. 


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
1. '__init__()' - Both 'Tones' and 'Grating' condition tables are used 
2. `start`      - It sets the grating and sound operation flags to true, it starts the sound and, via the super.start(), starts the grating  presentaion
3. `present`    - Checks if the auditory stimulus duration has elapsed and presents the grating stimulus  I
4. `stop`       - Verifies sound is stopped and logs stop event 
5. `ready_stim` - Fills the screen color if grating stimulus has stopped 

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
- `Tones`
- `Tones.tones_duration`
- `Tones.tone_frequency`
- `Tones.tone_pulse_freq`
- `Tones.tone_volume`

### 2. Grating Table
- `Grating`
- `Grating.theta`
- `Grating.spatial_freq`
- `Grating.phase`
- `Grating.contrast`
- `Grating.temporal_freq`
- `Grating.flatness_correction`
- `Grating.duration`

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

