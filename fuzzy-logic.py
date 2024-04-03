import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Membaca data dari file Excel
data = pd.read_excel('D:/SEMESTER 4/AI/Contoh/data.xlsx')

# Input variabel
usia = ctrl.Antecedent(np.arange(20, 81, 1), 'usia')
tekanan_darah = ctrl.Antecedent(np.arange(80, 181, 1), 'tekanan_darah')
kolesterol = ctrl.Antecedent(np.arange(100, 301, 1), 'kolesterol')
kesehatan = ctrl.Consequent(np.arange(0, 101, 1), 'kesehatan')

# Fungsi keanggotaan untuk variabel usia
usia['muda'] = fuzz.trimf(usia.universe, [20, 40, 60])
usia['paruh_baya'] = fuzz.trimf(usia.universe, [35, 50, 65])
usia['tua'] = fuzz.trimf(usia.universe, [60, 80, 80])

# Fungsi keanggotaan untuk variabel tekanan darah
tekanan_darah['rendah'] = fuzz.trimf(tekanan_darah.universe, [80, 110, 140])
tekanan_darah['normal'] = fuzz.trimf(tekanan_darah.universe, [100, 130, 160])
tekanan_darah['tinggi'] = fuzz.trimf(tekanan_darah.universe, [150, 170, 180])

# Fungsi keanggotaan untuk variabel kolesterol
kolesterol['rendah'] = fuzz.trimf(kolesterol.universe, [100, 175, 250])
kolesterol['normal'] = fuzz.trimf(kolesterol.universe, [160, 240, 300])
kolesterol['tinggi'] = fuzz.trimf(kolesterol.universe, [220, 300, 300])

# Fungsi keanggotaan untuk variabel kesehatan
kesehatan['rendah'] = fuzz.trimf(kesehatan.universe, [0, 50, 100])
kesehatan['sedang'] = fuzz.trimf(kesehatan.universe, [40, 80, 100])
kesehatan['tinggi'] = fuzz.trimf(kesehatan.universe, [70, 100, 100])

# Rules
rule1 = ctrl.Rule(usia['muda'] & tekanan_darah['rendah'] & kolesterol['rendah'], kesehatan['tinggi'])
rule2 = ctrl.Rule(usia['muda'] & tekanan_darah['normal'] & kolesterol['normal'], kesehatan['sedang'])
# Add more rules as needed

# Control System
kesehatan_ctrl = ctrl.ControlSystem([rule1, rule2])
kesehatan_sim = ctrl.ControlSystemSimulation(kesehatan_ctrl)

# Iterasi melalui setiap rekaman data
results = []
for i, row in data.iterrows():
    try:
        usia_value = row['usia']
        tekanan_darah_value = row['tekanan_darah']
        kolesterol_value = row['kolesterol']
    except KeyError:
        print(f"Error: Data row {i+1} has missing columns. Please check your data.")
        continue

    kesehatan_sim.input['usia'] = usia_value
    kesehatan_sim.input['tekanan_darah'] = tekanan_darah_value
    kesehatan_sim.input['kolesterol'] = kolesterol_value
    kesehatan_sim.compute()
    result = {'Data ke': i+1, 'Tingkat Kesehatan': kesehatan_sim.output['kesehatan']}
    results.append(result)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results to Excel file
results_df.to_excel('D:/SEMESTER 4/AI/Contoh/sufi.xlsx', index=False)



