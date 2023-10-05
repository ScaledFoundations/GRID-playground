GRID consists of a model bank composed of several foundation models as well as an LLM (currently GPT-4) for orchestration and code generation. We make use of the following open-source models as part of GRID. All credits go to the original authors.

GroundingDINO: https://github.com/IDEA-Research/GroundingDINO
YOLO v8: https://github.com/ultralytics/ultralytics
CLIPSeg: https://github.com/timojl/clipseg
GroundedSAM: https://github.com/IDEA-Research/Grounded-Segment-Anything
GIT: https://huggingface.co/microsoft/git-base-textvqa
LLaVa: https://github.com/haotian-liu/LLaVA
TTC: https://github.com/gengshan-y/expansion
DPVO: https://github.com/princeton-vl/DPVO
BLIP2: https://huggingface.co/Salesforce/blip2-opt-2.7b
TapNet: https://github.com/google-deepmind/tapnet

Running `/GRID/chat2grid.py` will open up a conversation with the LLM in GRID, where users can start by controlling the drone in AirGen through language commands, or pose more interesting perception-action problems that the LLM can start writing code for. Here is an example: 

![A picture of the AirGen simulator and the GRID interface together](../assets/grid_interface.png)

## Using the Foundation Models

Coming soon!

## Bring your own model

See http://docs.scaledfoundations.ai/models/byom.html

## Configuring the LLM

Coming soon! 
