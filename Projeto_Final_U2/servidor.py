import threading, socket, mraa, time, os

i2c = mraa.I2c(0)
i2c.address(0x04)
d3 = mraa.Pwm(3)        #L2
d3.period_us(700)
d5 = mraa.Pwm(5)        #L3
d5.period_us(700)
d6 = mraa.Pwm(6)        #DRV
d6.period_us(700)
d8 = mraa.Gpio(8)       #L1
d8.dir(mraa.DIR_OUT)
a1 = mraa.Aio(1)        #CH1
a0 = mraa.Aio(0)        #LDR

HOST = ''
PORT = 12000
SERVER = 'testServer'

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.setblocking(False)
listen_socket.listen(1)

print 'Servidor aguardando conexoes na porta %s ...' % PORT

global conectado
conectado = True

global init
init = False

global act
act = False

global temp
temp = 0

global umi
umi = 0

global luz
luz = 0

global curva
curva = 0

global tempo
tempo = 0

class recebeMsgCliente(threading.Thread):
    def __init__(self,clientes,chave):
        threading.Thread.__init__(self)
        self.clientes = clientes
        self.chave = chave
    def run(self):
        conectado = True
        global init
        global act
        while conectado:
            if self.chave in self.clientes:
                try:
                    msg = self.clientes[self.chave]['socket'].recv(2048)
                    if msg == 'iniciar()':
                        init = True
                        act = False
                        print('Iniciando processo de secagem')
                        self.clientes[self.chave]['socket'].send('Iniciando processo de secagem...\n')
                        thread_enviarMsgInicio = enviaMsgCliente(self.clientes,'Iniciando processo de secagem',self.chave)
                        thread_enviarMsgInicio.start()
                    elif msg == 'terminar()':
                        init = False
                        act = False
                        print('Terminando o processo de secagem')
                        self.clientes[self.chave]['socket'].send('Terminando o processo de secagem...\n')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Terminando o processo de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'curva1()':
                        act = True
                        init = True
                        print('Forcando a curva 1 de secagem')
                        threadCurva1.start()
                        self.clientes[self.chave]['socket'].send('Forcando a curva 1 de secagem...\n')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Forcando a curva 1 de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'curva2()':
                        act = True
                        init = True
                        print('Forcando a curva 2 de secagem')
                        threadCurva2.start()
                        self.clientes[self.chave]['socket'].send('Forcando a curva 2 de secagem...\n')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Forcando a curva 2 de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'curva3()':
                        act = True
                        init = True
                        print('Forcando a curva 3 de secagem')
                        threadCurva3.start()
                        self.clientes[self.chave]['socket'].send('Forcando a curva 3 de secagem...\n')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Forcando a curva 3 de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'curva4()':
                        act = True
                        init = True
                        print('Forcando a curva 4 de secagem')
                        threadCurva4.start()
                        self.clientes[self.chave]['socket'].send('Forcando a curva 4 de secagem...\n')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Forcando a curva 4 de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'curva5()':
                        act = True
                        init = True
                        print('Forcando a curva 5 de secagem')
                        threadCurva5.start()
                        self.clientes[self.chave]['socket'].send('Forcando a curva 5 de secagem...\n')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Forcando a curva 5 de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'sair()':
                        init = False
                        self.clientes[self.chave]['socket'].send('Saindo do servidor...')
                        self.clientes[self.chave]['socket'].close()
                        conectado = False
                        #print self.clientes[self.chave]['nick'], 'saiu'
                        for i in self.clientes.keys():
                                if self.clientes[i] == self.clientes[self.chave]:
                                    del self.clientes[i]
                                    break
                    else:
                        self.clientes[self.chave]['socket'].send('Comando incorreto. Tente novamente\n')
                except:
                    if self.chave not in self.clientes:
                        conectado = False
                        break
            else:
                conectado = False
                break

class enviaMsgCliente(threading.Thread):
    def __init__(self,clientes,mensagem,chave):
        threading.Thread.__init__(self)
        self.clientes = clientes
        self.msg = mensagem
        self.chave = chave
    def run(self):
        if bool(self.clientes) == True:
            for i in self.clientes.keys():
                if i != self.chave:
                    self.clientes[i]['socket'].send(self.msg)
        else:
            print 'Servidor vazio. Ninguem para enviar mensagem'

class servidor(threading.Thread):
    def __init__(self,clientes):
        threading.Thread.__init__(self)
        self.clientes = clientes
    def run(self):
        global conectado
        while conectado:
            msg = raw_input()
            if msg == 'sair()':
                print 'Fechando o servidor'
                if bool(self.clientes) == True:
                    for i in self.clientes.keys():
                        self.clientes[i]['socket'].send(msg)
                        self.clientes[i]['socket'].close()
                        #print self.clientes[i]['nick'], 'saiu'
                        del self.clientes[i]
                listen_socket.close()
                conectado = False
                # sys.exit(1)
                os._exit(1)

class botao(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global init
        global act
        while True:
            if(a1.read() == False):
                if (init == False):
                    init = True
                    act = False

class ledL1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            global init
            if init:
                d8.write(1)
            else:
                d8.write(0)

class ledLDR(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            global init
            if init:
                d3.enable(True)
                d3.write(a0.readFloat())
                global luz
                luz = a0.read()
            else:
                d3.enable(False)

class readI2c(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            global temp
            global umi
            temp = int(i2c.readByte())
            #print('Temp: %d' % temp)
            umi = int(i2c.readByte())
            #print('Umi: %d' % umi)
            time.sleep(2)

class conta(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global tempo
        while True:
            tempo = time.time()

class curva1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('Iniciando curva 1')
        d5.enable(True)
        d6.enable(True)
        global tempo
        global init
        pwm = 0
        d5.write(pwm)
        d6.write(pwm)
        print('pwm: %f' % pwm)
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.035
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 5):
            pass
        for i in range(5):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.06
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 5):
            pass
        for i in range(5):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm - 0.13
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        d5.enable(False)
        d6.enable(False)
        init = False

class curva2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('Iniciando curva 2')
        d5.enable(True)
        d6.enable(True)
        global tempo
        global init
        pwm = 0
        d5.write(pwm)
        d6.write(pwm)
        print('pwm: %f' % pwm)
        for i in range(20):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.035
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 5):
            pass
        for i in range(5):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.06
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 5):
            pass
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm - 0.10
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        d5.enable(False)
        d6.enable(False)
        init = False

class curva3(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('Iniciando curva 3')
        d5.enable(True)
        d6.enable(True)
        global tempo
        global init
        pwm = 0
        d5.write(pwm)
        d6.write(pwm)
        print('pwm: %f' % pwm)
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.035
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 10):
            pass
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.025
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 10):
            pass
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm - 0.06
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        d5.enable(False)
        d6.enable(False)
        init = False

class curva4(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('Iniciando curva 4')
        d5.enable(True)
        d6.enable(True)
        global tempo
        global init
        pwm = 0
        d5.write(pwm)
        d6.write(pwm)
        print('pwm: %f' % pwm)
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.055
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 5):
            pass
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.045
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 10):
            pass
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm - 0.10
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        d5.enable(False)
        d6.enable(False)
        init = False

class curva5(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('Iniciando curva 5')
        d5.enable(True)
        d6.enable(True)
        global tempo
        global init
        pwm = 0
        d5.write(pwm)
        d6.write(pwm)
        print('pwm: %f' % pwm)
        for i in range(10):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.035
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 5):
            pass
        for i in range(5):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm + 0.04
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        agora = tempo
        while(tempo - agora < 10):
            pass
        for i in range(20):
            agora = tempo
            while(tempo - agora < 1):
                pass
            pwm = pwm - 0.0275
            d5.write(pwm)
            d6.write(pwm)
            print('pwm: %f' % pwm)
        d5.enable(False)
        d6.enable(False)
        init = False

class secador(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            global init
            global act
            if ( (init == True) and (act == False) ):
                global temp
                global umi
                global luz
                global curva
                if( (temp > 20 and temp <= 50) and (umi > 80)  and (luz > 500 and luz <= 800) ):
                    curva = 1
                    act = True
                    threadCurva1.start()
                elif( (temp > 20 and temp <= 50) and (umi <= 70) and (luz > 500 and luz <= 800) ):
                    curva = 2
                    act = True
                    threadCurva2.start()
                elif( (temp > 20 and temp <= 50) and (umi <= 70) and (luz > 200 and luz <= 500) ):
                    curva = 3
                    act = True
                    threadCurva3.start()
                elif( (temp > 50 and temp <= 80) and (umi <= 60) and (luz > 200 and luz <= 700) ):
                    curva = 4
                    act = True
                    threadCurva4.start()
                else:
                    curva = 5
                    act = True
                    threadCurva5.start()

clientes = {}

threadServ = servidor(clientes)
threadServ.start()
threadConta = conta()
threadConta.start()
threadBotao = botao()
threadBotao.start()
threadLedL1 = ledL1()
threadLedL1.start()
threadLedLDR = ledLDR()
threadLedLDR.start()
threadReadI2c = readI2c()
threadReadI2c.start()
threadCurva1 = curva1()
threadCurva2 = curva2()
threadCurva3 = curva3()
threadCurva4 = curva4()
threadCurva5 = curva5()
threadSecador = secador()
threadSecador.start()

conn = False

while conectado:
    try:
        client_connection, client_address = listen_socket.accept()
        conn = True
    except:
        if conn == True:
            #text = client_connection.recv(2048)
            #print(text)
            clientes.update({client_address:{'ip':str(client_address[0]), 'porta':str(client_address[1]), 'socket':client_connection}})
            client_connection.send('Servidor: Voce esta conectado\n\n')
            client_connection.send('Comandos:\n')
            client_connection.send('iniciar()\t: Inicia a secagem de graos\n')
            client_connection.send('curva#()\t: Forca uma curva de secagem (#: 1 a 5)\n')
            client_connection.send('terminar()\t: Termina a secagem de graos\n')
            client_connection.send('sair()\t\t: Desconecta do servidor\n')
            threadRecebe = recebeMsgCliente(clientes,client_address)
            threadRecebe.start()
            conn = False