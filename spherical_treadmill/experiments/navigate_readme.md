**Navigate**

The Navigate module contains all commands used to control the behavioral assay. The Entry and Exit classes define the start and end of the task algorithm and can be easily modified to accommodate different experimental conditions. The remaining classes specify the parameters and transitions for each behavioral state.

The task begins in the Pretrial class, which initializes the behavioral and stimulus components, starts the trial timer, and transitions to the Trial class once all conditions are met. Trial governs stimulus presentation and, based on the animal’s responses, directs the workflow toward Reward, Abort, Punish, or Intertrial states.

The Trial logic is as follows:

- If the mouse licks within the reward radius and runs at $<0.025 m/s$, it transitions to Reward.

- Licking within the non-response radii triggers an Abort, restarting the trial.

- Licking within the response radii but outside the reward radius, with velocity $<0.025 m/s$, triggers Punish.

- If the trial exceeds the allowed duration (e.g., 3 minutes), the system proceeds to Intertrial.

In Reward, the software opens the water valve (see Section 3.2), logs the event timestamp, and returns to Trial. Abort logs the trial, moves to Intertrial, and starts a new trial, while Punish first introduces a delay, logs the event, and then restarts.

The reward radius is a subset of the broader response radii, which include the four odor release zones but exclude a small region near the initial position. In the easiest setting, the reward radius is centered near the starting point (usually middle of the virtual space). After the mouse successfully completes a defined number of consecutive trials, the reward region shifts farther away, progressively challenging the animal to navigate more accurately to obtain rewards.



