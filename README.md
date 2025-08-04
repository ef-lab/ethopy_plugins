# ethopy_plugins

The `Ethopy plugin` system provides a flexible way to extend the functionality by adding custom modules, behaviors, experiments, interfaces, and stimuli. The system supports both core modules and user plugins with intelligent conflict resolution.

## Plugin Categories

Ethopy supports two types of plugins:

- **Standalone Modules**: Individual Python files in the plugin directory
- **Categorized Plugins**: Modules organized in specific categories:\
  \- `behaviors`: Custom behavior implementations\
  \- `experiments`: Experiment definitions\
  \- `interfaces`: Hardware interface modules\
  \- `stimuli`: Stimulus control modules

## Plugin Installation

1. **Create a virtual environment and install `EthoPy`:**

   Follow instructions in [ethopy_package](https://ef-lab.github.io/ethopy_package/getting_started/#setting-up-a-virtual-environment)

2. **Installation of required packages:**

   Install any additional required packages, instructions will be provided in the README of the specific plugin 

3. **Clone the full repository:**

   ```bash
   mkdir -p ~/.ethopy/ethopy_plugins/ && cd ~/.ethopy/ethopy_plugins/
   git clone https://github.com/ef-lab/ethopy_plugins .
   ```
   Replace `ef-lab` with your username if using a fork.

4. **Set plugin path with environment variable:**

   **Linux/macOS:**
   ```bash
   export ETHOPY_PLUGIN_PATH=~/.ethopy/ethopy_plugins/your_plugin
   ```

   **Windows:**
   ```powershell
   $env:ETHOPY_PLUGIN_PATH = "$HOME\.ethopy\ethopy_plugins\your_plugin"
   ```

   Replace `your_plugin` with the actual name of the plugin you want to use (e.g., `openfield`, `vr_ball`).

## Running the Experiment

1. **Task configuration file `your_plugin_task.py`**:

The task configuration file sets up the experiment parameters and stimulus conditions. You need to specify the task path, create it if doesn't exist and add the configuration file: `/path_to_your_conf_file/your_plugin_task.py`

2. **Start EthoPy with the task**:

```bash
ethopy -p /path_to_your_conf_file/your_plugin_task.py
```

3. **Monitor the experiment**:
- Check the Control table for experiment status
- Monitor behavioral data in the database
- View log files for detailed information


## Troubleshooting

### Common Issues

1. **Plugin path**
```bash
# Check plugin path and if it matches the one you used to transfer your files
python -c "from ethopy.plugin_manager import PluginManager; pm = PluginManager(); print(pm._plugin_paths)"
```

2. **Database Connection**
- Verify database credentials
- Check table permissions
- Ensure schema exists

### Debug Logging

Enable detailed logging:
```bash
ethopy --log-console --log-level DEBUG -p /path_to_your_conf_file/plugin_task.py
```

## Best Practices

**Task Configuration**
- Use descriptive condition names
- Document parameter choices
- Test configurations before experiments

## Additional Resources

1. **Documentation**
- [Ethopy Plugin system](https://ef-lab.github.io/ethopy_package/plugin.html)
- [EthoPy Documentation](https://ef-lab.github.io/ethopy_package/)
- [DataJoint Documentation](https://docs.datajoint.org/)

2. **Source Code**
- [EthoPy GitHub Repository](https://github.com/ef-lab/ethopy_package)
- [Example Configurations](https://github.com/ef-lab/ethopy_package/tree/main/src/ethopy/task)

3. **Support**
- [Issue Tracker](https://github.com/ef-lab/ethopy_package/issues)
- [Contributing Guidelines](https://github.com/ef-lab/ethopy_package/blob/main/CONTRIBUTING.md)
