# Go/No-go task
from ethopy.experiment.match_to_sample import Experiment
from ethopy.stimuli.psycho_grating import PsychoGrating
from ethopy.Behaviors.MultiPort import MultiPort
from ethopy.core import logger


# define session parameters
session_params = {
    "start_time": "08:00:00",  # start time of the session
    "stop_time": "22:00:00",  # stop time of the session
    "setup_conf_idx": 1,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)
block = exp.Block(difficulty=0, next_up=0, next_down=0, trial_selection="staircase")

# define stimulus conditions
key = {
    # Experimental Parameters
    "intertrial_duration": 1000,
    "abort_duration": 0,
    "init_ready": 200,
    "delay_ready": 0,
    "resp_ready": 0,
}


conditions = []


Grating_Stimuli = PsychoGrating()
Grating_Stimuli.fill_colors.ready = []
Grating_Stimuli.fill_colors.background = []


# Define background color
Grating_Stimuli.fill_colors.set(
    {
        "background": (0, 0, 0),
        "start": (0.2, 0.2, 0.2),
        "ready": (0.3, 0.3, 0.3),
        "reward": (0.9, 0.9, 0.9),
        "punish": (0, 0, 0),
        "delay": (0.2, 0.2, 0.2),
    }
)

# Define grating condition
cue_grating = [0, 0, 90, 90]
resp_grating = [(0, 90), (90, 0), (90, 0), (0, 90)]
response_port = [1, 2, 1, 2]
reward_port = [1, 2, 1, 2]


# Define condition: during "cue period" a grating (vertical or horizontal) is presented, and during "response period" \
# two gratings (vertical and horizontal) are presented. The subject has to respond to the grating orientation \
# presented during the "cue period" by licking the corresponding port. If the response is correct, a reward is given, \
# otherwise a punishment is given.

for idx, port in enumerate(reward_port):
    conditions += exp.make_conditions(
        stim_class=Grating_Stimuli,
        stim_periods=["Cue", "Response"],
        conditions={
            **block.dict(),
            **key,
            "Cue": {
                "ori": [cue_grating[idx]],  # orientation
                "pos_x": 0,  # position
                "size": 15,  # size of stimulus
                "sf": 100,  # spatial frequency
                "duration": 200,  # duration of the cue period
            },
            "Response": {
                "ori": [resp_grating[idx]],
                "pos_x": (-6, 6),
                "size": 15,
                "sf": 100,
                "duration": 200,
            },
            "reward_port": [reward_port[idx]],  # reward port
            "response_port": [response_port[idx]],  # response port
            "cue_ready": 400,
            "cue_duration": 400,
            "delay_duration": 200,
            "response_duration": 2000,
            "reward_duration": 2000,
            "punish_duration": 3000,
            "reward_amount": 6,
        },
    )


# run experiments
exp.push_conditions(conditions)
exp.start()
