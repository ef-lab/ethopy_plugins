# Navigation in Virtual Reality in EthoPy

This guide explains how to use a Navigation experiment with a styrofoam ball and olfactory stimuli in EthoPy. The setup involves five main components:

1. `vr_ball.py` - The behavior plugin
2. `navigate.py` - The experiment plugin
3. `olfactory.py` - The stimulus plugin
4. `vr_odors.py` - The stimulus plugin
5. `ball_test.py` - The task configuration

## Setup Instructions

Follow steps 1-8 in [Plugin Installation](https://github.com/ef-lab/ethopy_plugins)

### Installation of required packages

No other packages are required <!-- !!! Double check!!!! -->

## Plugin Components

### 1. VR Ball Behavior (`vr_ball.py`)

The VR Ball behavior implements the behaviors that subjects can have on the ball and the virtual space settings.

```python
# Example usage in task configuration
from ethopy.behaviors.vr_ball import VRBall 

# Key parameters
params = {
    'x_sz': 2,                   # x dimension of the virtual space (m)
    'y_sz': 2,                   # y dimension of the virtual space (m)
    'x0': 1,                     # starting x location of each trial 
    'y0': 1,                     # starting y location of each trial 
    'response_loc_x': (0,2,2,0)  # x target location,
    'response_loc_y': (0,0,2,2)  # y target location,
}
```

#### States:
1. `Response` - Conditions of response (location and port)
2. `Reward` - Reward delivery (location, amount, type)


### 2. Navigate Experiment (`navigate.py`)

The Navigate experiment implements a behavioral paradigm where subjects must move towards a target stimulus to receive reward.

```python
# Example usage in task configuration
from ethopy.experiments.navigate import MatchToSample

# Key parameters
params = {
    'norun_response': 1,       # Animal should stop moving to give response and receive reward
    'trial_duration': 5000,    # Time allowed to complete 1 trial (ms)
    'reward_amount': 10,       # Reward amount (uL) for correct response
    'punish_duration': 1000,   # Timeout duration for incorrect response (ms)
}
```

#### States:
1. `PreTrial` - Preparation for trial
2. `Trial` - Present stimulus
3. `Abort` - Aborted Trial if trial_duration is over and animal hasn't respond
5. `Reward` - Deliver reward for correct response
6. `Punish` - Timeout for incorrect response

### 3. Olfactory Stimulus (`olfactory.py`)

The Olfactory stimulus plugin provides olfactory stimulus presentation by implementing pulses of odors. It further sets the colors of an screen to indicate state transitons (pretrial, trial, ready for response, reward, punish).

```python
# Example usage in task configuration
from ethopy.stimuli.olfactory import Olfactory

# Key parameters
params = {
    'concentration': 100,   # odor concentration (%)
    'odor_duration': 500,   # odor duration (ms)
    'dutycycle': 50,        # dutycycle of pulse (%)
    'delivery_port': 1,     # which port will deliver the odor   
}
```

#### Methods:
1. `start`      - It gets the current conditions and calls the give_odor() fucntion to deliver the odor

### 4. Virtual Olfactory Stimulus (`vr_odors.py`)

The vr_odors stimulus plugin provides olfactory stimulus presentation in the ball virtual environment. 

```python
# Example usage in task configuration
from ethopy.stimuli.vr_odors import VROdors

# Key parameters
params = {
    'extiction_factor': 3,   # gradient for calculating the odor proportions at the different x, y locations
    'odor_x': 1,             # odor at x location
    'odor_y': 1,             # odor at y location
    'delivery_port': 1,      # which port will deliver the odor   
}
```

#### Methods:
1. `start`      - It calls the start_odor() fucntion to start delivering the odors
2. `loc2odor`   - It calculates the odors dutycycles based on the animals location and an extinction factor
3. `present`    - Checks the position of the animal (x,y), calls the `loc2odor`, and updates the odor
4. `stop`       - It calls the stop_odor() fucntion to stop delivering the odors

### 5. Task Configuration (`ball_test.py`)

The task configuration file sets up the experiment parameters and stimulus conditions. You need to specify the task path, create it if doesn't exist and add the configuration file, e.g. `~/.ethopy/tasks/ball_test.py`

## Running the Experiment

1. **Start EthoPy with the task**:

```bash
ethopy -p ~/.ethopy/tasks/ball_test.py
```

2. **Monitor the experiment**:
- Check the Control table for experiment status
- Monitor behavioral data in the database
- View log files for detailed information

## Database Tables

### 1. Behavior Tables
- `VRBall` - Virtual environment information
- `VRBall.Response` - Subject responses locations
- `VRBall.Reward` - Subject rewards locations

### 2. Experiment Tables
- `Session` - Session information
- `Trial` - Trial data
- `Condition` - Trial conditions
- `Response` - Subject responses
- `Condition.Navigate` - Experiment conditions

### 3. Stimulus Tables
- `Olfactory`
- `Olfactory.Channel`
- `VROdors`
- `VROdors.Source`


## Troubleshooting

### Common Issues


## Additional Resources

1. **Documentation**
- ef-lab/ethopy_hardware/ball
