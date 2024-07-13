import ctypes
import os
import pyautogui
import time
from Xlib import X, display

file_dir = os.getcwd()

lib = ctypes.cdll.LoadLibrary(f'{file_dir}/cpp_playing_around/libfxprototypes.so')

start = time.time()
result = lib.sum_up(3, 5)
print(result)
end = time.time()

print('C sum fx exec period: ', end-start)

def sum(a, b):
    return a+b

start = time.time()
result = sum(3, 5)
print(result)
end = time.time()

print('python sum fx exec period: ', end-start)

# Using PyAutoGUI for general mouse control
# pyautogui.moveTo(100, 100)
# time.sleep(1)
# pyautogui.moveTo(200, 200)
# time.sleep(1)

# Using ctypes for specific features (e.g., custom acceleration)

x11 = ctypes.cdll.LoadLibrary('libX11.so')
x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
x11.XOpenDisplay.restype = ctypes.c_void_p

d = display.Display()
root = d.screen().root

def move_mouse(x, y):
    root.warp_pointer(x, y)
    d.sync()

def get_pointer_position():
    pointer = root.query_pointer()
    return pointer.root_x, pointer.root_y

# move_mouse(100, 100)
# time.sleep(1)
# move_mouse(200, 200)
# time.sleep(1)


def c_smooth_mouse_move(start_x, start_y, end_x, end_y, steps=10):
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    for i in range(steps):
        move_mouse(int(start_x + dx * i), int(start_y + dy * i))
        time.sleep(0.025)  # Small delay for smoother movement

c_smooth_mouse_move(200, 200, 400, 400)

def py_smooth_mouse_move(start_x, start_y, end_x, end_y, steps=10):
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    for i in range(steps):
        pyautogui.moveTo(int(start_x + dx * i), int(start_y + dy * i))
        time.sleep(0.025)  # Small delay for smoother movement

start = time.time()
c_smooth_mouse_move(200, 200, 400, 400)
end = time.time()

print('c mouse move fx exec period: ', end-start)

start = time.time()
py_smooth_mouse_move(200, 200, 400, 400)
end = time.time()

print('python mouse move fx exec period: ', end-start)