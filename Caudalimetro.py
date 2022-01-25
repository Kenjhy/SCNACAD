from machine import Pin
class Caudalimetro:
    def __init__(self):
        self.numPulsos = 0
        self.pulsosAcum = 0
        self.caudalmLxS = 0.0
        self.Sensor = Pin(15,Pin.IN)
        # 5880 / 60 = 98
        self.factorCalibracion = 700
        self.volumenTotal = 0.0
        self.consumoMaxActual = 0.0
    #Conteo de Pulsos
    def contarPulsos(self,_=None):
        self.pulsosAcum += 1
        self.numPulsos += 1
    def establecerIrq(self):
        self.Sensor.irq(trigger=Pin.IRQ_RISING, handler=self.contarPulsos)
        
