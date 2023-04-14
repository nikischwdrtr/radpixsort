import cv2,os,glob,shutil,ffmpeg
from random import randrange
from perlin_noise import PerlinNoise
import numpy as np,random
import numpy
import math
from pixelsort import pixelsort
from PIL import Image

# input values
# print ("video width")
# w = int(input("> value: "))
# print ("video height")
# h = int(input("> value: "))
# print ("how many tiles")
# howMany = int(input("> value: "))
# print ("tile size")
# tileSize = int(input("> value: "))
w = 1000
h = 1000
howMany = 100
tileSize = 50
angle = 90
threshL = 0.3
threshU = 0.7
blur = 0.009
iterations = 200
randomPix = []
randomPixCopy = []
pixels = []
n = []

# img = './screen.png'

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

    pilimg = Image.fromarray(cvimg)
    newImg = pixelsort(pilimg,angle=angle,lower_threshold=threshL,upper_threshold=threshU)
    newImg = pixelsort(newImg,lower_threshold=threshL,upper_threshold=threshU)
    newImg = newImg.convert('RGB')
    # newImg.show()
    newImg.save(os.path.join(newpatho+img[4:]))

# pixSort(img)

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

# apply gridPix
# pixSort(jpg_list[40])
for x in range(len(jpg_list)):
    pixSort(jpg_list[x])

# create new video
(
    ffmpeg
    .input(newpatho+'/'+'*.jpg', pattern_type='glob', framerate=25)
    .output('untitled.mp4')
    .run(quiet=True,overwrite_output=True)
)