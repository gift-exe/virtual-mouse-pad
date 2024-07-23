import pyautogui as pag
import time


X, Y = pag.size()

SMOOTHING = 2.5
prev_x, prev_y = 0, 0
smooth_x, smooth_y = 0, 0

c_x_store, c_y_store = None, None

IS_DETECTED = 0
ACCELERATION_FACTOR = 0.3

last_time = time.time()

def old_move_mouse_abs(x, y,):
    
    global smooth_x, smooth_y, prev_x, prev_y, x_, y_
    x_, y_ = x, y
    x, y = round(x, 2), round(y, 2)
    x_cord, y_cord = round(x*X), round(y*Y)
    
    # Smoothing mouse coords value (moving average)
    smooth_x = (prev_x * (SMOOTHING - 1) + x_cord) / SMOOTHING
    smooth_y = (prev_y * (SMOOTHING - 1) + y_cord) / SMOOTHING
    prev_x, prev_y = smooth_x, smooth_y

    print(f'{x} -> {smooth_x}, {y} -> {smooth_y}')

    pag.moveTo(x_cord, y_cord)

def old_move_mouse_rel(x, y):
    
    global smooth_x, smooth_y, prev_x, prev_y

    current_x, current_y = pag.position()
    x, y = round(x, 2), round(y, 2)
    delta_x, delta_y = (x - (current_x / X)) * X, (y - (current_y / Y)) * Y
    
    # Smoothing mouse coords value (moving average)
    smooth_x = (prev_x * (SMOOTHING - 1) + delta_x) / SMOOTHING
    smooth_y = (prev_y * (SMOOTHING - 1) + delta_y) / SMOOTHING

    prev_x, prev_y = smooth_x, smooth_y

    print(f'{x} -> {smooth_x} :: {y} -> {smooth_y}')

    pag.moveRel(smooth_x, smooth_y)

def move_mouse_rel(x, y):
    global smooth_x, smooth_y, prev_x, prev_y, IS_DETECTED, c_x_store, c_y_store

    current_x, current_y = c_x_store, c_y_store
    
    if IS_DETECTED == 1: current_x, current_y = pag.position()

    if current_x > X: current_x = X - 20
    if current_x < 0: current_x = 0 + 20
    if current_y > Y: current_y = Y - 20
    if current_y < 0: current_y = 0 + 20

    x, y = round(x, 2), round(y, 2)
    x_cord, y_cord = round(x*X), round(y*Y)
    
    # Smoothing mouse coords value
    smooth_x, smooth_y = moving_average(prev_x=prev_x, prev_y=prev_y, x_cord=x_cord, y_cord=y_cord)
    prev_x, prev_y = smooth_x, smooth_y

    delta_x, delta_y = round(smooth_x - current_x), round(smooth_y - current_y)

    _x, _y = pag.position()
    print(f'{x} -> {delta_x} :: {y} -> {delta_y} :: TRUE POSITION -> {_x, _y} :: PERCEIVED POSTION -> {c_x_store, c_y_store}')

    if IS_DETECTED == 1: IS_DETECTED = 2
    elif IS_DETECTED == 2: pag.moveRel(delta_x, delta_y)
    
    current_x += delta_x
    current_y += delta_y
    c_x_store, c_y_store = current_x, current_y
    
def move_mouse_accelerated(x, y):
    global smooth_x, smooth_y, prev_x, prev_y, IS_DETECTED, c_x_store, c_y_store, last_time

    current_x, current_y = c_x_store, c_y_store
    
    if IS_DETECTED == 1: current_x, current_y = pag.position()

    if current_x > X: current_x = X - 20
    if current_x < 0: current_x = 0 + 20
    if current_y > Y: current_y = Y - 20
    if current_y < 0: current_y = 0 + 20

    x, y = round(x, 2), round(y, 2)
    x_cord, y_cord = round(x*X), round(y*Y)
    
    # Smoothing mouse coords value
    smooth_x, smooth_y = moving_average(prev_x=prev_x, prev_y=prev_y, x_cord=x_cord, y_cord=y_cord) # x_cord, y_cord # 
    prev_x, prev_y = smooth_x, smooth_y

    delta_x, delta_y = round(smooth_x - current_x), round(smooth_y - current_y)

    # I want to add a kind of accelaration factor/effect/feature
    # I neeed to get the speed at which my fingers are moving sha
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    speed = (delta_x**2 + delta_y**2)**0.5/delta_time**0.2 if delta_time > 0 else 0

    # Adaptive scaling (Heuristic). just basically adding extra distance to the original distance. 
    # The extra distance is based on the speed and the accelaratio factor
    accelerated_delta_x = round(delta_x + (1 + ACCELERATION_FACTOR * speed)) if delta_x > 0 else round(delta_x - (1 + ACCELERATION_FACTOR * speed))
    accelerated_delta_y = round(delta_y + (1 + ACCELERATION_FACTOR * speed)) if delta_y > 0 else round(delta_y - (1 + ACCELERATION_FACTOR * speed))
    
    #print(f'dx -> {delta_x} :: acc_x -> {accelerated_delta_x} :: dy -> {delta_y} :: acc_y -> {accelerated_delta_y} :: speed -> {round(speed)}')

    if IS_DETECTED == 1: IS_DETECTED = 2
    elif IS_DETECTED == 2: pag.moveRel(accelerated_delta_x, accelerated_delta_y)
    
    current_x += delta_x
    current_y += delta_y
    c_x_store, c_y_store = current_x, current_y

def moving_average(prev_x, prev_y, x_cord, y_cord):
    smooth_x = (prev_x * (SMOOTHING - 1) + x_cord) / SMOOTHING
    smooth_y = (prev_y * (SMOOTHING - 1) + y_cord) / SMOOTHING
    return smooth_x, smooth_y

def exponential_moving_average(prev_x, prev_y, x_cord, y_cord, alpha=0.1):
    smooth_x = (alpha * x_cord) + ((1 - alpha) * prev_x)
    smooth_y = (alpha * y_cord) + ((1 - alpha) * prev_y)

    return smooth_x, smooth_y

def low_pass_filter():
    ...