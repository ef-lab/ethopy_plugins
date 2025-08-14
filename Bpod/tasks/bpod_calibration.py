from ethopy.experiments.calibrate import Experiment

# define calibration parameters
session_params = {
    "duration": [20, 30, 40, 150],
    "ports": [1, 2],
    "pulsenum": [60, 30, 20, 10],
    "pulse_interval": [40, 40, 40, 40],
    "save": True,
    # "setup_conf_idx": 1,  # index of the setup configuration for the BpodPorts
}

if "setup_conf_idx" not in session_params or session_params["setup_conf_idx"] is None:
    print("=" * 60)
    print("⚠️  CONFIGURATION REQUIRED")
    print("=" * 60)
    print("Please define 'setup_conf_idx' in session_params")
    print("This should be the index of your BpodPorts setup configuration")
    print("Example: \"setup_conf_idx\": 0")
    print("=" * 60)
    raise ValueError("setup_conf_idx parameter is required but not defined")

# run experiment
exp = Experiment()
exp.setup(logger, session_params)
exp.run()
