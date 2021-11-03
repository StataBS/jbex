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
            text = """Sie haben noch keinen Filter eingegegeben, die untenstehende Liste enthält alle verfügbaren Jahrbuch-Tabellen. Verwenden sie obige Felder um die Auswahl 
            auf einen Themenbereich einzugrenzen oder suchen sie nach einem Ausdruck im Titel.
            """
            if f['themenbereich'] != []:
                liste_themenbereiche = ", ".join(f['themenbereich'])
            if f['titel'][0] > "":
                liste_titel = ", ".join(f['titel'])
            if (f['titel'][0] > "") & (f['themenbereich'] == []):
                if len(f['titel']) > 1:
                    text = f"""Die untenstehende Liste enthält alle Tabellen welche die Ausdrücke **_{liste_titel}_** im Titel enthalten. """
                else:
                    text = f"""Die untenstehende Liste enthält alle Tabellen, welche den Ausdruck **_{liste_titel}_** im Titel enthalten. """
            
            elif (f['titel'][0] == "") & (f['themenbereich'] != []):
                if len(f['themenbereich']) > 1:
                 text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche **_{liste_themenbereiche}_**. """
                else:
                 text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs **_{liste_themenbereiche}_**. """ 
              
            elif (f['titel'][0] > "") & (f['themenbereich'] != []):
                if (len(f['themenbereich']) > 1) & (len(f['titel']) > 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche **_{liste_themenbereiche}_**, welche auch die Ausdrücke **_{liste_titel}_** im Titel enthalten."""
                elif (len(f['themenbereich']) > 1) & (len(f['titel']) == 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen der Themenbereiche **_{liste_themenbereiche}_**, welche auch den Ausdruck **_{liste_titel}_** im Titel enthält."""
                elif (len(f['themenbereich']) == 1) & (len(f['titel']) > 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs **_{liste_themenbereiche}_**, welche auch die Ausdrücke **_{liste_titel}_** im Titel enthalten."""
                elif (len(f['themenbereich']) == 1) & (len(f['titel']) == 1):
                    text = f"""Die untenstehende Liste enthält alle Tabellen des Themenbereichs **_{liste_themenbereiche}_**, welche auch den Ausdruck **_{liste_titel}_** im Titel enthält."""

            text += f' \n \n **Beim Selektieren eines Eintrags aus der Liste mit Tabellen werden alle Jahrbücher, welche die ausgewählte Tabelle enthalten, als interaktive Links angezeigt.**'
            return text
        
        #Generieren eines Dictionary für die Speicherung der Suchparameter
        f = {}
        f['thema']=[]
        f['jahrgang'] = 0
        f['titel'] = []

        #Eingabefenster für die Suchparameter.
        col1,col2 = st.columns([3,1])
        with col1:
            #Suchparameter: Textinput
            textinput = st.text_input("🔎 Titel der Tabelle enthält:")
            f['titel'] = tools.list_suchwoerter(textinput)
            #Suchparameter: Themenbereiche
            f['themenbereich'] = st.multiselect('🔎 Themenbereich:',  options=THEMENBEREICHE)
            #Suchparameter: Zu jedem Themenbereich werden die Themen angezeigt.
            ad_search=st.checkbox("Erweiterte Suchfunktion zu den Themenbereichen:")
            themen=[]
            for i in f['themenbereich']:  
                themen.extend(THEMEN.get(i))
            if ad_search:
                f['thema'] = st.multiselect('🔎 Thema:',  options=themen, help="Wählen Sie immer zuerst einen Themenbereich aus." )
        with col2:
            #Suchparameter: Einzelnes Jahrbuch
            st.markdown('##')
            jahrgang_box=st.checkbox(f'Jahrbuch auswählen:', key='check2')
            if jahrgang_box:  
                f['jahrgang']=st.number_input(f'Jahrbuch zwischen 1921 und {CURRENT_YEAR-1}',max_value=(CURRENT_YEAR-1), min_value=1921, help="""Es gibt kein Jahrbuch für das 
                Jahr 1980.""")
            
        
        #Daten werden nach den Suchparametern gefiltert.
        self.get_filtered_tabs(f)

        #Angaben zum Filter auf der Seite anzeigen lassen .
        st.markdown(get_filter_description())
        st.subheader('Liste der Tabellen')
        return [self.metadata_filtered, f['jahrgang'], jahrgang_box]
        

    def show_jahrbuecher(self, tabelle, df):
        #Liste aus Hyperlink mit allen Jahrbücher erstellen, sowie Informationen zu Daten und Themenbereich ausgeben.
        st.markdown('### Jahrbücher')
        jb_von = int(tabelle['Daten-Start'])
        jb_bis = CURRENT_YEAR -1 if tabelle['Daten-Ende'] == 'nan' else int(tabelle['Daten-Ende'])
        text = f"""Die Tabelle **_{str(tabelle['Titel'])}_** wird in **_{len(df)}_** verschiedenen Jahrbüchern geführt. 
        Die ältesten Daten von dieser Tabelle stammen aus dem Jahr **_{jb_von}_**; die jüngsten Daten aus dem Jahr **_{jb_bis}_**. 
        \n \n Klicken Sie auf den Link um die PDF-Datei zu öffnen:"""
        st.markdown(text)
        liste = ''
        for jahr in df['Jahrbuecher']:
            url = f"{URL_BASE}{jahr}.pdf"
            name = f'Statistisches Jahrbuch des Kantons Basel-Stadt {jahr}'
            liste += f"- [{name}]({url}) \n"
        st.markdown(liste)

    def show_jahrbuch(self,jahr):
        #Liste aus Hyperlink mit einem Jahrbuch erstellen.
        if jahr == 1980:
            return
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
            selected = tools.show_table(metadata_filtered, GridUpdateMode.SELECTION_CHANGED, 300)
            if len(selected) > 0:
                df_selected = tools.make_dataframe(selected)
                self.show_jahrbuecher(selected[0],df_selected)
        else:
            self.show_jahrbuch(jahrgang)
        


        
    
