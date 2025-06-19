import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt


# Daten laden
dateiname = "lab_2.csv"
df = pd.read_csv(dateiname, encoding="latin1", sep=';')

#print(df.head())  # Ausgabe der ersten Zeilen zur Überprüfung
#print(df.describe())  # Statistische Zusammenfassung der Daten


# Daten extrahieren
frequenz = df["hz"]
spalte_db = df["dB"]
#spalte_db = -df["db"].abs()  # Amplitude negativieren, wie üblich bei Bode-Diagrammen
#spalte_phase = df["gradv"]
#print(df["g"][0].dtype)
spalte_phase = -df["grad"]  # Phase negativieren, wie üblich bei Bode-Diagrammen

# Plot erstellen
fig, ax1 = plt.subplots(figsize=(8, 5))

# Linke Y-Achse (Amplitude in dB)
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]', color='blue')
line1 = ax1.semilogx(frequenz, spalte_db, color='blue', label='Amplitude [dB]') # marker='o')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

# dB-Achse invertieren (nach unten laufend)
ax1.invert_yaxis()

# X-Achse – saubere Ticks mit ganzzahligen Labels
ax1.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, 2.0, 5.0), numticks=10))
ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

amplitude_ticks = [0, -3, -10, -20, -30, -40, -50, -60, -70, -80, -90, -100]
tick_labels = [str(int(t)) for t in amplitude_ticks]

# Set the major tick locations
ax1.yaxis.set_major_locator(ticker.FixedLocator(amplitude_ticks))



# Rechte Y-Achse (Phase in Grad)
ax2 = ax1.twinx()
ax2.set_ylabel('Phase [°]', color='red')
line2 = ax2.semilogx(frequenz, spalte_phase, color='red', label='Phase [°]') #marker='s')
ax2.tick_params(axis='y', labelcolor='red')



# Assuming you have a figure and axes setup
# fig, ax2 = plt.subplots()

tick_locations = [0, -20, -40, -60, -80, -100]
tick_labels = [str(int(t)) for t in tick_locations]

ax2.yaxis.set_major_locator(ticker.FixedLocator(tick_locations))
ax2.yaxis.set_major_formatter(ticker.FixedFormatter(tick_labels))

# Legende
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right')


xticks = [10, 100, 1000, 10000]
ax1.set_xlim([10, 10000])
ax1.set_xticks(xticks)
ax1.set_xticklabels([str(t) for t in xticks])

# Titel & Layout
#plt.title("Bode-Diagramm – RC-Tiefpass 1. Ordnung (Messung)", fontsize=12)
plt.tight_layout()
plt.savefig("Bode_RC_2_Ordnung_Messung_lt.png", dpi=300)
plt.show()
