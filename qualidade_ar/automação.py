import time
import requests
import csv
from datetime import datetime

# Função que faz a requisição e salva os dados
def obter_dados():
    capitais = {
        'Brasília': (-15.7801, -47.9292),
        'São Paulo': (-23.5505, -46.6333),
        'Rio de Janeiro': (-22.9068, -43.1729),
        # Adicione mais capitais aqui
    }

    api_key = '8adb704874b2f95e10d7b7026419c1c3'
    arquivo = 'qualidade_do_ar_brasil_capitais.csv'

    with open(arquivo, 'a', newline='') as csvfile:
        fieldnames = ['Data', 'Capital', 'AQI', 'CO', 'NO', 'NO2', 'O3', 'SO2', 'PM2_5', 'PM10', 'NH3']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Se o arquivo está vazio, escreve o cabeçalho
        if csvfile.tell() == 0:
            writer.writeheader()

        for cidade, (lat, lon) in capitais.items():
            url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                poluentes = dados['list'][0]['components']
                aqi = dados['list'][0]['main']['aqi']
                writer.writerow({
                    'Data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Capital': cidade,
                    'AQI': aqi,
                    'CO': poluentes['co'],
                    'NO': poluentes['no'],
                    'NO2': poluentes['no2'],
                    'O3': poluentes['o3'],
                    'SO2': poluentes['so2'],
                    'PM2_5': poluentes['pm2_5'],
                    'PM10': poluentes['pm10'],
                    'NH3': poluentes['nh3']
                })
            else:
                print(f"Erro na requisição para {cidade}: {response.status_code}")
    
    print("Dados salvos no arquivo 'qualidade_do_ar_brasil_capitais.csv'.")

# Executa a função a cada 1 hora (3600 segundos)
while True:
    obter_dados()
    time.sleep(3600)  # 3600 segundos = 1 hora
