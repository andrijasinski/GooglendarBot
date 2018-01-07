# AI2017HW7

_*This repository contains source code for the project in "Artificial Intelligence" course at the University of Tartu.*_

* [Description](#description)
* [Authors](#authors)
* [Requirements](#requirements)
* [Installation](#installation)
* [How to run](#how-to-run)
* [How to use](#how-to-use)

## Description:
This project is a part of "Artificial Intelligence" course. Our chatbot allows you to get information about your plans/events in Google Calendar just by asking "What are my plans for tomorrow?" or any other question, containing keyword corresponding to your needs (more about that in "How to use" section). Fortunately, with this chatbot, you can play checkers in case you get bored. Just type "!checkers" and enjoy!

## Authors:
* Andri Jasinski (andri.jasinski@gmail.com)
* Daniil Konovalov (konovalov.daniil96@gmail.com)

## Requirements:
* Python
* PIP package manager
* IDE or command line

_NB! PIP comes pre-installed with Python versions 2.7.9 and 3.4_ 

## Installation:
If you have freshly pulled the source code from the repository you will need to install external packages by running:

```
$ cd AI2017HW7
$ pip install -r requirements.txt
```

## How to run:

*_NB! Entering "src" directory is required for application stable work._*

CLI:
```
$ cd src
$ python chatterbot.py
```

GUI:
```
$ cd src
$ python chatterbot_gui.py
```

## How to use:

### Greeting

Chatbot can ask you for your name and greet you with that.

Example:
```
Arvuti: Tere, mina olen juturobot-sekretär.
Kasutaja: Mina olen Andri
Arvuti: Tere Andri, meeldiv tutvuda.
```
  
### Fetching data from Google Calendar

Chatbot searches for keywords to find the day you need information about.  

Lists of keywords:

```
>>> EVENT = ["plaanid", "plaan", "plan", "tegevus", "tegevused", "teen"]
>>> DAYS = ["täna", "homme", "ülehomme", "esmaspäev", "teisipäev", "kolmapäev", "neljapäev", "reede", "laupäev", "pühapäev"]
```

Example:

```
Arvuti: Tere, mina olen juturobot-sekretär.
Kasutaja: Mis on minu plaanid teisipäeval?
Arvuti: Teisipäeval plaanis on järgmised üritused:
Kell 10:15 toimub "Agile software development exam", mis kestab kuni 14:00, aadressil Juhan Liivi 2.
```

### Special commands

Chatbot understands several special commands, that starts with "!" followed by keyword.

Commands:

* !logout - logout and delete all credentials
* !checkers OR !kabe - play checkers with AI


_NB! This repository contains code for GUI solutions ("chatterbot\_gui.py", "checkers,py") provided by "Artificial Intelligence" course teaching staff._