import pandas as pd
import numpy as np

def calculate_frequency_aligned_rms(df_short: pd.DataFrame, df_long: pd.DataFrame, 
                                     freq_col: str = 'Frequenz', 
                                     amplitude_col: str = 'Amplitude', 
                                     phase_col: str = 'Phase') -> dict:
    """
    Berechnet die Root Mean Square (RMS)-Differenz für Amplitude und Phase,
    indem die Werte des kürzeren DataFrames mit den Frequenz-ähnlichsten Werten
    des längeren DataFrames verglichen werden.

    Args:
        df_short (pd.DataFrame): Der kürzere DataFrame. Erwartet Spalten für Frequenz, Amplitude und Phase.
        df_long (pd.DataFrame): Der längere DataFrame. Erwartet Spalten für Frequenz, Amplitude und Phase.
        freq_col (str): Der Name der Frequenzspalte in beiden DataFrames.
        amplitude_col (str): Der Name der Amplitudenspalte in beiden DataFrames.
        phase_col (str): Der Name der Phasenspalte in beiden DataFrames.

    Returns:
        dict: Ein Dictionary, das die RMS-Differenz für Amplitude und Phase enthält.
              Gibt None zurück, wenn eine Übereinstimmung nicht gefunden werden kann.
    """

    if df_short.empty or df_long.empty:
        print("Einer der DataFrames ist leer.")
        return {'rms_amplitude': np.nan, 'rms_phase': np.nan}

    # Sicherstellen, dass die erforderlichen Spalten vorhanden sind
    required_cols = [freq_col, amplitude_col, phase_col]
    for col in required_cols:
        if col not in df_short.columns or col not in df_long.columns:
            raise ValueError(f"Spalte '{col}' nicht in einem oder beiden DataFrames gefunden.")

    # Sortiere beide DataFrames nach Frequenz, um die Suche zu optimieren
    df_short = df_short.sort_values(by=freq_col).reset_index(drop=True)
    df_long = df_long.sort_values(by=freq_col).reset_index(drop=True)

    amplitude_diffs = []
    phase_diffs = []

    # Iteriere durch den kürzeren DataFrame
    for index_short, row_short in df_short.iterrows():
        freq_short = row_short[freq_col]

        # Finde die am besten passende Frequenz im längeren DataFrame
        # Dies ist ein "Nächster Nachbar"-Ansatz.
        # Wir können abs(freq_long - freq_short) minimieren.
        diffs = np.abs(df_long[freq_col] - freq_short)
        closest_match_index = diffs.idxmin()
        
        row_long = df_long.loc[closest_match_index]
        freq_long = row_long[freq_col]

        # Optional: Setzen Sie eine Toleranz für die Frequenzübereinstimmung
        # Wenn die Frequenzdifferenz zu groß ist, überspringen Sie diese Messung
        # Sie müssen einen geeigneten Wert für freq_tolerance_factor festlegen
        # Beispiel: 0.01 bedeutet 1% Toleranz
        freq_tolerance_factor = 0.01  # Beispiel: 0.1% der Frequenz des längeren DF
        if abs(freq_short - freq_long) > freq_tolerance_factor * freq_long:
            print(f"Warnung: Frequenz {freq_short:.2f} (kurz) und {freq_long:.2f} (lang) weichen stark ab. Überspringe diesen Punkt.")
            continue

        # Berechne die Differenzen
        amplitude_diff = row_short[amplitude_col] - row_long[amplitude_col]
        phase_diff = row_short[phase_col] - row_long[phase_col] # Phasen können im Bogenmaß oder Grad sein

        amplitude_diffs.append(amplitude_diff)
        phase_diffs.append(phase_diff)
        #print(phase_diff)

    if not amplitude_diffs or not phase_diffs:
        print("Keine passenden Frequenzen gefunden, um RMS zu berechnen.")
        return {'rms_amplitude': np.nan, 'rms_phase': np.nan}

    # Berechne die Root Mean Square (RMS)
    rms_amplitude = np.sqrt(np.mean(np.square(amplitude_diffs)))
    rms_phase = np.sqrt(np.mean(np.square(phase_diffs)))

    return {'rms_amplitude': rms_amplitude, 'rms_phase': rms_phase}

# --- Beispielhafte Verwendung ---
if __name__ == "__main__":
    dateiname = "wertelab3Messung.csv"
    dn = "ltspicelab3.csv"
    df = pd.read_csv(dateiname, encoding="latin1", sep=',')
    dfr = pd.read_csv(dn, encoding="latin1", sep=',')

    print(calculate_frequency_aligned_rms(df, dfr,
                                     freq_col='Hz', 
                                     amplitude_col='db', 
                                     phase_col='grad'))
    