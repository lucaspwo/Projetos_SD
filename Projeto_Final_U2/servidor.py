import threading, socket, mraa, time

d3 = mraa.Pwm(3)        #L2
d3.period_us(100)       #10kHz
d5 = mraa.Pwm(5)        #L3
d5.period_us(100)       #10kHz
d6 = mraa.Pwm(6)        #DRV
d6.period_us(100)       #10kHz
d12 = mraa.Gpio(12)     #L1
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

class recebeMsgCliente(threading.Thread):
    def __init__(self,clientes,chave):
        threading.Thread.__init__(self)
        self.clientes = clientes
        self.chave = chave
    def run(self):
        conectado = True
        while conectado:
            if self.chave in self.clientes:
                try:
                    msg = self.clientes[self.chave]['socket'].recv(2048)
                    if msg == 'iniciar()':
                        global init
                        init = True
                        print('Iniciando processo de secagem')
                        self.clientes[self.chave]['socket'].send('Iniciando processo de secagem...\n')
                        thread_enviarMsgInicio = enviaMsgCliente(self.clientes,'Iniciando processo de secagem',self.chave)
                        thread_enviarMsgInicio.start()
                    elif msg == 'terminar()':
                        global init
                        init = False
                        print('Terminando o processo de secagem')
                        self.clientes[self.chave]['socket'].send('Terminando o processo de secagem...\n')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Terminando o processo de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'sair()':
                        global init
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

class botao(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            if(a1.read() == False):
                global init
                init = True


class secador(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        d3.enable(True)
        d5.enable(True)
        d6.enable(True)
        
        while True:
            global init
            while init:
                luz = a0.read()
                #receber valor DHT do Arduino (i2c)
                

clientes = {}

threadServ = servidor(clientes)
threadServ.start()
threadBotao = botao()
threadBotao.start()
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
            client_connection.send('terminar()\t: Termina a secagem de graos\n')
            client_connection.send('sair()\t\t: Desconecta do servidor\n')
            threadRecebe = recebeMsgCliente(clientes,client_address)
            threadRecebe.start()
            conn = False