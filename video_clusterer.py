from gui import *
import cv2
import numpy as np
import random

videos = []
points = []
labels = []
medoids = []

def process(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0-sigma)*v))
    upper_thresh = int(min(255, (1.0+sigma)*v))
    edge = cv2.Canny(gray, lower_thresh, upper_thresh)
    return edge

def edge_pixels(image):
    m, n = image.shape
    pixels = []
    for i in range(0, m, 10):
        for j in range(0, n, 10):
            if image[i, j]>0:
                pixels.append([i,j])
    return pixels

def start_recording():
    message("")
    global camera
    camera = cv2.VideoCapture(0)
    global stop, video
    stop = False
    video = []
    def internal():
        if not stop:
            return_value, image = camera.read()
            if show_edges():
                edge = process(image)
                get_window().show_image(cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR))
            else:
                get_window().show_image(image)
            video.append(image)
            get_window().after(10, internal)
    internal()

def stop_recording():
    global stop
    stop = True
    camera.release()
    return video, [edge_pixels(process(frame)) for frame in video]

def clear_command():
    global videos, points, labels, medoids
    videos = []
    points = []
    labels = []
    medoids = []
    message("")

def record_command():
    message("")
    video, edge_pixel_frames = stop_recording()
    videos.append(video)
    points.append(edge_pixel_frames)
    labels.append(-1)

def random_labels_command():
    global labels, means
    means = []
    for i in range(0, len(points)):
        labels[i] = random.randint(0, 1)

def train_command():
    return

def reclassify_all_command():
    return

def play(i, j):
    if i<len(videos):
        if labels[i]==0:
            message("Pick Up")
        else:
            message("Put Down")
        if j<len(videos[i]):
            if show_edges():
                edge = process(videos[i][j])
                get_window().show_image(cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR))
            else:
                get_window().show_image(videos[i][j])
            get_window().after(int((1.0/fps)*1000), lambda: play(i, j+1))
        else:
            get_window().after(1000, lambda: play(i+1, 0))

def play_command():
    play(0, 0)

add_button(0, 0, "Clear", clear_command, nothing)
show_edges = add_checkbox(0, 1, "Edges?", nothing)
add_button(0, 2, "Record", start_recording, record_command)
add_button(0, 3, "Random labels", random_labels_command, nothing)
add_button(1, 0, "Train", train_command, nothing)
add_button(1, 1, "Reclassify all", reclassify_all_command, nothing)
add_button(1, 2, "Play", play_command, nothing)
add_button(1, 3, "Exit", done, nothing)
message = add_message(2, 0, 2)
camera = cv2.VideoCapture(0)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = camera.get(cv2.CAP_PROP_FPS)
camera.release()
start_video(width, height, 3, 4)
