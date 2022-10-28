import os
import numpy as np
import raisimpy as raisim
import time
import copy

raisim.World.setLicenseFile(os.path.dirname(os.path.abspath(__file__)) + "/../raisimLib/rsc/activation.raisim")
a1_urdf_file = os.path.dirname(os.path.abspath(__file__)) + "/../raisimLib/rsc/a1/urdf/a1.urdf"

#  create raisim world
world = raisim.World()
world.setTimeStep(0.001)

# create objects
ground = world.addGround()
ground.setAppearance("steel")

# create robots
a1 = world.addArticulatedSystem(a1_urdf_file)
a1.setName("a1")

# a1 settings
# PD controller
a1_nominal_joint_config = np.array([0, 0, 0.54, 1.0, 0.0, 0.0, 0.0, 0.03, 0.4, -1.2,
                                        -0.03, 0.4, -1.2, 0.03, 0.4, -1.2, -0.03, 0.4, -1.2])
joint_pgain = 100.0*np.ones([a1.getDOF()])
joint_dgain = 1*np.ones([a1.getDOF()])
joint_velocity_target = np.zeros([a1.getDOF()])

a1.setGeneralizedCoordinate(a1_nominal_joint_config)
a1.setGeneralizedForce(np.zeros([a1.getDOF()]))
a1.setPdGains(joint_pgain, joint_dgain)
a1.setPdTarget(a1_nominal_joint_config, joint_velocity_target)
a1_joint_config = copy.deepcopy(a1_nominal_joint_config)
a1_joint_velocity_target = copy.deepcopy(joint_velocity_target)

# launch raisim server
server = raisim.RaisimServer(world)
server.focusOn(a1)
server.launchServer(8080)

print(a1.getDOF())
time.sleep(2)

# # Jacobians
# jaco_foot_lh_linear = a1.getDenseFrameJacobian("LF_ADAPTER_TO_FOOT")
# jaco_foot_lh_angular = a1.getDenseFrameRotationalJacobian("LF_ADAPTER_TO_FOOT")
# a1_joint_config[-1] = 0
# a1_joint_velocity_target[-1] = 0
for i in range(500000):
    time.sleep(0.001)
    a1_joint_config[9] = 0.1*np.sin(time.time()) #- 1.2
    # joint_velocity_target[9] = 0.1*np.sin(time.time())
    # a1.setPdTarget(a1_joint_config, joint_velocity_target)
    a1.setGeneralizedForce(a1_joint_config)
    server.integrateWorldThreadSafe()


    

server.killServer()

# if __name__ == '__main__':
    

