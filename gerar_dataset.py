import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configurações do posto
precos = {'Gasolina': 6.29, 'Etanol': 4.56, 'Diesel': 7.89}
bombas = {
    'Gasolina': list(range(1,7)),
    'Etanol': list(range(7,13)),
    'Diesel': list(range(13,19))
}
frentistas_dia = ['Caio', 'Luciano', 'Pedro']
frentistas_noite = ['Luís', 'Tarcísio', 'João']

# Datas: 7 dias a partir de 01/01/2023
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(7)]

# Gerar dados (seed fixo para reproducibilidade)
data = []
np.random.seed(42)

for date in dates:
    # Turno dia (6h-18h): mais movimento
    num_day = np.random.randint(120, 180)
    for _ in range(num_day):
        hour = np.random.randint(6, 18)
        minute = np.random.randint(0, 60)
        ts = datetime(date.year, date.month, date.day, hour, minute)
        combustivel = np.random.choice(list(bombas.keys()))
        bomba_id = np.random.choice(bombas[combustivel])
        frentista = np.random.choice(frentistas_dia)
        litros = round(np.random.uniform(10, 100), 2)
        valor = round(litros * precos[combustivel], 2)
        data.append([ts, date.date(), bomba_id, combustivel, frentista, litros, valor])
    
    # Turno noite (18h-6h): menos movimento
    num_night = np.random.randint(60, 100)
    for _ in range(num_night):
        if np.random.rand() > 0.3:
            hour = np.random.randint(18, 24)
            ts_date = date
        else:
            hour = np.random.randint(0, 6)
            ts_date = date + timedelta(days=1) if hour < 6 else date
        minute = np.random.randint(0, 60)
        ts = datetime(ts_date.year, ts_date.month, ts_date.day, hour, minute)
        combustivel = np.random.choice(list(bombas.keys()))
        bomba_id = np.random.choice(bombas[combustivel])
        frentista = np.random.choice(frentistas_noite)
        litros = round(np.random.uniform(10, 100), 2)
        valor = round(litros * precos[combustivel], 2)
        data.append([ts, date.date(), bomba_id, combustivel, frentista, litros, valor])

# Criar DataFrame
columns = ['Timestamp', 'Data', 'Bomba_ID', 'Tipo_Combustivel', 'Frentista', 'Litros_Vendidos', 'Valor_Total']
df = pd.DataFrame(data, columns=columns)
df = df.sort_values('Timestamp').reset_index(drop=True)

# Salvar como CSV
df.to_csv('vendas_posto.csv', index=False)
print(f"Dataset gerado com sucesso! {len(df)} registros salvos em 'vendas_posto.csv'")