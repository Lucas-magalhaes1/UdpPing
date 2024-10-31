import time  
from socket import * 

# Configurações do servidor
serverPort = 12000  
serverSocket = socket(AF_INET, SOCK_DGRAM)  # Cria um socket UDP
serverSocket.bind(('', serverPort))  # Liga o socket a todas as interfaces de rede na porta definida
print(f"Servidor UDP Heartbeat ativo na porta {serverPort}...")  

# Inicializar variáveis de controle
last_sequence = -1  # Armazena o último número de sequência recebido, inicializado como -1
timeout_interval = 5  # Intervalo de tempo (em segundos) para detectar inatividade do cliente
last_received_time = time.time()  # Marca o último tempo de recebimento para controle de inatividade

# Loop principal do servidor para monitoramento de pacotes
while True:
    try:
        # Definir um tempo limite para detectar a ausência do cliente
        serverSocket.settimeout(timeout_interval)  # Define o timeout para detectar inatividade do cliente

        # Receber o pacote do cliente
        message, address = serverSocket.recvfrom(1024)  # Recebe um pacote do cliente
        receive_time = time.time()  # Marca o tempo de recebimento do pacote

        # Extrair dados do pacote
        decoded_message = message.decode().split()  # Decodifica e divide a mensagem em uma lista
        sequence_number = int(decoded_message[1])  # Extrai o número de sequência do pacote
        send_time = float(decoded_message[2])  # Extrai o horário de envio do pacote

        # Calcular diferença de tempo (RTT simulado)
        time_diff = receive_time - send_time  # Calcula o RTT simulado
        print(f"Pacote {sequence_number} recebido de {address} | RTT: {time_diff:.4f} segundos")  # Exibe detalhes do pacote e RTT

        # Verificar pacotes perdidos
        if last_sequence != -1 and sequence_number > last_sequence + 1:  # Condição para detectar pacotes perdidos
            lost_packets = sequence_number - last_sequence - 1  
            print(f"Perda detectada: {lost_packets} pacotes ausentes")  
        # Atualizar o número de sequência e o tempo de recebimento
        last_sequence = sequence_number  # Atualiza o último número de sequência recebido
        last_received_time = receive_time  # Atualiza o último tempo de recebimento para monitorar a inatividade

    except timeout:
        # Verificar inatividade se o timeout for excedido
        print("Cliente inativo. Nenhum pacote recebido nos últimos 5 segundos.") 
        last_sequence = -1  # Reinicia o número de sequência para retomar a contagem quando um novo pacote chegar
