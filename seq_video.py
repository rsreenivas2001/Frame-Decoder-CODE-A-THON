import cv2
import random
import numpy as np

# Define the known sequence color patterns
known_patterns = [
    [(0, 0, 0), (192, 192, 192), (0, 255, 0), (128, 0, 128)],
    [(255, 255, 255), (0, 128, 128), (128, 128, 128), (0, 0, 255)],
    [(255, 0, 0), (0, 0, 128), (128, 0, 0), (255, 255, 0)],
    [(0, 255, 0), (255, 128, 0), (128, 128, 0), (0, 255, 255)],
    [(0, 0, 255), (0, 0, 0), (0, 128, 0), (255, 0, 255)],
    [(255, 255, 0), (255, 255, 0), (128, 0, 128), (192, 192, 192)],
    [(0, 255, 255), (0, 255, 255), (0, 128, 128), (128, 128, 128)],
    [(255, 0, 255), (255, 0, 255), (0, 0, 128), (128, 0, 0)],
    [(192, 192, 192), (192, 192, 192), (255, 128, 0), (128, 128, 0)],
    [(128, 128, 128), (255, 255, 255), (255, 255, 255), (0, 128, 0)],
    [(128, 0, 0), (255, 0, 0), (255, 0, 0), (128, 0, 128)],
    [(128, 128, 0), (0, 255, 0), (0, 255, 0), (0, 128, 128)],
    [(0, 128, 0), (0, 0, 255), (0, 0, 255), (0, 0, 128)],
    [(128, 0, 128), (128, 128, 128), (0, 0, 0), (255, 128, 0)],
    [(0, 128, 128), (128, 0, 0), (255, 255, 0), (0, 0, 0)],
    [(0, 0, 128), (128, 128, 0), (0, 255, 255), (255, 255, 255)],
    [(255, 128, 0), (0, 128, 0), (255, 0, 255), (255, 0, 0)]
]

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
# Open the webcam
cap = cv2.VideoCapture("D:\Code-a-thon\SeqOutput_TestVideo_3.avi")  # 0 represents the default webcam

# Variables to track the patterns
pattern_start_frames = [None] * len(known_patterns)
pattern_end_frames = [None] * len(known_patterns)
pattern_detected = [False] * len(known_patterns)
pattern_positions = [0] * len(known_patterns)

frame_delay = 250  # milliseconds
success, frame = cap.read()
frame_counter = 0
case = 250
target_fps = 1000/case
frame_skip_interval = int(cap.get(cv2.CAP_PROP_FPS) / target_fps)

res = []
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
        color = tuple(frame[y, x])

        distance, result = kdTree.query(color)
        dominant_color = main_colors[result]

        # Check for each known pattern
        for pattern_index, pattern in enumerate(known_patterns):
            # Check if the dominant color matches the color at the current position in the known pattern
            if dominant_color == pattern[pattern_positions[pattern_index]]:
                if not pattern_detected[pattern_index]:
                    pattern_start_frames[pattern_index] = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    pattern_detected[pattern_index] = True

                pattern_positions[pattern_index] += 1

                if pattern_positions[pattern_index] == len(pattern):
                    pattern_end_frames[pattern_index] = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    pattern_detected[pattern_index] = False
                    pattern_positions[pattern_index] = 0
                    res.append((pattern_index,pattern_start_frames[pattern_index],pattern_end_frames[pattern_index]+9))
                    break
            else:
                pattern_detected[pattern_index] = False
                pattern_positions[pattern_index] = 0  # Reset the position in the known pattern

        # Display the frame
        #cv2.imshow('Frame', frame)

        # Check for the 'q' key to exit
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    success, frame = cap.read()
    frame_counter += 1


# Print the start and end frame numbers of each pattern
for pattern_index, pattern in enumerate(known_patterns):
    print("Pattern", pattern_index + 1)
    print("Start frame:", pattern_start_frames[pattern_index])
    print("End frame:", pattern_end_frames[pattern_index])
    print()

print(res)
# Release the webcam and cleanup
cap.release()
cv2.destroyAllWindows()
