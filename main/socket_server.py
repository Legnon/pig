import socket


def run_server(port=4000, input_data="2:10"):
    host = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        msg = conn.recv(1024)
        print("Local : " + msg.decode())
        inp = input("Django server : ")
        conn.sendall(inp.en4)
        print("Local : " + msg.decode())
        conn.close()

        return msg.decode()

