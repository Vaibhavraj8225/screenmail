This app extracts html part of eml files renders them using playwright screenshot them and save it inside the screenshots directory.
This app is created to process batch of eml files at once to get the overview of them also it disable any javascript to avoid any suspicious action.
<br><br>
<br><br>
<b>How to install</b> <br>
pip install -r requirements.txt <br>
playwright install chromium <br>
python3 main.py
<br><br>
<br><br>
<b>IF installing dependecies require container use this method</b> <br>
python3 -m venv venv <br>
source venv/bin/activate <br>
pip install -r requirements.txt <br>
playwright install chromium <br>
python3 main.py
<br><br>
<br><br>
<b>Directory Structure</b>
<br><br>
screenmail/  <br>
│  <br>
├── emails/  <br>
│   ├── mail1.eml  <br>
│   ├── mail2.eml  <br>
│   └── ...  <br>
│ <br>
├── screenshots/  <br>
│   ├── mail1.png  <br>
│   ├── mail2.png  <br>
│   └── ...  <br>
│  <br>
├── rendered/  <br>
│   ├── mail1.html  <br>
│   ├── mail2.html  <br>
│   └── ...  <br>
│  <br>
├── logs/  <br>
│   └── errors.log  <br>
│  <br>
├──main.py  <br>
└── requirements.txt <br>
