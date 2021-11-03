# DocEx

## Installation
Auf remoteserver cmd-Shell eröffnen als Admin:
```
> git clone ssh://git@evpdstata01:/docex.git
> cd docex
> python 3.8 -m venv env
> LC: py -3.8 -m venv env
> env\scripts\activate
> pip install -r requirements.txt --proxy=http://<user>:<pwd>@radius.bs.ch:3128
```
Programm starten mit:
```
> streamlit run app.py
```