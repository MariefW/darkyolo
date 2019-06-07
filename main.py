import os
from os import walk
import PIL
from PIL import Image
import subprocess
import sys
import datetime
os.system

"""Extract Frame every 5 seconds"""
subprocess.call(['ffmpeg','-i','video/drone.mp4', '-vf','fps=1/5', 'video/drone%3d.jpg', '-hide_banner'])

"""Drone Video path"""
vidpath = "video/"

text_file = open('test.txt', 'w')

"""List of Images Path"""
txt_img_list = []

"""Iteration for showing pictures that we want to process"""
for (dirpath, dirnames, filenames) in walk(vidpath):
    txt_img_list.extend(filenames)
    break
print(txt_img_list)

"""Process"""
for txt_name in txt_img_list:
    """Save images path"""
    text_file.write('video/%s.jpg\n'%(  os.path.splitext(txt_name)[0]))

text_file.close()

"""Variable Init"""
d = 1
time = 5

"""Reading image path"""
with open('test.txt', 'r') as fobj:
    for line in fobj:
        image_List = [[num for num in line.split()] for line in fobj]

open("person.txt", "w").close()
"""Iteration for detecting images"""
for images in image_List:
    # commands = ['darknet.exe detector test data/obj.data cfg/yolov3-clone.cfg yolov3-clone_final.weights -dont_show', images[0]]
    commands = ["./darknet", "detector", "test", "data/obj.data", "cfg/yolov3-clone.cfg", "yolov3-clone_final.weights" ,"-dont_show", images[0]]
    os.system(', '.join(commands))

    output = subprocess.check_output(commands)
    output = output.decode("utf-8").split("\n")
    # print (output)
    # Count the number of lines that contain "person"
    numPeople = len([i.split(":")[0] for i in output if i.split(":")[0] == 'person'])

    print("{} people detected.".format(numPeople))
    """Change Seconds into minutes"""
    timeMinutes=str(datetime.timedelta(seconds=time))
    """Write total of people in the frame into person.txt"""
    with open("person.txt", "a") as myfile:
        myfile.write("{} - {} Person\n".format(timeMinutes, numPeople ))


    """Save predictions image into output folder"""
    predicted_image = Image.open("predictions.jpg")
    output_image = "output/predicted_image%3d.jpg"%d
    predicted_image.save(output_image)
    d+=1
    time+=5
