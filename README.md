# Live Quiz Bot 🤖
![License: MIT][ico-license]

# Disclaimer

Using this bot is forbidden, so **DO NOT USE IT!**

This code was first cloned from ``` https://github.com/sushant10/HQ_Bot```  
then I've changed it to fit the Live Quiz app. Now the code is pretty different because I faced some problems and I wanted a better structured code.

# Bot functionalities
The script runs a telegram bot that for each image it receives, it reads it using **pytesseract** and the search the options in parallel.

## Packages Used

Use python 3.6. In particular the packages/libraries used are...

* JSON - Data Storage 
* Pillow - Image manipulation
* Google-Search-API - Google searching
* wikipediaapi - Wikipedia searches
* pytesseract - Google's free/open source OCR (requires seperate installtion)
* beautifulsoup4 - Parse google searches/html
* lxml - Beautifulsoup parser
* opencv2 - Image maniplulation

*To easily install these*
1. Install python 3.6
2. Install above packages
    * `$ pip3 install -r requirements.txt`
3. For tesseract 
    * `$ brew install tesseract`
4. For opencv
    * `$ brew install opencv`


## Usage

Make sure all packages above are installed. For android phones use [Vysor][link-vysor] and for iOS use quicktime player. **The code expects the phone to be on the left side of the screen.** If you want to change the screenshot co-ordinates change the values inside the ImageGrab in the `screen_grab()` function. To use the script : 

```bash
$ git clone https://github.com/sushant10/HQ_Bot
$ cd HQ_Bot
$ pip3 install -r requirements.txt
$ python3 answer_bot.py
Press s to screenshot live game, sampq to run against sample questions or q to quit:
s
...Question...
```



## Contributing

All contributions welcome.

## Credits

- [Sushant Rao][link-author]
- [All Contributors][link-contributors]

## Special shout out
[Jake Mor][jake-mor] was the person behind HQuack, the most viral popular bot to help solve HQ questions. His implementation inspired me to try my own. I recommend reading this [article][jake-more] to learn more about the whole story.


## License

The MIT License (MIT)

[ico-license]: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
[link-author]: https://github.com/sushant10

[link-wikiapi]: https://pypi.python.org/pypi/wikipedia
[link-gapi]: https://github.com/abenassi/Google-Search-API
[link-mike]: https://github.com/mikealmond/hq-trivia-assistant
[link-tesseract]: https://github.com/tesseract-ocr/tesseract/wiki
[jake-mor]: http://jakemor.com/
[jake-more]: https://medium.com/@jakemor/hquack-my-public-hq-trivia-bot-is-shutting-down-5d9fcdbc9f6e
[sampq]: ()
