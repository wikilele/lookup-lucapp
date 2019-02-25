# Live Quiz Bot 
![License: MIT][ico-license]

# Disclaimer

Using this bot is forbidden, so **DO NOT USE IT!**

This code was first cloned from ``` https://github.com/sushant10/HQ_Bot``` (credits [Sushant Rao][link-author])

then I've changed it to fit the Live Quiz app. Now the code is pretty different because I faced some problems and I wanted a better structured code.

# Bot functionalities
The script runs a telegram bot that for each image it receives, it reads the image using **pytesseract** and then searches the options in parallel.

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

*To easily install these*
1. Install python 3.6
2. Install above packages
    * `$ pip3 install -r requirements.txt`
3. **tesseract** and **opecv** are also listed in the ```requirements.txt``` file, but if the istallation doesn't work try this:
    * `$ brew install tesseract`
    * `$ brew install opencv`


## Usage

```bash
$ pip3 install -r requirements.txt
$ python3 answer_bot.py
    The script/bot is running | Ctrl-C to stop 

// from your smartphone send the screen of the question to the telegram bot chat
```

## License

The MIT License (MIT)

[ico-license]: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
[link-author]: https://github.com/sushant10

