import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker # Import für erweiterte Tick-Formatierung

# --- Daten laden ---
# Ersetzen Sie 'lab_2_2_ordnung.csv' durch den tatsächlichen Namen Ihrer Datendatei.
# Stellen Sie sicher, dass die Datei im selben Verzeichnis wie das Skript liegt
# oder geben Sie den vollständigen Pfad zur Datei an.
# Der Parameter 'encoding="latin1"' und 'sep=';'' wird beibehalten, da Sie ihn verwendet haben.
try:
    dateiname = "lab_2_2_ordnung.csv"
    df = pd.read_csv(dateiname, encoding="latin1", sep=';')

    # --- Daten extrahieren ---
    # Behalten die Spaltennamen bei, die Sie in Ihrem Beispiel verwendet haben.
    frequenz = df["Hz"]
    spalte_db = df["Vin"]
    # spalte_db = -df["db"].abs() # Diese Zeile ist auskommentiert, da Sie 'dB' verwenden.
    #spalte_phase = -df["g"]  # Phase negativieren, wie üblich bei Bode-Diagrammen

    # --- Plot erstellen (eine einzige Figur mit zwei Y-Achsen) ---
    fig, ax1 = plt.subplots(figsize=(8, 5)) # Passt die Figurengröße an

    # --- Linke Y-Achse (Amplitude in dB) ---
    ax1.set_xlabel('Frequenz [Hz]')
    ax1.set_ylabel('Eingangsstrom in mV', color='blue')
    # semilogx für logarithmische X-Achse; marker für Datenpunkte
    line1 = ax1.semilogx(frequenz, spalte_db, color='blue', label='Amplitude [dB]', marker='o')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5) # Raster für bessere Lesbarkeit

    # dB-Achse invertieren (nach unten laufend), wie im Bode-Diagramm üblich
    #ax1.invert_yaxis()

    # --- X-Achse – saubere Ticks mit ganzzahligen Labels ---
    # LogLocator und FormatStrFormatter für schönere logarithmische Skala-Ticks
    ax1.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, 2.0, 5.0), numticks=10))
    ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

    # Festlegen und Beschriften der Y-Ticks für Amplitude
    #amplitude_ticks_values = [0, -3, -10, -20, -30, -40, -50, -60, -70, -80, -90, -100]
    # Wichtig: Sie müssen die Ticks auf der Achse setzen, bevor Sie die Labels invertieren.
    # Wenn Sie invert_yaxis() aufrufen, werden die internen Werte entsprechend angepasst.
    # Hier werden die positiven Entsprechungen gesetzt, da die Achse invertiert wird.
    #ax1.set_yticks([abs(t) for t in amplitude_ticks_values])
    #ax1.set_yticklabels([str(int(t)) for t in amplitude_ticks_values])



    # --- Legende ---
    # Kombiniert die Linien beider Achsen für eine gemeinsame Legende
    lines = line1 
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower right')

    # --- X-Achsenbereich und Ticks festlegen ---
    xticks = [10, 100, 1000, 10000, 100000, 1000000]
    ax1.set_xlim([10, 1000000])
    ax1.set_xticks(xticks)
    ax1.set_xticklabels([str(t) for t in xticks])

    # --- Titel & Layout ---
    #plt.title("Bode-Diagramm – RC-Filter (Messung)", fontsize=14) # Angepasster Titel
    plt.tight_layout() # Passt das Layout an, um Überlappungen zu vermeiden
    plt.savefig("2_Ordnung_veränderung_strom.png", dpi=300) # Speichert den Plot als Bild
    plt.show() # Zeigt den Plot an
except:
    print("Fehler beim Laden der Datei oder beim Erstellen des Plots. Stellen Sie sicher, dass die Datei existiert und korrekt formatiert ist.")
