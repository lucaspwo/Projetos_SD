import mraa, time                           #Importando os modulos

spi = mraa.Spi(0)                           #Habilitando o SPI
spi.frequency(4000000)                      #Definindo a frequencia de 4MHz

tx = bytearray(3)                           #Criando o bytearray que armazenara os
tx[0] = 0                                   # valores dos bytes enviados
tx[1] = 0
tx[2] = 0

global i                                    #Inicializando a variavel que contara de
i = 0                                       # forma crescente
while True:
    i = i + 1
    tx[0] = i                               #Definindo o valor de saida
    print('Valor enviado: %d' % tx[0])      #Exibindo a saida antes do envio
    rx = spi.write(tx)                      #Enviando os bytes
    print('Valor recebido: %d' % rx[2])     #Exibindo o valor recebido
    time.sleep(1)