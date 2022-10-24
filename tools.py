from pickle import TRUE
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import re
from const import *
import numpy as np
import fitz
import os
import requests
import time
import base64


def get_table(tbl_dic: dict) -> str:
    result = '<table>'
    for key, value in tbl_dic.items():
        result += f'<tr><td>{key}</td><td>{value}</td><tr>'

    result += '</table>'
    return result


def get_href(tit, url):
    result = f'<a href = "{url}" target = "_blank">{tit}</a>'
    return result


def right(text, amount):
    return text[-amount:]


def left(text, amount):
    return text[:amount]


def get_list_index(lst: list, value):
    try: 
        result = lst.index(value)
    except:
        result = 0
    return result


def make_dic(df: pd.DataFrame, key_col: str, value_col: str):
    keys = df[key_col]
    values = df[value_col]
    result = dict(zip(keys, values))
    return result


#DataFrame für Auflistung der Jahrbücher und Erstellen des PDF-Dokumentes
def make_dataframe(selected: list, df1: pd.DataFrame ):
    listval = []
    listkeys = []
    listepos =[]

    listval = list(selected[0].values())[6:]
    listkeys = [re.sub("\D","",x) for x in list(selected[0].keys())[6:]]
    for i, val in enumerate(listkeys):
                    listkeys[i] = int(val)
                    if val == "198081":
                        listkeys[i] = 1981
    df = pd.DataFrame(data=[listkeys,listval]).transpose()
    df.columns=['Jahrbuecher','Datenjahre']


    #Positionsliste der gewählten Tabelle umwandeln
    if all(df1['Kürzel']!=selected[0]['Kürzel']):
        zeros = pd.Series(data=np.zeros(len(df['Datenjahre']),dtype="int"),name='Position')
        df=df.join(zeros)
        df_selected = df[df['Datenjahre'].str.contains("x")==False]
        return df_selected
    else:
        df_pos = df1[df1['Kürzel']==selected[0]['Kürzel']].transpose()[4:]
        df_pos.columns=["Position"]
    #Datenjahre der gewählten Tabelle umwandeln
        for x in df_pos.index:
            if x == "JB-1980/81":
                listepos.append(int(1981))
            else:
                listepos.append(int(re.sub("\D","",x)))          
        df_pos['Jahrbuecher'] = listepos
    #Zusammenführen der Tabellen
        df = pd.merge(df,df_pos, on="Jahrbuecher", how="left")
        df_selected = df[df['Datenjahre'].str.contains("x")==False]
        df_selected = df_selected.copy()
        df_selected[['Position']]=df_selected[['Position']].astype('int64')
        return df_selected
    
    
#Hilffunktionen drei Suchparameter
def list_suchwoerter(textinput:str):
    wordlist = re.split(r'[\b\W\b]+',textinput)
    j=0
    while j <=4:
        wordlist = remove_smallwords(wordlist)
        for word in wordlist:
            for i in ["oder","und","der","die","das","den","diesen","dem","dieser", "nach"]:
                if word==i:
                    wordlist.pop(wordlist.index(word))
                else:
                    continue
        j +=1
    return wordlist


def remove_smallwords(wordlist):
    for word in wordlist: 
        if len(word)<3:
            wordlist.pop(wordlist.index(word))
        else:
            continue
    return wordlist


def sort_themenbereich():
    liste = THEMENBEREICHE.copy()
    liste.sort()
    return liste


#Tabelle erstellen
def show_table(df:pd.DataFrame, update_mode, height: int, col_cfg:list=[], sel_cfg: list=[], pag_cfg: list=[] ,autohight: bool=False):
    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=False, value=True, 
    enableRowGroup=False, editable=False,sorteable=False,filterable=False,resizable=True,cellStyle={'font-size': '12px'}, hide ="true")  
    if col_cfg != None:
        for col in col_cfg:
            gb.configure_column(field=col['name'],width=col['width'], tooltipField=col['name'],suppressSizeToFit=col['suppressSizeToFit'], hide=col['vis'])
    gb.configure_selection('single', use_checkbox=False, rowMultiSelectWithClick=False, suppressRowDeselection=True)
    if sel_cfg != []:
        for i in sel_cfg:
            gb.configure_selection(selection_mode=i["rowSelection"], rowMultiSelectWithClick=i["rowMultiSelectWithClick"])
    gb.configure_pagination(paginationAutoPageSize=True)
    if pag_cfg != []:
        for i in pag_cfg:
            gb.configure_pagination(enabled=i["enabled"])
    gb.configure_auto_height(autohight)
    gb.configure_grid_options(enableBrowserTooltips=True)
    gridOptions = gb.build()
    #Display the grid
    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        height=height,
        width= '100%', 
        theme='fresh',
        data_return_mode= DataReturnMode.FILTERED_AND_SORTED, 
        update_mode = update_mode,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        enable_enterprise_modules=False,
        )
    df_result = grid_response['data']
    selected = grid_response['selected_rows']
    return selected


#Neuer Teil für die Erstellung des PDF-Dokuments und Preview-Funktion

""" def open_doc(buch: str):
    doc = fitz.open(f"{JAHRBUCH_ORDNER}/Stat-JB-BS-{buch}.pdf")
    return doc """

def open_doc(buch: str):
    url=f"{URL_BASE}{buch}.pdf"
    response = requests.get(url)
    with open(f"{TEMP}temp{buch}.pdf", 'wb') as f:
        f.write(response.content)
    f.close()
    doc = fitz.open(f"{TEMP}temp{buch}.pdf")
    return doc 


def make_pdf(df, *args):
    doc2 = fitz.open()
    fontname_to_use = "Times-Roman"
    fontsize_to_use = 7
    for i in df.index:
        if pd.isna(df["Jahrbuecher"][i]):
            continue  
        else:
            pos=df["Position"][i]
            if pos == "nan":
                continue
            else:
                doc = open_doc(df["Jahrbuecher"][i])
                pos = int(float(pos)-1)
                page = doc[pos]
                if df["Jahrbuecher"][i] < 1995:
                    text = f'Jahrbuch-{df["Jahrbuecher"][i]}'
                    rect_x1 = 25
                    rect_x2 = 90  
                    rect_y1 = 5
                    rect_y2 = 19  
                    rect = (rect_x1, rect_y1, rect_x2, rect_y2)
                    rc = page.insert_textbox(rect, text,
                    fontsize=fontsize_to_use,
                    fontname=fontname_to_use,
                    color=(1,0,0))
                    doc2.insert_pdf(doc, from_page=pos,to_page=(int(pos+args[0])))
                else: 
                    doc2.insert_pdf(doc, from_page=pos,to_page=(int(pos+args[0])))
                doc.close()
                delete_jahrbuch(df["Jahrbuecher"][i])        
    doc2.save(f"{TEMP}temp.pdf",deflate=True,expand=True)
    doc2.close()
    return f"{TEMP}temp.pdf"



def open_pdf_base64(df, *args): 
    pdf = make_pdf(df,args[0]) 
    with open(pdf, "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    return base64_pdf



def spinner(df2, *args): 
    def open_pdf(df: pd.DataFrame, *args):
        with open(make_pdf(df,args[0]), "rb") as pdf_file:
            binary_pdf = pdf_file.read()
            return binary_pdf
    with st.spinner("Bitte haben Sie etwas Geduld. Zusammenstellung läuft..."):
        return open_pdf(df2, args[0])


def delete_temp():
    for f in os.listdir(TEMP):
        os.remove(os.path.join(TEMP,f))
    return


def delete_jahrbuch(jahr):
    path = os.path.join(TEMP, f"temp{jahr}.pdf")
    os.remove(path)
    return

def clickhandle():
            delete_temp()
            st.legacy_caching.clear_cache()
            del st.session_state["selectbox_switch"]
            del st.session_state["Check_years"]
            st.session_state["Check_years"] = False
            st.session_state["selectbox_switch"]=""


#Tabellen für die Selektion der Jahrbücher
def selected_dataframe(after_slider_df,new_selected_table):
        liste = []
        def map_function(val): 
            for key, dic in enumerate(new_selected_table): 
                liste.append(dic["Jahrbuecher"])
            if val in liste:
                return True
            else:
                return False
        new_ranged_df = after_slider_df.loc[list(map(map_function,after_slider_df["Jahrbuecher"]))] 
        return new_ranged_df

#Funtionen für die Erstellung des Preview.
def show_preview(df, *args):
    pdf = open_pdf_base64(df,args[0])
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf}" width="100%" height="930px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def text_preview(new_selected_df):
        if new_selected_df.shape[0]==1:
            text = f"""Es wird die Tabelle aus dem Jahrbuch {new_selected_df["Jahrbuecher"].iat[0]} angezeigt"""
        else:
            text = f"""Es werden die Tabellen aus den Jahrbüchern {new_selected_df["Jahrbuecher"].iat[0]} und {new_selected_df["Jahrbuecher"].iat[-1]} angezeigt"""
        return text


def checkbox_disable_func(checkbox_allyears, new_selected_df):
    if (checkbox_allyears==False and new_selected_df.empty):  
        return True
    else:
        return False
