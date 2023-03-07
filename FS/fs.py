from flask import Flask, abort, Response, request
from socket import *

app = Flask(__name__)

@app.route('/')
def initialize():
    return "You should visit /fibonacci with several parameters to obtain the IP address"

@app.route('/register', methods=["PUT"], endpoint="register")
def register():
    data = request.json
    hostname = data.get("hostname")
    ip = data.get("ip")
    as_ip = data.get("as_ip")
    as_port = data.get("as_port")

    if not all((hostname, ip, as_ip, as_port)):
        abort(400, "Missing Parameters!")

    dns_Message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
    address = (as_ip, int(as_port))

    fibonacciSocket = socket(AF_INET, SOCK_DGRAM)
    fibonacciSocket.sendto(dns_Message.encode(), address)

    response, addr = fibonacciSocket.recvfrom(2048)
    print(response.decode())

    return Response("Registration Finished!", status=201)

@app.route('/fibonacci', methods=["GET"], endpoint="fibonacci")
def fibonacci():
    num = request.args.get("number")

    if not num:
        abort(400, "Missing Parameters")
    elif not num.isdigit():
        abort(400, "Wrong Parameter Type")

    num = int(num)

    def fib(n):
        a, b = 1, 1
        for i in range(n - 1):
            a, b = b, a + b
        return a

    return str(fib(num))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
