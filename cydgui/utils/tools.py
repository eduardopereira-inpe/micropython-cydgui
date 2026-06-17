import gc
import urequests
import ujson


def remove_acentos(texto):
    """Remove acentos e caracteres especiais para compatibilidade com a fonte do display."""
    if not texto:
        return ""
    
    substituicoes = {
        'á':'a', 'à':'a', 'â':'a', 'ã':'a', 'ä':'a',
        'é':'e', 'è':'e', 'ê':'e', 'ë':'e',
        'í':'i', 'ì':'i', 'î':'i', 'ï':'i',
        'ó':'o', 'ò':'o', 'ô':'o', 'õ':'o', 'ö':'o',
        'ú':'u', 'ù':'u', 'û':'u', 'ü':'u',
        'ç':'c',
        'Á':'A', 'À':'A', 'Â':'A', 'Ã':'A', 'Ä':'A',
        'É':'E', 'È':'E', 'Ê':'E', 'Ë':'E',
        'Í':'I', 'Ì':'I', 'Î':'I', 'Ï':'I',
        'Ó':'O', 'Ò':'O', 'Ô':'O', 'Õ':'O', 'Ö':'O',
        'Ú':'U', 'Ù':'U', 'Û':'U', 'Ü':'U',
        'Ç':'C'
    }
    
    resultado = ""
    for char in texto:
        resultado += substituicoes.get(char, char)
    return resultado

def get_lat_lon_from_my_ip() -> dict:

    msg = {
        "Public IP": None,
        "Latitude": None,
        "Longitude": None,
        "Error": "Unknown error"
    }

    response = None

    try:
        gc.collect()
        response = urequests.get("http://ip-api.com/json")
        data = response.json()


        if data.get("status") == "success":
            msg = {
                "Public IP": data.get("query"),
                "Latitude": data.get("lat"),
                "Longitude": data.get("lon"),
                "Error": None
            }

    except Exception as e:
        msg = {
            "Public IP": None,
            "Latitude": None,
            "Longitude": None,
            "Error": "Could not retrieve geolocation: {}".format(e)
        }

    finally:
        if response:
            response.close()

    gc.collect()
    return msg



def get_weather_by_coords(lat, lon, api_key):
    """
    Busca o clima atual usando Latitude e Longitude.
    Retorna um dicionário com os dados ou None em caso de erro.
    """

    # Forçamos a limpeza de memória antes da requisição para evitar travamentos
    gc.collect()

    try:
            
        # URL da OpenWeatherMap usando lat e lon em vez de nome da cidade
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
        
        print(url)
        
        response = urequests.get(url)

        
        dados = ujson.loads(response.text)
        
        response.close()
        gc.collect()
        

        
        if dados.get("cod") == 200:
            descricao = dados["weather"][0]["description"]            
            
            # Fazemos o capitalize "na mão" contornando a limitação do MicroPython
            if len(descricao) > 0:
                descricao = descricao[0].upper() + descricao[1:]     
            return {
                "local": dados.get("name", "Local"),
                "descricao": descricao,
                "id": dados["weather"][0]["id"],
                "temp": dados["main"]["temp"],
                "sensacao": dados["main"]["feels_like"],
                "umidade": dados["main"]["humidity"],
                "pressao": dados["main"]["pressure"], # hPa
                "vento": dados["wind"]["speed"],      # m/s
                "visibilidade": dados.get("visibility", 0) / 1000, # km
                "sucesso": True
            }
        else:
            print("Erro na resposta da API:", dados.get("message", "Erro desconhecido"))
            response.close()
            return {"sucesso": False, "erro": dados.get("message")}
            
    except OSError as e:
        if e.args[0] == -202:
            print("Erro de DNS/Sem internet. Tentando reconectar...")
        else:
            print("Erro na requisição HTTP:", e)
        return {"sucesso": False, "erro": "Falha de conexão"}
        
    except ValueError as e:
        # O ujson levanta ValueError se o texto não for um JSON válido
        print("Erro ao tentar ler o JSON:", e)
        print("Texto recebido da API:", response.text)
        response.close()
        return {"sucesso": False, "erro": "JSON inválido"}