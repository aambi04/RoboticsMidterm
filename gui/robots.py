import numpy as np

#constants TODO: look at these measurments more closely
L = 4
H = 2
R = 1   # wheel radius
ri = 0.25   # roller radius

#
# def processRectangle()

def processing(v_d, theta_d, theta_new):         #20 ms readings

    print "cos", round(np.cos(theta_d - theta_new),2)
    v_cx = v_d * np.cos(theta_d - theta_new)

    v_cy = v_d * np.sin(theta_d - theta_new)


    # wheelRotationalVelocity(v_cx, v_cy, omega)

    return v_cx, v_cy

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

    # print psi


wheelRotationalVelocity(4,5,0)