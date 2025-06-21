# Integration of PsychoPy in EthoPy

PsychoPy is Python-based open-source package that enables the creation and manipulation of visual stimuli. For more information, visit their: [PsychoPy](https://www.psychopy.org/). \
This guide explains how to install and import implement PsychoPy through EthoPy. The setup involves three main components:

1. `MatchToSample.py` - The experiment plugin
2. `PsychoGrating.py` - The stimulus plugin
3. `PsychoPresenter.py` - The utils plugin 
4. `PsychoGrating_test.py` - The task configuration



## Setup instruction

`PsychoPy` (2024.1.2) needs specific version of Python packages. For this reason, we have create a requirement.txt that install PsychoPy with all neseccery packages.



### PsychoPy installation

1. **Open the terminal in raspberry pi and create a python script**:

```bash
nano install_psychopy.py
```
 

2. **Copy-paste in your python script the `install_psychopy.py` and save it.**


3. **Run the `install_psychopy.py` script.**

```bash
sudo python install_psychopy.py
```



## Plugin components

### 1. Match to sample experiment (`MatchTosample.py`)
The Match to Sample experiment implements a behavioral paradigm where subjects must match a sample stimulus with a target stimulus. 

```python
# Example usage in task configuration
from ethopy.experiment.MatchToSample import *

# Key parameters
params = {
    'cue_duration': 1000,       # Duration of sample presentation (ms)
    'delay_duration': 500,      # Delay between sample and choice (ms)
    'response_duration': 10000, # Time allowed for response (ms)
    'reward_amount': 7,         # Reward amount for correct response
    'punish_duration': 3000,    # Timeout duration for incorrect response (ms)
}
```



#### States:
1. `PreTrial` - Preparation for trial
2. `Cue` - Present sample stimulus
3. `Delay` - Delay period
4. `Response` - Present choice stimuli
5. `Reward` - Deliver reward for correct response
6. `Punish` - Timeout for incorrect response


### 2. PsychoGrating stimulus (`PsychoGrating.py`)

The PsychoGrating stimulus provides grating stimuli presentation using psychopy.

```python
from ethopy.stimuli.PsychoGrating import *
```

#### Features:
- Multiple gratings management
- Grating transformation (rotation, position, spatial & temporal frequency, mask, size, texture)



### 3. PsychoPresenter util(`PsychoPresenter.py`)

The PsychoPresenter util handles the monitor parameters about how stimuli are presented. 
```python
# In PsychoGrating stimuli
from utils.PsychoPresenter import *

# import in task configuration
from ethopy.stimuli.PsychoGrating import *

```

#### Features
- Fill screen with color
- Update the screen
- Close the window
- Photodiode support
- Monitor warping




### 4. Task Configuration (`PsychoGrating_test.py`)

The task configuration file sets up the experiment parameters and stimulus conditions. 




## Running the Experiment

1. **Start EthoPy wirh task**:

```bash
ethopy -p ~/.ethopy/tasks/PsychoGrating_test.py
```


2. **Monitor the experiment**:
- check the Control table for experiment status
- Monitor behavioral data in the database
- View log diles for detailed information




## Database Tables

### 1. Experiment Tables
- `Session` - Session information
- `Trial` - Trial data
- `Condition` - Trial conditions
- `Response` - Subject responses
- `MatchToSample` - Experiment conditions


### 2. Stimulus Tables
- `psycho_grating` Live Share

## Troubleshooting 

1. **Python version** 

PsychoPy mentions, "_We strongly recommend you use Python 3.10 or 3.8._"

2. **Stimulus Display**
- Verify PsychoPy installation
- Check model file paths
- Confirm screen configuration

3. **Database Connection**
- Verify database credentials
- Check table perimissions
- Ensure schema exists


### Debug Logging

Enable detailed logging:
```bash
ethopy --log-console --log-level DEBUG -p your_task_path.py
```



## Best Practices

**Task Configuration**
- Use descriptive condition names
- Document parameter choices
- Test configurations before experiments. 

## Additional Resources

1. **Documentation**
- [DataJoint Documentation](https://docs.datajoint.org/)

2. **Source Code**
- [PsychoPy GitHub Repository](https://github.com/psychopy/psychopy.git) 

