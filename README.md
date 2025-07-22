# ethopy_plugins

The `Ethopy plugin` system provides a flexible way to extend the functionality by adding custom modules, behaviors, experiments, interfaces, and stimuli. The system supports both core modules and user plugins with intelligent conflict resolution.

# Plugin Categories

Ethopy supports two types of plugins:

- **Standalone Modules**: Individual Python files in the plugin directory
- **Categorized Plugins**: Modules organized in specific categories: 
      -  `behaviors`: Custom behavior implementations 
      - `experiments`: Experiment definitions 
      - `interfaces`: Hardware interface modules 
      - `stimuli`: Stimulus control modules


## Importing plugins

1. **Install `EthoPy`**

    ```bash
    pip install ethopy
    ```

2. **Git clone repository**

   ```bash
   git clone https://github.com/user/repository.git
   ```

   Replace `user/repository.git` with the actual GitHub repository URL.

3. **Add Path to the plugins**

   ```bash
   export ETHOPY_PLUGIN_PATH=~/.ethopy/ethopy_plugins/plugin_folder_name

   # for Windows:
   $env:ETHOPY_PLUGIN_PATH = "$HOME\.ethopy\ethopy_plugins\plugin_folder_name"
   ```
   Replace `plugin_folder_name` with the specific folder that you want.   
