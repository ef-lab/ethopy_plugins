import numpy as np

from ethopy.experiment.MatchToSample import *
from ethopy.stimuli.PsychoGrating import *
from ethopy.core.behavior import *
from ethopy.behaviors.multi_port import *




# define session parameters
session_params = {
    'start_time'           : '08:00:00',
    'stop_time'            : '22:00:00',
    'setup_conf_idx'       : 1,
    'max_reward'           : 1200,
    'min_reward'           : 750,
    'hydrate_delay'        : 0,
    #'bias_window'          : 5,
    #'staircase_window'     : 20,
    #'stair_up'             : 0.7,
    #'stair_down'           : 0.55,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)

block = exp.Block(
    difficulty=0, 
    next_up=0, 
    next_down=0, 
    trial_selection='staircase'
)


# define stimulus conditions
key = {
    # Experimental parameters
    'intertrial_duration': 1000,
    'abort_duration'     : 0,
    'init_ready'         : 200,
    'delay_ready'        : 0,
    'resp_ready'         : 0,

    # Stimulus parameters
    'contrast'           : 1,
    'warper'             : 1,
}


repeat_n = 1
conditions = []

# vertical grating
cue_grating  = [0]
resp_grating = [(0,90), (90,0)]
reward_port = [1,2]
resp_ports   = [1,2]

# horizontal grating
Hcue_grating  = [90]
Hresp_grating = [(0,90), (90,0)]
Hreward_port = [1,2]
Hresp_ports   = [2,1]


Grating_Stimuli = PsychoGrating()
Grating_Stimuli.fill_colors.ready = []
Grating_Stimuli.fill_colors.background = []

Grating_Stimuli.fill_colors.set({'background': (0.5, 0.5, 0.5)})


# Define horizontal grating condition
for idx, port in enumerate(reward_port):
    # cue period (vertical grating) & Response period (vertical & horizontal)
    conditions += exp.make_conditions(stim_class=Grating_Stimuli, stim_periods=['Cue', 'Response'], conditions={
        **block.dict(), **key, 'Cue': {
                                    'ori'            : [0],
                                    'pos_x'          : (0),
                                    'size'           : 10,
                                    'sf'             : .3,
                                    'duration'       : 10000
                                },


                                'Response': {
                                    'ori'            : [resp_grating[idx]],
                                    'pos_x'          : [(-6, 6)],
                                    'size'           : 10,
                                    'sf'             : .3,
                                    'duration'       : 10000
                                },

                                'reward_port'        : port,
                                'response_port'      : resp_ports[idx],
                                'cue_duration'       : 400,
                                'cue_ready'          : 0,
                                'delay_duration'     : 500,
                                'response_duration'  : 10000,
                                'reward_duration'    : 2000,
                                'punish_duration'    : 3000,
                                'reward_amount'      : 7,


    })


# Define vertical grating conditions
for idx, port in enumerate(reward_port):
    # cue period (horizontal grating) & Response period (vertical & horizontal)
    conditions += exp.make_conditions(stim_class=Grating_Stimuli, stim_periods=['Cue', 'Response'], conditions={
        **block.dict(), **key, 'Cue': {
                                    'ori'            : [90],
                                    'pos_x'          : (0),
                                    'size'           : 10,
                                    'sf'             : .3,
                                    'duration'       : 10000
                                },

                                'Response': {
                                    'ori'            : [Hresp_grating[idx]],
                                    'pos_x'          : [(-6, 6)],
                                    'size'           : 10,
                                    'sf'             : .3,
                                    'duration'       : 10000
                                },

                                'reward_port'        : port,
                                'response_port'      : Hresp_ports[idx],
                                'cue_duration'       : 400,
                                'cue_ready'          : 0,
                                'delay_duration'     : 500,
                                'response_duration'  : 10000,
                                'reward_duration'    : 2000,
                                'punish_duration'    : 3000,
                                'reward_amount'      : 7,
    })

# run experiments
exp.push_conditions(conditions)
exp.start()