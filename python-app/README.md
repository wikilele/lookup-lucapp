# Python - proof of work

This code was first cloned from ``` https://github.com/sushant10/HQ_Bot``` (credits [Sushant Rao][link-author])

then I've changed it to fit the Live Quiz app. Now the code is pretty different because I faced some problems and I wanted a better structured code.

## Bot functionalities
The script assumes your smartphone is connected to the pc, it takes a screenshot, reads the image using **pytesseract** and then searches the options in parallel.

## Packages Used

Use python 3.6. In particular the packages/libraries used are...

* JSON - Data Storage 
* Pillow - Image manipulation
* Google-Search-API - Google searching
* wikipediaapi - Wikipedia searches
* pytesseract - Google's free/open source OCR (may require seperate installtion)
* beautifulsoup4 - Parse google searches/html
* lxml - Beautifulsoup parser
* opencv2 - Image maniplulation
* [adb] - to take the screenshot

*To easily install these*
1. Install python 3.6
2. Install above packages
    * `$ pip3 install -r requirements.txt`
3. **tesseract** and **opecv** are also listed in the ```requirements.txt``` file, but if the istallation doesn't work google  for the correct way to install them
4. Install adb 
    * `sudo apt-get install android-tools-adb android-tools-fastboot`


## Usage

```bash
$ pip3 install -r requirements.txt
$ python3 main.py
    Press s to screenshot live game  or q to quit:

```

[link-author]: https://github.com/sushant10
[adb]: https://developer.android.com/studio/command-line/adb