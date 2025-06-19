import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np # Import numpy for the 10**() function

# Daten laden
dateiname = "wertelab3Messung.csv"
dn = "ltspicelab3.csv"
df = pd.read_csv(dateiname, encoding="latin1", sep=',')
dfr = pd.read_csv(dn, encoding="latin1", sep=',')

frequenz = df["Hz"]
#spalte1 = df["ideal"]          # This is your 'ideal' column, kept as is
spalte2 = df["grad"]    # This is your 'performance' column, kept as is

fr = dfr["Hz"]
spalte3 = dfr["grad"]            # This is your 'db' column

# Convert spalte3 (which is in dB) to a linear scale to match spalte1 and spalte2
#s3_linear = 10**(spalte3/20) # This converts dB to linear amplitude/gain

fig, ax1 = plt.subplots(figsize=(8, 5))

# Set the single Y-axis label to "Amplitude" or "Gain"
ax1.set_xlabel('Frequenz [Hz]')
ax1.set_ylabel('Phase [°]') # Changed Y-axis label
ax1.tick_params(axis='y')

# Plot all data on ax1
# spalte2 and spalte1 are used directly

#ax1.semilogx(frequenz, spalte1, color='red', linestyle="--", label='G Ideal')
# s3_linear is used for the simulated data
ax1.semilogx(fr, spalte3, color='green', linestyle=":", label='phase Simulation')
ax1.semilogx(frequenz, spalte2, color='blue', label='phase Messung')

ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

# X-Achse – saubere Ticks mit ganzzahligen Labels
ax1.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, 2.0, 5.0), numticks=10))
ax1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

# Legende
ax1.legend(loc='upper left')

xticks = [100, 1000, 10000, 100000, 1000000, 10000000]
ax1.set_xlim([100, 10000000])
ax1.set_xticks(xticks)
ax1.set_xticklabels([str(t) for t in xticks])

# Titel & Layout
#plt.title("Verstärkungsfaktoren (Messung, Ideal, Simulation)", fontsize=12)
plt.tight_layout()
plt.savefig("plotperformancegrad.png", dpi=300)
plt.show()