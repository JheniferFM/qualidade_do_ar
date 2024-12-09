import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import csv
import time

# Função com retry e exponential backoff
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_air_quality_data(lat, lon, api_key):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url, timeout=50)  # Aumentei o timeout para 50 segundos
    response.raise_for_status()  # Lança uma exceção se a resposta não for 200
    return response.json()

# Coordenadas das capitais brasileiras
capitais = {
    'Rio Branco': (-9.0238, -67.9085),
    'Maceió': (-9.6658, -35.7353),
    'Macapá': (0.0345, -51.0694),
    'Manaus': (-3.1190, -60.1719),
    'Boa Vista': (2.8230, -60.6753),
    'Porto Velho': (-8.7614, -63.9039),
    'Palmas': (-10.1857, -48.3337),
    'Aracaju': (-10.9472, -37.0731),
    'Salvador': (-12.9714, -38.5014),
    'Fortaleza': (-3.7172, -38.5437),
    'Brasília': (-15.7801, -47.9292),
    'Goiânia': (-16.6869, -49.2648),
    'São Luís': (-2.5297, -44.3028),
    'Cuiabá': (-15.6010, -56.0978),
    'Campo Grande': (-20.4697, -54.6201),
    'Belo Horizonte': (-19.9208, -43.9378),
    'Vitória': (-20.3155, -40.3128),
    'Rio de Janeiro': (-22.9068, -43.1729),
    'São Paulo': (-23.5505, -46.6333),
    'Curitiba': (-25.4296, -49.2719),
    'Recife': (-8.0476, -34.8770),
    'Natal': (-5.7945, -35.2110),
    'João Pessoa': (-7.1152, -34.8610),
    'Teresina': (-5.0890, -42.8018),
    'Palhoça': (-27.6454, -48.6899),
    'Porto Alegre': (-30.0346, -51.2177),
    'Florianópolis': (-27.5954, -48.5480),
    'Cuiabá': (-15.6010, -56.0978),
    'Belém': (-1.4558, -48.4902),
    'Teresina': (-5.0890, -42.8018),
    'Porto Alegre': (-30.0346, -51.2177),
    'Florianópolis': (-27.5954, -48.5480)
}

# Sua chave de API
api_key = '8adb704874b2f95e10d7b7026419c1c3'

# Listar dados
dados = []
for cidade, (lat, lon) in capitais.items():
    try:
        data = get_air_quality_data(lat, lon, api_key)
        aqi = data['list'][0]['main']['aqi']
        poluentes = data['list'][0]['components']
        poluicao = {
            'cidade': cidade,
            'aqi': aqi,
            'co': poluentes.get('co', 'N/A'),
            'no': poluentes.get('no', 'N/A'),
            'no2': poluentes.get('no2', 'N/A'),
            'o3': poluentes.get('o3', 'N/A'),
            'so2': poluentes.get('so2', 'N/A'),
            'pm2_5': poluentes.get('pm2_5', 'N/A'),
            'pm10': poluentes.get('pm10', 'N/A'),
            'nh3': poluentes.get('nh3', 'N/A')
        }
        dados.append(poluicao)
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para {cidade}: {e}")
    time.sleep(1)  # Aguardar entre as requisições para evitar sobrecarga na API

# Salvar os dados em um arquivo CSV
with open('qualidade_do_ar_brasil_capitais.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['cidade', 'aqi', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3'])
    writer.writeheader()
    writer.writerows(dados)

print("Dados salvos no arquivo 'qualidade_do_ar_brasil_capitais.csv'.")
