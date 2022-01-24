from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
#Manejo de Pantalla
ancho=128
alto=64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)
print(i2c.scan())
def mostrarEnPantalla(caudal, volumen):
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
    oled.show()
    