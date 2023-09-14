# Gesture Control Demonstration

Demonstrates gesture control algorithms via laptop webcam. Run `GestureControlDemo.py` to adjust your laptop's screen brightness with your hand gestures. Pinch your index finger and your thumb close together to reduce your screen brightness, and vice versa. 

All the code in this repository is taken from the Princeton University Robotics Club Drone Team repository: https://github.com/princeton-robotics-club/Drone-Team.

Run the following instructions to clone this repository and run a gesture control algorithm via your laptop webcam:
1. Install VSCode and git according to the instructions in this document: https://docs.google.com/document/d/1LeeeOWqW6S5IID_blqhmAa0N-b9Ontir8AWGzNsqFd4/edit?usp=sharing 
2. Open a new terminal in VSCode with Ctrl+Shift+`
3. Open a bash terminal by selecting `Git Bash` from the drop-down list next to the `+` sign in your terminal. 
4. In your bash terminal, navigate to your desired folder and run `git clone https://github.com/yijint/gesture-control-demo.git` to clone this repository in that folder. 
5. In your bash terminal, run `pip install -r requirements.txt` to install all the Python packages needed to run the code in this repository. There might be some additional packages that you don't need. If you only want to install the packages you absolutely need, you can skip to step 6 to run `GestureControlDemo.py`. You will be prompted with the Python packages you need to install, which you can install by running `pip install <package-name>` one by one. This is a more time-consuming option but gives you more control over which packages you are installing. 
6. In your bash terminal, run `python GestureControlDemo.py`. This should open your laptop's camera and allow you to play around with the gesture control algorithm as described above. If you get a `ModuleNotFoundError: No module named 'cv2`, run `pip install opencv-python` and then re-run `python GestureControlDemo.py`
8. To terminate the program, run `Ctrl+C` in your terminal.  
