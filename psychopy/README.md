<h1 align="center">Integration of PsychoPy in EthoPy</h1>

PsychoPy is Python-based open-source package that enables the creation and manipulation of visual stimuli. For more information, visit their: [PsychoPy](https://www.psychopy.org/). \
This guide explains how to install and import implement PsychoPy through EthoPy. The setup involves three main components:

1. `MatchToSample.py` - The experiment plugin
2. `PsychoGrating.py` - The stimulus plugin
3. `PsychoPresenter.py` - The utils plugin 
4. `PsychoGrating_test.py` - The task configuration
5. `PsychoDummyPorts.py` - The Interface plugin


# Setup instruction

`PsychoPy` (2024.1.2) needs specific version of Python packages. For this reason, we have create a requirement.txt that install PsychoPy with all necessary packages.

## Plugin Installation
Instead of manually copying the plugin files, yoy can use Git sparse checkout to clone only the `psychopy` folder from the repository.

### Clone only the `psychopy` Folder

1. **Initialize the new Git repository**:
```bash
mkdir -p ~/.ethopy/ethopy_plugins/ && cd ~/.ethopy/ethopy_plugins/
git init
```

2. **Add the remote repository**:

```bash
git remote add origin https://github.com/ef-lab/ethopy_plugins
```
<ins>Note</ins>: Replace `user/repository.git` with the actual GitHub repository URL.

3. **Enable sparse chechout**:
```bash
git config core.sparseCheckout true
```

4. **Specify the folder to fetch**:
```bash
echo "psychopy" >> .git/info/sparse-checkout
```
<ins>Note</ins>: Replace `psychopy` with the actual path inside the repository.

5. **Pull the specified folder**:
```bash
git pull origin main
```
<ins>Note</ins>: If the repository uses a different branch (e.g. develop), replace `main` with that branch. 

6. **Add Path to the plugins**:
```bash
export ETHOPY_PLUGIN_PATH=~/.ethopy/ethopy_plugins/psychopy
```



## PsychoPy installation


<details>
<summary><b>Raspbian OS</b></summary>


1. **Verify python version** 
_PsychoPy mentions, "We strongly recommend you use Python 3.10 or 3.8."_
```bash
python --version # or python -V
sudo apt install python3.10 python3.10-venv python3.10-dev      # Otherwise, install python3.10
```

2. **Create a virtual environment (venv)**
```bash
python -m venv psychopy_venv         # or python3.10 -m venv psychopy_venv
source psychopy_env/bin/activate     # activate the venv
```

3. **Update `pip` (<ins>OPTIONAL</ins>)**:
```bash
pip install --upgrade pip
```

4. **Install `UV`** 
_UV is an extremely fast Python package and project manager, written in Rust. For more information, vitit their [UV](https://docs.astral.sh/uv/). We recommend uv for a more quick installation of libraries and psychopy too_
```bash
pip install uv
```

5. **Install `EthoPy`**:
```bash
pip install EthoPy
```

6. **Connect to the repository**
```bash
ls          # list files
cd EthoPy   # go to the EthoPy directory
```

7. **Install `PsychoPy`**:
```bash
uv pip install psychopy==2024.1.2 --no-deps
```
<ins>Note 1:</ins> PsychoPy is a large package, and its installation can take considerable time. By default, it attempts to install several dependencies such as `wxPython` (<i>useful for certain parts of PsychoPy, especially for Builder view or any of its graphical user interface  (GUI) components</i>). However, since wxPython is often platform-specific and slow to installation, we recommend installing PsychoPy without dependencies and manually managing only the ones you need.

<ins>Note 2:</ins> We recommend installing `psychopy==2024.1.2`, as it has been tested and shown to be compatible with EthoPy's structure and state machine logic.


8. **Create a `requirements.txt`**:
```bash
nano requirement.txt

#add: 
# core dependencies for psychopy
numpy==1.24.4           # for stimulus generation, timing precision and fast array operations
pandas==2.0.3           # data analysis library
pyzmq==26.2.1           # Communication between processes or networked components. 
setuptools==66.1.1      # for packaging and distributing Python projects
json_tricks==3.17.3     # save/load complex data in JSON
h5py==3.13.0            # library for HDF5 binary data format.
```

9.  **Install `requirements.txt`**:
```bash
uv pip install -r requirements.txt
```
<ins>Note:</ins> In case, you want install wxPython too, we recomment: 

```bash
uv pip install wxPython>=4.1.1
nano requirement.txt

# add:
psychopy==2024.1.2
numpy==1.24.4           
pandas==2.0.3           
pyzmq==26.2.1          
setuptools==66.1.1      
json_tricks==3.17.3     
h5py==3.13.0            

uv pip install -r requirements.txt

```
</details>



<details>

<summary><b>Mac OS</b></summary>

</details>


<details>

<summary><b>Windows</b></summary>

If you are in Windows, you can install and run EthoPy and PsychoPy either through `Ubuntu` or `PowerShell`. 

<details>

<summary>Ubuntu</summary>

1. **Install Ubuntu via wsl**

For an easier way, we recommend to install Ubuntu via wsl. For more information, visit their [WSL](https://ubuntu.com/desktop/wsl). \
<ins>Note</ins> The above script has been tested in Ubuntu 24.04.2 LTS

2. **Install `pyenv`**: 

`pyenv` is a Python version management tool that allows you to install and swithc between multiple Python versions without affecting your system's global Python version. `PsychoPy` runs with Python 3.8 or 3.10, so we recommend using `pyenv` in order to avoid any conflicts with other packages or Python environemnts. For installation, visit their [pyenv](https://github.com/pyenv/pyenv.git).

3. **Create a `virtual environment`**:
```bash
# install python version (e.g. v3.10)
pyenv install 3.10
# create a virtual environment 
pyenv virtualenv 3.10 psych_env
# activate it
pyenv activate psych_env  
```

4. **Verify `python` version**:
```bash
python --version # or python -V
```

<!-- 3. **Verify `python` version**:

```bash
python --version # or python -V
sudo apt install python3.10 python3.10-venv python3.10-dev      # Otherwise, install python3.10
``` -->

5. **Update `pip` (<ins>OPTIONAL</ins>)**:
```bash
pip install --upgrade pip
```

6. **Install `UV`** (<ins>OPTIONAL</ins>):

_UV is an extremely fast Python package and project manager, written in Rust. For more information, vitit their [UV](https://docs.astral.sh/uv/). We recommend uv for a more quick installation of libraries and psychopy too_
```bash
pip install uv
```

7. **Install `EthoPy`**:
```bash
uv pip install EthoPy
```

8. **Install `PsychoPy`**:
```bash
uv pip install psychopy==2024.1.2 --no-deps
```
<ins>Note 1:</ins> PsychoPy is a large package, and its installation can take considerable time. By default, it attempts to install several dependencies such as `wxPython` (<i>useful for certain parts of PsychoPy, especially for Builder view or any of its graphical user interface  (GUI) components</i>). However, since wxPython is often platform-specific and slow to installation, we recommend installing PsychoPy without dependencies and manually managing only the ones you need.

<ins>Note 2:</ins> We recommend installing `psychopy==2024.1.2`, as it has been tested and shown to be compatible with EthoPy's structure and state machine logic.


9. **Create a `requirements.txt`**:
```bash
nano requirement.txt

#add: 
# core dependencies for psychopy
numpy==1.24.4           # for stimulus generation, timing precision and fast array operations
pandas==2.0.3           # data analysis library
pyzmq==26.2.1           # Communication between processes or networked components. 
setuptools==66.1.1      # for packaging and distributing Python projects
json_tricks==3.17.3     # save/load complex data in JSON
h5py==3.13.0            # library for HDF5 binary data format.
PyYAML==6.0.2 
pyserial==3.5 
requests==2.32.4 
pyglet==1.5.27 
python-bidi==0.6.6 
arabic-reshaper==3.0.0 
freetype-py==2.5.1
```

10.  **Install `requirements.txt`**:
```bash
uv pip install -r requirements.txt
```

<ins>Note:</ins> In case, you want install wxPython too, we recomment: 

```bash
uv pip install wxPython>=4.1.1

nano requirement.txt
# add:
psychopy==2024.1.2
numpy==1.24.4           
pandas==2.0.3           
pyzmq==26.2.1          
setuptools==66.1.1      
json_tricks==3.17.3     
h5py==3.13.0
PyYAML==6.0.2 
pyserial==3.5 
requests==2.32.4 
pyglet==1.5.27 
python-bidi==0.6.6 
arabic-reshaper==3.0.0 
freetype-py==2.5.1            

uv pip install -r requirements.txt
```

11. **Run your experiment**:
```bash
python run.py psychopy_test.py
```

</details>

<details>

<summary>Powershell</summary>

1. **Run Windows Powershell as Administrator**

2. **Install `pyenv`**: 

To install `pyenv` in Windows, it's recommended to use [`pyenv-win`](https://github.com/pyenv-win/pyenv-win.git).

3. **Create a `virtual environment`**:
```bash
# install python version (e.g. v3.10)
pyenv install 3.10
# create a virtual environment 
pyenv virtualenv 3.10 psych_env
# activate it
pyenv activate psych_env  
```

4. **Verify `python` version**:
```bash
python --version # or python -V
```

<!-- 3. **Verify `python` version**:

```bash
python --version # or python -V
sudo apt install python3.10 python3.10-venv python3.10-dev      # Otherwise, install python3.10
``` -->

5. **Update `pip` (<ins>OPTIONAL</ins>)**:
```bash
pip install --upgrade pip
```

6. **Install `UV`** (<ins>OPTIONAL</ins>):

_UV is an extremely fast Python package and project manager, written in Rust. For more information, vitit their [UV](https://docs.astral.sh/uv/). We recommend uv for a more quick installation of libraries and psychopy too_
```bash
pip install uv
```

7. **Install `EthoPy`**:
```bash
uv pip install EthoPy
```

8. **Install `PsychoPy`**:
```bash
uv pip install psychopy==2024.1.2 --no-deps
```
<ins>Note 1:</ins> PsychoPy is a large package, and its installation can take considerable time. By default, it attempts to install several dependencies such as `wxPython` (<i>useful for certain parts of PsychoPy, especially for Builder view or any of its graphical user interface  (GUI) components</i>). However, since wxPython is often platform-specific and slow to installation, we recommend installing PsychoPy without dependencies and manually managing only the ones you need.

<ins>Note 2:</ins> We recommend installing `psychopy==2024.1.2`, as it has been tested and shown to be compatible with EthoPy's structure and state machine logic.


9. **Create a `requirements.txt`**:
```bash
nano requirement.txt

#add: 
# core dependencies for psychopy
numpy==1.24.4           # for stimulus generation, timing precision and fast array operations
pandas==2.0.3           # data analysis library
pyzmq==26.2.1           # Communication between processes or networked components. 
setuptools==66.1.1      # for packaging and distributing Python projects
json_tricks==3.17.3     # save/load complex data in JSON
h5py==3.13.0            # library for HDF5 binary data format.
PyYAML==6.0.2 
pyserial==3.5 
requests==2.32.4 
pyglet==1.5.27 
python-bidi==0.6.6 
arabic-reshaper==3.0.0 
freetype-py==2.5.1
```

10.  **Install `requirements.txt`**:
```bash
uv pip install -r requirements.txt
```

<ins>Note:</ins> In case, you want install wxPython too, we recomment: 

```bash
uv pip install wxPython>=4.1.1

nano requirement.txt
# add:
psychopy==2024.1.2
numpy==1.24.4           
pandas==2.0.3           
pyzmq==26.2.1          
setuptools==66.1.1      
json_tricks==3.17.3     
h5py==3.13.0
PyYAML==6.0.2 
pyserial==3.5 
requests==2.32.4 
pyglet==1.5.27 
python-bidi==0.6.6 
arabic-reshaper==3.0.0 
freetype-py==2.5.1            

uv pip install -r requirements.txt
```

11. **Run your experiment**:
```bash
python run.py psychopy_test.py
```

</details>

</details>

# Plugin components

## 1. Match to sample experiment (`MatchTosample.py`)
The Match to Sample experiment implements a behavioral paradigm where subjects must match a sample stimulus with a target stimulus. 

```python
# Example usage in task configuration
from ethopy.experiment.MatchToSample import ExperimentClass, State

# Key parameters
params = {
    'cue_duration': 400,       # Duration of sample presentation (ms)
    'delay_duration': 200,     # Delay between sample and choice (ms)
    'response_duration': 2000, # Time allowed for response (ms)
    'reward_amount': 6,        # Reward amount for correct response
    'punish_duration': 3000,   # Timeout duration for incorrect response (ms)
}
```

#### States:
1. `PreTrial` - Preparation for trial
2. `Cue` - Present sample stimulus
3. `Delay` - Delay period
4. `Response` - Present choice stimuli
5. `Reward` - Deliver reward for correct response
6. `Punish` - Timeout for incorrect response



## 2. PsychoGrating stimulus (`PsychoGrating.py`)

The PsychoGrating stimulus provides grating stimuli presentation using psychopy.

```python
from ethopy.stimuli.PsychoGrating import PsychoGrating
```

#### Features:
- Multiple gratings management
- Grating transformation (rotation, position, spatial & temporal frequency, mask, size, texture)



## 3. PsychoPresenter util(`PsychoPresenter.py`)

The PsychoPresenter util handles the monitor parameters about how stimuli are presented. 
```python
# In PsychoGrating stimuli
from ethopy.utils.PsychoPresenter import Presenter

# import in task configuration
from ethopy.stimuli.PsychoGrating import PsychoGrating

```

#### Features
- Fill screen with color
- Update the screen
- Close the window
- Photodiode support
- Monitor warping




## 4. Task Configuration (`psychopy.py`)

The task configuration file sets up the experiment parameters and stimulus conditions. 




# Running the Experiment

## 1. **Start EthoPy with task**:

```bash
ethopy -p ~/.ethopy/tasks/PsychoGrating_test.py
```


## 2. **Monitor the experiment**:
- check the Control table for experiment status
- Monitor behavioral data in the database
- View log files for detailed information




# Database Tables

## 1. Experiment Tables
- `Session` - Session information
- `Trial` - Trial data
- `Condition` - Trial conditions
- `Response` - Subject responses
- `MatchToSample` - Experiment conditions


## 2. Stimulus Tables
- `psycho_grating` Live Share


# Troubleshooting 

## 1. **Python version** 

PsychoPy mentions, "_We strongly recommend you use Python 3.10 or 3.8._"

## 2. **PsychoPy Installation**:

-  `Cannot initiate the connection to archive.raspberrypi.org:80 (2a00:1098:84:1e0::2). - connect (101: Network is unreachable)`
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
## 4. Segmentation Fault During OpenGL Stimulus Rendering in WSL 
`WSL`, while powerful for running Linux environments inside Windows, has struggled with OpenGL graphic rendering. How to fix it:

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


## 5. **Stimulus Display**
- Verify PsychoPy installation
- Check model file paths
- Confirm screen configuration

## 6. **Database Connection**
- Verify database credentials
- Check table permission
- Ensure schema exists


# Debug Logging

Enable detailed logging:
```bash
ethopy --log-console --log-level DEBUG -p your_task_path.py
```



# Best Practices

**Task Configuration**
- Use descriptive condition names
- Document parameter choices
- Test configurations before experiments. 

# Additional Resources

1. **Documentation**
- [DataJoint Documentation](https://docs.datajoint.org/)
- [Homebrew Documentation](https://docs.brew.sh/Homebrew-and-Python)

2. **Source Code**
- [PsychoPy GitHub Repository](https://github.com/psychopy/psychopy.git) 
- [Example Configurations](https://github.com/ef-lab/ethopy_package/tree/main/src/ethopy/task)

3. **Support**
- [Issue Tracker](https://github.com/ef-lab/ethopy_package/issues)
- [Contributing Guidelines](https://github.com/ef-lab/ethopy_package/blob/main/CONTRIBUTING.md)

4. **Youtube Channels**
- [How I handle multiple Python Versons(pyenv)](https://youtu.be/MVyb-nI4KyI?si=r4yPumW4yJU2mHu4) | NetworkChuck
- [Managing Multiple Python Versions With pyenv](https://realpython.com/intro-to-pyenv/) | Real Python

