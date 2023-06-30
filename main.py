import random

import cv2
import numpy as np
import time

from scipy.spatial import KDTree

main_colors = [(0,0,0),
                (255,255,255),
                (255,0,0),
                (0,255,0),
                (0,0,255),
                (255,255,0),
                (0,255,255),
                (255,0,255),
                (192,192,192),
                (128,128,128),
                (128,0,0),
                (128,128,0),
                (0,128,0),
                (128,0,128),
                (0,128,128),
                (0,0,128),
                (255,128,0)
                ]
kdTree = KDTree(main_colors)
# Define the known sequence color patterns
known_patterns = [
    [(255, 0, 0), (0, 255, 0), (0, 0, 255)],                  # Example pattern 1 (red, green, blue)
    [(0, 0, 255), (0, 255, 0), (255, 0, 0)],                  # Example pattern 2 (blue, green, red)
    [(0, 255, 0), (255, 0, 0), (0, 0, 255)],                  # Example pattern 3 (green, red, blue)
    [(255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 0, 0)] # Example pattern 4 (yellow, cyan, magenta, red)
]

# Open the webcam
cap = cv2.VideoCapture("D:\Code-a-thon\SeqOutput_TestVideo_3.avi")  # 0 represents the default webcam

# Variables to track the patterns
pattern_start_frames = [None] * len(known_patterns)
pattern_end_frames = [None] * len(known_patterns)
pattern_detected = [False] * len(known_patterns)
pattern_positions = [0] * len(known_patterns)

# Time delay for each frame (4 frames per second)
frame_delay = 250  # milliseconds
success, frame = cap.read()
frame_counter = 0
case = 250
target_fps = 1000/case
frame_skip_interval = int(cap.get(cv2.CAP_PROP_FPS) / target_fps)
# Process frames from the webcam
while success:
    if frame_counter % frame_skip_interval == 0:


        # Convert frame to the suitable color representation (e.g., RGB to HSV)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Extract the dominant color of the frame (e.g., by finding the mode color)
        dominant_color = cv2.mean(frame)[:3]
        height, width, _ = frame.shape

        # Generate random pixel coordinates
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        color = tuple(frame[y,x])
        #print(dominant_color)
        distance, result = kdTree.query(color)
        nearest_color = main_colors[result]
        print(nearest_color)
        # try:
        #     named_color = convert_rgb_to_names(color)
        #     print(named_color,color)
        # except:
        #     print(color)
        # Display the frame
        cv2.imshow('Frame', frame)

        # Check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    success, frame = cap.read()
    frame_counter += 1

# Print the start and end frame numbers of each pattern

# Release the webcam and cleanup
cap.release()
cv2.destroyAllWindows()

