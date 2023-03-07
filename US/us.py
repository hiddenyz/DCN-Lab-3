from flask import Flask, abort, request
from socket import *

app = Flask(__name__)

@app.route('/')

def initialize():
    return "You should visit /fibonacci with several parameters to obtain the IP address"


@app.route('/fibonacci', methods = ["GET"], endpoint="fibonacci")
def us():
    required_params = ["hostname", "fs_port", "number", "as_ip", "as_port"]
    for param in required_params:
        if param not in request.args:
            abort(400)

    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    dns_message = "TYPE=A\n" + "NAME=" + hostname
    user_socket = socket(AF_INET, SOCK_DGRAM)
    address = (as_ip, int(as_port))
    user_socket.sendto(dns_message.encode(), address)
    response_message, authoritative_address = user_socket.recvfrom(2048)
    response = response_message.decode().split('\n')
    
    ip = "0.0.0.0"
    for line in response:
        name, value = line.split('=')
        if name == 'VALUE':
            ip = value
            break

        if ip == "0.0.0.0":
            return "No IP address", 400
        else:
            return ip

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
