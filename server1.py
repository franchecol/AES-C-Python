import socket

SOCK_BUFFER = 1024

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = ("0.0.0.0",5000)
    # server_address = ("'localhost'",'192.168.1.102')
    print(f"Iniciando servidor en {server_address[0]}, en puerto {server_address[1]}")
    sock.bind(server_address) #asociamos la direccion al socket
    #principal diferencia, el servidor hace un bind. Ata el socket a sí mismo
    
    sock.listen(5) #cuantas conexiones puedo permitir que aparezcan
    
    while True:
        print("Esperando conexiones")
        
        
        try:
            conn, client_address = sock.accept()
            print(f"Conexion de {client_address}")
            while True:
                data = conn.recv(SOCK_BUFFER)
                if data:    
                    print(f"Recibi {data} de {client_address}")
                    conn.sendall(data)
                else:
                    break
        except Exception as e:
            print(f"Sucedio algo: {e}")
        except KeyboardInterrupt:
            print("cliente cerro la sesion")
            conn.close()
        finally:
            print("cliente cerro la sesion")
            conn.close()
    