# read sensor data in AirGen

from typing import List, Tuple, Dict, Any, Optional, Callable
import numpy as np
import rerun as rr

import airgen

from airgen.utils.collect import data_collector

# setup client
client = airgen.connect_airgen(robot_type="multirotor")
client.enableApiControl(True)
client.takeoffAsync().join()

rr.init("airgen/sensor")
rr.serve()


def readSensors(client: airgen.VehicleClient) -> dict:
    sensor_data = {}
    sensor_data["barometer"] = client.getBarometerData()
    sensor_data["imu"] = client.getImuData()
    sensor_data["gps"] = client.getGpsData()

    sensor_data["magnetometer"] = client.getMagnetometerData()
    sensor_data["distance1"] = client.getDistanceSensorData(
        distance_sensor_name="Distance1"
    )
    sensor_data["distance2"] = client.getDistanceSensorData(
        distance_sensor_name="Distance2"
    )
    sensor_data["lidar"] = client.getLidarData()
    return sensor_data


@data_collector(readSensors, time_delta=4.0)
def move_task(
    client: airgen.MultirotorClient, position: Tuple[float], **kwargs
) -> None | Tuple[None, List[dict]]:
    client.moveToPositionAsync(*position, 1).join()


_, sensor_data = move_task(client, (0, 0, -10), _collect_data=True)
for i, data in enumerate(sensor_data):
    lidar = data["lidar"]
    rr.log_points(
        f"airgen/sensor/lidar_{i}",
        np.array(lidar.point_cloud).reshape(-1, 3),
        class_ids=lidar.segmentation,
    )
print(f"collected {len(sensor_data)} measurements during moving task")

rr.disconnect()
rr.rerun_shutdown()
