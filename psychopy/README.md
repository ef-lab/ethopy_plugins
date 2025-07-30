# Integration of PsychoPy in EthoPy

PsychoPy is a Python-based open-source package that enables the creation and manipulation of visual stimuli. For more information, visit: [PsychoPy](https://www.psychopy.org/). \
This guide explains how to install and import PsychoPy into your EthoPy environment. The setup involves five main components:

1. `match_to_sample.py` - The experiment plugin
2. `psycho_grating.py` - The stimulus plugin
3. `psycho_presenter.py` - The utils plugin
4. `psychopy_test.py` - The task configuration
5. `psych_dummy_port.py` = The interface plugin

## Setup instruction

Follow steps 1-8 in [Plugin Installation](https://github.com/ef-lab/ethopy_plugins)

### Installation of required packages
PsychoPy is required for this plugin. For more information, visit their [PsychoPy GitHub repository](https://github.com/psychopy/psychopy.git)

```bash
pip install psychopy
```
Note: UV is an extremely fast Python package and project manager, written in Rust. For more information, visit their [UV](https://docs.astral.sh/uv/). We recommend uv for a more quick installation of libraries and psychopy too:

```bash
pip install uv
uv pip install psychopy
```

## Plugin components

### 1. Match to sample experiment (`match_to_sample.py`)

The Match to Sample experiment implements a behavioral paradigm where subjects must match a sample stimulus with a target stimulus.

```python
# Example usage in task configuration
from ethopy.experiment.match_to_sample import Experiment

# Key parameters
params = {
    "cue_duration": 400,  # Duration of sample presentation (ms)
    "delay_duration": 200,  # Delay between sample and choice (ms)
    "response_duration": 2000,  # Time allowed for response (ms)
    "reward_amount": 6,  # Reward amount for correct response
    "punish_duration": 3000,  # Timeout duration for incorrect response (ms)
}
```

#### States:

1. `PreTrial` - Preparation for trial
1. `Cue` - Present sample stimulus
1. `Delay` - Delay period
1. `Response` - Present choice stimuli
1. `Reward` - Deliver reward for correct response
1. `Punish` - Timeout for incorrect response


### 2. PsychoGrating stimulus (`psycho_grating.py`)

The PsychoGrating stimulus provides grating stimuli presentation using psychopy.

```python
# Example usage in task configuration
from ethopy.stimuli.psycho_grating import PsychoGrating
```

#### Features:

- Multiple gratings management
- Grating transformation (rotation, position, spatial & temporal frequency, mask, size, texture)

### 3. PsychoPresenter util (`psycho_presenter.py`)

The PsychoPresenter util handles the monitor parameters about how stimuli are presented.

```python
# In PsychoGrating stimuli
from ethopy.utils.psycho_presenter import Presenter

# import in task configuration
from ethopy.stimuli.psycho_grating import PsychoGrating
```

#### Features:

- Fill screen with color
- Update the screen
- Close the window
- Photodiode support
- Monitor warping

### 4. PsychoDummyPort interface (`psych_dummy_port.py`)
The PsychDummyPort interface handles all communication with hardware.

### 5. Task Configuration (`psychopy_test.py`)

The `task` configuration file sets up the experiment parameters and stimulus conditions.


## Running the Experiment

1. **Start EthoPy with task**:

```bash
ethopy -p ~/.ethopy/tasks/psychopy_test.py
```

2. **Monitor the experiment**:

- check the Control table for experiment status
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
- `psycho_grating`

## Troubleshooting

### Common Issues

1. **Python version**

PsychoPy mentions, "_We strongly recommend you use Python 3.10 or 3.8._"

2. **PsychoPy Installation**

If you encounter issues with the connection to `archive.raspberrypi.org`

```bash
# run 
sudo ufw disable

sudo nano /etc/apt/sources.list
# add the following entry
deb http://legacy.raspbian.org/raspbian/ jessie main contrib

# run
sudo apt update

# install stuff... .

# run after 
sudo ufw enable
```

3. **Segmentation Fault During OpenGL Stimulus Rendering in WSL**

`WSL`, while powerful for running Linux environments inside Windows, has struggled with OpenGL graphic rendering. How to fix it:

<details>
<summary><b>Step-by-step</b></summary>

<Ins>Step 1:</ins> Be sure that OpenGL packages are already installed.

```bash
pip show PyOpenGL PyOpenGL_accelerate
# Otherwise:
pip install PyOpenGL PyOpenGL_accelerate    # or uv pip install...
```

<ins>Step 2:</ins> Update WSL to WSLg (if not already)
`WSLg` add GUI support and some OpenGL passthrough.

```bash
# Open PowerShell or Command Prompt as Administrator. 
wsl -l -v 

# If you see `version 2`, you're running WSL2, otherwise:
wsl --update
wsl --shutdown
wsl     # start wsl again

# Verify the WSL version in PowerShell or in Cmd
wsl --list --verbose
```

<ins>Step 3:</ins> Verify that WSLg environment is active

```bash
# Install a simple GUI tool
sudo apt install x11-apps

# Launch a basic GUI app
xeyes   
# If it opens two spooky eyeballs that follow your mouse, your display is working.

# OpenGL benchmark
glxgears
# If you see three colorful gears spinning smoothly, your GPU passthrough via WSLg is operational.

# run your experiment
python run.py psychopy_test.py
```

<ins>Step 4:</ins> Force software rendering
If your experiment doesn't run, the issue is likely in how OpenGL interacts with your GPU driver inside WSL. The crash often stems from how `Mesa` (<ins>the Linux graphics stack</ins>) interfaces with `Direct3D` via `D3D12` on Windows. To fix it:

```bash
export LIBGL_ALWAYS_SOFTWARE=1
python run.py psychopy_test.py
```

If this works, it confirms the crash is GPU-related. To avoid typing the command, you can add it to your `.bashrc` or `.zshrc`.

```bash
nano ~/.bashrc

# add at the bottom:
export LIBGL_ALWAYS_SOFTWARE=1

# save and apply the changes with:
source ~/.bashrc

# run your experiment
python run.py psychopy_test.py
```

</details>

4. **Fixing ‘alsa/asoundlib.h’ Not Found Error for psychtoolbox@3.0.19.14**

This error occurs due to missing development libraries required for compiling native bildings. 
```bash
# Before installing Psychtoolbox, ensure your system is updated:
sudo apt update
sudo apt upgrade

sudo apt install portaudio19-dev # PortAudio (audio backend)
sudo apt install libusb-1.0.0-dev # libusb (USB/HID device support)
sudo apt install libxi-dev # XInput (X11 input extension)

pip install psychtoolbox # install Psychtoolbox
```

5. **`wxpython` (v4.2.3) was included because `psychopy` (v.2025.1.1) depends on `wxpython`**

```bash
# Install the required libraries:
sudo apt install libgtk-3-dev libwebkit2gtk-4.0-dev libgl1-mesa-dev libglu1-mesa-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libjpeg-dev libtiff-dev libpng-dev libnotify-dev freeglut3-dev

# Install wxPython
pip install wxpython==4.2.3
```

6. **Stimulus Display**

- Verify PsychoPy installation
- Check model file paths
- Confirm screen configuration

# Additional Resources

1. **Source Code**

- [PsychoPy GitHub Repository](https://github.com/psychopy/psychopy.git)

