# Match to Sample with Panda3D in EthoPy

This guide explains how to use the Match to Sample experiment with Panda3D visual stimuli in EthoPy. The setup involves three main components:

1. `match_to_sample.py` - The experiment plugin
2. `panda.py` - The stimulus plugin
3. `panda_test.py` - The task configuration

## Setup Instructions

### Installation
```bash
pip install panda3d
```
For more information, visit their [Panda3D GitHub repository](https://github.com/panda3d/panda3d/tree/master).

### 1. Plugin Installation

Instead of manually copying the plugin files, you can use **Git sparse checkout** to clone only the `objects_panda` folder from the repository.

#### Clone Only the `objects_panda` Folder

1. **Initialize a new Git repository:**
   ```bash
   mkdir ethopy_plugins && cd ethopy_plugins
   git init
   ```

2. **Add the remote repository:**
   ```bash
   git remote add origin https://github.com/user/repository.git
   ```
   Replace `user/repository.git` with the actual GitHub repository URL.

3. **Enable sparse checkout:**
   ```bash
   git config core.sparseCheckout true
   ```

4. **Specify the folder to fetch:**
   ```bash
   echo "path/to/objects_panda" >> .git/info/sparse-checkout
   ```
   Replace `path/to/objects_panda` with the actual path inside the repository.

5. **Pull the specified folder:**
   ```bash
   git pull origin main
   ```
   If the repository uses a different branch (e.g., `develop`), replace `main` with that branch.

### 2. Task Configuration

Copy the task configuration to your preferred location:

```bash
# Create tasks directory
mkdir -p ~/.ethopy/tasks

# Copy task configuration
cp panda_test.py ~/.ethopy/tasks/
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

The task configuration file sets up the experiment parameters and stimulus conditions.

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

1. **Plugin path**
```bash
# Check plugin path and if it matches the one you used to transfer your files
python -c "from ethopy.plugin_manager import PluginManager; pm = PluginManager(); print(pm._plugin_paths)"
```

2. **Stimulus Display**
- Verify Panda3D installation
- Check model file paths
- Confirm screen configuration

3. **Database Connection**
- Verify database credentials
- Check table permissions
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
- Test configurations before experiments

## Additional Resources

1. **Documentation**
- [EthoPy Documentation](https://ef-lab.github.io/ethopy_package/)
- [Panda3D Manual](https://docs.panda3d.org/1.10/python/index)
- [DataJoint Documentation](https://docs.datajoint.org/)

2. **Source Code**
- [EthoPy GitHub Repository](https://github.com/ef-lab/ethopy_package)
- [Example Configurations](https://github.com/ef-lab/ethopy_package/tree/main/src/ethopy/task)

3. **Support**
- [Issue Tracker](https://github.com/ef-lab/ethopy_package/issues)
- [Contributing Guidelines](https://github.com/ef-lab/ethopy_package/blob/main/CONTRIBUTING.md)

