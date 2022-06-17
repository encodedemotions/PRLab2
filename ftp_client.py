import socket
import sys

FTP_IP = '127.0.0.1'
FTP_PORT = 8003
BUFFER_SIZE = 1024
message = "Hello, World! FROM FTP "

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((FTP_IP, FTP_PORT))
    print("Connection successful")
    print("Type 'resend' to send the contents of the client file")
    print("Type 'receive' to receive the contents of the server file")
    print("Type 'exit' to quit")
    # print(message)
    lower_message = message.lower()
    while lower_message != "exit":
        lower_message = message.lower()

        if lower_message != "resend":
            w_stream = open("ftp_client", "w")
            w_stream.write(message)
            w_stream.close()
        r_stream = open("ftp_client", "r")
        file_contents = r_stream.readlines()
        file_string = ""
        for string in file_contents:
            file_string += string
        data = s.send(bytes(file_string, encoding='utf8'))
        response = s.recv(BUFFER_SIZE)
        response_str = response.decode("utf-8")
        print(response_str)
        message = sys.stdin.readline().strip('\n')

    s.close()
