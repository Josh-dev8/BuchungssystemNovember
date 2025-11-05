# Buchungssystem November

Ein einfacher Prototyp für ein webbasiertes Buchungssystem eines Massagestudios. Die Anwendung nutzt Flask und eine SQLite-Datenbank (leichtgewichtiges SQL-System), um Massagekategorien und deren Behandlungen zu verwalten.

## Voraussetzungen

- Python 3.11 oder neuer (für andere Python-Versionen können kleinere Anpassungen nötig sein)
- Ein virtuelles Python-Umfeld wird empfohlen

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # unter Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py --init-db  # optional, siehe Hinweis unten
```

> **Hinweis:** Die Flask-Anwendung initialisiert die SQLite-Datenbank beim Start automatisch. Der manuelle Aufruf von `python app.py --init-db` setzt die Beispieldaten auf den Ausgangszustand zurück.

Der optionale Befehl erstellt die Datei `massage.db`, legt die benötigten Tabellen an und befüllt sie mit den Beispieldaten (Rückenmassage, Aromatherapie und Sportmassage mit unterschiedlichen Daueroptionen).

## Anwendung starten

```bash
flask --app app run
```

Die Anwendung steht danach unter <http://127.0.0.1:5000> zur Verfügung.

## Funktionsweise

- Nach dem Laden der Seite werden automatisch alle verfügbaren Kategorien aus der Datenbank geladen.
- Sobald eine Kategorie ausgewählt wird, erscheinen Buttons mit den verfügbaren Daueroptionen aus dieser Kategorie.
- Beim Klick auf einen Button erscheint eine einfache Bestätigungsnachricht. Dieser Schritt kann später durch eine echte Buchungslogik ersetzt werden.

## Weiterführende Ideen

- Benutzerverwaltung mit Login und Terminkalender
- Verwaltung freier Zeiten und Termine im Backend
- Automatisierte Bestätigungs-E-Mails
- Mehrsprachige Oberfläche
