try:
    import vgamepad as vg
except ModuleNotFoundError:
    from subprocess import call
    call('make_venv.bat')
    exit('Virtual enviroment was load')

import socket


class Gamepad_user:
    buttons = {
        'DPAD_UP': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
        'DPAD_DOWN': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        'DPAD_LEFT': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        'DPAD_RIGHT': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        'START': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
        'BACK': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        'LEFT_THUMB': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
        'RIGHT_THUMB': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        'LEFT_SHOULDER': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
        'RIGHT_SHOULDER': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
        'GUIDE': vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
        'A': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
        'B': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
        'X': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
        'Y': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    }

    users_dict = {}

    def __init__(self, addr: tuple) -> None:
        self.gamepad = vg.VX360Gamepad()
        self.joystick = {'w': 0.0, 'a': 0.0, 's': 0.0, 'd': 0.0}
        Gamepad_user.users_dict[addr[0]] = self
        print('new user: {}'.format(addr))


    def gamepad_action(self, data: str) -> None:
        """
        Transformation data into gamepad action\n
        Check if joystick\n
        Check press or release
        """

        data = data.split()

        is_joystick = int(data[0])
        is_press = int(data[1])
        if is_joystick:     #if joystick
            if is_press: #if press
                self.joystick[data[2]] = 1.0
            else:       #if release
                self.joystick[data[2]] -= 1.0
            self.gamepad.left_joystick_float(x_value_float=self.joystick['d']-self.joystick['a'], y_value_float=self.joystick['w']-self.joystick['s'])
        elif is_press:   #if not joystick and press
            self.gamepad.press_button(button=Gamepad_user.buttons[data[2]])
        else:
            self.gamepad.release_button(button=Gamepad_user.buttons[data[2]])
        self.gamepad.update()
    

    def receiving_new_data(addr: tuple, data: str) -> bytes:

        if addr[0] not in Gamepad_user.users_dict:
            if len(Gamepad_user.users_dict) == 4:
                return 'max users at same time'.encode()
            new_user = Gamepad_user(addr)
            new_user.gamepad_action(data)
        else:
            Gamepad_user.users_dict[addr[0]].gamepad_action(data)
        return f'user {addr}: {data} done'.encode()


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 5005))
    print(socket.gethostbyname(socket.gethostname()))

    while True:
        data, addr = server_socket.recvfrom(1024)
        data = data.decode('cp1251')
        #print('Connection from:', addr)
        #print('Data:', data)
        
        response = Gamepad_user.receiving_new_data(addr, data)

        server_socket.sendto(response, addr)
    