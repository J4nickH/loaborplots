import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt


# Daten laden
dateiname = "messung1.ordnung.csv"
df = pd.read_csv(dateiname, encoding="latin1", sep=';')

frequenz = df["hz"]
spalte_db = df["dB"]
spalte_phase = -df["grad"]

fig, ax1 = plt.subplots(figsize=(8, 5))

# Linke Y-Achse (Amplitude in dB)
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]', color='blue')
line1 = ax1.semilogx(frequenz, spalte_db, color='blue', label='Amplitude [dB]', marker='o') # marker='o')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

# dB-Achse invertieren (nach unten laufend)
ax1.invert_yaxis()

# X-Achse – saubere Ticks mit ganzzahligen Labels
ax1.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, 2.0, 5.0), numticks=10))
ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

amplitude_ticks = [0, 3, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tick_labels = [str(int(t)) for t in amplitude_ticks]

# Set the major tick locations
ax1.set_yticks(amplitude_ticks)
ax1.set_yticklabels(tick_labels)


# Rechte Y-Achse (Phase in Grad)
ax2 = ax1.twinx()
ax2.set_ylabel('Phase [°]', color='red')
line2 = ax2.semilogx(frequenz, spalte_phase, color='red', label='Phase [°]', marker ='s') #marker='s')
ax2.tick_params(axis='y', labelcolor='red')



# Assuming you have a figure and axes setup
# fig, ax2 = plt.subplots()

tick_locations2 = [0, -20, -40, -60, -80, -100]
tick_labels2 = [str(int(t)) for t in tick_locations2]

ax2.set_yticks(tick_locations2)
ax2.set_yticklabels(tick_labels2)

# Legende
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right')


xticks = [1, 10, 100, 1000, 10000, 100000, 1000000]
ax1.set_xlim([1, 1000000])
ax1.set_xticks(xticks)
ax1.set_xticklabels([str(t) for t in xticks])

# Titel & Layout
#plt.title("Bode-Diagramm – RC-Tiefpass 1. Ordnung (Messung)", fontsize=12)
plt.tight_layout()
plt.savefig("Bode1.Ordnung_Messung_vergleich.png", dpi=300)
plt.show()