import threading, os, time
from socket import *

global conectado
conectado = True

class recebeMsg (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.client_Socket = clientSocket
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        global conectado
        #ouvir o que o servidor vai mandar e imprimir em tela
        while conectado:
            msg = self.client_Socket.recv(2048)
            # print msg
            if msg == 'sair()':
                print 'O servidor fechou'
                conectado = False
                clientSocket.close()
                # break
                os._exit(1)
            else:
                print msg

serverName = '127.0.0.1' #inserir o ip do servidor
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

thread = recebeMsg (clientSocket)
thread.start()

try:
    while conectado:
        #Parte para enviar as mensagens
        try:
            sentence = raw_input()
            clientSocket.send(sentence)
            if sentence == 'sair()':
                conectado = False
                clientSocket.close()
                break
        except:
            time.sleep(0.05)
finally:
    clientSocket.close()