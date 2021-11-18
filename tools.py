import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import re
import const


def get_table(tbl_dic: dict) -> str:
    result = '<table>'
    for key, value in tbl_dic.items():
        result += f'<tr><td>{key}</td><td>{value}</td><tr>'

    result += '</table>'
    return result


def get_list_index(lst: list, value):
    try: 
        result = lst.index(value)
    except:
        result = 0
    return result


def make_dataframe(selected: list ):
    listval = []
    listkeys = []
    listval = list(selected[0].values())[6:]
    listkeys = [re.sub("\D","",x) for x in list(selected[0].keys())[6:]]
    for i, val in enumerate(listkeys):
                    listkeys[i] = int(val)
                    if val == "198081":
                        listkeys[i] = 1981
    df = pd.DataFrame(data=[listval,listkeys]).transpose()
    df.columns=['Datenjahre', 'Jahrbuecher']
    df_selected= df[df['Datenjahre'].str.contains("x")==False]
    return df_selected


def make_dic(df: pd.DataFrame, key_col: str, value_col: str):
    keys = df[key_col]
    values = df[value_col]
    result = dict(zip(keys, values))
    return result


def get_href(tit, url):
    result = f'<a href = "{url}" target = "_blank">{tit}</a>'
    return result


def right(text, amount):
    return text[-amount:]


def left(text, amount):
    return text[:amount]


def show_table(df:pd.DataFrame, update_mode, height: int, col_cfg:list=[]):
    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df[["Titel","Themenbereich","Thema"]])

    gb.configure_default_column(groupable=False, value=True, enableRowGroup=False, editable=False,sorteable=False,filterable=False,resizable=True,cellStyle={'font-size': '12px'})
    
    if col_cfg != None:
        for col in col_cfg:
            gb.configure_column(field=col['name'],width=col['width'], tooltipField=col['name'],suppressSizeToFit=col['suppressSizeToFit'])


    gb.configure_selection('single', use_checkbox=False, rowMultiSelectWithClick=False, suppressRowDeselection=True)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_grid_options(domLayout='normal',enableBrowserTooltips=True)
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


def list_suchwoerter(textinput:str):
    wordlist = re.split(r'[\b\W\b]+',textinput)
    wordlist = remove_smallwords(wordlist)
    for word in wordlist:
        if word=="oder":
            wordlist.pop(wordlist.index(word))
        else:
            continue
    return wordlist


def remove_smallwords(wordlist):
    for word in wordlist: 
        if len(word)<=3:
            wordlist.pop(wordlist.index(word))
        else:
            continue
    return wordlist


def sort_themenbereich():
    liste = const.THEMENBEREICHE.copy()
    liste.sort()
    return liste








