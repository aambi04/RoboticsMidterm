import numpy as np

# global variables
theta = 0
omega_d = 1  # assuming a constant

psi_1 = 0
psi_2 = 0
psi_3 = 0
psi_4 = 0

#constants TODO: look at these measurments more closely
L = 4
H = 2
R = 1   # wheel radius
ri = 0.25   # roller radius

#
# def processRectangle()

def processing(v_d, theta_d, delta_t = 20):         #20 ms readings

    delta_theta =  omega_d * delta_t

    theta_new = theta + delta_theta

    v_cx = v_d * np.cos(theta_d - (theta_new + delta_theta))

    v_cy = v_d * np.sin(theta_d - (theta_new + delta_theta))

    omega = delta_theta/delta_t

    wheelRotationalVelocity(v_cx, v_cy, omega)

def wheelRotationalVelocity (vx, vy, theta):

    state_matrix = np.transpose([[vx,vy,theta]])                # take the transpose of the state vector. Dimnesions are 3x1

  #  print state_matrix

    inverse_kinematic = np.array([[1, 1, -(L+H)], [-1, 1, (L+H)], [-1, 1, -(L+H)], [1, 1, (L+H)]])     # kinematic equations
  #
  #   trans = np.transpose(kinematic_matrix)
  #
  #   result =  np.dot(kinematic_matrix, trans)
  #
  # #  print result
  #
  #   inv = np.linalg.inv(result)
  #
  #  # print inv
  #
  #   right_inv = np.dot(trans, inv)                      # Psuedo inverse is invertible on the right not left
  #
  #  # print right_inv

    psi = (1/R) * np.dot(inverse_kinematic, state_matrix)       # find the velocities of each of the wheels

    print psi


wheelRotationalVelocity(4,5,0)