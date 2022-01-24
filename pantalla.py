from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from utime import sleep
from framebuf import FrameBuffer, MONO_HLSB

#Manejo de Pantalla
ancho=128
alto=64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)
print(i2c.scan())
def mostrarEnPantalla(caudal, volumen, velocidad):
    #global oled
    oled.fill(0)
    oled.text("Caudal: ", 0,0)
    oled.text(str(round(caudal,2))+" mL/Seg", 0,10)
    oled.text("Volumen Total: ", 0,20)
    if volumen > 999.99:
        textoVol = str(round(volumen/1000, 2)) + "L"
    else:
        textoVol = str(round(volumen,2))+" mL"
    oled.text(textoVol, 0,30)
    oled.text("Velocidad: ", 0, 40)
    oled.text(str(velocidad), 0, 50)
    oled.show()
    
def mostrarLogoInicial():
    dibujo= open("images/logo_scnacad.pbm", "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    oled.blit(FrameBuffer(icono, x, y, MONO_HLSB), 0, 0) # ruta y sitio de ubicación
    oled.show()  #mostrar
    sleep(3)
    