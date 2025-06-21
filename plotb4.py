import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Daten laden
dateiname = "messung2lab4.csv"
df = pd.read_csv(dateiname, encoding="latin1", sep=',')

# Wichtig: Du hast 'dn = ""' und 'dp = pd.read_csv(dn, ...)' gelassen.
# Das wird einen Fehler verursachen, weil 'dn' leer ist.
# Du musst hier den korrekten Dateinamen für dein zweites CSV angeben, z.B.:
dateiname_dp = "mess2lab4high.csv" # <--- HIER DEINEN ZWEITEN DATEINAMEN EINFÜGEN!
dp = pd.read_csv(dateiname_dp, encoding="latin1", sep=',')


# Daten für df vorbereiten
frequenz_df = df["Hz"]
df['db'] = 20 * np.log10(df['amp'] / df['in'])
spalte_db_df = df["db"]
spalte_phase_df = df["phase"]

# Daten für dp vorbereiten
frequenz_dp = dp["Hzh"]
dp["dB"] = 20 * np.log10(dp["amph"] / dp["inh"])
spalte_db_dp = dp["dB"]
spalte_phase_dp = dp["phaseh"]

fig, ax1 = plt.subplots(figsize=(8, 5))

# Linke Y-Achse (Amplitude in dB)
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Amplitude [dB]', color='blue')

# Plot für df (Amplitude)
line1_df = ax1.semilogx(frequenz_df, spalte_db_df, color='blue', label='Amplitude (Messung 1) [dB]', marker='o')

# Plot für dp (Amplitude) - Farbe oder Marker anpassen, um sie zu unterscheiden
line1_dp = ax1.semilogx(frequenz_dp, spalte_db_dp, label='_nolegend_', color='blue', marker='o')


ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

# X-Achse – saubere Ticks mit ganzzahligen Labels
ax1.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, 2.0, 5.0), numticks=10))
ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

amplitude_ticks = [10, 0, -10, -20, -30, -40, -50, -60, -70]
tick_labels = [str(int(t)) for t in amplitude_ticks]

# Set the major tick locations
ax1.set_yticks(amplitude_ticks)
ax1.set_yticklabels(tick_labels)


# Rechte Y-Achse (Phase in Grad)
ax2 = ax1.twinx()
ax2.set_ylabel('Phase [°]', color='red')

# Plot für df (Phase)
line2_df = ax2.semilogx(frequenz_df, spalte_phase_df, color='red', label='Phase (Messung 1) [°]', linestyle = "--", marker='s')

# Plot für dp (Phase) - Farbe oder Marker anpassen, um sie zu unterscheiden
line2_dp = ax2.semilogx(frequenz_dp, spalte_phase_dp, label='_nolegend_', color='red', linestyle = "--", marker='s')

ax2.tick_params(axis='y', labelcolor='red')


tick_locations2 = [-180, -135, -90, -45, 0, 45, 90, 135, 180]
tick_labels2 = [str(int(t)) for t in tick_locations2]

ax2.set_yticks(tick_locations2)
ax2.set_yticklabels(tick_labels2)

# Legende für alle Linien
lines = line1_df + line1_dp + line2_df + line2_dp
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')


xticks = [100, 1000, 10000, 100000, 1000000, 10000000]
ax1.set_xlim([100, 10000000])
ax1.set_xticks(xticks)
ax1.set_xticklabels([str(t) for t in xticks])

# Titel & Layout
#plt.title("Bode-Diagramm – RC-Tiefpass 1. Ordnung (Messung)", fontsize=12) # Optional
plt.tight_layout()
#plt.savefig("Bodelab3messung_beide.png", dpi=300) # Dateinamen angepasst
plt.show()
