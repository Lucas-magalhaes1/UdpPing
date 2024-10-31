import time  
from socket import * 

# Definir o endereço do servidor e a porta
serverName = "127.0.0.1" 
serverPort = 12000  

# Criar um socket UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)  
clientSocket.settimeout(1)  # Define um tempo limite de 1 segundo para respostas

# Inicializar variáveis para estatísticas
total_pings = 10 
rtts = [] 
lost_packets = 0  

# Enviar 10 pacotes Ping para o servidor
for sequence_number in range(1, total_pings + 1): 
    # Formatar a mensagem de ping com número de sequência e horário de envio
    message = f"Ping {sequence_number} {time.time()}"  
    try:
        # Registrar o tempo de envio do pacote
        send_time = time.time()  # Marca o horário de envio do pacote
        # Enviar a mensagem ao servidor
        clientSocket.sendto(message.encode(), (serverName, serverPort))  # Envia a mensagem codificada ao servidor
        
        # Tentar receber a resposta do servidor
        response, serverAddress = clientSocket.recvfrom(1024)  # Aguarda a resposta do servidor
        # Registrar o tempo de recebimento do pacote
        receive_time = time.time()  # Marca o horário de recebimento do pacote
        # Calcular o Round-Trip Time (RTT)
        rtt = receive_time - send_time  
        rtts.append(rtt)  # Adiciona o RTT calculado à lista de RTTs

        # Imprimir a resposta e o RTT
        print(f"Resposta do servidor: {response.decode()}")  # Exibe a resposta decodificada do servidor
        print(f"RTT: {rtt:.4f} segundos")  
    except timeout:
        # Caso o tempo limite seja excedido, registrar timeout
        print("Requisição expirou")  
        lost_packets += 1  # Incrementa o contador de pacotes perdidos

# Fechar o socket após enviar os pings
clientSocket.close()

# Cálculo de estatísticas
if rtts:  
    min_rtt = min(rtts)  
    max_rtt = max(rtts)  
    avg_rtt = sum(rtts) / len(rtts)  # Calcula a média dos RTTs
    packet_loss_rate = (lost_packets / total_pings) * 100  # Calcula a taxa de perda de pacotes em %

    print("\n--- Estatísticas do Ping ---")
    print(f"RTT mínimo: {min_rtt:.4f} segundos")  
    print(f"RTT máximo: {max_rtt:.4f} segundos")  
    print(f"RTT médio: {avg_rtt:.4f} segundos") 
    print(f"Taxa de perda de pacotes: {packet_loss_rate:.2f}%")  
else:
    print("Nenhum pacote foi recebido.") 
