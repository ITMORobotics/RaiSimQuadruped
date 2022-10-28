import os
import numpy as np
import raisimpy as raisim
import time


raisim.World.setLicenseFile(os.path.dirname(os.path.abspath(__file__)) + "/../raisimLib/rsc/activation.raisim")
aliengo_urdf_file = os.path.dirname(os.path.abspath(__file__)) + "/../raisimLib/rsc/aliengo/aliengo.urdf"
# aliengo_urdf_file = os.path.dirname(os.path.abspath(__file__)) + "/../raisimLib/rsc/a1/urdf/a1.urdf"
#  create raisim world
world = raisim.World()
world.setTimeStep(0.001)

# create objects
ground = world.addGround()
ground.setAppearance("steel")

# create robots
aliengo = world.addArticulatedSystem(aliengo_urdf_file)
aliengo.setName("aliengo")

# aliengo settings
# PD controller
aliengo_nominal_joint_config = np.array([0, 0, 0.54, 1.0, 0.0, 0.0, 0.0, 0.03, 0.4, -0.8,
                                        -0.03, 0.4, -0.8, 0.03, -0.4, 0.8, -0.03, -0.4, 0])
joint_pgain = 100.0*np.ones([aliengo.getDOF()])
joint_dgain = 1*np.ones([aliengo.getDOF()])
joint_velocity_target = np.zeros([aliengo.getDOF()])

aliengo.setGeneralizedCoordinate(aliengo_nominal_joint_config)
aliengo.setGeneralizedForce(np.zeros([aliengo.getDOF()]))
aliengo.setPdGains(joint_pgain, joint_dgain)
aliengo.setPdTarget(aliengo_nominal_joint_config, joint_velocity_target)

print(aliengo.getDOF())
# launch raisim server
server = raisim.RaisimServer(world)
server.focusOn(aliengo)
server.launchServer(8080)

for i in range(500000):
    time.sleep(0.001)
    aliengo_nominal_joint_config[-1] = 0.5*np.sin(time.time())
    aliengo.setPdTarget(aliengo_nominal_joint_config, joint_velocity_target)
    server.integrateWorldThreadSafe()

server.killServer()

# if __name__ == '__main__':
    

