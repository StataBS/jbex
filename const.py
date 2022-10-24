from datetime import datetime, date


THEMENBEREICHE = [
'Bevölkerung',
'Raum, Landschaft, Umwelt',
'Arbeit und Erwerb',
'Volkswirtschaft',
'Preise',
'Industrie und Dienstleistungen',
'Landwirtschaft',
'Energie',
'Bau- und Wohnungswesen',
'Tourismus',
'Verkehr und Mobilität',
'Finanzmärkte und Banken',
'Soziale Sicherheit',
'Gesundheit',
'Bildung und Wissenschaft',
'Kultur, Sport, Freizeit',
'Politik',
'Öffentliche Finanzen',
'Kriminalität und Strafrecht',
'Wirtschaftliche und soziale Situation der Bevölkerung',
]

TABELLEN_FILE = './data/metadaten.txt'
POSITIONSLISTEN_FILE = './data/positionsliste.txt'
TEMP = './temp/'
URL_BASE = 'https://charts.basleratlas.ch/zahlenspiegel/files/Stat-JB-BS-'
URL_STAT_BASEL = 'https://www.statistik.bs.ch/'
JAHRBUCH_ORDNER = 'P:/1_Arbeitsbereiche/5_Publikationen/4_Jahrbuch\PDF-Archiv'

THEMEN = {
'Bevölkerung': ['Übergeordnete Bevölkerungsentwicklung',
'Bevölkerungsbestand und -struktur',
'Haushalte',
'Geburten und Todesfälle',
'Heiraten und Scheidungen',
'Räumliche Bevölkerungsbewegungen',
'Bürgerrechtswechel',
'Sprachen und Religionen'],

'Raum, Landschaft, Umwelt': ['Räumliche Gliederung und Bodennutzung',
'Rhein',
'Witterung',
'Wasserversorgung und Wasserverbrauch',
'Luftschadstoffe',
'Entsorgung'],

'Arbeit und Erwerb': ['Erwerbspersonen',
'Beschäftigte',
'Löhne',
'Arbeitslose',
'Ausländische Erwerbstätige',
'Unbezahlte Arbeit'],

'Volkswirtschaft': ['Volkseinkommen'],

'Preise': ['Basler Index der Konsumentenpreise (BIK)',
'Landesindex der Konsumentenpreise (LIK)',
'Detailhandelspreise'],

'Industrie und Dienstleistungen': ['Messen',
'Unternehmen',
'Betreibungen und Konkurse',
'Aussenhandel'],

'Landwirtschaft': ['Betriebe und Nutzfläche',
'Nutztierbestand'],

'Energie': ['Energieversorgung und -verbrauch'],

'Bau- und Wohnungswesen': ['Gebäude und Wohnungen',
'Leerstand',
'Mietpreise',
'Grundstückshandel',
'Gebäudeversicherung',
'Baukosten'],

'Tourismus': ['Hotels',
'Parahotellerie',
'Gastgewerbe'],

'Verkehr und Mobilität': ['Verkehrszählung',
'Motorfahrzeuge',
'Öffentlicher Verkehr',
'Luftverkehr',
'Rheinhäfen',
'Pendler',
'Mobilitätsverhalten',
'Strassenverkehrsunfälle',
'Nachrichtenverkehr',
'Strassenrechnung'],

'Finanzmärkte und Banken': ['Grundpfandbelastung',
'Banken'],

'Soziale Sicherheit': ['Sozialversicherungen',
'Sozialleistungen',
'Sozialhilfe',
'Versicherungen'],

'Gesundheit': ['Spitäler, Heime, Spitex',
'Sterblichkeit',
'Prävention, Praxen, Rettung'],

'Bildung und Wissenschaft': ['Schulen und Schulpersonal',
'Heim- und Sonderschulen',
'Berufsfachschulen',
'Hochschulen',
'Stipendien',
'Bildungsniveau',
'Bildungsabschlüsse'],

'Kultur, Sport, Freizeit': ['Kultureinrichtungen',
'Tierbestände',
'Sport und Freizeit',
'Rekrutierung und Berufsfeuerwehr'],

'Politik': ['Parteien',
'Abstimmungen',
'Wahlen'],

'Öffentliche Finanzen': ['Staatsrechnung',
'Steuern',
'Staatspersonal'],

'Kriminalität und Strafrecht': ['Rechtswesen',
'Polizei',
'Rückweisungen und Polizeidienstleistungen',
'Ordnungsbussen und Überweisungen'],

'Wirtschaftliche und soziale Situation der Bevölkerung': ['Justizvollzug',
'Opferhilfe und Rechtsmedizin',
'Haushaltsbudget',
'Grundversorgung'],
}



COL_CFG = [{"name":"Titel","width":400,"suppressSizeToFit":"false", "vis":"false"},
                    {"name":"Themenbereich","width":120,"suppressSizeToFit":"false", "vis":"false"},
                    {"name":"Thema","width":120,"suppressSizeToFit":"false", "vis":"false"}]

COL_CFG_2 =[{"name":"Jahrbuecher","width":100,"suppressSizeToFit":"false", "vis":"false"},{"name":"Datenjahre","width":100,"suppressSizeToFit":"false", "vis":"false"}]

CHANGE_STYLE_MULTI1 = '''
<style>
div.row-widget.stMultiSelect>div[data-baseweb="select"]>div>div>div:nth-child(2n+0){visibility: hidden;}
div.row-widget.stMultiSelect>div[data-baseweb="select"]>div>div>div:nth-child(2n+0)::before{content: "Option wählen"; visibility: visible;}
div.row-widget.stMultiSelect>div[data-baseweb="select"]>div>div:first-child{color:#e3e3e3;}
div.row-widget-stMultiSelect>div[data-baseweb="select"]
</style>'''


CHANGE_STYLE_ANLEITUNG =''' 
<style>
div.streamlit-expanderHeader{font-size: 16px}
</style>
'''

CHANGE_STYLE_CLEARBUTTON='''
<style> 
div.stButton>button:first-child{font-size: 9px;}
</style>'''

CHANGE_STYLE_DOWNLOADBUTTON='''
<style> 
div.stDownloadButton>button:first-child{font-size: 16px; background-color: #0A3B19; color: white}
</style>'''


CHANGE_STYLE_SLIDER = ''' 
<style> 
div.stSlider>div{width: 90%; padding-left: 15px}
div.stSlider>label{font-size: 16px}
div.StyledThumbValue{font-size:10px}
</style>
'''

CHANGE_STYLE_NUMBERINPUT = '''
<style> 
div.stNumberInput>label{width: 100%; font-size: 16px}
div.stNumberInput>div{width: 100%;}
</style>
'''
CHANGE_STYLE_CHECKBOX= '''
<style> 
div.row-widget.stCheckbox{margin-top: 28px}
</style>
'''

CHANGE_STYLE_SELECTBOX= '''
<style> 
div.row-widget>label{width: 100%; font-size: 16px}
div.row-widget.stSelectbox>div[data-baseweb="select"]>div{width: 100%;}
</style>
'''

