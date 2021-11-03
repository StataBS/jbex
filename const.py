from datetime import datetime, date


THEMENBEREICHE = [
'Bevölkerung',
'Raum, Landschaft, Umwelt',
'Arbeit und Erwerb',
'Volkswirtschaft',
'Preise',
'Industrie und Dienstleistungen',
'Land- und Forstwirtschaft',
'Energie',
'Bau- und Wohnungswesen',
'Tourismus',
'Verkehr',
'Finanzmärkte und Banken',
'Soziale Sicherheit',
'Gesundheit',
'Bildung und Wissenschaft',
'Kultur und Sport',
'Politik',
'Öffentliche Finanzen',
'Kriminalität und Strafrecht',
'Wirtschaftliche und soziale Situation der Bevölkerung',

]

TABELLEN_FILE = './data/metadaten.txt'
URL_BASE = 'https://charts.basleratlas.ch/zahlenspiegel/files/Stat-JB-BS-'


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

'Land- und Forstwirtschaft': ['Betriebe und Nutzfläche',
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

'Verkehr': ['Verkehrszählung',
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

'Kultur und Sport': ['Kultureinrichtungen',
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

JAHRBUECHER = list(range(1921,1980,1))+ list(range(1981,(date.today().year),1))