import os
import subprocess

def run_command(command):
    """Executes a command in the terminal and prints the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e.stderr}")
        exit(1)

def install_psychopy():
    print("Updating apt packages...")
    run_command("sudo apt update")

    print("Installing build dependencies...")
    run_command("sudo apt install -y build-essential libssl-dev libffi-dev python3-dev")

    print("Upgrading pip...")
    run_command("pip install --upgrade pip")

    print("Installing specific versions of Python packages...")
    run_command("pip install numpy==1.24.4")
    run_command("pip install pyglet==1.5.27")
    run_command("pip install pandas==2.0.3")
    run_command("pip install pyzmq==26.2.1")
    run_command("pip install setuptools==66.1.1")
    run_command("pip install json_tricks==3.17.3")
    #run_command("pip install wxPython>=4.1.1")
    run_command("pip install h5py==3.13.0")

    print("Installing libpcre2-32-0...")
    run_command("sudo apt install libpcre2-32-0")

    print("Installing python-bidi...")
    run_command("pip install python-bidi")

    print("Installing remaining PsychoPy dependencies...")
    run_command("pip install arabic-reshaper astunparse esprima ffpyplayer freetype-py future gevent gitpython javascripthon markdown-it-py msgpack-numpy openpyxl psychtoolbox pyparallel pypi-search python-gitlab python-vlc questplus soundfile tables ujson websockets xmlschema")

    print("Installing PsychoPy...")
    run_command("pip install psychopy==2024.1.2 --no-deps")

if __name__ == "__main__":
    install_psychopy()
