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
__version__ = '0.1.1'
version_date = '2021-12-14'
my_name = 'Jahrbuch-App'
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
        background-color: #e3e3e3;
        padding-top: 10px;
        padding-right: 10px;
        padding-bottom: 10px;
        padding-left: 10px;
        border-radius: 10px;
        width: 260px;
    }}
    </style>
    <div id ="appinfo">
    App: {my_name}<br>
    App-Version: {__version__} ({version_date})<br>
    Implementierung App: {tools.get_href('Statistisches Amt Basel-Stadt',URL_STAT_BASEL)}<br>
    Kontakt: <a target='Statistisches Amt Basel-Stadt' href='mailto:stata@bs.ch'>Statistisches Amt Basel-Stadt</a><br>
    </div>
    """
    return text


def page_boarder():
    text = f"""<style>
        .reportview-container .main .block-container{{
        padding-top: 1rem;
        padding-right: rem;
        padding-left: 1rem;
        padding-bottom: 10rem;
        }}</style>"""
    return text

def remove_menu():
    text = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
    return text


def clear_button():
    st.markdown(CHANGE_STYLE_CLEARBUTTON, unsafe_allow_html=True)
    button1=st.button(label="Clear Cache", key="button1")
    if button1:
        st.legacy_caching.clear_cache()


def show_titel():
    lottie_json = load_lottiefile('./images/11793-books-stack.json')
    col1,col2=st.columns([0.4,3])
    with col1:
        st_lottie(lottie_json, height=75, width=100,key="lottie1")
    with col2:
        st.header(f"Willkommen in der {my_name}")


def initial_widget_states():
    for key in ["multi1","text1","check1"]:
        if key not in st.session_state:
            st.session_state["multi1"]=[]
            st.session_state["text1"]=""
            st.session_state["check1"]=False


def print_anleitung():
    if st.session_state.get("check1")==False:
        if st.session_state.get("multi1")==[]:
            if st.session_state.get("text1")=="":
                show_anleitung(True)
            else:
                show_anleitung(False)
        else:   
            show_anleitung(False)
    else:   
        show_anleitung(False)


def show_anleitung(exp_value: bool):
    #Anleitung zur Suchfunktion
    st.markdown(CHANGE_STYLE_ANLEITUNG,unsafe_allow_html=True)
    placerholder_expander = st.empty()
    with placerholder_expander.expander(label="Hier können Sie gezielt in den Statistischen Jahrbüchern suchen. 3 Einstiegspunkte stehen Ihnen zur Verfügung.", expanded=exp_value):
        st.markdown(f'''<p style="font-size:16px";><b>1. Freitextsuche in den Tabellen-Titeln</b><br>
        Sie können mehrere Suchbegriffe kombinieren. So erhalten Sie rasch einen Überblick, 
        ob Zahlen zu Ihren Suchbegriffen vorhanden sind und über welchen Zeitraum.<br>  
        <b>2. Thematische Suche</b><br>  
        Das Feld "Themenbereich" enthält eine Auswahlliste, die nach den 19 Themen der öffentlichen Statistik gegliedert ist. 
        Zur weiteren Eingrenzung ist jeder Themenbereich in Themen unterteilt.<br>  
        <b>3. Suche nach Jahrbuch-Ausgaben</b><br>
        Falls Sie an einer speziellen Jahrbuch-Ausgabe interessiert sind.<br><br> 
        Die Ergebnisse Ihrer Suche werden in Form einer Liste mit Tabellen ausgegeben.<br>
        <b>Viel Erfolg bei der Datenrecherche!</b></p>''', unsafe_allow_html=True)


@st.cache 
def get_data():
    #Metadaten aus einer Textdatei importieren.
    metadata = pd.read_csv(TABELLEN_FILE, sep='\t')
    positionsliste = pd.read_csv(POSITIONSLISTEN_FILE, sep='\t')
    return metadata, positionsliste


def main():
    st.set_page_config(page_title=my_name_short, page_icon='./images/favicon.png', layout='wide', initial_sidebar_state='auto') 
    st.markdown(remove_menu(), unsafe_allow_html=True)
    st.markdown(page_boarder(),unsafe_allow_html=True,)
    
    #App-Titel anzeigen
    show_titel()
    st.markdown('<br>', unsafe_allow_html=True)
    
    #Status der Eingabefenster initiieren. 
    initial_widget_states()
    
    #Anleitung Ein-und Ausklappen
    print_anleitung()
    st.markdown(f'<p style="font-size:16px";><br></p><br>', unsafe_allow_html=True)
    
    #Metadaten initiieren
    metadata, positionsliste = get_data()
    #Metadaten ohne Jahrbuch 2021
    metadata_ohne21 = metadata.drop("JB-2021",axis=1, inplace=False)
    positionsliste_ohne21 = positionsliste.drop("JB-2021",axis=1, inplace=False)
    #Suchfunktion initiieren und anzeigen
    app = jbex_find.App(metadata_ohne21, positionsliste_ohne21)
    app.show_menu()


    #App-Infos anzeigen lassen
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(get_app_info(), unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    clear_button()


if __name__ == '__main__':
    main()
