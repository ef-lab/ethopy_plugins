# ethopy_plugins

`plugins` are packages that extend the extend the functionality by adding custom modules, behaviors, experiments, interfaces and stimuli.

Each plugin contains:
1. `Behavior` plugins
2. `Experiment` plugins
3. `Interface` plugins
4. `Stimulus` plugins

## Importing plugins

### In Mac OS/Linux:

1. **Initialize a new Git repository:**
   ```bash
   mkdir -p ~/.ethopy/ethopy_plugins/ && cd ~/.ethopy/ethopy_plugins/
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
   echo "plugin_folder_name" >> .git/info/sparse-checkout
   ```
   Replace `plugin_folder_name` with the actual path inside the repository.

5. **Pull the specified folder:**
   ```bash
   git pull origin main
   ```
   If the repository uses a different branch (e.g., `develop`), replace `main` with that branch.

6. **Add Path to the plugins**
   ```bash
   export ETHOPY_PLUGIN_PATH=~/.ethopy/ethopy_plugins/plugin_folder_name
   ```

### In Windows:

1. **Run Windows `Powershell` as Administrator**

2. **Initialize a new Git repository:**
   ```bash
    mkdir "$HOME\.ethopy\plugin_folder_name"
    Set-Location "$HOME\.ethopy\plugin_folder_name"
    git init
   ```

3. **Add the remote repository:**
   ```bash
   git remote add origin https://github.com/user/repository.git
   ```
   Replace `user/repository.git` with the actual GitHub repository URL.

4. **Enable sparse checkout:**
   ```bash
   git config core.sparseCheckout true
   ```

5. **Specify the folder to fetch:**
   ```bash
   Add-Content .git\info\sparse-checkout "plugin_folder_name"
   ```
   Replace `plugin_folder_name` with the actual path inside the repository.

6. **Pull the specified folder:**
   ```bash
   git pull origin main
   ```
   If the repository uses a different branch (e.g., `develop`), replace `main` with that branch.

7. **Add Path to the plugins**
   ```bash
   $env:ETHOPY_PLUGIN_PATH = "$HOME\.ethopy\ethopy_plugins\plugin_folder_name"
   ```
