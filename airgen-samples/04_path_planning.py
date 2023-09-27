import airgen
import numpy as np 

class DroneController:
    def __init__(self):
        # Initialize a drone client 
        self.drone_client = airgen.MultirotorClient()
        
        # Reset previous state if any
        self.drone_client.reset()
        
        # Confirm the connection, and enable offboard (API) control
        self.drone_client.confirmConnection()
        self.drone_client.enableApiControl(True)

        # Take off
        self.drone_client.takeoffAsync().join()


        # Get navigation map information from the simulation world
        self.nav_mesh_info = self.drone_client.getNavMeshInfo()
        print("Nav mesh info: {}".format(self.nav_mesh_info))

    def sample_random_pose(self):
        # calculate bounds of the nav mesh
        amplitude = np.absolute(np.array([self.nav_mesh_info[2]['x_val'] - self.nav_mesh_info[1]['x_val'], self.nav_mesh_info[2]['y_val'] - self.nav_mesh_info[1]['y_val'], self.nav_mesh_info[2]['z_val'] - self.nav_mesh_info[1]['z_val']]))/2.0
        # sample a random point on the nav mesh
        random_point = airgen.Vector3r(np.random.uniform(self.nav_mesh_info[0]['x_val']-amplitude[0], self.nav_mesh_info[0]['x_val']+amplitude[0]), np.random.uniform(self.nav_mesh_info[0]['y_val']-amplitude[1], self.nav_mesh_info[0]['y_val']+amplitude[1]), np.random.uniform(self.nav_mesh_info[0]['z_val']-amplitude[2], self.nav_mesh_info[0]['z_val']+amplitude[2]))
        # sample a random yaw angle
        random_yaw = np.random.uniform(-np.pi, np.pi)
        return airgen.Pose(random_point, airgen.Quaternionr(airgen.Vector3r(0, 0, random_yaw)))

    def plan_and_move(self):
        # Get current pose of the drone in 6-DOF
        start_pose = self.drone_client.simGetVehiclePose()

        # Sample a random valid pose in the environment
        goal_pose = self.sample_random_pose()
        goal_pose.position.z_val = start_pose.position.z_val

        # Compute a collision-free path between start and goal
        trajectory = self.drone_client.simPlanPath(start_pose.position, goal_pose.position, True, True)

        points = []
        for waypoint in trajectory:
            points.append(
                airgen.Vector3r(waypoint["x_val"], waypoint["y_val"], waypoint["z_val"])
            )

        # Move the drone along the planned path at a velocity of 5 m/s
        velocity = 5.0
        self.drone_client.moveOnPathAsync(
            points,
            velocity,
            120,
            airgen.DrivetrainType.ForwardOnly,
            airgen.YawMode(False, 0),
            -1,
            0,
        ).join()

controller = DroneController()

while True:
    try:
        pose = controller.sample_random_pose()
        print(f"Moving to new position: [{pose.position.x_val}, {pose.position.y_val}, {pose.position.z_val}]")
        controller.plan_and_move()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, exiting...")
        client = airgen.MultirotorClient()
        client.reset()
        break
