# Dokumentation Jahrbuch-App


## Zusammenfassung

Die nachfolgend beschriebene Webapplikation hat zum Zweck die digitalisierten [Jahrbüchern](https://www.statistik.bs.ch/zahlen/statistisches-jahrbuch/pdf-archiv.html) nach ihren Tabellen zu durchsuchen und sich ausgewählte Tabellen anzeigen zulassen oder ein PDF-Dokument mit den gewünschten Tabellen zu generieren. Der User kann aus 3 Einstiegspunkte auswählen:

1. Freitextsuche in den Tabellen-Titeln
2. Thematische Suche
3. Suche nach Jahrbuch-Ausgaben

## Akteure und Verantwortlichkeiten

NB: Umsetzung

## Installation

- Die gesamte App liegt auf dem github-Repo [jbex] <span style="color: red;">(Link)</span> und auf dem gitolite-Repo vor. Die App kann mit einer lokalen Entwicklungsumgebung gestartet werden. In dem README des git-Repo ist die Installation beschrieben.
- Die App läuft über [Heroku](https://jbex-stata-intern.herokuapp.com/).

## Python (streamlit)

- Die App wurde mit dem open-source app framework [streamlit](https://streamlit.io/) programmiert.
- Eine zentrale Funktion für die App hat das File `app.py` und `jbex_find`. Die Initierung der Metadaten und der App erfolgt im File `App.py`. Die Logik für die Suchfunktion, dem Anzeigen von Tabellen und dem Generieren von PDF-Dokumenten wird im File `jbex_find` definiert. Konstanten werden im File `const.py` definiert und Hilffunktionen für die App im File `tools.py`.

## Variablen

Die folgenden Variablen sind zentral im Code:

| Bezeichnung                                                                                | Variable              |
| :----------------------------------------------------------------------------------------- | :-------------------- |
| Dataframe mit den Seitenzahlen zu den einzelenen Tabellen pro Jahrbuch.                                                     | `positionsliste`      |
| Dataframe mit allen Metainformationen zu den einzelnen Tabellen.                                                       | `metadata`            |
| Alle Suchkriterien werden in der Variable f gespeichert.                                   | `f`                   |
| Alle Metainformationen zu der ausgewählten Tabelle.                                         | `selected`            |
| Dataframe mit den kombinierten Metainformationen und Seitenzahlen zu der ausgewählten Tabelle. | `df_datenjahre_jahre` | 
| Dataframe mit den  Metainformationen und Seitenzahlen nach der Filterung mit dem Slider. | `after_slider_df` |
| Dataframe mit den kombinierten Metainformationen und Seitenzahlen nach zweiter Auswahl der Tabellen. | `new_selected_df` |

---

Die Daten werden wie folgt prozessiert:
Der User wählt zwischen drei Einstiegspunkte aus.

1. Freitextsuche in den Tabellen-Titeln: Der Freitext wird prozessiert und gewisse Füllwörter (und, oder, usw.) entfernt. Alle Wörter werden in der Variable `f` als Liste gespeichert. Die Wörter werden mit den Tabellentiteln aus der Variable `metadata` verglichen. Bei allen Übereinstimmungen werden die Metadaten für die Filterung der Tabellen benützt. Die gefilterten Tabellen werden in einer Liste angezeigt. 

1. Thematische Suche: Nach der Auswahl des Themenbereich und Themas werden diese in der Variable `f`. Der Themenbereich werden mit den Tabellentiteln aus der Variable `metadata` verglichen. Die gefilterten Tabellen nach Themenbereich (und Thema) werden in einer Liste angezeigt. 

1. Suche nach Jahrbuch-Ausgaben: Nach der Auswahl eines spezifischen Jahrbuchs (nach Jahr) wird das ausgewählte Jahr in der Variable `f` gespeichert. Die in dieser Ausgabe vorhanden Tabellen werden in einer Tabelle angezeigt. 

Nach den Einstiegspunkten 1. und 2. folgt: 
1. Nach der Auswahl einer einzelnen Tabelle durch den User werden die Metadaten zu dieser Tabelle in der Variable `selected` gespeichert. Mit den Metadaten zur Tabelle aus der Variable `selected` wird die Seitenzahlen aus der Variable `positionsliste` herausgefiltert und eine kombiniertes Dataframe `df_datenjahre_jahre` mit alle Metadaten zu dieser Tabelle erstellt. 
1. Für die selektierte Tabelle erscheinen nun weitere Filtermöglichkeiten.
    1. Mit Hilfe eines Sliders kann die Zeitspanne der Publikationsjahre gefiltert werden. Das gefilterte Metadaten werden in der Variable `after_slider_df` gespeichert. Die beiden Variablen "Jahrbuecher" und "Datenjahre" werden in einer weiteren Liste dargestellt. 
    1. Durch Auswahl von einer oder mehrere Zeilen aus der Liste wird ein Dataframe `new_selected_df` mit allen Metadaten zu den selektierten Zeilen zusammengestellt. Mit einem Radiobutton besteht die Möglichkeit alle Zeilen auszuwählen.
    1. Nach der Auswahl der Datenjahre besteht die Möglichkeit sich die Tabellen anzeigen zu lassen, dabei wird ein neues PDF-Dokument zusammengestellt, im temp-Ordner gespeichert und in der App in einem iFrame angezeigt. Bei der Auswahl von mehr als zwei Zeilen wird immer ein PDF-Dokument mit den Tabellen aus dem ältesten und dem neusten Jahrbuch generiert und angezeigt. Die zweite Möglichkeit besteht darin, sich ein PDF-Dokument zum Herunterladen zu erstellen, dabei wird ein PDF-Dokument mit allen selektierten Tabellen erstellt und im temp-Ordner abgespeichert. 
    1. Nach dem Anzeigen oder Herunterladen werden alle Dokumente im temp-Ordner gelöscht.

Nach Einstiegspunkt 3. folgt: 
1. Nach der Auswahl einer einzelnen Tabelle durch den User werden die Metadaten zu dieser Tabelle in der Variable `selected` gespeichert. Mit den Metadaten zur Tabelle aus der Variable `selected` wird die Seitenzahlen aus der Variable `positionsliste` herausgefiltert und eine kombiniertes Dataframe `df_datenjahre_jahre` mit alle Daten zu dieser Tabelle erstellt. Die Links zu den Jahrbüchern werden danach mit Hilfe der Variablen `selected` und `df_datenjahre_jahre` generiert. 

## Wartungsarbeiten
1. ...

### Jährliche Wartungsarbeiten

1. Neues Metadaten-File und Positionsliste-File (csv) hinzufügen.

### Sporadische Wartungsarbeiten

1. Updates der Pakete (alle wichtigen Pakete sind in requirements.txt hinterlegt)

## Troubleshooting

1. ....
