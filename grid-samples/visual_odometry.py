# Visual Odometry using the AirGen simulator. 
# This script expects the AirGen simulator to be set to "ComputerVision" mode.
# Uses DPVO to compute up-to-scale poses from RGB data.

import numpy as np
import rerun as rr
import airgen
from airgen.utils.sensor import imagetype2request, responses2images
from grid import GRIDConfig
from grid.model.perception.vo.vo_dpvo import VO

# Point this to the directory that contains `external`
GRIDConfig.set_main_dir("/GRID")

rr.init('vo')
rr.serve()

# Assuming a 640x480 camera with 90 degree FoV. This should match the
# setting in the AirGen settings.json
calib = np.array([320, 320, 320, 240])
dpvo = VO(calib)

c = airgen.connect_airgen(robot_type="vehicle")
c.confirmConnection()

t = 0

imagetypes = [airgen.ImageType.Scene]
image_requests = [
    imagetype2request("front_center", image_type) for image_type in imagetypes
]

while True:
    try:
        responses = c.simGetImages(requests = image_requests)
        image = responses2images(responses)[0][0]
        current_pose = dpvo.run(image)
        rr.log_point(f'vo/position/pos_{t}', [current_pose[0], current_pose[1], -current_pose[2]])

        t += 1
    except KeyboardInterrupt:
        pred_traj = dpvo.terminate()
        break
