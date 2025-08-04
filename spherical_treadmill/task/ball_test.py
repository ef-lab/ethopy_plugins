# Navigate on a VR ball
import numpy as np

from ethopy.experiment.navigate import Experiment
from ethopy.stimuli.vr_odors import VROdors
from ethopy.behaviors.vr_ball import VRBall 
from ethopy.core import logger


# define session parameters
session_params = {
    "start_time": "08:00:00",  # start time of the session
    "stop_time": "22:00:00",  # stop time of the session
    "setup_conf_idx": 3,
}


exp = Experiment()
exp.setup(logger, VRBall, session_params) 

np.random.seed(0)
conditions = []

block = exp.Block(difficulty=0, next_up=0, next_down=0, trial_selection="staircase")

non_resp = .1
scale = 2   #has to change every time the environment size changes - depending on the space the radii change
radius = 2**.5*(scale/2) - non_resp

conditions += exp.make_conditions(
    stim_class=VROdors(), 
    conditions={**block.dict(),
                'odorant_id'            : (1, 2, 4, 3),
                'delivery_port'         : (1, 2, 4, 3),
                'odor_x'                : (0, scale, scale, 0),
                'odor_y'                : (0, 0, scale, scale),
                'x0'                    : scale/2,
                'y0'                    : scale/2,
                'theta0'                : 0,
                'x_sz'                  : scale,
                'y_sz'                  : scale,
                'response_loc_x'        : (0, scale, scale, 0),
                'response_loc_y'        : (0, 0, scale, scale),
                'reward_loc_x'          : (0, scale, scale, 0),
                'reward_loc_y'          : (0, 0, scale, scale),
                'extiction_factor'      : 3,
                'radius'                : radius*10, # .5 .7  1
                'reward_amount'         : 10,
                'trial_duration'        : 3000,
                })

# run experiments
exp.push_conditions(conditions)
exp.start()
