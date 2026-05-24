from pynput import keyboard
from pynput import mouse
from threading import Timer
import time
import subprocess

##### settings
# config_file = "testfile.cfg"
# config_file = "C:/Logiciels/RivaTuner Statistics Server/Profiles/ffxiv_dx11.exe.cfg"
app = "ffxiv_dx11.exe"
rtss_cli = "C:/Logiciels/RivaTuner Statistics Server/Profiles/rtss-cli.exe"

default_fps = 60 # max fps
reduced_fps = 45 # fps when not active & bellow reduced_threshold recent actions
low_fps = 30 # fps after idle_1_timer
min_fps = 10 # fps after idle_2_timer

active_timer = 30 # time in seconds before fps can be reduced again after an active_key was pressed
reduced_threshold = 30 # number of actions. important_keys add more actions. chat_key removes actions. -1 action per second.
idle_1_timer = 30 # seconds
idle_2_timer = 300 # seconds

active_keys = ["Key.ctrl_l", "&", "é", "\"", "\'", "(", "-", "è", "_", "ç", "à", ")", "=", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
important_keys = ["z", "q", "s", "d"]
chat_key = ["Key.enter"]
# Button.left
#####

actions = 0
next_tick = 1
last_action = time.time()
current_fps = default_fps

def apply_idle():
    global actions, next_tick

    actions = max(0, min(actions, reduced_threshold+15))
    fps = default_fps

    if actions < reduced_threshold:
        fps = reduced_fps
    if time.time() - last_action > idle_2_timer:
        fps = min_fps
    elif time.time() - last_action > idle_1_timer:
        fps = low_fps

    print(f"actions: {actions}, current fps: {fps}")
    actions -= 1
    next_tick = 1
    change_fps_limit(fps)
    run()


def force_active(duration=active_timer):
    global next_tick
    timer.cancel()
    change_fps_limit(default_fps)
    next_tick = duration
    run()


def on_input(key):
    global actions, last_action

    last_action = time.time()

    if key in active_keys:
        force_active()
    elif key in chat_key:
        actions -= 30
    elif key in important_keys:
        actions += 5
    else:
        actions += 1


def change_fps_limit(fps):
    global current_fps, next_tick

    if fps == current_fps:
        return
    elif fps > current_fps:
        next_tick = 10 # prevent changing fps (decreasing) too often
        
    subprocess.run(
        f'"{rtss_cli}" property:set {app} FramerateLimit {fps}',
        shell=True
    )
    print(f"setting fps to: {fps}")
    current_fps = fps
    # with open(config_file, "r+") as file:
    #     content = file.read()
    #     fps_pos = content.find("[Framerate]\nLimit=") + 19
    #     file.seek(fps_pos)
    #     file.write(str(fps))


def run():
    global timer
    timer = Timer(next_tick, apply_idle)
    timer.start()

timer = Timer(next_tick, apply_idle)
run()


def on_release(key):
    try:
        on_input(key.char)
    except AttributeError:
        on_input(str(key))

def on_click(x, y, button, pressed):
    if pressed:
        on_input(str(button))

kb_listener = keyboard.Listener(on_release=on_release)
m_listener = mouse.Listener(on_click=on_click)

kb_listener.start()
m_listener.start()

kb_listener.join()
m_listener.join()