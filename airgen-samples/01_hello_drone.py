# baisc drone operations

import airgen

client = airgen.connect_airgen(robot_type="multirotor")
client.enableApiControl(True)

# Take off

client.takeoffAsync().join()

# Move to an altitude of 25 meters

client.moveToZAsync(-25, 5).join()

# Fly in a square path using velocity control

client.moveByVelocityAsync(5, 0, 0, 5).join()
client.moveByVelocityAsync(0, 5, 0, 5).join()
client.moveByVelocityAsync(-5, 0, 0, 5).join()
client.moveByVelocityAsync(0, -5, 0, 5).join()

client.hoverAsync().join()

# Fly in a square path using waypoints

waypoints = [
    airgen.Vector3r(25, 0, -25),
    airgen.Vector3r(25, 25, -25),
    airgen.Vector3r(0, 25, -25),
    airgen.Vector3r(0, 0, -25),
]

client.moveOnPathAsync(
    waypoints,
    5,
    60,
    airgen.DrivetrainType.MaxDegreeOfFreedom,
    airgen.YawMode(False, 0),
    -1,
    1,
).join()

# Fly in a square path with yaw angle relative to the direction of travel

client.moveOnPathAsync(
    waypoints, 5, 60, airgen.DrivetrainType.ForwardOnly, airgen.YawMode(False, 0), -1, 1
).join()

# Land

client.moveToZAsync(-2, 5).join()
client.landAsync().join()
