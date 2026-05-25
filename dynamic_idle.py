from pynput import keyboard
from pynput import mouse
import time
import subprocess

##### settings
debug = True
app = "ffxiv_dx11.exe" # or "Global"
rtss_cli = "C:/Logiciels/RivaTuner Statistics Server/Profiles/rtss-cli.exe"

default_fps = 60 # max fps
reduced_fps = 45 # fps when not active & bellow reduced_threshold recent actions
low_fps = 30 # fps after idle_1_timer
min_fps = 10 # fps after idle_2_timer

active_timer = 20 # time in seconds before fps can be reduced again after increasing
reduced_threshold = 30 # number of actions. important_keys add more actions. chat_keys removes actions. -1 action per second.
idle_1_timer = 30 # seconds
idle_2_timer = 300 # seconds
loop_interval = 1 # s
decay = 1 # how many actions to decay per loop

active_keys = ["Key.ctrl_l"] 
important_keys = ["z", "q", "s", "d", "&", "é", "\"", "\'", "(", "-", "è", "_", "ç", "à", ")", "=", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
chat_keys = ["Key.enter"]
# Button.left
#####

actions = 0
pause_until = 0
last_action = time.time()
current_fps = default_fps

def apply_idle():
    global actions

    actions = max(0, min(actions, reduced_threshold+15))
    fps = default_fps

    if actions < reduced_threshold:
        fps = reduced_fps
    if time.time() - last_action > idle_2_timer:
        fps = min_fps
    elif time.time() - last_action > idle_1_timer:
        fps = low_fps

    if debug:
        with open ('dynamic_idle_log.log', 'a') as logger:
            logger.write(f"actions: {actions}, current fps: {fps}\n")
        print(f"actions: {actions}, current fps: {fps}")

    actions -= decay
    change_fps_limit(fps)


def force_active(duration=active_timer):
    change_fps_limit(default_fps)
    pause_timer(duration)


def on_input(key):
    global actions, last_action

    last_action = time.time()

    if key in active_keys:
        force_active()
    elif key in chat_keys:
        actions -= 30
    elif key in important_keys:
        actions += 5
    else:
        actions += 1


def change_fps_limit(fps):
    global current_fps

    if fps == current_fps:
        return
    elif fps > current_fps:
        pause_timer(active_timer) # prevent changing fps (decreasing) too often
    
    current_fps = fps

    if debug:
        with open ('dynamic_idle_log.log', 'a') as logger:
            logger.write(f"setting fps to: {fps}")
        print(f"setting fps to: {fps}")

    subprocess.run(
        f'"{rtss_cli}" property:set {app} FramerateLimit {fps}',
        shell=True
    )


def on_release(key):
    try:
        on_input(key.char)
    except AttributeError:
        on_input(str(key))

def on_click(x, y, button, pressed):
    if pressed:
        on_input(str(button))

kb_listener = keyboard.Listener(on_release=on_release)
kb_listener.start()

m_listener = mouse.Listener(on_click=on_click)
m_listener.start()


def pause_timer(duration):
    global pause_until
    pause_until = time.time() + duration

def start():
    while True:
        now = time.time()

        if now < pause_until:
            sleep_time = pause_until - now
            time.sleep(min(sleep_time, 1))
            continue

        apply_idle()
        time.sleep(loop_interval)

start()

# kb_listener.join()
# m_listener.join()