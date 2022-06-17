import http.client
import sys

HTTP_IP = '127.0.0.1'
HTTP_PORT = 8002
BUFFER_SIZE = 1024
message = "Hello, World! FROM HTTP "
URL = HTTP_IP + ":" + str(HTTP_PORT)

if __name__ == '__main__':
    conn = http.client.HTTPConnection(HTTP_IP, HTTP_PORT)
    print("Connection successful")



    # print("Sent:", str(message))
    # print("Received:", response_str)

    while True:
        conn.request("GET", URL, bytes(message, encoding='utf8'))
        response = conn.getresponse()
        response_str = response.read().decode("utf-8")
        # data = s.send(bytes(message, encoding='utf8'))
        if message == 'exit':
            break
        # response = s.recv(BUFFER_SIZE)
        # response_str = response.decode("utf-8")
        print(response_str)
        message = sys.stdin.readline().strip('\n')

    conn.close()
