# FUNCIÓN PARA ESTABLECER LA CONEXIÓN WIFI (STATION)
import network   # importa el módulo network
import ujson    # importa módulo para json
def conectarwifi():
    with open("configwifi.json") as configFile: #Apertura de fichero
        wifiConfig = ujson.load(configFile)
    sta_if = network.WLAN(network.STA_IF)     # instancia el objeto -sta_if- para realizar la conexión en modo STA
    if not sta_if.isconnected():              # si no existe conexión...
        sta_if.active(True)                       # activa el interfaz STA del ESP32
        sta_if.connect(wifiConfig["ssid"], wifiConfig["pwd"])            # inicia la conexión con el AP
        print('Conectando a la red', wifiConfig["ssid"] +"...")
        while not sta_if.isconnected():           # ...si no se ha establecido la conexión...
            pass                                  # ...repite el bucle...
    print('Configuración de red (IP/netmask/gw/DNS):', sta_if.ifconfig())
    