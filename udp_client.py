import socket
import sys

UDP_IP = '127.0.0.1'
UDP_PORT = 8001
BUFFER_SIZE = 1024
message = "Hello, World! FROM UDP "

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Type 'exit' to quit")
    print(message)

    while True:
        data = s.sendto(bytes(message, encoding='utf8'), (UDP_IP, UDP_PORT))
        response = s.recvfrom(BUFFER_SIZE)[0]
        response_str = response.decode("utf-8")
        if message == 'exit':
            break
        print(response_str)
        message = sys.stdin.readline().strip('\n')

    s.close()
