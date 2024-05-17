import socket
import select
import sys

# Skapa en ny socket för klienten
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

# Använd första argumentet som IP-adress
IP_address = str(sys.argv[1])

# Använd andra argumentet som portnummer
Port = int(sys.argv[2])

# Anslut klienten till servern med IP-adress och portnummer
server.connect((IP_address, Port))

while True:
    # Upprätthåller en lista med möjliga input-strömmar
    sockets_list = [sys.stdin, server]

    """ 
    Det finns två möjliga input-situationer. Antingen vill användaren ge
    manuell input för att skicka till andra, eller så skickar servern ett 
    meddelande som ska skrivas ut på skärmen. Select returnerar från 
    sockets_list, den ström som är redo för input. Om servern vill skicka 
    ett meddelande kommer if-villkoret att vara sant. Om användaren vill 
    skicka ett meddelande kommer else-villkoret att vara sant.
    """
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode()
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message.encode())
            sys.stdout.write("<You> ")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()
