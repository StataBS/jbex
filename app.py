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
__version__ = '0.1.0'
version_date = '2021-11-15'
my_name = 'Wilkommen in der Jahrbuch-App'
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
    Kontakt: <a href="mailto:stata@bs.ch">Statistisches Amt Basel-Stadt</a><br>
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
    placerholder_expander = st.empty()
    with placerholder_expander.expander(label="Hier können Sie gezielt in den statistischen Jahrbüchern suchen. 3 Einstiegspunkte stehen Ihnen zur Verfügung.", expanded=True):
        st.markdown(f'''<p style="font-size:16px";><b>1. Freitextsuche in den Tabellen-Titeln</b><br>
        Sie können mehrere Suchbegriffe kombinieren. So erhalten Sie rasch einen Überblick, 
        ob Zahlen zu Ihren Suchbegriffen vorhanden sind und über welchen Zeitraum.<br>  
        <b>2. Thematische Suche</b><br>  
        Das Feld "Themenbereich" enthält eine Auswahlliste, die nach den 19 Themen der öffentlichen Statistik gegliedert ist. 
        Zur weiteren Eingrenzung ist jeder Themenbereich in Themen unterteilt.<br>  
        <b>3. Suche nach Jahrbuch-Ausgaben</b><br>  
        Falls Sie an einer speziellen Jahrbuch-Ausgabe interessiert sind.  
        \n Die Ergebnisse Ihrer Suche werden in Form einer Liste mit Tabellen ausgegeben.</p>''', unsafe_allow_html=True)
    st.markdown('#')
    st.markdown(f'<p style="font-size:16px";><b>Viel Spass bei der Datenrecherche; wir hoffen, Sie werden rasch fündig!</b></p>', unsafe_allow_html=True)
    st.markdown('##')
    metadata = get_data()
    app = jbex_find.App(metadata)
    app.show_menu() 
    st.markdown("""<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}header {visibility: hidden;}</style>""", unsafe_allow_html=True)
    st.markdown('##')
    text = get_app_info()
    st.markdown(text, unsafe_allow_html=True)
    st.markdown('#')
    st.markdown('''<style> div.stButton>button:first-child{font-size: 9px;} </style>''', unsafe_allow_html=True)
    button1=st.button(label="Clear Cache", key="button1")
    
    if button1:
        st.legacy_caching.clear_cache()

if __name__ == '__main__':
    main()
