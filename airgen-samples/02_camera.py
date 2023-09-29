# reading images from camera in AirGen

from typing import List, Any, Literal, Tuple, Dict, Callable
import os
import math
import numpy as np
import rerun as rr

import airgen
from airgen.utils.sensor import imagetype2request, responses2images

client = airgen.connect_airgen(robot_type="multirotor")
client.enableApiControl(True)
client.takeoffAsync().join()
client.moveToPositionAsync(0, 0, -10, 5).join()
rr.init("airgen/camera")
rr.serve()

## part I: read images from camera in AirGen
print("Part I: read images from camera in AirGen\n")
# read every type of airgen image except for segmentation, which is discussed next
imagetypes = [
    airgen.ImageType.Scene,
    airgen.ImageType.DepthPlanar,
    airgen.ImageType.DepthPerspective,
    airgen.ImageType.DepthVis,
    airgen.ImageType.DisparityNormalized,
    airgen.ImageType.SurfaceNormals,
    airgen.ImageType.Infrared,
    airgen.ImageType.OpticalFlow,
    airgen.ImageType.OpticalFlowVis,
]
images = []
image_requests = [
    imagetype2request("front_center", image_type) for image_type in imagetypes
]

image_responses = client.simGetImages(requests=image_requests)
images = responses2images(image_responses)

for i, (image, _) in enumerate(images):
    print(
        f"{imagetypes[i]}'s image as numpy array: type={type(image)}, dtype={image.dtype}, shape={image.shape}"
    )


# visualize the images in rerun
# visualize the images
rr.log_image("airgen/camera/rgb", images[0][0])
rr.log_depth_image("airgen/camera/depth_perspective", images[1][0])
rr.log_depth_image("airgen/camera/depth_planar", images[2][0])
rr.log_image("airgen/camera/depth_vis", images[3][0])
rr.log_segmentation_image("airgen/camera/normalized_disparity", images[4][0])
rr.log_image(
    "airgen/camera/infrared", images[6][0]
)  # todo: infrared image is not working
rr.log_image("airgen/camera/optical_flow_vis", images[8][0])

## part II: read segmentation image from camera in AirGen
print("Part II: read segmentation image from camera in AirGen\n")
# Segmentation images capture the attribute: `SegmentationID` assigned to each object in the simulation scene.
# Initially, each object (mesh) is assigned random `SegmentationID` (`uint8`). When we request a
# `Segmentation` image from AirGen simulator, the camera captures the `SegmentationID` of all objects in the scene.
# One main usage of segmentation image is to extract specific objects
# or instances from the scene for processing or training of models.
# 1. the first step of using segmentation image is usually setting all objects' `SegmentationID` to 0,
# 2. then setting specific objects (through object name) to some non-zero values.
# 3. request the segmentation image from AirGen simulator.
#       The raw image data in response is represented as a numpy array with `dtype=uint8` and `shape=(height, width, 3)`,
#       where each RGB channel (or tuple of RGB values) corresponds to a fixed `SegmentationID` between `[0, 255]`.
# 4. finally we map the RGB values to `SegmentationID` to get the segmentation image.

# see all objects in the environment

objects = client.simListSceneObjects()
print("All objects in the environment:", objects)

# set all objects' `SegmentationID` to 0
client.simSetSegmentationObjectID("[\w]*", 0, is_name_regex=True)

# set the SegmentationID of all objects to 1
client.simSetSegmentationObjectID("[\w]*", 1, is_name_regex=True)


requests = [imagetype2request("front_center", airgen.ImageType.Segmentation)]
responses = client.simGetImages(requests=requests)
# in the helper function:  `responses2image`, the raw segmentation image (in RGB format) is converted to a numpy array of `SegmentationIDs`
segmentation_image = responses2images(responses)[0][0]
print(
    f"Segmentation image as numpy array: type={type(segmentation_image)}, dtype={segmentation_image.dtype}, shape={segmentation_image.shape}"
)
rr.log_segmentation_image("airgen/camera/segmentation", segmentation_image)

## part III: visualize trajectory along with camera captures in 3D space
print("Part III: visualize trajectory along with camera captures in 3D space\n")

from airgen.utils.mechanics import depth2pointcloud
from airgen.utils.collect import data_collector
from airgen.utils.visualize import rr_camera_capture_logger


def collect_camera_capture(client) -> dict:
    # use rr.log with `time_less=True` to log data inside data collection task
    requests = [
        imagetype2request("front_center", airgen.ImageType.DepthPerspective),
        imagetype2request("front_center", airgen.ImageType.Scene),
        imagetype2request("bottom_center", airgen.ImageType.DepthPerspective),
        imagetype2request("bottom_center", airgen.ImageType.Scene),
    ]
    responses = client.simGetImages(requests=requests)
    images = responses2images(responses)
    ## can also visualize inside rerun, let's leave that to the user
    return {
        "front_depth": images[0],
        "front_rgb": images[1],
        "bottom_depth": images[2],
        "bottom_rgb": images[3],
    }


@data_collector(collect_camera_capture, time_delta=0.2)
def move_task(client, **kwargs) -> None | Tuple[None, list]:
    client.moveToPositionAsync(0, 0, -10, 5).join()
    client.moveToPositionAsync(10, 10, -10, 5).join()


_, data = move_task(client, _collect_data=True)


capture_logger = rr_camera_capture_logger("airgen/world")
for i, capture in enumerate(data):
    for camera_name, camera_data in capture.items():
        if i == 0 and camera_name.endswith("depth"):
            # compute point cloud and visualize it in rerun
            # remove points that are too far away
            mask = np.where(camera_data[0] < 1000.0, 1, 0).astype(np.uint8)
            point_cloud = depth2pointcloud(
                depth=camera_data[0], camera_param=camera_data[1], mask=mask
            )
            rr.log_points(f"airgen/world/point_cloud/{camera_name}", point_cloud)
        # camera_data is a tuple of (image, camera_params)
        if camera_name.endswith("rgb"):
            capture_logger(
                camera_data[0], camera_data[1], camera_name=f"{camera_name}_{i}"
            )
# shutdown rerun server
rr.disconnect()
rr.rerun_shutdown()
