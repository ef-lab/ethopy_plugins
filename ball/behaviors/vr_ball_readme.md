**VR Ball**

The transformation of physical ball movements into virtual reality (VR) inputs in EthoPy relies on four sets of equations. Each optical sensor has two axes: a lateral (x-axis) and a vertical (y-axis). Both x-axes encode the rotational movement of the ball. The y-axis of the sensor positioned in front of the ball captures forward/backward (palindromic) motion, whereas the y-axis of the sensor on the right side detects lateral (side-to-side) motion. To minimize measurement noise caused by the ball’s surface irregularities, the sensors are placed as close as possible to the supporting bearings, which reduces distance fluctuations.

Because palindromic and lateral movements also influence the tracking signals of the opposite sensor, the first set of equations (1) compensates for these cross-axis errors. The contamination of the rotational signal by the y-axes is then used to calculate the correct theta steps for each sensor (2, θ_step₁,₂), whose mean provides the total rotational displacement (θ).

Given the 2D nature of the VR space, the third set of equations (3) converts the cleaned signals from each sensor into x- and y-coordinate displacements, taking into account that the sensors are positioned at a 55° inclination (as described in ethopy_hardware/ball). Finally, the fourth set of equations (4) applies basic spherical trigonometry to combine the two sensor inputs into global 2D coordinates. These coordinates are then used to render the virtual environment in real time, producing the subject’s 2D trajectory for each behavioral session.


1. Calculate the theta contamination caused by the y axis of each laser mouse.

$ θ_{c1} = y_2 * sin^2φ_{z1} $

$ θ_{c2} = - y_1 * sin^2φ_{z2} $


2. Calculate each mouse's theta by subtracting the analogous theta contamination produced by the y-axes and let total theta be the mean of both sensors' corrected values.

$ θstep_n =\dfrac{x_{n} - θ_{cn}}{sin^{2}φ_{zn}}, \: $     for   $ n=1,2 $ 

$ θ = \dfrac{θstep_{1} + θstep_{2}}{2} $ 

3. Transform the 3-dimensional data acquisition to a virtual 2-dimensional environment with transf-x and transf-y values by using spherical trigonometry.

$ transf_{x} = y_{2} * cosθy_{1} - y_{1} * θ_{y1} $

$ transf_{y} = y_{2} * cosθy_{1} + y_{1} * θ_{y1} $

4. Using the transformational x and y and the total theta to properly set the x and the y axes of the virtual space.

$ x = - transf_{x} * sinθ - transf_{y} * cosθ $

$ y = - transf_{x} * cosθ + transf_{y} * sinθ $