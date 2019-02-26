

from answer_bot import solve_quiz, bcolors
import os
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print("Time spent " + str(te-ts))
        return result

    return timed

@timeit
def main():
    imgpath = "Screens/screen.png"
    os.system("adb exec-out screencap -p > " + imgpath)
    solve_quiz(imgpath)


if __name__ == '__main__':
    os.system("adb devices")

    main()
