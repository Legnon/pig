import socket

def run_server(port=4000):
  host = ''
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    print("receving")
    while True:
        msg = conn.recv(1024)
        print("Local : " + msg.decode())
        inp = input("Django server : ")
        conn.sendall(inp.encode())
    
    conn.close()

if __name__ == '__main__':
  run_server()
