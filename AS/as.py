from socket import *

dns_records = {}

authoritative_socket = socket(AF_INET, SOCK_DGRAM)
authoritative_socket.bind(('', 53533))

while True:
    message, client_address = authoritative_socket.recvfrom(2048)
    message = message.decode()

    print(message)

    fields = message.strip().split('\n')
    if len(fields) != 3:
        print("Invalid DNS request")
    else:
        dns_type = fields[0].split('=')[1]
        hostname = fields[1].split('=')[1]
        ip = fields[2].split('=')[1]

        if dns_type == 'A':
            dns_records[hostname] = ip
            response = b'Finished registration'
        elif dns_type == 'Q':
            if hostname in dns_records:
                ip = dns_records[hostname]
            else:
                ip = '0.0.0.0'
            response = f'TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10'.encode()
        else:
            print("Invalid DNS type")
        
        authoritative_socket.sendto(response, client_address)
