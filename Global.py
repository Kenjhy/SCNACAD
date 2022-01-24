class Variables:
    def __init__(self):
        #Temporizadores para pulsos
        self.inicioTemporizador = 0
        self.tiempoTranscurrido = 0.00
        #Estado envío mensajes
        self.msgAdvertenciaEnviada = False
        self.msgLimiteEnviado = False
        self.msgCierreEnviado = False
        