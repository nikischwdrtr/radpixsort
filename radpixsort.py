import cv2,os,glob,shutil,ffmpeg
import numpy as np,random
import numpy
from pixelsort import pixelsort
from PIL import Image

print (" ")
print (" ___________________________________")
print ("|                    __             |")
print ("|    _________ _____/ /             |")
print ("|   / ___/ __ `/ __  /              |")
print ("|  / /  / /_/ / /_/ /               |")
print ("| /_/   \__,_/\__,_/                |")
print ("|           ____  (_)  __           |")
print ("|          / __ \/ / |/_/           |")
print ("|         / /_/ / />  <             |")
print ("|        / .___/_/_/|_|        __   |")
print ("|       /_/   _________  _____/ /_  |")
print ("|            / ___/ __ \/ ___/ __/  |")
print ("|           (__  ) /_/ / /  / /_    |")
print ("|          /____/\____/_/   \__/    |")
print ("|___________________________________|")
print ("|                                   |")
print ("| radpixsort.py v0.1 2023           |")
print ("| \ \ radial blur                   |")
print ("|       && pixel sort               |")
print ("|           video algorithm         |")
print ("|                                   |")
print ("|___________________________________|")
print ("|                                   |")
print ("| dev@niklausiff.ch                 |")
print ("| https://www.niklausiff.ch         |")
print ("|___________________________________|")
print (" ")

print (">>> 0/3 settings")
print ("_____________________________________")
print (" ")

# input values
print ("video width")
w = int(input("> value: "))
print ("video height")
h = int(input("> value: "))
print ("angle for the pixel sort algorithm")
angle = int(input("> value: "))
print ("lower threshold (0-1)")
threshL = float(input("> value: "))
print ("upper threshold (0-1)")
threshU = float(input("> value: "))
print ("blur amount (0-1)")
blur = float(input("> value: "))
print ("how many radial blur iterations")
iterations = int(input("> value: "))
print ("do you want a frame preview (y/n)")
testFrame = input("> value: ")
randomPix = []
randomPixCopy = []
pixels = []
n = []

print ("_____________________________________")
print (" ")
print (">>> 1/3 create folders")

# create new folders / delete if already exists
dir = './'
directoryog = 'og'
filesog = os.listdir(dir)
newpathog = os.path.join(dir, directoryog)
if os.path.exists(newpathog):
    shutil.rmtree(newpathog)
os.mkdir(newpathog)
directoryo = 'output'
fileso = os.listdir(dir)
newpatho = os.path.join(dir, directoryo)
if os.path.exists(newpatho):
    shutil.rmtree(newpatho)
os.mkdir(newpatho)

# pixSort function
def pixSort(img):
    # resize image and convert to openCV
    noScale = Image.open(img)
    image = noScale.resize((w,h))
    cvimg = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

    # radial blur
    center_x = w/2
    center_y = h/2
    growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
    shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
    growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)
    shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)
    growMapx, growMapy = np.abs(growMapx), np.abs(growMapy)
    for i in range(iterations):
        tmp1 = cv2.remap(cvimg, growMapx, growMapy, cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        tmp2 = cv2.remap(cvimg, shrinkMapx, shrinkMapy, cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        cvimg = cv2.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)

    # pixel sort algorithm
    pilimg = Image.fromarray(cvimg)
    newImg = pixelsort(pilimg,angle=angle,lower_threshold=threshL,upper_threshold=threshU)
    newImg = pixelsort(newImg,lower_threshold=threshL,upper_threshold=threshU)
    
    # save img/show preview
    newImg = newImg.convert('RGB')
    if testFrame == 'y':
        newImg.show()
    else:
        newImg.save(os.path.join(newpatho+img[4:]))

# get movie
getVideo = []
for filename in os.listdir(dir):
    if filename.endswith('.avi') or filename.endswith('.AVI') or filename.endswith('.mp4') or filename.endswith('.MP4') or filename.endswith('.mov') or filename.endswith('.MOV'):
        getVideo.append(filename)

# get all frames
(
    ffmpeg
    .input(getVideo[0])
    .filter('fps', fps='25')
    .output('og/%09d.jpg', start_number=0)
    .overwrite_output()
    .run(quiet=True)
)

# get list of files
pathog = newpathog+'/'
jpg_list = sorted(glob.glob(pathog + "*.jpg"))

# get test frame
if testFrame == 'y':
    print ("_____________________________________")
    print (" ")
    print (">>> 1.5/3 show test frame")
    pixSort(jpg_list[random.randint(0,len(jpg_list))])
    testFrame = 'n'
    input("> press ENTER to continue..")

print ("_____________________________________")
print (" ")
print (">>> 2/3 apply radpixsort to frames")
print ("_____________________________________")

# apply pixSort and radial blur
for x in range(len(jpg_list)):
    pixSort(jpg_list[x])

print (" ")
print (">>> 3/3 create new video")
print ("_____________________________________")

# create new video
(
    ffmpeg
    .input(newpatho+'/'+'*.jpg', pattern_type='glob', framerate=25)
    .output('untitled.mp4')
    .run(quiet=True,overwrite_output=True)
)

print (" ")
print (" ___________________________________")
print ("|                                   |")
print ("| finished                          |")
print ("|___________________________________|")
print ("|                                   |")
print ("| new video:                        |")
print ("|   ./untitled.mp4                  |")
print ("|                                   |")
print ("| orignial frames:                  |")
print ("|   ./og/                           |")
print ("|                                   |")
print ("| processed frames:                 |")
print ("|   ./output/                       |")
print ("|                                   |")
print ("|___________________________________|")
print ("|                                   |")
print ("| dev@niklausiff.ch                 |")
print ("| https://www.niklausiff.ch         |")
print ("|___________________________________|")
print (" ")