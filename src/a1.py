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
ground.setAppearance("white")

# create robots
a1 = world.addArticulatedSystem(a1_urdf_file)
a1.setName("a1")

# a1 settings
# PD controller
a1_nominal_joint_config = np.array([0, 0, 0.54, 1.0, 0.0, 0.0, 0.0, 0.03, 0.4, -1.2,
                                        -0.03, 0.4, -1.2, 0.03, 0.4, -1.2, -0.03, 0.4, -1.2])
joint_pgain = 100.0*np.ones([a1.getDOF()])
joint_pgain[[8,11,14,17]] = 0
joint_dgain = 1*np.ones([a1.getDOF()])
joint_dgain[[8,11,14,17]] = 0
joint_velocity_target = np.zeros([a1.getDOF()])

a1.setGeneralizedCoordinate(a1_nominal_joint_config)
a1.setGeneralizedForce(np.zeros([a1.getDOF()]))
a1.setPdGains(joint_pgain, joint_dgain)
a1.setPdTarget(a1_nominal_joint_config, joint_velocity_target)
a1_joint_config = copy.deepcopy(a1_nominal_joint_config)
# a1_joint_velocity_target = copy.deepcopy(joint_velocity_target)

# launch raisim server
server = raisim.RaisimServer(world)
server.focusOn(a1)
server.launchServer(8080)

print(a1.getDOF())
time.sleep(2)

# Jacobians
jaco_FR_foot_linear = a1.getDenseFrameJacobian("FR_foot_fixed")
jaco_FR_foot_angulaer = a1.getDenseFrameJacobian("FR_foot_fixed")

print(jaco_FR_foot_linear)
print(jaco_FR_foot_angulaer)

for i in range(500000):
    time.sleep(0.001)
    # a1_joint_config[[8,11]] = 3*np.sin(1.25*time.time()+np.pi/2) + 3 #- 1.2
    # joint_velocity_target[9] = 0.1*np.sin(time.time())
    # a1.setPdTarget(a1_joint_config, joint_velocity_target)
    # a1.setGeneralizedForce(a1_joint_config)
    server.integrateWorldThreadSafe()



server.killServer()

# if __name__ == '__main__':
    

