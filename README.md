# radpixsort

![untitled-3](https://user-images.githubusercontent.com/40233850/232833562-82207b7e-3e50-4853-bc32-b461dad51dc9.gif)

python video script working with pixel sorting and radial blur

the pixel sort algorithm in use is made by [HexCodeFFF & satyarth](https://github.com/satyarth/pixelsort), which is based on the work of [Kim Asendorf](https://kimasendorf.com/)

python packages you need:
[opencv](https://pypi.org/project/opencv-python/), [glob](https://pypi.org/project/glob2/), [ffmpeg](https://pypi.org/project/ffmpeg-python/), [numpy](https://pypi.org/project/numpy/), [pixelsort](https://pypi.org/project/pixelsort/), [pillow](https://pypi.org/project/Pillow/)

1. put video you want to use and radpixsort.py in new empty folder
2. open terminal
3. navigate to the folder with script and video (cd)
4. run 'python3 radpixsort.py'

you can always kill the running script and just rerun it
your progress won't be lost, you will be ask if you want to continue, or reset everything

this script isn't meant to be perfomative or anything, it works really slow, rendering out every single frame of the video and processes it
the rawness of the process makes it interesting tho
