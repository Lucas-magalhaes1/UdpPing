import random
from socket import *

# Configuração do servidor
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Atribuir endereço IP e número da porta ao socket
serverSocket.bind(('', serverPort))
print(f"Servidor UDP de Ping ativo na porta {serverPort}...")

while True:
    # Gerar número aleatório entre 0 e 10
    rand = random.randint(0, 10)

    # Receber o pacote do cliente junto com o endereço de origem
    message, address = serverSocket.recvfrom(1024)

    # Colocar a mensagem recebida em maiúsculas
    message = message.upper()

    # Se o número rand for menor que 4, consideramos que o pacote foi perdido e não respondemos
    if rand < 4:
        print("Simulando perda de pacote.")
        continue

    # Caso contrário, o servidor responde
    serverSocket.sendto(message, address)
    print(f"Respondendo ao cliente {address} com a mensagem: {message.decode()}")
