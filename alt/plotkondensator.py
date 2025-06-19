import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Hier musst du den korrekten Pfad zu deiner CSV-Datei angeben
file_path = 'weg_kondensator.csv'

try:
    # Lese die CSV-Datei in ein Pandas DataFrame ein
    df = pd.read_csv(file_path)

    # Füge die neue Spalte 'xx' basierend auf 'x' hinzu
    # Dies ist deine transformierte Y-Achse
    df["xx"] =  1.15*df["x"]

    # Die Daten für den Plot
    # x_data ist df['y'] (Zeit in s)
    # y_data ist df['xx'] (Amplitude in V)
    x_data = df['y'].values
    y_data = df["xx"].values

    # Sicherstellen, dass die Daten für Interpolation aufsteigend sortiert sind
    # Dies ist wichtig für make_interp_spline
    sort_indices = np.argsort(x_data)
    x_data_sorted = x_data[sort_indices]
    y_data_sorted = y_data[sort_indices]

    # Erstelle eine viel feinere Reihe von X-Werten, um die Kurve glatt zu machen
    # Wir erstellen 500 Punkte zwischen dem Minimum und Maximum von x_data
    # Dies ist wichtig, damit der Spline "durchgezogen" aussieht
    x_new = np.linspace(x_data_sorted.min(), x_data_sorted.max(), 500)

    # Erstelle die Spline-Interpolation
    # k=3 für kubischen Spline (oft eine gute Wahl für glatte Kurven)
    # Beachte: k muss <= len(x_data_sorted) - 1 sein. Für sehr wenige Punkte,
    # könnte k=1 (linear) oder k=2 (quadratisch) besser sein.
    # Bei 'weg_kondensator.csv' gehe ich davon aus, dass genug Punkte vorhanden sind.
    if len(x_data_sorted) > 3: # Stelle sicher, dass genügend Punkte für k=3 vorhanden sind
        spl = make_interp_spline(x_data_sorted, y_data_sorted, k=3)
    else:
        # Fallback für zu wenige Punkte, z.B. lineare Interpolation
        spl = make_interp_spline(x_data_sorted, y_data_sorted, k=1)


    # Berechne die Y-Werte für die neuen X-Werte, um die glatte Kurve zu erhalten
    y_smooth = spl(x_new)

    # Erstelle den Plot
    plt.figure(figsize=(10, 6)) # Optional: Größe des Plots anpassen

    # Originalpunkte als Scatter-Plot hinzufügen (optional, zur Visualisierung)
    #plt.scatter(x_data, y_data, color='blue', label='Originalpunkte', alpha=0.6)

    # Glatte Kurve plotten
    plt.plot(x_new, y_smooth, color='red', linestyle='-', label='Geglättete Kurve')

    # Beschriftungen und Titel
    plt.xlabel('Zeit in s')
    plt.ylabel('Amplitude in V')
    #plt.title('Geglättete Kurve der Amplitude über die Zeit')
    plt.grid(True) # Optional: Gitterlinien hinzufügen
    #plt.legend() # Zeigt die Legende mit den Labels an
    plt.tight_layout() # Passt das Layout an, um Überschneidungen zu vermeiden
    plt.savefig('kondensator_plot_spannuungsbereitstellung.png', dpi=300) # Speichert den Plot als PNG-Datei
    plt.show()

except FileNotFoundError:
    print(f"Fehler: Die Datei wurde nicht gefunden unter '{file_path}'. Bitte überprüfe den Pfad.")
except pd.errors.EmptyDataError:
    print("Fehler: Die CSV-Datei ist leer.")
except KeyError as e:
    print(f"Fehler: Eine benötigte Spalte wurde nicht gefunden: {e}. Bitte überprüfe die Spaltennamen in deiner CSV-Datei.")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")