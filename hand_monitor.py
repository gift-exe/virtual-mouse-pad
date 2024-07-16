import cv2
import mediapipe as mp
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import queue
from mouse import *
import mouse

import warnings
warnings.filterwarnings('ignore')

INDEX_FINGER = 8
MIDDLE_FINGER = 12

FPS_LIMIT = 10
last_frame_time = 0
frame_time = 1.0 / FPS_LIMIT

frame_queue = queue.Queue()

def calculate_fps(image):
    global last_frame_time

    this_frame_time = time.time()
    fps = 1 / (this_frame_time - last_frame_time)
    last_frame_time = this_frame_time
    
    #write fps on screen
    cv2.putText(image, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def process_frame(frame_id, image, hands):

    calculate_fps(image)
    
    #hand recognition
    recognize_hands = hands.process(image)
    if recognize_hands.multi_hand_landmarks: 
        hand = recognize_hands.multi_hand_landmarks[0] # contains data on recognize hands
        index_cords = hand.landmark[INDEX_FINGER] # extract the position of the index finger

        if mouse.IS_DETECTED == 0: mouse.IS_DETECTED = 1
        
        move_mouse_rel(index_cords.x, index_cords.y)
        
        h, w, c = image.shape
        x, y = int(index_cords.x * w), int(index_cords.y * h)
        cv2.circle(image, (x, y), 3, (255, 0, 255), cv2.FILLED)

    else:
        mouse.IS_DETECTED = 0
    
    return frame_id, image

def display_frame():
    last_displayed_id = 0
    frames_buffer = {}

    while True:
        frame_id, image = frame_queue.get()
        frames_buffer[frame_id] = image

        while last_displayed_id + 1 in frames_buffer:
            last_displayed_id += 1
            frame = frames_buffer.pop(last_displayed_id)
            cv2.imshow('CamOutput', frame)
            cv2.waitKey(1)
        
            
def main():

    video_cap = cv2.VideoCapture(0) # use laptop's camera
    video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    hand_solution = mp.solutions.hands
    hands = hand_solution.Hands(
            static_image_mode=False,  # Set to False to detect hands in video
            max_num_hands=1,  # Detect only one hand to reduce processing
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
    
    frame_id = 0

    display_thread = threading.Thread(target=display_frame, daemon=True)
    display_thread.start()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}

        while True:
            start_time = time.time()
            success, image = video_cap.read()

            if success:
                # main stuff
                image = cv2.flip(image, 1)

                frame_id += 1
                future = executor.submit(process_frame, frame_id, image, hands)

                futures[future] = frame_id

                for future in as_completed(futures):
                    frame_id = futures.pop(future)
                    result_frame_id, processed_image = future.result()
                    frame_queue.put((result_frame_id, processed_image))


                # frame limiting when hands are being detected, so that we would not process too many frames 
                # (since somee frrames might have fluctuations in finger position)
                end_time = time.time()
                elapsed_time = end_time - start_time
                time_to_wait = max(0, frame_time - elapsed_time)
                time.sleep(time_to_wait)
    
    return
if __name__ == '__main__':
    main()