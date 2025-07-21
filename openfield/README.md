# OpenField Experiment with Panda3D in EthoPy

This guide explains how to use the OpenField experiment with Panda3D visual stimuli and real-time animal tracking in EthoPy. 

## What is the OpenField Experiment?

The OpenField experiment is a behavioral paradigm where animals freely navigate within a defined arena while being tracked in real-time using computer vision. This plugin implements an advanced version that combines:

- **Real-time pose estimation** using DeepLabCut to track animal position (nose, ears) with sub-centimeter precision
- **3D stimulus presentation** using Panda3D with ego-centric perspective that follows the animal's viewpoint
- **Spatial navigation tasks** where animals approach specific locations to receive rewards
- **Arena calibration system** that automatically detects arena corners and converts between camera and real-world coordinates

### Experimental Flow:

1. **Arena Setup**: The system automatically detects arena corners using a DLC model and calculates perspective transformation
2. **Animal Tracking**: Continuous pose estimation tracks the animal's head position (nose + ears) and orientation
3. **Stimulus Presentation**: 3D objects are rendered from the animal's perspective with dynamic camera positioning
4. **Behavioral Task**: Animals navigate to response locations to trigger rewards, with customizable spatial contingencies
5. **Data Collection**: All pose data, behavioral events, and stimulus presentations are logged to the database

The experiment is ideal for studying spatial navigation, visual object recognition, and approach behaviors in freely moving animals.

## Setup involves three main components:

1. `openfield.py` - The behavior plugin for tracking and spatial contingencies
2. `approach.py` - The experiment plugin for trial structure and state management
3. `panda.py` - The stimulus plugin for 3D visual presentation

## Setup Instructions

### Installation

#### Basic Installation
```bash
pip install -r requirements.txt
```

#### DeepLabCut Live Setup with CUDA Support (Ubuntu)

For real-time pose estimation, you'll need to set up DeepLabCut Live with CUDA support:

**1. Install CUDA 11.8**
```bash
# Update system and install dependencies
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install gcc-9 g++-9

# Set up GCC alternatives
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 --slave /usr/bin/g++ g++ /usr/bin/g++-9 --slave /usr/bin/gcov gcov /usr/bin/gcov-9

# Download and install CUDA 11.8
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run --toolkit --no-opengl-libs

# Add CUDA to PATH (use immediate export first, then add to bashrc)
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
echo 'export PATH=/usr/local/cuda-11.8/bin${PATH:+:${PATH}}' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
source ~/.bashrc

# Verify CUDA installation
nvcc --version
# Expected output:
# nvcc: NVIDIA (R) Cuda compiler driver
# Copyright (c) 2005-2022 NVIDIA Corporation
# Built on Wed_Sep_21_10:33:58_PDT_2022
# Cuda compilation tools, release 11.8, V11.8.89
# Build cuda_11.8.r11.8/compiler.31833905_0
```

**2. Install cuDNN 8.6**
```bash
# Download cuDNN from NVIDIA website, then:
tar -xvf cudnn-linux-x86_64-8.6.0.163_cuda11-archive.tar.xz
sudo cp cudnn-*-archive/include/cudnn*.h /usr/local/cuda/include
sudo cp -P cudnn-*-archive/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

**3. Set up Python Environment**
```bash
# Install Python virtual environment support
sudo apt install python3-venv

# Create virtual environment
python3 -m venv tf_env
source tf_env/bin/activate

# Install TensorFlow 2.12 (compatible with CUDA 11.8)
pip install tensorflow==2.12

# Verify GPU detection
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Install DeepLabCut Live and dependencies
pip install deeplabcut-live
pip install opencv-python --upgrade

# Test DLC Live installation
dlc-live-test
```

**4. Alternative: Conda Environment**
```bash
# Install Miniconda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
source ~/miniconda3/bin/activate

# Create DeepLabCut environment from YAML file (if available)
conda env create -f DEEPLABCUT.yaml
conda activate DEEPLABCUT

# Or create manually:
conda create -n dlc-live python=3.8
conda activate dlc-live
pip install tensorflow==2.12
pip install deeplabcut-live
```

### Plugin Installation

Instead of manually copying the plugin files, you can use **Git sparse checkout** to clone only the `openfield` folder from the repository.

#### Clone Only the `openfield` Folder

1. **Initialize a new Git repository:**
   ```bash
   mkdir -p ~/.ethopy/ethopy_plugins/ && cd ~/.ethopy/ethopy_plugins/
   git init
   ```

2. **Add the remote repository:**
   ```bash
   git remote add origin https://github.com/ef-lab/ethopy_plugins
   ```

3. **Enable sparse checkout:**
   ```bash
   git config core.sparseCheckout true
   ```

4. **Specify the folder to fetch:**
   ```bash
   echo "openfield" >> .git/info/sparse-checkout
   ```

5. **Pull the specified folder:**
   ```bash
   git pull origin main
   ```

6. **Add Path to the plugins**
   ```bash
   export ETHOPY_PLUGIN_PATH=~/.ethopy/ethopy_plugins/openfield
   ```

### Upload Objects

Upload 3D objects from folder to the Objects table in the stimulus schema:

```bash
python upload_objects.py
```

## Plugin Components

### 1. OpenField Behavior (`openfield.py`)

The OpenField behavior implements an open field experiment paradigm where subjects navigate freely in a defined area with real-time tracking.

```python
# Example usage in task configuration
from ethopy.behavior.openfield import OpenField

# Key parameters
params = {
    'model_path': '/path/to/dlc/model',
    'response_loc_x': -0.3,     # Response locations relative to the screen
    'response_loc_y': 0.3,
    'init_loc_x': 20,                 # Starting position
    'init_loc_y': 150,
    'radius':7-,                   # Detection radius (cm)
    'reward_amount': 6,              # Reward amount
    'reward_type': 'water'           # Reward type
}
```

#### Features:
- Real-time animal tracking using DeepLabCut
- Response location detection with radius-based proximity
- Reward port management and delivery
- Position logging and activity tracking
- Arena coordinate system conversion
- Shared memory integration for pose data

### 2. Approach Experiment (`approach.py`)

The Approach experiment implements a behavioral paradigm where animals approach specific locations for rewards with adaptive trial selection.

```python
# Example usage in task configuration
from ethopy.experiments.approach import Approach

# Key parameters
params = {
    'trial_selection': 'staircase',  # Trial selection method
    'max_reward': 3000,              # Maximum reward amount
    'min_reward': 500,               # Minimum reward amount
    'trial_duration': 10000,         # Trial duration (ms)
    'init_ready': 1000,              # Time at init position (ms)
    'trial_ready': 500,              # Time at response position (ms)
    'punish_duration': 2000,         # Punishment timeout (ms)
    'intertrial_duration': 1000,     # Inter-trial interval (ms)
}
```

#### States:
1. `Entry` - Experiment initialization
2. `PreTrial` - Preparation and initialization check
3. `Trial` - Active trial with stimulus presentation
4. `Reward` - Deliver reward for correct response
5. `Punish` - Timeout for incorrect response  
6. `Abort` - Handle trial timeout
7. `InterTrial` - Inter-trial interval
8. `Hydrate` - Hydration during sleep periods
9. `Offtime` - Sleep/rest periods
10. `Exit` - Experiment termination

### 3. Panda3D Stimulus (`panda.py`)

The Panda stimulus plugin provides 3D visual stimulus presentation with perspective-based rendering that follows the animal's position.

```python
# Example usage in task configuration
from ethopy.stimuli.panda import Panda
```

#### Features:
- 3D model loading and display
- Real-time camera positioning based on animal location
- Perspective-based object presentation with ego-centric view
- Dynamic field of view adjustment (dolly zoom)
- Object transformation (rotation, position, scaling)
- Shared memory integration for real-time pose data
- Movie playback capability

## Running the Experiment

1. **Configure arena setup and upload 3D objects**

2. **Start EthoPy with the task**:
```bash
ethopy -p ~/.ethopy/tasks/openfield_task.py
```

3. **Monitor the experiment**:
- Check the Control table for experiment status
- Monitor behavioral data in the database
- View log files for detailed information

## Database Tables and Configuration

### Required User Configuration Tables

These tables must be configured by the user before running experiments:

#### 1. **SetupConfigurationArena** - Arena Physical Setup
**User must populate:** Physical arena parameters and model paths

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `setup_conf_idx` | int | Setup configuration index | 1 |
| `arena_idx` | tinyint | Arena identifier | 1 |
| `size` | int | Arena size in cm | 60 |
| `description` | varchar(256) | Arena description | "60cm square arena" |

#### 2. **SetupConfigurationArena.Models** - DLC Model Configuration
**User must populate:** Paths to DeepLabCut models

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | varchar(256) | Model identifier | "bodyparts_model" |
| `path` | varchar(256) | Full path to DLC model | "/path/to/dlc/model" |
| `target` | enum | Model type | "bodyparts" or "corners" |

*Required models:*
- **bodyparts**: Tracks nose, left ear, right ear for pose estimation
- **corners**: Detects 4 arena corners for coordinate transformation

#### 3. **SetupConfigurationArena.Screen** - Visual Display Setup
**User must populate:** Screen position relative to arena

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `screen_idx` | tinyint | Screen identifier | 1 |
| `start_x` | float | Screen start x position (cm) | -30 |
| `start_y` | float | Screen start y position (cm) | 30 |
| `stop_x` | float | Screen end x position (cm) | 30 |
| `stop_y` | float | Screen end y position (cm) | 30 |

#### 4. **SetupConfigurationArena.Port** - Reward Port Locations
**User must populate:** Physical port positions in arena coordinates

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `port` | tinyint | Port number | 1 |
| `type` | enum | Port type | "Lick" or "Proximity" |
| `position_x` | float | Port x position (cm from center) | 20 |
| `position_y` | float | Port y position (cm from center) | 20 |

#### 5. **Objects** - 3D Stimulus Objects
**User must populate:** Upload 3D objects for stimulus presentation

| Field | Type | Description |
|-------|------|-------------|
| `obj_id` | int | Unique object identifier |
| `description` | varchar(256) | Object description |
| `object` | longblob | 3D object file data (.egg format) |
| `file_name` | varchar(255) | Original filename |

### Experimental Condition Tables

These define the experimental parameters:

#### 6. **OpenField** - Behavior Conditions
**User configures:** Spatial task parameters

| Field | Type | Description | Coordinate System |
|-------|------|-------------|-------------------|
| `model_path` | varchar(256) | Path to DLC bodyparts model | - |

#### 7. **OpenField.Response** - Response Location Definitions
**User configures:** Where animals must go to trigger responses

| Field | Type | Description | Coordinate System |
|-------|------|-------------|-------------------|
| `response_loc_x` | float | Response x position | **Screen coordinates** (-1 to 1) |
| `response_loc_y` | float | Response y position | **Screen coordinates** (-1 to 1) |
| `radius` | float | Detection radius (cm) | Arena coordinates |
| `response_ready` | float | Time required at location (ms) | - |
| `response_port` | tinyint | Associated port number | - |

#### 8. **OpenField.Init** - Initialization Positions
**User configures:** Where animals must be to start trials

| Field | Type | Description | Coordinate System |
|-------|------|-------------|-------------------|
| `init_loc_x` | float | Initial x position | **Arena coordinates** (cm from center) |
| `init_loc_y` | float | Initial y position | **Arena coordinates** (cm from center) |
| `init_radius` | float | Detection radius (cm) | Arena coordinates |
| `init_ready` | float | Time required at location (ms) | - |

#### 9. **OpenField.Reward** - Reward Configuration
**User configures:** Reward contingencies and amounts

| Field | Type | Description | Coordinate System |
|-------|------|-------------|-------------------|
| `reward_loc_x` | float | Reward x position | **Screen coordinates** (-1 to 1) |
| `reward_loc_y` | float | Reward y position | **Screen coordinates** (-1 to 1) |
| `reward_port` | tinyint | Port for reward delivery | - |
| `reward_amount` | float | Reward amount (μL or arbitrary units) | - |
| `reward_type` | varchar(16) | Type of reward | "water", "food", etc. |
| `radius` | float | Detection radius (cm) | Arena coordinates |

### Coordinate System Explanation

**Critical:** The plugin uses two different coordinate systems:

1. **Screen Coordinates** (`response_loc_x/y`, `reward_loc_x/y`):
   - Range: -1.0 to 1.0 
   - Relative to visual display screen position
   - Converted to arena coordinates using screen position parameters

2. **Arena Coordinates** (`init_loc_x/y`, port positions, radii):
   - Units: centimeters from arena center
   - Real physical distances in the arena
   - Used directly for proximity detection

### Automatically Generated Tables

These are populated automatically during experiments:

#### 10. **ConfigurationArena.Corners** - Detected Arena Corners
**Auto-generated:** Corner detection results

| Field | Type | Description |
|-------|------|-------------|
| `corners` | blob | Detected corner positions in camera coordinates |
| `affine_matrix` | blob | Transform matrix from camera to arena coordinates |

#### 11. **Activity** & **Activity.Openfield** - Animal Tracking Data
**Auto-generated:** Real-time position and behavioral events

| Field | Type | Description |
|-------|------|-------------|
| `animal_loc_x` | float | Animal x position (arena coordinates) |
| `animal_loc_y` | float | Animal y position (arena coordinates) |
| `time` | float | Timestamp |
| `in_pos` | int | Whether animal is in target location (0/1) |
| `resp_loc_x` | float | Target response location x |
| `resp_loc_y` | float | Target response location y |

### DLC Data Logging

The system automatically logs detailed pose estimation data:

- **Raw DLC output**: All detected keypoints with confidence scores
- **Processed poses**: Filtered and corrected pose data with interpolation for low-confidence detections  
- **Transformed coordinates**: Arena coordinates after perspective transformation
- **Head orientation**: Calculated from nose-to-ear vectors for directional analysis

## Troubleshooting

### Common Issues

1. **Plugin path**
```bash
# Check plugin path and if it matches the one you used to transfer your files
python -c "from ethopy.plugin_manager import PluginManager; pm = PluginManager(); print(pm._plugin_paths)"
```

2. **DeepLabCut Setup**
- Verify both body part and corner detection models are configured
- Check model paths in SetupConfigurationArena.Models table
- Ensure camera is properly initialized before DLC

3. **Arena Calibration**
- Verify arena corners are detected within 60 seconds
- Check coordinate system calibration
- Ensure proper affine matrix calculation

4. **Animal Tracking**
- Verify shared memory configuration
- Check pose estimation process is running
- Monitor activity logging for position data

5. **Stimulus Display**
- Verify Panda3D installation
- Check 3D object file paths and Objects table
- Confirm screen configuration matches arena setup
- Test perspective mode functionality

### Debug Logging

Enable detailed logging:
```bash
ethopy --log-console --log-level DEBUG -p your_task_path.py
```

### Optional System Tools

Install additional tools for monitoring and debugging:

```bash
# System monitoring
sudo apt install htop

# Network tools  
sudo apt install net-tools
sudo apt install ethtool

# Check GPU status
watch -n1 nvidia-smi

# Check network interface timing (for precision timing)
ethtool -T enp7s0  # replace with your network interface
```

## Best Practices

**Arena Setup**
- Calibrate arena coordinates before experiments
- Test tracking accuracy across the entire arena
- Verify reward port positions and functionality

**Task Configuration**
- Use appropriate timing parameters for your species
- Test response detection radii in the actual arena
- Validate reward amounts and delivery timing

**3D Stimulus Presentation**
- Store objects in database before experiments
- Test perspective mode with live tracking
- Verify object positioning relative to animal location

## Additional Resources

1. **Documentation**
- [EthoPy Documentation](https://ef-lab.github.io/ethopy_package/)
- [Panda3D Manual](https://docs.panda3d.org/1.10/python/index)
- [DeepLabCut Documentation](http://www.mackenziemathislab.org/deeplabcut)
- [DataJoint Documentation](https://docs.datajoint.org/)

2. **Source Code**
- [EthoPy GitHub Repository](https://github.com/ef-lab/ethopy_package)
- [Example Configurations](https://github.com/ef-lab/ethopy_package/tree/main/src/ethopy/task)

3. **Support**
- [Issue Tracker](https://github.com/ef-lab/ethopy_package/issues)
- [Contributing Guidelines](https://github.com/ef-lab/ethopy_package/blob/main/CONTRIBUTING.md)