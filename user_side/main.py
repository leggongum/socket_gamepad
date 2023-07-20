try:
    from pynput import keyboard, mouse
except ModuleNotFoundError:
    from subprocess import call
    call('make_venv.bat')
    exit('Virtual enviroment was load')

from socket import socket, AF_INET, SOCK_DGRAM

from config import HOST, PORT, KEYS


to_server = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(3.0)

R_KEYS = {'й': 'q', 'ц': 'w', 'у':'e', 'к':'r', 'е':'t', 'н':'y', 'г':'u', 'ш':'i', 'щ':'o', 'з':'p', 'х':'[', 'ъ':']',
          'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';', 'э': "'", 
          'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', 'ё': '`'}

def transform_key(key):
    key_value = str(key).strip("'")
    key_value = key_value[4:].lower() if key_value[0] == 'K' else key_value.lower()
    key_value = R_KEYS.get(key_value, key_value)
    return key_value


def send_to_server(key, pressed):
    key_value = transform_key(key)

    if key_value not in KEYS:
        return

    data = f'{1 if key_value in "wasd" else 2 if key_value in "ijkl" else 0} {pressed} {KEYS[key_value]}'
    client_socket.sendto(data.encode(), to_server)
    data, addr = client_socket.recvfrom(1024)
    #print(data)


def on_click(x, y, key, pressed):
    send_to_server(key, 1 if pressed else 0)


def on_press(key):
    send_to_server(key, 1)


def on_release(key):
    send_to_server(key, 0)


if __name__ == '__main__':
    m_listener = mouse.Listener(on_click=on_click)
    m_listener.start()
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=True) as listener:
        listener.join()
    client_socket.close()
