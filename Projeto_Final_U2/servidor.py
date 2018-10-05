import threading, socket

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
                        print('Iniciando processo de secagem')
                        thread_enviarMsgInicio = enviaMsgCliente(self.clientes,'Iniciando processo de secagem',self.chave)
                        thread_enviarMsgInicio.start()
                    elif msg == 'terminar()':
                        print('Terminando o processo de secagem')
                        thread_enviarMsgTermina = enviaMsgCliente(self.clientes,'Terminando o processo de secagem',self.chave)
                        thread_enviarMsgTermina.start()
                    elif msg == 'sair()':
                        self.clientes[self.chave]['socket'].close()
                        conectado = False
                        #print self.clientes[self.chave]['nick'], 'saiu'
                        for i in self.clientes.keys():
                                if self.clientes[i] == self.clientes[self.chave]:
                                    del self.clientes[i]
                                    break
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

clientes = {}

threadServ = servidor(clientes)
threadServ.start()

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
            client_connection.send('Servidor escreveu: Voce esta conectado')
            threadRecebe = recebeMsgCliente(clientes,client_address)
            threadRecebe.start()
            conn = False