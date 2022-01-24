from _thread import start_new_thread
from machine import enable_irq, disable_irq
from utime import sleep, ticks_ms, ticks_diff
import red
import servicios
import pantalla
from Caudalimetro import Caudalimetro
from BombaAgua import BombaAgua
from Global import Variables

#Inicio Caudalímetro
caudalimetro = Caudalimetro()
#Definir IRQ para lectura de pulsos de caudalímetro
caudalimetro.establecerIrq()
#Inicio Motor
bombaAgua = BombaAgua()
#Inicialización variables Globales
variables = Variables()
#Temporizadores para pulsos
variables.inicioTemporizador = ticks_ms()
variables.tiempoTranscurrido = 0.00
#Estado envío mensajes
variables.msgAdvertenciaEnviada = False
variables.msgLimiteEnviado = False
variables.msgCierreEnviado = False
#Conectar a la red
red.conectarwifi()
#Ejecuta los servicios de IoT
def actualizaServIOT():
    while True:
        sleep(5)
        velMotor = servicios.actualizaConsumo(caudalimetro.caudalmLxS, caudalimetro.volumenTotal)
        print("Velocidad", velMotor)
        consumoMax = servicios.obtenerConsumoMaximo()
        print("Consumo maximo",consumoMax)
        #Advertencia de consumo
        if consumoMax > 0:
            porcConsumo = int((caudalimetro.volumenTotal * 100) / consumoMax)
            if porcConsumo >= 80 and variables.msgAdvertenciaEnviada is False:
                servicios.enviaMensajeTelegram("mensaje_telegram_advertencia", round(caudalimetro.volumenTotal,2), consumoMax, velMotor)
                variables.msgAdvertenciaEnviada = True
        #Control de motor y consumo
        if velMotor == 0 or (caudalimetro.volumenTotal > consumoMax > 0):
            print("Motor Detenido")
            bombaAgua.dc_motor.stop()
            if velMotor == 0 and variables.msgCierreEnviado is False:
                servicios.enviaMensajeTelegram("mensaje_telegram_apagado", round(caudalimetro.volumenTotal,2), consumoMax, velMotor)
                variables.msgCierreEnviado = True
            if caudalimetro.volumenTotal > consumoMax > 0 and variables.msgLimiteEnviado is False:
                servicios.enviaMensajeTelegram("mensaje_telegram_limitecons", round(caudalimetro.volumenTotal,2), consumoMax, velMotor)
                variables.msgLimiteEnviado = True
        if velMotor > 0 and (consumoMax == 0 or consumoMax > caudalimetro.consumoMaxActual or caudalimetro.volumenTotal < consumoMax):
            print("Motor Encendido, velocidad: ", velMotor)
            bombaAgua.dc_motor.forward(velMotor)
            if bombaAgua.velocidadActual != velMotor:
                servicios.enviaMensajeTelegram("mensaje_telegram_encendido", round(caudalimetro.volumenTotal,2), consumoMax, velMotor)
            if consumoMax > caudalimetro.consumoMaxActual:
                variables.msgAdvertenciaEnviada = False
            variables.msgLimiteEnviado = False
            variables.msgCierreEnviado = False
            bombaAgua.velocidadActual = velMotor
            caudalimetro.consumoMaxActual = consumoMax
#Calcula el flujo de agua de acuerdo a los pulsos por segundo
def calcularFlujo():
    variables.tiempoTranscurrido = ticks_diff(ticks_ms(), variables.inicioTemporizador)
    if variables.tiempoTranscurrido >= 1000:
        estado = disable_irq()
#         if caudalimetro.numPulsos > 400:
#             caudalimetro.numPulsos -= caudalimetro.numPulsos
#             caudalimetro.pulsosAcum -= caudalimetro.numPulsos
        print("Pulsos:",caudalimetro.numPulsos, "Pulsos Acumulados:", caudalimetro.pulsosAcum)
        caudalimetro.caudalmLxS = ((1000.0 /variables.tiempoTranscurrido) * caudalimetro.numPulsos) / caudalimetro.factorCalibracion
        mlFlujo = (caudalimetro.caudalmLxS / 120) * 1000
        caudalimetro.volumenTotal += mlFlujo
        #print("Caudal: ",round(caudalmLxS,2),"mL/Seg","- volumenTotal:",round(volumenTotal,2),"mL")
        caudalimetro.numPulsos = 0
        enable_irq(estado)
        variables.inicioTemporizador = ticks_ms()
        pantalla.mostrarEnPantalla(caudalimetro.caudalmLxS,caudalimetro.volumenTotal)
#Inicia código principal
def do_main():
    #Se inicia un hilo independiente para actualización de servicio IOT en Thinger.io
    start_new_thread(actualizaServIOT, ())
    while True:
        calcularFlujo()

if __name__ == "__main__":
    do_main()
    