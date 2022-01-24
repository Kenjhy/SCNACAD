from machine import Pin, PWM
from dcmotor import DCMotor
class BombaAgua:
    def __init__(self):
        self.velocidadActual = 0
        self.frequency = 50
        self.pin1 = Pin(27, Pin.OUT)
        self.pin2 = Pin(26, Pin.OUT)
        self.enable = PWM(Pin(14), self.frequency)
        self.dc_motor = DCMotor(self.pin1, self.pin2, self.enable)
        self.dc_motor = DCMotor(self.pin1, self.pin2, self.enable, 350, 1023)
        self.dc_motor.forward(self.velocidadActual)