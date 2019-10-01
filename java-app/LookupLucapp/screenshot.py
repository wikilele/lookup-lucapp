import os
import sys

# python is way better to do this stuff
os.system("adb devices")
# imgpath = "Screens/screen.png"
os.system("adb exec-out screencap -p > " + sys.argv[1])
