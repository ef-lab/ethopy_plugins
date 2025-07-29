# --- Ethopy Module Imports ---
# Ensure these paths correctly point to your ethopy installation structure.
from ethopy.experiments.match_port import Experiment
from ethopy.behaviors.multi_port import MultiPort
from ethopy.stimuli.tones import Tones


# --- Session Parameters (Typically Fixed) ---
# These parameters generally define the overall session constraints.
session_params = {
    "max_reward": 3000,      # Maximum total reward, default is based on experiment type
    "min_reward": 30,        # Minimum total reward, default is based on experiment type
    "setup_conf_idx": 0,     # Index for setup configuration, default is 0
    # Add any other relevant session-wide parameters here
    # hydrate_delay: int # delay of hydration in minutes after session ends, default is based on experiment type
    # user_name:  "bot" # name of user running the experiment default is "bot"
    # start_time: "" # session start time if not defined, session will start based on control table
    # stop_time: "" # session stop time if not defined, session will stop based on control table
}

# --- Experiment Initialization and Setup ---
exp = Experiment()  # Instantiate the experiment controller
exp.setup(logger, MultiPort, session_params)  # Pass the actual imported class

# --- Trial Conditions Definitions ---
# Define the parameters that can vary from trial to trial.
# Split into categories for clarity.

# 1. Experiment Control Conditions: How the trial progresses.
experiment_conditions = {
    'init_ready': 10,
    'trial_ready': 100,
    'intertrial_duration': 1000,
    'trial_duration': 5000,
    'reward_duration': 2000,
    'punish_duration': 1000,
    'abort_duration': 500,
    'noresponse_intertrial': True,
    'incremental_punishment': 0,
    'stair_up': 0.8,
    'stair_down': 0,
    'trial_selection': 'staircase',
    'staircase_window': 20,
    'bias_window': 5,
    'metric': 'accuracy',
    'antibias': True,
}

# 2. Behavior Conditions: Related to animal's actions and reinforcement.
behavior_conditions = {
    'reward_amount': 5,
    'reward_type': 'water',
}

# 3. Stimulus Conditions: Parameters for the sensory stimulus presented.
stimulus_conditions = {
    'tone_duration': 3000,
    'tone_frequency': 40000,
}

# --- Combine Conditions for Trial Generation ---
# Merge the dictionaries to create a base set of conditions for a single trial type.
all_conditions = {
    **experiment_conditions,
    **behavior_conditions,
    **stimulus_conditions
}

ports=[1,2]
tn_freq  = [0, 100]  

# --- Generate the List of Trial Conditions ---
conditions = []  # Initialize an empty list to hold all trial dictionaries
block=exp.Block(difficulty=1, next_down=1, next_up=1)
for idx, port in enumerate(ports):
    conditions += exp.make_conditions(stim_class=Tones(), conditions={**block.dict(),
                                                                        **all_conditions,
                                                                        'tone_pulse_freq': tn_freq[idx],
                                                                        'tone_volume'     : 0,  
                                                                        'reward_port'  : port,
                                                                        'response_port': port})

# --- Push Conditions and Start Experiment ---
exp.push_conditions(conditions)  # Load the trial sequence into the experiment
exp.start()  # Begin the trial sequence execution
