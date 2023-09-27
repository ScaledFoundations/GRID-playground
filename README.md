# General Robot Intelligence Development (GRID) 

GRID is a platform for rapid infusion of safe intelligence into robotic platforms built by Scaled Foundations. 

The aim of the GRID platform is to enable robots to learn, compose and adapt skills to their physical capabilities, environmental constraints and goals. The GRID platform consists of a high fidelity simulator, foundation models for perception and action, and an orchestration layer powered by language models. This modular design enables various deep ML components and existing foundation models to be easily usable in a wider variety of robot-centric problems. To know more about our vision and technology, please read our [technical report](https://scaledfoundations.ai/wp-content/uploads/GRID_paper.pdf).

![image](https://github.com/ScaledFoundations/GRID-playground/assets/2274262/1b21ff88-f596-4fec-aabd-f0b0d35e153b)

The usage of GRID is governed by the Responsible AI License. GRID is free to use for non-commercial research purposes. If you find our work useful in your research, please cite us as:

```
@techreport{sf2023grid,
  title = {GRID: A Platform for General Robot Intelligence Development},
  author = {Scaled Foundations},
  note  =  {\url{http://scaledfoundations.ai/wp-content/uploads/GRID_paper.pdf}}
}
```

## NOTE

The GRID platform is currently in alpha, and is continuously evolving. We will be constantly adding new features and sample scripts, so please keep an eye out for updates!
 
## Quick Start

1. Visit our website at https://portal.scaledfoundations.ai and sign up for an account.
2. Once signed up, you will be able to access our precompiled binary releases for the AirGen simulator.
3. Download the binary of your choice, and copy the `airgen-samples/settings.json` to the Documents folder of the user. Then run the downloaded simulation through `.\run.bat` or `./run.sh` inside the folder.
4. If you wish to experiment with the simulation, we provide a few sample scripts in this repo under `airgen-samples`.
5. To get started with the full AI capabilities of GRID, we provide a Docker image. If you wish to run the simulator on Windows, we recommend using WSL2 for the models.
6. Pull and run the Docker image
```
docker pull scaledfoundations/grid:base
docker run -it --gpus all --network host grid:base
```
7. For the LLM interaction mode in GRID, run
```
cd /GRID
python chat2grid.py
```

A detailed description of the models and configurations along with more samples are coming soon!

## What can you do with GRID? 

GRID aims to be a platform for rapid prototyping of AI capabilities for robotics through foundation models and simulation. At the core of GRID is a <i>Foundation Mosaic</i>, a combination of several foundation models for perception, state estimation, safety, and control. An orchestration and reasoning layer powered by large language models allows for natural interaction and makes use of the underlying models to solve complex robotics tasks. GRID makes use of AirGen, a state of the art aerial robotics simulator for data generation and evaluation. 

## Simulation

Simulation plays a central role in GRID for data generation, evaluation, and feedback. GRID uses AirGen, a high-fidelity aerial robotics simulator built on top of [AirSim](https://github.com/microsoft/AirSim). AirGen is capable of simulating a wide variety of scenes (both synthetic and geospatial) and generating data composed of a rich collection of sensor modalities.

![image](https://docs.scaledfoundations.ai/_images/summary.png)

## Scenarios

We try to set up and solve several robotics related scenarios with real life impact. We posit that the rich collection of models within GRID, coupled with the effective copilot-like behavior of LLMs allows for very rapid prototyping of robot intelligence that is deployable. 

1. Wildfire search and rescue
   
![image](https://github.com/ScaledFoundations/GRID-playground/assets/2274262/f5aa3b7d-df6e-4b7d-9c00-f3df4d102b85)

2. Vision-based landing

![Screenshot 2023-09-27 054641](https://github.com/ScaledFoundations/GRID-playground/assets/2274262/a2b407c7-7e01-4282-8b43-57902d2ce57a)

3. Infrastructure inspection

![Screenshot 2023-09-27 054714](https://github.com/ScaledFoundations/GRID-playground/assets/2274262/66e34c7b-4ccd-4e64-832e-d25caa769141)
   
4. Safe navigation using time-to-collision

![Screenshot 2023-09-27 054544](https://github.com/ScaledFoundations/GRID-playground/assets/2274262/9acbb6ff-3ec5-4d5f-a629-0ec2290ffc34)


