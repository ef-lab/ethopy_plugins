# ethopy_plugins

The `Ethopy plugin` system provides a flexible way to extend the functionality by adding custom modules, behaviors, experiments, interfaces, and stimuli. The system supports both core modules and user plugins with intelligent conflict resolution.

# Plugin Categories

Ethopy supports two types of plugins:

- **Standalone Modules**: Individual Python files in the plugin directory
- **Categorized Plugins**: Modules organized in specific categories:
  \- `behaviors`: Custom behavior implementations
  \- `experiments`: Experiment definitions
  \- `interfaces`: Hardware interface modules
  \- `stimuli`: Stimulus control modules

### Plugin Installation

1. **Create a virtual environment and install `EthoPy`**

   Follow instructions here: https://ef-lab.github.io/ethopy_package/getting_started/#setting-up-a-virtual-environment

#### Install `your_plugin` Clone Only the  Folder
Instead of manually copying the plugin files, you can use **Git sparse checkout** to clone only the `your_plugin` folder from the repository.

2. **Initialize a new Git repository:**
   ```bash
   mkdir -p ~/.ethopy/ethopy_plugins/ && cd ~/.ethopy/ethopy_plugins/
   git init
   ```

3. **Add the remote repository:**
   ```bash
   git remote add origin https://github.com/ef-lab/ethopy_plugins
   ```
   Replace `ef-lab` with your username.

4. **Enable sparse checkout:**
   ```bash
   git config core.sparseCheckout true
   ```

5. **Specify the folder to fetch:**
   ```bash
   echo "your_plugin" >> .git/info/sparse-checkout
   ```
   Replace `your_plugin` with the actual path inside the repository.

6. **Pull the specified folder:**
   ```bash
   git pull origin main
   ```
   If the repository uses a different branch (e.g., `develop`), replace `main` with that branch.

7. **Add Path to the plugins**
   ```bash
   export ETHOPY_PLUGIN_PATH=~/.ethopy/ethopy_plugins/your_plugin

   # for Windows:
   $env:ETHOPY_PLUGIN_PATH = "$HOME\.ethopy\ethopy_plugins\your_plugin"
   ```
   Replace `your_plugin` with the actual name of the plugin you want to use.



