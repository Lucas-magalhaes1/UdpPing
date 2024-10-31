import time
from socket import *

# Configurações do cliente
serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Enviar pacotes de heartbeat a cada 1 segundo
sequence_number = 1
try:
    while True:
        # Formatar a mensagem com o número de sequência e o timestamp atual
        message = f"Heartbeat {sequence_number} {time.time()}"
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print(f"Enviado pacote {sequence_number} para o servidor.")

        # Incrementar o número de sequência
        sequence_number += 1
        time.sleep(1)  # Aguardar 1 segundo antes de enviar o próximo pacote
except KeyboardInterrupt:
    print("Cliente encerrado manualmente.")
finally:
    clientSocket.close()
