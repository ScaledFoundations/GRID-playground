import airgen
import threading


def run_drone(id: int):
    client = airgen.connect_airgen(robot_type="multirotor")
    client.confirmConnection()

    vehicle_name = f"Drone_{id}"
    pose = airgen.Pose(airgen.Vector3r(0, 5 * id, 0), airgen.Quaternionr(0, 0, 0, 0))

    print(f"Creating {vehicle_name}")
    success = client.simAddVehicle(vehicle_name, "SimpleFlight", pose)
    client.enableApiControl(True, vehicle_name)

    if not success:
        print(f"Failed to create {vehicle_name}")
        return

    client.moveToZAsync(-25, 5, vehicle_name=vehicle_name)


if __name__ == "__main__":
    num_vehicles = 5

    print(f"Creating {num_vehicles} vehicles")

    threads = []
    for id in range(num_vehicles, 0, -1):
        t = threading.Thread(target=run_drone, args=(id,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
