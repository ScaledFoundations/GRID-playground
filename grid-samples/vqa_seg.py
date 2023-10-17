import os
import rerun as rr
import airgen
from airgen.utils.sensor import ImageType, imagetype2request, responses2images

# Enable logging visual data inside GRID's models
os.environ["TURN_ON_RERUN"] = "1"

from grid import GRIDConfig
# Replace this with the main directory of GRID that contains `external`
GRIDConfig.set_main_dir("/workspaces/GRID")

from grid.model.perception.vqa.gllava import GLLaVA
from grid.model.perception.segmentation.gsam import GroundedSAM

llava = GLLaVA()
gsam = GroundedSAM()

# Initialize the AirGen client
c = airgen.MultirotorClient()
c.confirmConnection()
c.enableApiControl(True)
c.armDisarm(True)
c.takeoffAsync().join() 

responses = c.simGetImages([imagetype2request("front_center", ImageType.Scene)])
image = responses2images(responses)[0][0]
obj = llava.run(image, "Describe the scene, and pick a single object of interest")
print(obj)

# Example output: The scene is a large, open field with a road running through it. 
#                   In the distance, there are several wind turbines, which are the main focus 
#                   of the image. These wind turbines are situated in the middle of the field, 
#                   and they are spinning, indicating that they are generating electricity from 
#                   the wind. The presence of these turbines suggests that the area is likely 
#                   a wind farm, which harnesses the power of the wind to produce clean and 
#                   renewable energy

seg = gsam.segment_object(image, "wind turbines")
