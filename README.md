This app extracts html part of eml files renders them using playwright screenshot them and save it inside the screenshots directory.
This app is created to process batch of eml files at once to get the overview of them also it disable any javascript to avoid any suspicious action.
<br><br>
<b>Directory Structure</b>
screenmail/
│
├── emails/
│   ├── mail1.eml
│   ├── mail2.eml
│   └── ...
│
├── screenshots/
│   ├── mail1.png
│   ├── mail2.png
│   └── ...
│
├── rendered/
│   ├── mail1.html
│   ├── mail2.html
│   └── ...
│
├── logs/
│   └── errors.log
│
└── main.py
