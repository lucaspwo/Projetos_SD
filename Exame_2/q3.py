import mraa                                                 #Importando os modulos
import time

u = mraa.Uart(0)                                            #Inicializacao da UART

u.setBaudRate(115200)                                       #Baudrate 115200
u.setMode(8, mraa.UART_PARITY_NONE, 1)                      #8 bits de dados, 1 de parada e sem paridade
u.setFlowcontrol(False, False)                              #Sem flow control

msg_b = bytearray("Ola, Arduino em bytearray!", "ascii")    #Enviando como bytearray
print("Enviando como bytearray: '{0}'".format(msg_b))
u.write(msg_b)
u.flush()
time.sleep(1.5)                                             #Sleep para garantir o recebimento no Arduino
msg_s = "Ola, Arduino em string!"
print("Enviando mensagem como string: '{0}'".format(msg_s))
u.writeStr(msg_s)
time.sleep(1.5)
u.writeStr("X")
print("Existe algo do outro lado?")
time.sleep(1.5)
if u.dataAvailable(100):                                    #Esperando resposta, com 100ms de timeout
    print("'{0}', diz o Arduino".format(u.readStr(20)))
else:
    print("Nenhum dado recebido. Existe algo conectado?")