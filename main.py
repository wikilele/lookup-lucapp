
from answer_bot import solve_quiz, bcolors
import os
import mydecorators


@mydecorators.timeit("main")
def main():
    imgpath = "Screens/screen.png"
    os.system("adb exec-out screencap -p > " + imgpath)
    solve_quiz(imgpath)


if __name__ == '__main__':
    os.system("adb devices")

    while True:
        keypressed = input(bcolors.WARNING +
                            '\nPress s to screenshot live game, sampq to run against sample questions or q to quit:\n'
                            + bcolors.ENDC)
        if keypressed == 's':
            main()
        elif keypressed == 'q':
            break
        else:
            print(bcolors.FAIL + "\nUnknown input" + bcolors.ENDC)
