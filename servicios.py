import urequests
import ujson

#Envía mensajes a Telegram a través de IFTTT
def enviaMensajeTelegram(nombreEvento, consumoActual, consumoLimite, velocidadMotor):
    url = "https://maker.ifttt.com/trigger/" + nombreEvento + "/with/key/*KEY_HERE*"
    respuesta = urequests.get(url+"?value1="+str(consumoActual / 1000)+"&value2="+str(consumoLimite / 1000)+"&value3="+str(velocidadMotor))
    print(respuesta.status_code, respuesta.text)
    respuesta.close()
 #Actualiza el consumo en Thinger.io y devuelve la velocidad del motor
def actualizaConsumo(caudalmLxS, volumenTotal):
    payload = ujson.dumps({
           "mLxSeg":caudalmLxS,
            "volumenTotal": volumenTotal / 1000 #Conversión de mililitros a litros
        })
    request_url = "https://api.thinger.io/v3/users/*USER*/devices/ESP3201/callback/data"
    header_data = { "content-type": 'application/json', "Authorization": 'Bearer *KEY_HERE*'}
    resp = urequests.post(request_url, headers = header_data, data = payload)
    velMotor = int(resp.json())
    return velMotor
#Obtiene el valor del consumo máximo configurado en Thinger.io
def obtenerConsumoMaximo():
    payload = ujson.dumps({})
    request_url = "https://api.thinger.io/v3/users/*USER*/devices/ESP32B/callback/data"
    header_data = { "content-type": 'application/json', "Authorization": 'Bearer *KEY_HERE*'}
    resp = urequests.post(request_url, headers = header_data, data = payload)
    consumoMax = float(resp.json()) * 1000 #Conversión de litros a mililitros
    return consumoMax

