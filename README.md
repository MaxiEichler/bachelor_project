# Bachelor Project - Wrexham University

## Overview
This repository contains the source code for my Bachelor Project at Wrexham University. 
The project connects breadboard contact points electrically together with analogue switch arrays a Raspberry Pi 4 Model B and the selction between modes.
Data mode: bidirectional 40 mA
Power mode: unidirectional 240 mA

## Repository Structure
The project is organized into modular components to separate hardware control from the user interface and core logic:

* **`gui/`**: Contains the frontend files (HTML, CSS, JavaScript) and user interface configurations.
* **`hardware/`**: Handles the direct communication and control of external hardware components.
* **`logic/`**: Contains the core algorithmic logic and data processing scripts.
* **`main.py`**: The main entry point to initialize and run the application.
* **`requirements.txt`**: Lists all the necessary Python dependencies required to run the project.
