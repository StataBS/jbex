"""
Diese App erlaubt die Suche nach Jahrbüchern ab 2021, welche als pdf-Dateien hinterlegt sind.
"""
import io
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
from const import *
import jbex_find
import requests
import json
import tools


__author__ = 'Lukas Calmbach'
__version__ = '0.0.9'
version_date = '2021-10-28'
my_name = 'Jahrbuch-Suche Basel-Stadt'
my_name_short = 'JBEx'


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
        
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_app_info():
    """
    Zeigt die Applikations-Infos verwendeter Datenbankserver etc. an.
    """

    text = f"""
    <style>
        #appinfo {{
        font-size: 11px;
        background-color: lightblue;
        padding-top: 10px;
        padding-right: 10px;
        padding-bottom: 10px;
        padding-left: 10px;
        border-radius: 10px;
    }}
    </style>
    <div id ="appinfo">
    App: {my_name}<br>
    App-Version: {__version__} ({version_date})<br>
    Implementierung App: {tools.get_href('Statistisches Amt Basel-Stadt',URL_STAT_BASEL)}<br>
    Kontakt: <a href="mailto:nathalie.grillon@bs.ch">Nathalie Grillon</a><br>
    </div>
    """
    return text

@st.cache 
def get_data():
    metadata = pd.read_csv(TABELLEN_FILE, sep='\t')
    return metadata

def main():
    lottie_json = load_lottiefile('./images/11793-books-stack.json')
    st.set_page_config(page_title=my_name_short, page_icon='./images/favicon.png', layout='wide', initial_sidebar_state='auto') 
    col1,col2=st.columns([0.4,3])
    with col1:
        st_lottie(lottie_json, height=75, width=100,key="lottie1")
    with col2:
        st.header(f"{my_name}")
    st.markdown('##')
    with st.expander("Anleitung zur Suchfunktion"):
        st.markdown('''Die vorliegende Anwendung hilft ihnen bei der gezielten Suche nach Jahrbuch-Inhalten. 
        Sie haben drei Einstiegspunkte: Die Freitextsuche in den Tabellen-Titeln – wobei mehrere Suchbegriffe kombiniert werden können – 
        ermöglicht ihnen einen raschen Überblick, ob Zahlen zu ihrem Thema vorhanden sind. 
        Falls sie an einer speziellen Jahrbuch-Ausgabe interessiert sind, gehen sie über den Zugang «Jahrbuch auswählen». 
        Der thematische Einstieg schliesslich erfolgt über das Feld «Themenbereich» mittels Dropdown-Liste, 
        wobei die Suche über das Feld «Thema» zusätzlich spezifiziert/eingegrenzt werden kann. 
        Die Ergebnisse ihrer Suche werden in Form einer Liste mit Tabellen ausgeben...
        \n Viel Spass bei der Datenrecherche; wir hoffen, sie werden rasch fündig!''')
    st.markdown('##')

    metadata = get_data()
    app = jbex_find.App(metadata)
    app.show_menu()
    
    st.markdown('##')
    text = get_app_info()
    st.markdown(text, unsafe_allow_html=True)
    st.markdown('#')
    if st.button(label="Clear Cache👈"):
        st.legacy_caching.clear_cache()

if __name__ == '__main__':
    main()
