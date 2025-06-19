import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Hier musst du den korrekten Pfad zu deiner CSV-Datei angeben
file_path = 'Tau Zeitkonstante RC einfach.csv'

try:
    # Lese die CSV-Datei in ein Pandas DataFrame ein
    df = pd.read_csv(file_path)

    # Füge die neue Spalte 'xx' basierend auf 'x' hinzu
    # Dies ist deine transformierte Y-Achse
    df["xx"] =  df["x"]*2

    # Die Daten für den Plot
    # x_data ist df['y'] (Zeit in s)
    # y_data ist df['xx'] (Amplitude in V)
    x_data = df['y'].values +340.0E-06
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
    if len(x_data_sorted) > 3:
        spl = make_interp_spline(x_data_sorted, y_data_sorted, k=3)
    else:
        spl = make_interp_spline(x_data_sorted, y_data_sorted, k=1)

    # Berechne die Y-Werte für die neuen X-Werte, um die glatte Kurve zu erhalten
    y_smooth = spl(x_new)

    # Erstelle den Plot
    plt.figure(figsize=(10, 6))

    # Glatte Kurve plotten
    plt.plot(x_new, y_smooth, color='blue', linestyle='-', label='Geglättete Kurve')

    # --- Hinzufügen der Linien ---

    # 1. Berechne den 63%-Wert der Amplitude
    min_amplitude = np.min(y_smooth)
    max_amplitude = np.max(y_smooth)
    # The 63% value for a charging RC circuit is typically 63% of the final voltage.
    # For a discharging circuit, it's 37% of the initial voltage (or 63% of the decay).
    # Assuming this is a charging curve starting from a lower value towards a higher value:
    amplitude_63_percent = min_amplitude + (max_amplitude - min_amplitude) * 0.63

    # 2. Zeichne die horizontale Linie bei 63% Amplitude
    plt.axhline(y=amplitude_63_percent, color='red', linestyle='--', label=f'63% Amplitude ({amplitude_63_percent:.2f} V)')

    # 3. Finde den ersten Schnittpunkt der geglätteten Kurve mit der 63%-Linie
    # Finde den Index des ersten Punktes, bei dem y_smooth den 63%-Wert überschreitet oder erreicht
    intersection_index = np.where(y_smooth >= amplitude_63_percent)[0]
    if len(intersection_index) > 0:
        first_intersection_x = x_new[intersection_index[0]]
        first_intersection_y = y_smooth[intersection_index[0]] # This should be close to amplitude_63_percent

        # 4. Zeichne die vertikale Linie vom Schnittpunkt zur x-Achse
        plt.axvline(x=first_intersection_x, color='green', linestyle=':', label=f'Schnittpunkt bei {first_intersection_x:.6f} s')
        # Optional: Einen Marker am Schnittpunkt setzen
        plt.plot(first_intersection_x, first_intersection_y, 'go') # Grüner Kreis am Schnittpunkt
    else:
        print("Hinweis: Die geglättete Kurve erreicht den 63%-Amplitude-Wert nicht im geplotteten Bereich.")


    # 5. Zeichne eine vertikale Linie bei x = 0 (oder dem Startwert deiner relevanten Zeit)
    # Basierend auf deiner x_data = df['y'].values + 340.0E-06, könnte 340.0E-06 der Startpunkt sein.
    # Wenn du eine Linie bei dem Minimum von x_new ziehen möchtest, das ist:
    zero_time_line_x = x_new.min()
    plt.axvline(x=zero_time_line_x, color='purple', linestyle=':', label=f'Startzeit (0) bei {zero_time_line_x:.6f} s')


    # Beschriftungen und Titel
    plt.xlabel('Zeit in s')
    plt.ylabel('Amplitude in V')
    #plt.title('Geglättete RC-Kurve mit Zeitkonstanten-Analyse')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('kondensator_plot_ladekurve.png', dpi=300)
    plt.show()

except FileNotFoundError:
    print(f"Fehler: Die Datei wurde nicht gefunden unter '{file_path}'. Bitte überprüfe den Pfad.")
except pd.errors.EmptyDataError:
    print("Fehler: Die CSV-Datei ist leer.")
except KeyError as e:
    print(f"Fehler: Eine benötigte Spalte wurde nicht gefunden: {e}. Bitte überprüfe die Spaltennamen in deiner CSV-Datei.")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")