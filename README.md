# web scraper

## Overview

Example of scraping information from specific website using Python + Selenium library.  
* Website: <https://www.aihitdata.com/>
* Scraping info: Website, email, phone, address of companies from specific domain

## Installation

```
pip install -r requirements.txt
```
Also, browser drivers need to be installed([details](https://github.com/robotframework/SeleniumLibrary#id9)):
```
pip install webdrivermanager
webdrivermanager firefox chrome --linkpath /usr/local/bin
```

### Run

```
python scrapper.py
```

Results of scraping - companies info - will be stored in `result` directory

### Usefull resources

* <https://github.com/robotframework/robotframework> - Robot Framework 
* <https://github.com/robotframework/SeleniumLibrary> - SeleniumLibrary
* <https://selenium-python.readthedocs.io/> - Selenium with Python
