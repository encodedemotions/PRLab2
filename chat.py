import os
import socket
import ssl
import threading
import http.server
import smtplib

# Get email host, user email, and user password from .env file
# .env file does not get uploaded to github
from chatbot import get_response

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 465

ssl_context = ssl.create_default_context()

HOST = '127.0.0.1'
TCP_PORT = 8000

UDP_PORT = 8001

HTTP_PORT = 8002

FTP_PORT = 8003


class Chat:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((HOST, TCP_PORT))

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((HOST, UDP_PORT))

        self.http_server = http.server.HTTPServer((HOST, HTTP_PORT), HttpHandler)

        self.ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ftp_socket.bind((HOST, FTP_PORT))

        self.smtp_host = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=ssl_context)
        # self.smtp_host.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        self.client_history = {}

    def get_response(self, string, client) -> str:
        print(client)
        split_string = string.split()
        if split_string and split_string[0] == 'email':
            if len(split_string) > 1:
                receiver_email = split_string[1]
            else:
                return "Please provide email to send to. Eg:email hello@who.dis"
            if client in self.client_history:
                body_text = ""
                email_body_list = self.client_history[client]
                for qa in email_body_list:
                    body_text += qa
                email_body = f"From: {EMAIL_HOST_USER}\r\nTo: {receiver_email}\r\n\r\n{body_text}"
                try:
                    print("Trying to send:", email_body)
                    self.smtp_host.sendmail(EMAIL_HOST_USER, receiver_email, msg=email_body)
                except:
                    return f"Could not send email to receiver:{receiver_email}"

                return "Email sent to " + receiver_email
            else:
                return "This client has no history with this chat, no email was sent."
        else:
            response = get_response(string)
            if client in self.client_history:
                self.client_history[client].append("Q:" + string + "\nA:" + response + "\n")
            else:
                self.client_history[client] = ["Q:" + string + "\nA:" + response + "\n"]
            return response

    def run(self):
        print("Starting server initialization")
        tcp_tread = threading.Thread(target=self.run_tcp)
        udp_thread = threading.Thread(target=self.run_udp)
        http_thread = threading.Thread(target=self.run_http)
        ftp_thread = threading.Thread(target=self.run_ftp)

        tcp_tread.start()
        udp_thread.start()
        http_thread.start()
        ftp_thread.start()

    def run_tcp(self):
        self.tcp_socket.listen()
        print("TCP Server initialized")
        while True:
            conn, _ = self.tcp_socket.accept()
            peer_name = conn.getpeername()
            client = peer_name[0] + str(peer_name[1])
            print("TCP connection established with client:", client)
            try:
                while conn:
                    data = conn.recv(1024)  # Maximum message length is 1024 bytes
                    if data:
                        # Converting the data from byte to string.
                        string_data = data.decode(encoding='utf-8')
                        if string_data == 'exit':
                            raise Exception("exit")
                        print("Received via TCP:", string_data)
                        # Sending response
                        send_data = self.get_response(string_data, client)
                        conn.sendall(bytes(send_data, encoding='utf8'))
                        print("Sent back via TCP:", send_data)

            except:
                print(f"TCP connection with client:{client} was interrupted")
                continue

    def run_udp(self):
        print("UDP Server initialized")
        while True:
            data = self.udp_socket.recvfrom(1024)  # Maximum message length is 1024 bytes
            if data:
                # Converting the data from byte to string.
                string_data = data[0].decode(encoding='utf-8')
                peer_name = data[1]
                client = peer_name[0] + str(peer_name[1])
                print("Received via UDP:", string_data)
                # Sending response
                if string_data:
                    send_data = self.get_response(string_data, client)
                    self.udp_socket.sendto(bytes(send_data, encoding='utf8'), data[1])
                    print("Sent back via UDP:", send_data)

    def run_http(self):
        print("HTTP Server initialized")
        self.http_server.serve_forever()

    def run_ftp(self):
        self.ftp_socket.listen()
        print("FTP Sever initialized")
        while True:
            conn, _ = self.ftp_socket.accept()
            try:
                while conn:
                    data = conn.recv(1024)  # Maximum message length is 1024 bytes
                    if data:
                        # Converting the data from byte to string.
                        string_data = data.decode(encoding='utf-8')
                        print("Received via FTP:", string_data)

                        # Sending response
                        peer_name = conn.getpeername()
                        client = peer_name[0] + str(peer_name[1])

                        send_data = self.get_response(string_data, client)
                        if string_data != 'receive':
                            w_stream = open("ftp_server", "w")
                            w_stream.write(send_data)
                            w_stream.close()

                        r_stream = open('ftp_server', 'r')
                        file_contents = r_stream.readlines()
                        r_stream.close()
                        string_contents = ""
                        for string in file_contents:
                            string_contents += string
                        conn.sendall(bytes(string_contents, encoding='utf8'))
                        print("Sent back via FTP:", send_data)

            except:
                continue


class HttpHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_response()

        client = self.path

        response_data = chat.get_response(post_data.decode(encoding='utf-8'), client)
        self.wfile.write(bytes(response_data, encoding='utf-8'))


chat = Chat()
if __name__ == '__main__':
    chat.run()
