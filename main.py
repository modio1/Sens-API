import ctypes
import threading
import time
import requests as req
X_SETTING = 0
Y_SETTING = 0
SMOOTH_SETTING = 0

# [* API CALLS *]

response = req.get("http://127.0.0.1:5000/api/get")
profile_json = response.json()

print("=====Choose a profile=====")
for profile in profile_json:
    print(profile['name'])
prof = input("Select a profile: ")

# [* REMINDER *]
# [* This needs to be changed once the API is deployed *]
prof_resp = req.get(f"http://127.0.0.1:5000/api/getbyname/{prof}")
X_SETTING = prof_resp.json()['x_sens']
Y_SETTING = prof_resp.json()['y_sens']
SMOOTH_SETTING = prof_resp.json()['smooth']

# [* PROGRAM LOGIC STARTS HERE *]

# Gets key states using ctypes
def is_mouse_button_3_pressed():
    return ctypes.windll.user32.GetKeyState(0x02) & 0x8000 != 0

def is_mouse_button_1_pressed():
    return ctypes.windll.user32.GetKeyState(0x01) & 0x8000 != 0

def is_capslock_pressed():
    return ctypes.windll.user32.GetKeyState(0x14) & 1 != 0

def move_mouse_relative(x, y, smoothness):
    ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)
    time.sleep(smoothness)

def monitor_capslock():
    while True:
        if is_capslock_pressed():

            while is_mouse_button_3_pressed():
                while is_mouse_button_1_pressed():
                    move_mouse_relative(X_SETTING, Y_SETTING, SMOOTH_SETTING)
        else:
            pass

        time.sleep(.01)


capslock_thread = threading.Thread(target=monitor_capslock)
capslock_thread.daemon = True
capslock_thread.start()

while True:
    # GUI logic goes here

    time.sleep(1)

