import mraa, random             #Importacao dos modulos

d3 = mraa.Pwm(3)                #Definindo o pino digital 3 como saida PWM
d3.period_us(700)               #Definindo a frequencia da taxa de atualizacao da saida PWM
a0 = mraa.Aio(0)                #Marcando o pino A0 como entrada analogica
a1 = mraa.Aio(1)                #Marcando o pino A1 como entrada analogica
a2 = mraa.Aio(2)                #Marcando o pino A2 como entrada analogica
a3 = mraa.Aio(3)                #Marcando o pino A3 como entrada analogica
a4 = mraa.Aio(4)                #Marcando o pino A4 como entrada analogica

d3.enable(True)                 #Ativando a saida PWM
d3.write(0)                     #Escrevendo 0 no pino D3

while True:
    soma = 0
    for i in range(5):          #Laco for para ler todas as 5 entradas
        if(i == 0):             #Codigo para ler uma entrada analogica por loop do laco,
            x = a0.read()       # multiplicar com um valor aleatorio w e somar com a variavel
            w = random.random() # soma
        elif(i == 1):
            x = a1.read()
            w = random.random()
        elif(i == 2):
            x = a2.read()
            w = random.random()
        elif(i == 3):
            x = a3.read()
            w = random.random()
        else:
            x = a4.read()
            w = random.random()
        soma = soma + w*x
    y = int(soma)               #Separacao da parte inteira da soma
    d3.write(y)                 #Escrita na saida PWM o valor de y