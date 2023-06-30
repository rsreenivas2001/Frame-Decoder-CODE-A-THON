# from webcolors import rgb_to_name
# named_color = rgb_to_name((0,128,0), spec='css3')
# print(named_color)
#
# import scipy.spatial as sp
#
# #Add more colors to this array if you need
# main_colors = [(0,0,0),
#                 (255,255,255),
#                 (255,0,0),
#                 (0,255,0),
#                 (0,0,255),
#                 (255,255,0),
#                 (0,255,255),
#                 (255,0,255),
#                 (192,192,192),
#                 (128,128,128),
#                 (128,0,0),
#                 (128,128,0),
#                 (0,128,0),
#                 (128,0,128),
#                 (0,128,128),
#                 (0,0,128),
#                 (255,128,0)
#                 ]
#
# #replace r,g,b variables with your pixel rgb values
#
# kdTree = sp.KDTree(main_colors)
# ditsance,result = kdTree.query((0,127,0))
# nearest_color = main_colors[result]
#
# print(nearest_color)


import cv2

# Open the video file
video = cv2.VideoCapture('D:\Code-a-thon\SeqOutput_TestVideo_3.avi')

# Get the frames per second (FPS) of the video
fps = video.get(cv2.CAP_PROP_FPS)
print(fps)