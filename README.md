# 🍅 Pomodoro Timer (pdoro)

Ein stilvolles, Terminal-basiertes **Pomodoro Timer** mit Live-Progress-Bar, farbiger Ausgabe und einfacher Bedienung.

Gebaut mit der [**Rich**](https://github.com/Textualize/rich) Bibliothek für eine wunderschöne Terminal-UI.

## Features

✨ **Hauptfunktionen:**
- 🎨 **Moderne Terminal-UI** mit eleganten Panels und Farben
- 📊 **Live Progress-Bar** mit animiertem Balken
- ⏱️ **Echtzeit Countdown** in MM:SS Format (läuft herunter)
- ⌨️ Jederzeit mit CTRL+C abbrechbar
- 🎯 Vordefinierte Sessions (work, break)
- 🛠️ Custom Sessions mit beliebigem Namen und Dauer
- � **Statistiken & Tracking** - Verfolge deine täglichen und gesamten Sessions
- �📝 Integrierte Help mit Beispielen
- 🔧 Einfache Automatische Installation mit Abhängigkeiten

## Installation

### Option 1: Automatische Installation ⭐ (Empfohlen)

```bash
cd /path/to/pdoro
python3 install.py
```

Das Skript:
- 📦 Installiert automatisch benötigte Abhängigkeiten (`rich`)
- 🔗 Erstellt einen ausführbaren Wrapper in `~/.local/bin/pdoro`
- 🌍 Macht pdoro überall verfügbar

### Option 2: Manuelle Installation

```bash
# Abhängigkeiten installieren
pip install rich

# pdoro.py copy zu ~/.local/bin/
cp pdoro.py ~/.local/bin/pdoro
chmod +x ~/.local/bin/pdoro

# Falls ~/.local/bin nicht in PATH ist, zu Shell-Config hinzufügen:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Anforderungen

- **Python 3.6+**
- **Linux/macOS/Windows** (mit Terminal)
- **Rich Bibliothek** (wird automatisch installiert)

## Verwendung

### Grundlegende Kommandos

```bash
# 45 Min Arbeitsphase starten
pdoro work

# 10 Min Pause starten
pdoro break

# Custom Session mit eigener Dauer
pdoro focus -d 90        # 90 Min Focus Session
pdoro gym -d 60          # 60 Min Gym Session

# Alle verfügbaren Sessions anzeigen
pdoro --list

# Statistiken anzeigen
pdoro --stats            # Zeige tägliche und gesamte Statistiken

# Hilfe anzeigen
pdoro -h
```

### Während einer Session

Die Ausgabe zeigt:
- 📦 Ein elegantes Panel mit der Session-Info
- 📊 Eine Live Progress-Bar mit Balkendarstellung
- ⏱️ Die verbleibende Zeit in MM:SS Format
- 🚀 Animierte Fortschrittsanzeige
- 📊 Deine Statistiken für heute (Sessions zu Anfang und Ende)

Beispiel während der Ausführung:
```
╭─────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│                              ☕  BREAK SESSION                               │
│                                                                              │
╰─────────────────────────────────────────────────────────────────────────────╯
📊 Heute: 2 Sessions (1 Arbeit, 1 Pause)
⏱️  Dauer: 3 Minuten
⚠️  Drücke CTRL+C zum Beenden

🚀 Sitzung läuft ╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 02:45
```

**CTRL+C** drücken um sofort zu beenden:
```
⏸  Session abgebrochen!
```

## Beispiele

### Beispiel 1: 45 Min Work-Session starten
```bash
$ pdoro work

╭─────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│                             💼  WORK SESSION                                │
│                                                                              │
╰─────────────────────────────────────────────────────────────────────────────╯
⏱️  Dauer: 45 Minuten
⚠️  Drücke CTRL+C zum Beenden

🚀 Sitzung läuft ╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42:15
```

### Beispiel 2: Custom 90-Minuten Session
```bash
$ pdoro focus -d 90

╭─────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│                            🚀  FOCUS SESSION                                │
│                                                                              │
╰─────────────────────────────────────────────────────────────────────────────╯
⏱️  Dauer: 90 Minuten
⚠️  Drücke CTRL+C zum Beenden

🚀 Sitzung läuft ╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 89:30
```

### Beispiel 3: Alle Sessions anzeigen
```bash
$ pdoro -l

Available Sessions:
  • work: 45 minutes 💼
  • break: 10 minutes ☕

```

### Beispiel 4: Nach Abschluss
```
╭─────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│             ✅  WORK SESSION ABGESCHLOSSEN!                                │
│                                                                              │
╰─────────────────────────────────────────────────────────────────────────────╯
🎉 Glückwunsch!

📊 Heute insgesamt: 3 Sessions (2 Arbeit, 1 Pause)
```

### Beispiel 5: Statistiken anzeigen
```bash
$ pdoro --stats

📊 Pomodoro Statistics
  2026-03-14
    Sessions: 3
    Work: 2
    Break: 1

  All Time
    Total Sessions: 42
    Work Sessions: 28
    Break Sessions: 14
```

## Vordefinierte Sessions

| Session | Dauer | Emoji |
|---------|-------|-------|
| `work`  | 45 Min | 💼 |
| `break` | 10 Min | ☕ |

## Optionen

```
usage: pdoro [-h] [-d MINUTES] [-l] [-s] SESSION

positional arguments:
  SESSION               Session type (work, break) oder beliebiger Sessionname

optional arguments:
  -h, --help            Zeigt diese Hilfemeldung an
  -d MINUTES, --duration MINUTES
                        Setzt custom Dauer in Minuten
  -l, --list            Zeigt alle verfügbaren Sessions an
  -s, --stats           Zeigt Statistiken für heute und alle Zeit
```

## Dateien

```
./
├── pdoro.py           # Hauptprogramm mit Rich UI
├── install.py         # Automatisches Installationsskript
└── README.md          # Diese Datei
```

## Architektur

### pdoro.py
Die Hauptanwendung mit folgenden Komponenten:

```python
class StatsManager:
    - load_stats()         # Lädt Statistiken aus Datei
    - save_stats()         # Speichert Statistiken
    - increment_session()  # Zählt Session hoch
    - get_today_stats()    # Gibt heute's Statistiken
    
class PomodorTimer:
    - SESSIONS: Dictionary mit vordefinierter Sessions
    - EMOJIS: Session-spezifische Emojis
    - console: Rich Console für schöne Ausgabe
    - stats_manager: StatsManager Instanz
    - Rich Panel: Elegante Rahmen um Session-Info
    - Rich Progress: Animierte Progress Bar mit Countdown
    
    def run()          # Führt eine Session aus
    def format_time()  # Formatiert Zeit MM:SS
    def main()         # Argument Parser und Einstiegspunkt
```

### install.py
Das Installationsskript:
- 🔍 Prüft auf benötigte Dateien
- 📦 Installiert automatisch `rich` Abhängigkeit
- 🔗 Erstellt einen ausführbaren Wrapper
- 🔐 Setzt korrekte Permissions
- ✅ Prüft PATH-Konfiguration

### Statistiken
Die Statistiken werden in `~/.local/share/pdoro/stats.json` gespeichert:
```json
{
  "total_sessions": 42,
  "work_sessions": 28,
  "break_sessions": 14,
  "daily": {
    "2026-03-14": {
      "total": 3,
      "work": 2,
      "break": 1
    }
  }
}
```

## Tipps & Tricks

### 1. Mit Systembenachrichtigungen arbeiten
```bash
# Nach Session notification senden (Linux)
pdoro work && notify-send "Pomodoro Timer" "Work session complete!"
```

### 2. Mehrere Sessions hintereinander
```bash
# Work + Break Zyklus
pdoro work && sleep 2 && pdoro break
```

### 3. Custom Durations schnell testen
```bash
# Nur 5 Min zum Testen
pdoro meeting -d 5
```

### 4. Als Alias hinzufügen
```bash
# .bashrc oder .zshrc
alias pomo='pdoro work'
alias pomodoro='pdoro'
```

## Fehlerbehebung

### pdoro: command not found
**Lösung:** Installationsskript nochmal ausführen oder PATH aktualisieren:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Timer läuft im Hintergrund weiter
**Lösung:** Mit CTRL+C beenden und warten, bis der Prozess sich beendet.

### Falsche Session-Dauer
**Lösung:** Mit `-d` Flag die Dauer explizit setzen:
```bash
pdoro work -d 30  # Override default 45 Min
```

## Entwicklung

### Struktur verstehen
- `PomodorTimer` Klasse handhabt Timer-Logik
- `argparse` für CLI-Argument Parsing
- `signal` für sauberes Beenden
- ANSI-Codes für Terminal-Styling

### Eigene Sessions hinzufügen
In `pdoro.py` die `SESSIONS` Dictionary erweitern:
```python
SESSIONS: Dict[str, int] = {
    "work": 45,
    "break": 10,
    "pomodoro": 25,    # Neue Session
    "long_break": 15,  # Neue Session
}
```

## Lizenz

Frei verwendbar und modifizierbar.

## Autor

Erstellt als Pomodoro Timer Projekt 🍅

---

**Viel Produktivität mit pdoro!** 🚀
