# Jahrbuch-App
Autor: Lukas Calmbach & Niklaus Baltisberger

## Installation
Auf remoteserver cmd-Shell eröffnen als Admin:

1. git clone ssh://git@evpdstata01:/jbex.git
1. cd jbex
1. py -3.8 -m venv env
1. env\scripts\activate
1. pip install -r requirements.txt `--proxy=http://<user>:<pwd>@radius.bs.ch:3128`

Programm starten mit:
1. streamlit run app.py
