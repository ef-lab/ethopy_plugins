# Match to Sample task with Panda3D in EthoPy

This guide explains how to use the Match to Sample experiment with Panda3D visual stimuli in EthoPy. The setup involves three main components:

1. `match_to_sample.py` - The experiment plugin
2. `panda.py` - The stimulus plugin
3. `panda_test.py` - The task configuration

## Setup Instructions

Follow steps 1-8 in [Plugin Installation](https://github.com/ef-lab/ethopy_plugins)

### Installation of required packages

Panda3D is required for this plugin. For more information, visit their [Panda3D GitHub repository](https://github.com/panda3d/panda3d/tree/master).

```bash
pip install panda3d
```

### Upload Objects

Upload egg objects from folder objs to the table #Objects at stimulus schema

```bash
python upload_objects.py
```

## Plugin Components

### 1. Match to Sample Experiment (`match_to_sample.py`)

The Match to Sample experiment implements a behavioral paradigm where subjects must match a sample stimulus with a target stimulus.

```python
# Example usage in task configuration
from ethopy.experiments.match_to_sample import MatchToSample

# Key parameters
params = {
    'cue_period': 1000,      # Duration of sample presentation (ms)
    'delay_period': 500,     # Delay between sample and choice (ms)
    'response_period': 2000, # Time allowed for response (ms)
    'reward_amount': 3,      # Reward amount for correct response
    'punish_period': 1000,   # Timeout duration for incorrect response (ms)
}
```

#### States:
1. `PreTrial` - Preparation for trial
2. `Cue` - Present sample stimulus
3. `Delay` - Delay period
4. `Response` - Present choice stimuli
5. `Reward` - Deliver reward for correct response
6. `Punish` - Timeout for incorrect response

### 2. Panda3D Stimulus (`panda.py`)

The Panda stimulus plugin provides 3D visual stimulus presentation using Panda3D.

```python
# Example usage in task configuration
from ethopy.stimuli.panda import Panda
```

#### Features:
- 3D model loading and display
- Camera control
- Lighting setup
- Model transformation (rotation, position)
- Multiple object management

### 3. Task Configuration (`panda_test.py`)

The task configuration file sets up the experiment parameters and stimulus conditions. You need to specify the task path, create it if doesn't exist and add the configuration file, e.g. `~/.ethopy/tasks/panda_test.py`

## Running the Experiment

1. **Start EthoPy with the task**:

```bash
ethopy -p ~/.ethopy/tasks/panda_test.py
```

2. **Monitor the experiment**:
- Check the Control table for experiment status
- Monitor behavioral data in the database
- View log files for detailed information

## Database Tables

### 1. Experiment Tables
- `Session` - Session information
- `Trial` - Trial data
- `Condition` - Trial conditions
- `Response` - Subject responses
- `MatchToSample` - Experiment conditions

### 2. Stimulus Tables
- `Panda`
- `Panda.Object`
- `Panda.Environment`
- `Panda.Light`
- `Panda.Movie`

## Troubleshooting

### Common Issues

1. **Stimulus Display**
- Verify Panda3D installation
- Check model file paths
- Confirm screen configuration


## Additional Resources

1. **Documentation**
- [Panda3D Manual](https://docs.panda3d.org/1.10/python/index)
