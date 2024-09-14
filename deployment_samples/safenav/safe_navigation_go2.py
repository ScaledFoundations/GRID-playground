import numpy as np

import atexit
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2 as cv
from grid.model.perception.depth.midas import MIDAS
from grid.robot.locomotion.go2 import Go2

import math
import rerun as rr

def get_formatted_midas_image(rgb_image, midas):
    midas_image = midas.run(rgb_image.data)
    formatted = (midas_image * 255 / np.max(midas_image)).astype("uint8")
    return formatted

def preprocess_depth_image(depth_image):
    '''
    this function takes a depth image and normzalizes it
    i/p:  accepts a depth image from the depth sensor
    o/p: outputs a normalized depth image of the same size
    '''
    # Normalize or process your depth image
    return depth_image / depth_image.max()

def divide_into_grid(depth_image, num_horizontal_patches, num_vertical_patches):
    '''
    this function takes a depth image and creates n_horizontal * n_vertical patches out of it 
    i/p 
    depth_image: accepts a normalized depth image from the depth sensor
    num_horizontal_patches:  number of horizontal patches
    num_vertical_patches:  number of vertical patches  
    o/p: outputs a normalized depth image of the same size
    '''
    patches = []
    patch_height = depth_image.shape[0] // num_vertical_patches
    patch_width = depth_image.shape[1] // num_horizontal_patches
    for v in range(num_vertical_patches):
        for h in range(num_horizontal_patches):
            patch = depth_image[v * patch_height:(v + 1) * patch_height,
                                h * patch_width:(h + 1) * patch_width]
            patches.append(patch)
    return patches

def compute_safety_metric(patches):
    '''
    accepts a list of patches and computes a safety metric for each patch
    i/p:  list of patches
    o/p:  list of safety metrics
    '''

    return [np.mean(patch) for patch in patches]

def determine_best_patch(safety_metrics, num_horizontal_patches, num_vertical_patches):
    '''
    accepts a list of safety metrics and returns the index of the best patch
    i/p:  
    safety_metrics: list of safety metrics
    num_horizontal_patches:  number of horizontal patches
    num_vertical_patches:  number of vertical patches

    o/p:  index of the best patch
    '''
    # Reshape metrics array into grid form
    metrics_grid = np.array(safety_metrics).reshape((num_vertical_patches, num_horizontal_patches))
    # Find index of the best patch
    best_patch_index = np.unravel_index(np.argmin(metrics_grid), metrics_grid.shape)
    return best_patch_index

def map_patch_to_steering(patch_index, num_horizontal_patches, num_vertical_patches):
    '''
    accepts a patch index and maps it to a steering command
    i/p: 
    patch_index: index of the best patch
    num_horizontal_patches:  number of horizontal patches
    num_vertical_patches:  number of vertical patches
    
    o/p:  yaw and pitch values
    '''
    # Simplified mapping
    yaw = (patch_index[1] - num_horizontal_patches // 2) * (180 / num_horizontal_patches)
    pitch = (patch_index[0] - num_vertical_patches // 2) * (180 / num_vertical_patches)
    print(yaw, pitch)
    return yaw, pitch

def main_navigation_loop(agent, grid_size=3, iterations=1000, yaw_clip=(-30, 30)):
    ''' 
    Main navigation loop for the agent
    '''

    robot_agent = agent
    midas = MIDAS()

    rr.init("safenav")
    rr.connect()  

    print('initialized')
    for i in range(iterations):
        # Get the depth image using MIDAS
        rgb_image = robot_agent.getImage(camera_name="front_center", image_type="rgb")
        if rgb_image is None:
            continue
        depth_image = get_formatted_midas_image(rgb_image, midas)

        rr.log("safenav/rgb_image", rr.Image(rgb_image.data))
        
        # Preprocess the depth image
        depth_image[depth_image > 60000] = 10
        processed_image = preprocess_depth_image(depth_image)
        rr.log("safenav/depth_image", rr.Image(processed_image))
        patches_img = divide_into_grid(processed_image, grid_size, 1)  # Example grid size

        # Compute safety metrics
        safety_metrics = compute_safety_metric(patches_img)
        best_patch_index = determine_best_patch(safety_metrics, grid_size, 1)
        print(best_patch_index)

        # Map patch to steering
        yaw, pitch = map_patch_to_steering(best_patch_index, grid_size, 1)
        # Clip the yaw and pitch values
        yaw = np.clip(yaw, yaw_clip[0], yaw_clip[1])

        yaw_rad = np.deg2rad(yaw) 

        # Move the agent to the destination position
        vel = Velocity(.4, 0, -yaw_rad)
        robot_agent.moveByVelocity(vel, .3)

if __name__ == "__main__":
    robot = Go2()
    main_navigation_loop(robot)
