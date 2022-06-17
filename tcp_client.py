import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 8000
BUFFER_SIZE = 1024
message = "Hello, World! FROM TCP "

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("Connection successful")
    print("Type 'exit' to quit")
    print(message)

    while True:
        data = s.send(bytes(message, encoding='utf8'))
        if message == 'exit':
            break
        response = s.recv(BUFFER_SIZE)
        response_str = response.decode("utf-8")
        print(response_str)
        message = sys.stdin.readline().strip('\n')

    s.close()
