"""
Diese App erlaubt das Browsen von Jahrbüchern

Kontakt: lukas.calmbach@bs.ch
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


CURRENT_YEAR = date.today().year
class App():
    def __init__(self, metadata):
        self.record = {}
        self.metadata_df = metadata
        self.metadata_filtered = self.metadata_df

    
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
            text =f'''<span style="color:red">__Sie haben noch keinen Filter eingegegeben, die untenstehende Liste enthält alle verfügbaren Jahrbuch-Tabellen. 
            Verwenden sie obige Felder um die Auswahl auf einen Themenbereich einzugrenzen oder suchen sie nach Wörtern im Titel der Tabelle.__</span>'''
            if f['themenbereich'] != []:
                liste_themenbereiche = ", ".join(f['themenbereich'])
            if f['titel']!=[]:
                for i, wort in enumerate(f['titel']):
                    f['titel'][i]=wort.capitalize()
                liste_titel = ", ".join(f['titel'])
            if (f['titel']!=[]) & (f['themenbereich'] == []):
                if len(f['titel']) > 1:
                    text = f"""Die untenstehende Liste enthält alle Tabellen welche die Ausdrücke **_{liste_titel}_** im Titel enthalten. """
                else:
                    text = f"""Die untenstehende Liste enthält alle Tabellen, welche den Ausdruck **_{liste_titel}_** im Titel enthalten. """
            
            elif (f['titel']==[]) & (f['themenbereich'] != []):
                if len(f['themenbereich']) > 1:
                 text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche **_{liste_themenbereiche}_**. """
                else:
                 text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs **_{liste_themenbereiche}_**. """ 
              
            elif (f['titel']!=[]) & (f['themenbereich'] != []):
                if (len(f['themenbereich']) > 1) & (len(f['titel']) > 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche **_{liste_themenbereiche}_**, welche auch die Ausdrücke **_{liste_titel}_** im Titel enthalten."""
                elif (len(f['themenbereich']) > 1) & (len(f['titel']) == 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche **_{liste_themenbereiche}_**, welche auch den Ausdruck **_{liste_titel}_** im Titel enthält."""
                elif (len(f['themenbereich']) == 1) & (len(f['titel']) > 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs **_{liste_themenbereiche}_**, welche auch die Ausdrücke **_{liste_titel}_** im Titel enthalten."""
                elif (len(f['themenbereich']) == 1) & (len(f['titel']) == 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs **_{liste_themenbereiche}_**, welche auch den Ausdruck **_{liste_titel}_** im Titel enthält."""

            return text
        
        #Generieren eines Dictionary für die Speicherung der Suchparameter
        f = {}
        f['themenbereich']=[]
        f['thema']=[]
        f['jahrgang'] = 0
        f['titel'] = []

        #Eingabefenster für die Suchparameter.
        
        #Suchparameter: Einzelnes Jahrbuch
        placeholder_jahrgang = st.empty()
        with placeholder_jahrgang.container():
            st.write("🔎 Suchen sie nach einem spezifischen Jahrbuch?")
            jahrgang_box=st.checkbox("Nach einem spezifischen Jahrbuch suchen.", key='check1')
        if jahrgang_box== True:
            f['jahrgang']=st.number_input(f'Jahrbuch zwischen 1921 und {CURRENT_YEAR-1}',max_value=(CURRENT_YEAR-1), min_value=1921, help="""Im Jahr 1981 ist eine
                Doppelausgabe aus den Jahren 1980/81 erschienen.""")    
        st.markdown('#')
    
        
        #Suchparameter: Textinput
        placeholder_text = st.empty()
        with placeholder_text.container():
            st.write("🔎 Suchen sie nach Daten mit spezifischen Wörtern im Tabellentitel, dann benützen Sie folgende Suchfunktionen.")
            textinput = st.text_input("Nach Wörter im Tabellentitel suchen:",key='text1', help='Nach einer Eingabe oder Änderung muss man mit der Eingabetaste bestätigen.')
            f['titel'] = tools.list_suchwoerter(textinput)
            
        st.markdown('#')
        
        #Suchparameter: Themenbereiche und die Themen .
        placeholder_themenbereich = st.empty()
        with placeholder_themenbereich.container():
            st.write("🔎 Suchen sie nach Daten zu einem Themenbereich und Thema, dann benützen Sie folgende Suchfunktionen.")     
            f['themenbereich'] = st.multiselect('Nach Themenbereich suchen:',options=THEMENBEREICHE, key='multi1')
            themen=[]
            for i in f['themenbereich']:  
                themen.extend(THEMEN.get(i))
            f['thema'] = st.multiselect(label='Nach Thema suchen:' ,options=themen, help="Wählen Sie immer zuerst einen Themenbereich aus." )
        st.markdown('#')

        if f['titel']!=[]:
            placeholder_jahrgang.empty()
            placeholder_themenbereich.empty()
            f['themenbereich'].clear()
        if jahrgang_box== True:
            placeholder_themenbereich.empty()
            placeholder_text.empty()
        if f['themenbereich']!=[]:
            placeholder_jahrgang.empty()
            placeholder_text.empty()
        if jahrgang_box == False:
            self.get_filtered_tabs(f)
            if self.metadata_filtered.empty==False:
                st.markdown(get_filter_description(),unsafe_allow_html=True)
            else: 
                st.markdown(f'<span style="color:red">__Es konnte kein Suchergebnis gefunden werden.__</span>',unsafe_allow_html=True)
    
        return [self.metadata_filtered, f['jahrgang'], jahrgang_box]
        

    def show_jahrbuecher(self, tabelle, df):
        #Liste aus Hyperlink mit allen Jahrbücher erstellen, sowie Informationen zu Daten und Themenbereich ausgeben.
        st.markdown('### Jahrbücher')
        jb_von = int(tabelle['Daten-Start'])
        jb_bis = CURRENT_YEAR -1 if tabelle['Daten-Ende'] == 'nan' else int(tabelle['Daten-Ende'])
        text = f"""Die Tabelle __{str(tabelle['Titel'])}__ wird in __{len(df)}__ verschiedenen Jahrbüchern geführt. 
        Im Jahrbuch aus dem Jahr __{df['Jahrbuecher'].iloc[0]}__ findet man die ältesten Daten, welche aus dem Jahr __{jb_von}__ stammen. 
        Die jüngsten Daten findet man im Jahrbuch __{df.iat[-1,-1]}__ und sie stammen aus dem Jahr __{jb_bis}__. 
        \n \n Klicken Sie auf den Link, um die PDF-Datei zu öffnen:"""
        st.markdown(text)
        liste = ''
        for jahr in df['Jahrbuecher']:
            url = f"{URL_BASE}{jahr}.pdf"
            name = f'Statistisches Jahrbuch des Kantons Basel-Stadt {jahr}'
            liste += f"- [{name}]({url}) \n"
        st.markdown(liste)

    def show_jahrbuch(self,jahr):
        #Liste aus Hyperlink mit einem Jahrbuch erstellen.
        if jahr == 1980 or jahr == 1981:
            st.markdown('### Jahrbücher')
            liste = ''
            url = f"{URL_BASE}1981.pdf"
            name = f'Statistisches Jahrbuch des Kantons Basel-Stadt 1980/81'
            liste += f"- [{name}]({url})"
            st.markdown(liste)
        else:
            st.markdown('### Jahrbücher')
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
            name = f"**{df['Jahrbuecher'].iloc[i]}:**\t_{df['Values'].iloc[i]}_"
            liste += f"- {name} \n"   
        st.markdown(liste)
        
    
    def show_menu(self):
        metadata_filtered,jahrgang, jahrgang_box = self.get_tabelle()  
        if jahrgang_box == False:
            st.markdown('##')
            st.subheader('Liste der Tabellen')
            st.markdown('**Wählen Sie aus der Liste ein Titel aus. Nach der Auswahl  werden Ihnen alle alle Jahrbücher, welche diese Tabelle enthält,  als interaktive Links angezeigt.**')
            selected = tools.show_table(metadata_filtered, GridUpdateMode.SELECTION_CHANGED, 340)
            if len(selected) > 0:
                df_selected = tools.make_dataframe(selected)
                self.show_jahrbuecher(selected[0],df_selected)
            
        else:
            st.markdown('##')
            self.show_jahrbuch(jahrgang)
        


        
    
