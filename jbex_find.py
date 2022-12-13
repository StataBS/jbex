"""
Diese App erlaubt das Browsen von Jahrbüchern

Kontakt: lukas.calmbach@bs.ch, niklaus.baltisberger@bs.ch
"""
from enum import Enum
import io
import pandas as pd
import streamlit as st
from datetime import datetime, date
from st_aggrid import GridUpdateMode
from const import *
import re
import tools
import app
import numpy as np
import fitz
import base64
import time




CURRENT_YEAR = date.today().year
DATA_YEAR = CURRENT_YEAR
class App():
    def __init__(self, metadata, positionsliste):
        self.record = {}
        self.metadata_df = metadata
        self.metadata_filtered = self.metadata_df
        self.positionsliste = positionsliste

    
    def get_metadata(self):
        sql = qry['metadata']
        df, ok, err_msg = db.get_recordset(self.conn, sql)
        return df


    def get_status_list(self):
        query = qry['lookup_code'].format(80) #category status
        result  = pd.DataFrame.from_dict({'id': [-1], 'value': ['<alle>']}, orient='columns')
        df, ok, err_msg = db.get_recordset(self.conn, query)
        if ok:
            result = result.append(df.set_index('id'))
        return result

    
    def get_filtered_tabs(self, filter):
        if len(filter['titel']) != 0:
            for i in filter['titel']:
                self.metadata_filtered = self.metadata_filtered[self.metadata_filtered['Titel'].str.contains(i, case=False)]
        if filter['themenbereich'] != []:
            if filter['thema'] == []:
                self.metadata_filtered = self.metadata_filtered[self.metadata_filtered['Themenbereich'].isin(filter['themenbereich'])]
            else:
                self.metadata_filtered = self.metadata_filtered[self.metadata_filtered['Thema'].isin(filter['thema'])]


    def get_tabelle(self):
        def get_filter_description():
            text =f'''<p style="color:red"><b>Sie haben noch keinen Filter eingegegeben. Die untenstehende Liste enthält alle verfügbaren Jahrbuch-Tabellen. 
            Verwenden Sie obige Felder, um die Auswahl auf einen Themenbereich einzugrenzen, oder suchen Sie nach Wörtern im Tabellentitel.</b></p>'''
            if f['themenbereich'] != []:
                liste_themenbereiche = ", ".join(f['themenbereich'])
            if len(f['titel'])!= []:
                for i, wort in enumerate(f['titel']):
                    f['titel'][i]=wort.capitalize()
                    liste_titel = ", ".join(f['titel'])
            
            if (f['titel']!=[]) & (f['themenbereich'] == []):
                if len(f['titel']) == 1:
                    text = f"""Die untenstehende Liste enthält alle Tabellen, welche das Wort __{f['titel'][0]}__ im Titel enthalten. """
                elif len(f['titel']) == 2:
                    text = f"""Die untenstehende Liste enthält alle Tabellen welche die Wörter __{f['titel'][0]}__ und __{f['titel'][1]}__ im Titel enthalten. """
                else:
                    text = f"""Die untenstehende Liste enthält alle Tabellen welche die Wörter __{liste_titel}__ im Titel enthalten. """
                    
            elif (f['titel']==[]) & (f['themenbereich'] != []):
                if len(f['themenbereich']) > 1:
                 text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche __{liste_themenbereiche}__. """
                else:
                 text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs __{liste_themenbereiche}__. """ 
              
            elif (f['titel']!=[]) & (f['themenbereich'] != []):
                if (len(f['themenbereich']) > 1) & (len(f['titel']) > 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche __{liste_themenbereiche}__, welche auch die Wörter __{liste_titel}__ im Titel enthalten."""
                elif (len(f['themenbereich']) > 1) & (len(f['titel']) == 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche __{liste_themenbereiche}__, welche auch das Wort __{liste_titel}__ im Titel enthält."""
                elif (len(f['themenbereich']) == 1) & (len(f['titel']) > 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs __{liste_themenbereiche}__, welche auch die Wörter __{liste_titel}__ im Titel enthalten."""
                elif (len(f['themenbereich']) == 1) & (len(f['titel']) == 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs __{liste_themenbereiche}__, welche auch das Wort __{liste_titel}__ im Titel enthält."""

            return text

        #Generieren eines Dictionary für die Speicherung der Suchparameter
        f = {}
        f['themenbereich']=[]
        f['thema']=[]
        f['jahrgang'] = 0
        f['titel'] = []

        #Eingabefenster für die Suchparameter.
        #Suchparameter: Textinput
        placeholder_text = st.empty()
        with placeholder_text.container():
            st.write("🔎 Wörter im Tabellentitel suchen:")
            st.markdown('<br>', unsafe_allow_html=True)
            textinput = st.text_input("Wörter im Tabellentitel suchen:",key='text1', help='Eine Eingabe muss mit der Eingabetaste bestätigen werden.')
            f['titel'] = tools.list_suchwoerter(textinput) 
        st.markdown('<br>', unsafe_allow_html=True)
        
        #Suchparameter: Themenbereiche und die Themen .
        placeholder_themenbereich = st.empty()
        with placeholder_themenbereich.container():
            st.write("🔎 Themenbereich auswählen:")
            col1, col2=st.columns([1.315,1])
            with col1:
                st.markdown(CHANGE_STYLE_MULTI1,unsafe_allow_html=True)
                f['themenbereich'] = st.multiselect(label='Themenbereich:',options=tools.sort_themenbereich(), key='multi1')
            with col2:
                themen=[]
                for i in f['themenbereich']:  
                    themen.extend(THEMEN.get(i))
                    themen.sort()
                st.markdown(CHANGE_STYLE_MULTI1,unsafe_allow_html=True)
                f['thema'] = st.multiselect(label='Thema (optional):' ,options=themen, help="Wählen Sie immer zuerst einen Themenbereich aus.", key="multi2")
        st.markdown('<br>', unsafe_allow_html=True)

        #Suchparameter: Einzelnes Jahrbuch
        placeholder_jahrgang = st.empty()
        with placeholder_jahrgang.container():
            st.write("🔎 Jahrbuch-Ausgabe auswählen:")
            jahrgang_box=st.checkbox("Eine spezifische Jahrbuch-Ausgabe auswählen.", key='check1')
        if jahrgang_box== True:
            f['jahrgang']=st.number_input(f'Jahrbuch zwischen 1921 und {DATA_YEAR}',max_value=(DATA_YEAR), min_value=1921, help="""Im Jahr 1981 ist eine
                Doppelausgabe aus den Jahren 1980/81 erschienen.""")    
        st.markdown('<br>', unsafe_allow_html=True)

        #Ein und Ausklappen der einzelnen Suchfunktionen
        if f['titel']!=[]:
            placeholder_jahrgang.empty()
            placeholder_themenbereich.empty()
        if jahrgang_box== True:
            placeholder_themenbereich.empty()
            placeholder_text.empty()
        if f['themenbereich']!=[]:
            placeholder_jahrgang.empty()
            placeholder_text.empty()
        if jahrgang_box == False:
            #Filtern der Tabellen nach Filterparameter
            self.get_filtered_tabs(f)
            if self.metadata_filtered.empty==False:
                st.markdown(get_filter_description(),unsafe_allow_html=True)
            else: 
                st.markdown(f'<p style="color:red"><b>Es konnte kein Suchergebnis gefunden werden.</b></p>',unsafe_allow_html=True)
        return [self.metadata_filtered, f['jahrgang'], jahrgang_box]
        

    def show_jahrbuecher(self, tabelle, df):
        #Liste aus Hyperlinks mit allen Jahrbücher erstellen, sowie Informationen zu Daten und Themenbereich ausgeben.
        st.subheader('__Jahrbücher__')
        jb_von = int(tabelle['Daten-Start'])
        jb_bis = DATA_YEAR if tabelle['Daten-Ende']== 0 else int(tabelle['Daten-Ende'])
        text = f"""Die Tabelle __'{str(tabelle['Titel'])}'__ wird in den Ausgaben von __{df['Jahrbuecher'].iloc[0]}__ bis __{df['Jahrbuecher'].iloc[-1]}__ in __{len(df)}__ 
        verschiedenen Jahrbüchern geführt. Die Einzeldaten decken einen Zeitraum von __{jb_von}__ bis __{jb_bis}__ ab. 
        \n \n Klicken Sie auf den Link, um die PDF-Datei des jeweiligen Jahrbuchs zu öffnen:"""
        st.markdown(text)
        liste = ''
        for i in df.index:
            if   df['Position'][i] != 0:
                url = f"{URL_BASE}{df['Jahrbuecher'][i]}.pdf#page={df['Position'][i]}"
                name = f"Statistisches Jahrbuch des Kantons Basel-Stadt {df['Jahrbuecher'][i]}"
                liste += f"- [{name}]({url}) \n"
            else:
                url = f"{URL_BASE}{df['Jahrbuecher'][i]}.pdf"
                name = f"Statistisches Jahrbuch des Kantons Basel-Stadt {df['Jahrbuecher'][i]}"
                liste += f"- [{name}]({url}) \n"
        st.markdown(liste)


    def show_jahrbuch(self,jahr):
        #Hyperlink mit einem Jahrbuch erstellen.
        if jahr == 1980 or jahr == 1981:
            st.subheader('__Jahrbuch__')
            st.markdown(f"Sie können die Gesamtausgabe des __Jahrbuchs__ __1980/81__ als PDF-Datei herunterladen.")
            liste = ''
            url = f"{URL_BASE}1981.pdf"
            name = f'Statistisches Jahrbuch des Kantons Basel-Stadt 1980/81'
            liste += f"- [{name}]({url})"
            st.markdown(liste)
        else:
            st.subheader('__Jahrbuch__')
            st.markdown(f"Sie können die Gesamtausgabe des __Jahrbuchs__ __{jahr}__ als PDF-Datei herunterladen.")
            liste = ''
            url = f"{URL_BASE}{jahr}.pdf"
            name = f'Statistisches Jahrbuch des Kantons Basel-Stadt {jahr}'
            liste += f"- [{name}]({url})"
            st.markdown(liste)
    

    def show_datenreihe_jahrbuecher (self,df):
        #Erstellen einer Liste mit den Datenreihe, welche in jedem Jahrbuch zu finden ist.
        text1 = f'Für die selektierte Tabelle sind in jedem Jahrbuch folgende Datenjahre enthalten.\n'
        st.markdown(text1)
        liste = ''
        for i in range(len(df)):
            name = f"**{df['Jahrbuecher'].iloc[i]}:**\t_{df['Datenjahre'].iloc[i]}_"
            liste += f"- {name} \n"   
        st.markdown(liste)


    
    def show_preview_download_pdf(self,selected, df_datenjahre_jahre):
        #Layout
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown(f"""Sie haben die Tabelle __'{selected["Titel"]}'__ ausgewählt. Sie können sich nun die Tabelle anzeigen 
        lassen oder ein PDF-Dokument zum Herunterladen zusammenstellen.""") 
        col1,col2,col3=st.columns([4.5,0.5,8])
        with col1:
            st.markdown(CHANGE_STYLE_SLIDER, unsafe_allow_html=True)
            placeholderSlider = st.empty()
        with col3:
            st.markdown(CHANGE_STYLE_CHECKBOX, unsafe_allow_html=True)
            placeholderCheckbox = st.empty()
        st.markdown("<br/>", unsafe_allow_html=True)
        placeholderTableContainer = st.empty()
        st.markdown("<br/>", unsafe_allow_html=True)
        placeholderEndPage = st.empty()
        st.markdown("<br/>", unsafe_allow_html=True)
        placeholderSelectPreviewPDF = st.empty()
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        placeholderTextPreview = st.empty()
        placeholderPreviewContainer = st.empty()
        placeholderButtonDownload = st.empty()

        #Slider zum Auswählen der Zeitspanne und Tabelle darstellen
        start = df_datenjahre_jahre["Jahrbuecher"].iat[0]
        ende = df_datenjahre_jahre["Jahrbuecher"].iat[-1]

        if(start != ende):
            slider_range = placeholderSlider.slider("1. Wählen Sie eine Zeitspanne für die ausgewählte Jahrbuchtabelle aus. ",
            value=[start,ende], min_value=start, max_value=ende, key="slider_years")
            after_slider_df = df_datenjahre_jahre[(df_datenjahre_jahre['Jahrbuecher']>=slider_range[0]) & (df_datenjahre_jahre['Jahrbuecher']<=slider_range[1])]
            
        else:
            after_slider_df = df_datenjahre_jahre[(df_datenjahre_jahre['Jahrbuecher']==start)]
        

        #Daten nach der Auswahl der Zeitspanne filtern
        new_selected_df = pd.DataFrame()
        #Checkbox um alle Jahrbücher in der gewählten Zeitspanne zu selektieren.
        checkbox_allyears = placeholderCheckbox.checkbox(label="Ich möchte alle Jahrbücher aus der gewählten Zeitspanne.", key="Check_years")
        if (checkbox_allyears==False):
            with placeholderTableContainer.container():
                #Erstellen der interaktiven Tabelle und filtern der Daten nach ausgewählten Jahrbüchern.
                st.markdown(f"Selektieren Sie die gewünschten Jahrbücher in der untenstehenden Tabelle.")
                new_selected_table = tools.show_table(after_slider_df, GridUpdateMode.SELECTION_CHANGED,300,autohight=False, col_cfg=COL_CFG_2, 
                sel_cfg=[{"rowSelection":"multiple", "rowMultiSelectWithClick": "true"}], pag_cfg=[{"enabled": False}])
                new_selected_df = tools.selected_dataframe(after_slider_df,new_selected_table)       
        else:
            placeholderTableContainer = st.empty()
            new_selected_df = pd.DataFrame()
    
        #Input der Zahl für die Auswahl der fortlaufenden Tabellenseiten.
        st.markdown(CHANGE_STYLE_NUMBERINPUT, unsafe_allow_html=True)
        end_page = placeholderEndPage.number_input(label="2. Wie viele fortlaufende Seiten nach jeder ausgewählten Tabelle im Jahrbuch wollen Sie? (Achtung: Jahrbuchtabellen können auch über mehrere Seiten gehen!)", 
            min_value=0,max_value=6, step=1, help="Sie können zwischen 0 bis 6 zusätzlichen Seiten auswählen.", key="numberinput_pages")

        #Auswahl zwischen Preview und PDF-Dokument.
        st.markdown(CHANGE_STYLE_SELECTBOX, unsafe_allow_html=True)
        SelectPreviewPDF = placeholderSelectPreviewPDF.selectbox(label="3. Tabelle anzeigen lassen oder PDF-Dokument erstellen.",options= ["","Tabelle anzeigen","PDF-Dokument erstellen"],
        key="selectbox_switch", disabled=tools.checkbox_disable_func(checkbox_allyears, new_selected_df), help="""Wählen Sie 'Tabelle anzeigen', so wird immer nur die älteste und die 
        jüngste Tabelle angezeigt""")
        name = f'{selected["Kürzel"]}_{selected["Titel"]}'
        #Logik für Preview:
        if ((SelectPreviewPDF=="Tabelle anzeigen" and checkbox_allyears==False) and new_selected_df.empty == False): 
            preview_df = df_datenjahre_jahre[(df_datenjahre_jahre['Jahrbuecher']==new_selected_df["Jahrbuecher"].iat[0]) | 
            (df_datenjahre_jahre['Jahrbuecher']==new_selected_df["Jahrbuecher"].iat[-1])] 
            with placeholderTextPreview.container():
                st.markdown(tools.text_preview(new_selected_df)) 
            with placeholderPreviewContainer.container():
                tools.show_preview(preview_df, end_page) 
            tools.delete_temp()

        elif (SelectPreviewPDF=="Tabelle anzeigen" and checkbox_allyears==True): 
            preview_df = df_datenjahre_jahre[(df_datenjahre_jahre['Jahrbuecher']==after_slider_df["Jahrbuecher"].iat[0]) | 
            (df_datenjahre_jahre['Jahrbuecher']==after_slider_df["Jahrbuecher"].iat[-1])]
            with placeholderTextPreview.container():
                st.markdown(tools.text_preview(after_slider_df)) 
            with placeholderPreviewContainer.container():
                tools.show_preview(preview_df, end_page) 
            tools.delete_temp()
        #Logik für PDF-Dokument: 
        elif (SelectPreviewPDF=="PDF-Dokument erstellen" and checkbox_allyears==False and new_selected_df.empty == False):   
            placeholderSlider.empty()
            placeholderTableContainer.empty()
            placeholderEndPage.empty()
            placeholderCheckbox.empty()
            get_pdf = tools.spinner(new_selected_df,end_page)
            st.markdown(CHANGE_STYLE_DOWNLOADBUTTON, unsafe_allow_html=True)  
            placeholderButtonDownload.download_button(label=f'PDF Herunterladen', 
            data=get_pdf, file_name=f"{name}.pdf",mime='application/octet-stream', key="download1", on_click=tools.clickhandle)
        elif  (SelectPreviewPDF=="PDF-Dokument erstellen" and checkbox_allyears==True):   
            placeholderSlider.empty()
            placeholderTableContainer.empty()
            placeholderEndPage.empty()
            placeholderCheckbox.empty()
            get_pdf = tools.spinner(after_slider_df,end_page)
            st.markdown(CHANGE_STYLE_DOWNLOADBUTTON, unsafe_allow_html=True)   
            placeholderButtonDownload.download_button(label=f'PDF Herunterladen', 
            data=get_pdf, file_name=f"{name}.pdf",mime='application/octet-stream', key="download1", on_click=tools.clickhandle)
        elif (SelectPreviewPDF=="" and checkbox_allyears==False and new_selected_df.empty == True): 
            st.info("Selektieren Sie in der oberen Tabelle mindestens ein Jahrbuch oder aktivieren Sie das Feld 'Ich möchte alle Jahrbücher aus der gewählten Zeitspanne'.")
        elif (SelectPreviewPDF==""): 
            st.info("Wählen Sie zwischen 'Tabelle anzeigen' oder 'PDF-Dokument erstellen' aus.")
        else: 
            st.info("Selektieren Sie in der oberen Tabelle mindestens ein Jahrbuch oder aktivieren Sie das Feld 'Ich möchte alle Jahrbücher aus der gewählten Zeitspanne'.")
 
        
    def show_menu(self):

        df_metadata_filtered,jahrgang, jahrgang_box = self.get_tabelle() 

        #Wenn die spezifische Jahrbuchsuchfunktion nicht aktiviert ist:
        if jahrgang_box == False:
            st.markdown('<br><br>', unsafe_allow_html=True)
            st.subheader('__Liste der Tabellen__')
            st.markdown('''__Markieren Sie einen Tabellentitel, um zu sehen, 
            in welchen Jahrbüchern Daten vorhanden sind. Die Jahrbücher werden als interaktive Links angezeigt.__''')
            selected = tools.show_table(df_metadata_filtered, GridUpdateMode.SELECTION_CHANGED, 310, col_cfg=COL_CFG)
            if len(selected) > 0: 
                # col1, col2 = st.columns(2)
                #with col1:
                df_datenjahre_jahre = tools.make_dataframe(selected,self.positionsliste)
                #    self.show_jahrbuecher(selected[0],df_datenjahre_jahre)
                #with col2:
                self.show_preview_download_pdf(selected[0], df_datenjahre_jahre)

        #Wenn die spezifische Jahrbuchsuchfunktion aktiviert ist:
        else:
            st.markdown('<br><br>', unsafe_allow_html=True)
            self.show_jahrbuch(jahrgang)
            st.markdown('<br><br>', unsafe_allow_html=True)
            st.subheader('__Tabellenverzeichnis__')
            st.markdown('__Markieren Sie einen Tabellentitel, um zu sehen, in welchen Jahrbüchern diese Tabelle enthalten ist.__')          
            if jahrgang != 1980 | jahrgang !=1981:
                selected = tools.show_table(df_metadata_filtered[df_metadata_filtered[f"JB-{jahrgang}"].str.contains("x")==False], GridUpdateMode.SELECTION_CHANGED, 340, col_cfg=COL_CFG)
            else: 
                selected = tools.show_table(df_metadata_filtered[df_metadata_filtered[f"JB-1980/81"].str.contains("x")==False], GridUpdateMode.SELECTION_CHANGED, 340, col_cfg=COL_CFG)
            
            if len(selected) > 0: 
               df_datenjahre_jahre = tools.make_dataframe(selected,self.positionsliste)
               self.show_jahrbuecher(selected[0],df_datenjahre_jahre)
           
           
      
            
            