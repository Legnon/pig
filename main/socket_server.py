import socket


def run_server(port=4001, input_data="2:10"):
    host = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        msg = conn.recv(1024)
        print("Local : " + msg.decode())
        conn.sendall(input_data.encode())
        msg = conn.recv(1024)
        print("Local : " + msg.decode())
        message = msg.decode()
        conn.close()
        print(message)

        return message


if __name__ == "__main__":
    run_server()
