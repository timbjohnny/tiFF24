# Pac-Man von Thommy, Fabian und Tim
Pac-Man ist ein Arcade-Spiel aus dem 20. Jahrhundert, bei dem es darum geht, den höchsten score zu erreichen.
Dieses Projekt ist ein inoffizielles Remake des Klassikers, ausschließlich in Python mithilfe der Library Pygame entwickelt.

## Features
- Das Spiel an sich
- Ein Leaderboard
- Ein Level-Editor zur Erstellung eigener Level (Implementation manuell)

## Getting Started
Um das Spiel zu starten ist nichts nötig außer die Spieldateien und ggf. eine Installation von Pygame
- Um Pygame zu installieren: "pip install pygame" in den Terminal eingeben
- Spiel starten

## Level-Editor
Man kann den Level-Editor erreichen mittels der "L"-Taste auf dem Hauptmenü
Daraufhin kann man durch drücken der Tasten 0-9 verschiedene Elemente auswählen
- 0: "Nichts" - um platzierte Elemente zu löschen
- 1: Punkte - einsammelbare Objekte im Spiel um den Score zu erhöhen
- 2: Dünne Wand - durchlässig für die Geister, um aus dem Spawn-Bereich zu kommen. Für Pac-Man nicht durchlässig
- 3: Vertikale Dicke Wand - Grenzt das Spielfeld für Pac-Man und die Geister ein
- 4: Horizontale Dicke Wand - Grenzt das Spielfeld für Pac-Man und die Geister ein
- 5: Kurve (Oben Rechts) - Gleiche Funktionalität wie Wände, nur mit rundem touch
- 6: Kurve (Oben Links) - Gleiche Funktionalität wie Wände, nur mit rundem touch
- 7: Kurve (Unten Links) - Gleiche Funktionalität wie Wände, nur mit rundem touch
- 8: Kurve (Unten Rechts) - Gleiche Funktionalität wie Wände, nur mit rundem touch
- 9: Power-Up - versetzt Geister in ängstlichen Zustand, soblad Pac-Man das Item isst. Zudem kann er auch die Geister essen, welche dann in ihren Spawn zurückkehren

Welches Element momentan ausgewählt ist, sieht man in der unteren linken Ecke.

Sobald das Level fertig kann man dieses mit der "S"-Taste speichern. Gespeichert wird das Level dann im Root-Verzeichnis, in welchem auch die main.py gespeichert ist, unter dem namen "custom-level.json".
Diese Datei enthält den Aufbau für das Level, in einem für das Programm verständlichem Format, sowie auch die Zeilen- und Reihenzahl.
Möchte man an einem Level später weiterarbeiten, so kann man dies tun indem man die "L"-Taste drückt um das vorher gespeicherte Level zu laden.

### Ein fertiges Level ins Spiel implementieren
