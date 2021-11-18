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
import app



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
            textinput = st.text_input("Wörter im Tabellentitel suchen:",key='text1', help='Nach einer Eingabe muss man mit der Eingabetaste bestätigen.')
            f['titel'] = tools.list_suchwoerter(textinput)   
        st.markdown('#')
        
        #Suchparameter: Themenbereiche und die Themen .
        placeholder_themenbereich = st.empty()
        with placeholder_themenbereich.container():
            st.write("🔎 Themenbereich auswählen:")
            col1, col2=st.columns(2)
            with col1: 
                f['themenbereich'] = st.multiselect(label='Themenbereich:',options=tools.sort_themenbereich(), key='multi1')
            with col2:
                themen=[]
                for i in f['themenbereich']:  
                    themen.extend(THEMEN.get(i))
                    themen.sort()
                f['thema'] = st.multiselect(label='Thema (optional):' ,options=themen, help="Wählen Sie immer zuerst einen Themenbereich aus." )
        st.markdown('#')

        #Suchparameter: Einzelnes Jahrbuch
        placeholder_jahrgang = st.empty()
        with placeholder_jahrgang.container():
            jahrgang_box=st.checkbox("Eine spezifische Jahrbuch-Ausgabe auswählen.", key='check1')
        if jahrgang_box== True:
            f['jahrgang']=st.number_input(f'Jahrbuch zwischen 1921 und {CURRENT_YEAR-1}',max_value=(CURRENT_YEAR-1), min_value=1921, help="""Im Jahr 1981 ist eine
                Doppelausgabe aus den Jahren 1980/81 erschienen.""")    
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
            #Filtern der Tabellen nach Filterparameter
            self.get_filtered_tabs(f)
            if self.metadata_filtered.empty==False:
                st.markdown(get_filter_description(),unsafe_allow_html=True)
            else: 
                st.markdown(f'<p style="color:red"><b>Es konnte kein Suchergebnis gefunden werden.</b></p>',unsafe_allow_html=True)
        return [self.metadata_filtered, f['jahrgang'], jahrgang_box]
        

    def show_jahrbuecher(self, tabelle, df):
        #Liste aus Hyperlinks mit allen Jahrbücher erstellen, sowie Informationen zu Daten und Themenbereich ausgeben.
        st.markdown('### Jahrbücher')
        jb_von = int(tabelle['Daten-Start'])
        jb_bis = CURRENT_YEAR -1 if tabelle['Daten-Ende'] == 'nan' else int(tabelle['Daten-Ende'])
        text = f"""Die Tabelle __{str(tabelle['Titel'])}__ wird in __{len(df)}__ verschiedenen Jahrbüchern geführt. 
        Im Jahrbuch aus dem Jahr __{df['Jahrbuecher'].iloc[0]}__ findet man die ältesten Daten, welche aus dem Jahr __{jb_von}__ stammen. 
        Die jüngsten Daten findet man im Jahrbuch __{df.iat[-1,-1]}__; sie stammen aus dem Jahr __{jb_bis}__. 
        \n \n Klicken Sie auf den Link, um die PDF-Datei zu öffnen:"""
        st.markdown(text)
        liste = ''
        for jahr in df['Jahrbuecher']:  
            if jahr != 1981:
                url = f"{URL_BASE}{jahr}.pdf"
                name = f'Statistisches Jahrbuch des Kantons Basel-Stadt {jahr}'
                liste += f"- [{name}]({url}) \n"
            elif jahr == 1981:
                url = f"{URL_BASE}{jahr}.pdf"
                name = f'Statistisches Jahrbuch des Kantons Basel-Stadt 1980/81'
                liste += f"- [{name}]({url}) \n"
        st.markdown(liste)


    def show_jahrbuch(self,jahr):
        #Hyperlink mit einem Jahrbuch erstellen.
        if jahr == 1980 or jahr == 1981:
            st.markdown('### Jahrbücher')
            st.markdown(f"Sie können die Gesamtausgabe des __Jahrbuchs__ __1980/81__ als PDF-Datei herunterladen.")
            liste = ''
            url = f"{URL_BASE}1981.pdf"
            name = f'Statistisches Jahrbuch des Kantons Basel-Stadt 1980/81'
            liste += f"- [{name}]({url})"
            st.markdown(liste)
        else:
            st.markdown('### Jahrbücher')
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
        
    
    def show_menu(self):
        df_metadata_filtered,jahrgang, jahrgang_box = self.get_tabelle() 

        if jahrgang_box == False:
            st.markdown('##')
            st.subheader('Liste der Tabellen')
            st.markdown('**Markieren Sie einen Tabellentitel, um zu sehen, in welchen Jahrbüchern Daten vorhanden sind. Die Jahrbücher werden als interaktive Links angezeigt.**')
            selected = tools.show_table(df_metadata_filtered, GridUpdateMode.SELECTION_CHANGED, 310, col_cfg=COL_CFG)
            if len(selected) > 0:  
                df_datenjahre_jahre = tools.make_dataframe(selected)
                self.show_jahrbuecher(selected[0],df_datenjahre_jahre)    
        else:
            st.markdown('##')
            self.show_jahrbuch(jahrgang)
            st.markdown('##')
            st.subheader('Tabellenverzeichnis')
            st.markdown('**Markieren Sie einen Tabellentitel, um zu sehen, in welchen Jahrbüchern diese Tabelle enthalten ist.**')          
            if jahrgang != 1980 | jahrgang !=1981:
                selected = tools.show_table(df_metadata_filtered[df_metadata_filtered[f"JB-{jahrgang}"].str.contains("x")==False], GridUpdateMode.SELECTION_CHANGED, 340, col_cfg=col_cfg)
            else: 
                selected = tools.show_table(df_metadata_filtered[df_metadata_filtered[f"JB-1980/81"].str.contains("x")==False], GridUpdateMode.SELECTION_CHANGED, 340, col_cfg=col_cfg)
            
            if len(selected) > 0: 
               df_datenjahre_jahre = tools.make_dataframe(selected)
               self.show_jahrbuecher(selected[0],df_datenjahre_jahre)
           
           
      
            
            
           

        


        
    
