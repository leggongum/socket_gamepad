# socket_gamepad
This application enables remotely connect device as a gamepad to computer. 
Used python libs: vgamepad, pynput, socket.

You must install python before use.

To install virtual enviroment you need (for server_side and user_side): 
1) Press Win+R
2) cmd
3) cd %path_to_directory%
4) python main.py


server_side: 
Download this directory on computer with Windows. Socket_gamepads will be connected to this computer.
Install virtual enviroment. Then command 'venv\Scripts\python main.py' will start server


user_side:
Download this directory on computer (OS may be different). This computer will connect to computer with started server.
Install virtual enviroment. Then command 'venv\Scripts\python main.py' (or 'venv/bin/python main.py' for Linux) will start connect to server.
In file 'settings.json' you can change server ip, server port, keys from keyboard -> gamepad action.
