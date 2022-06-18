import socket
import cv2
import numpy as np
from PIL import Image





def negativo_im(array_in,T,array_out):
    for i in range(T):
        array_out[i] = 255-array_in[i]
        
        

n = 0
SOCK_BUFFER = 1024

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 5005
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while n <1:
            print("Esperando conexiones")
            conn,addr = s.accept()
            with conn:
                print(f'Conectado por{addr}')
                data0 = conn.recv(SOCK_BUFFER)
                if not data0:
                    break
                decode_data0 = int(data0.decode("utf-8"))
                print(f"valor longitud data0 es {decode_data0}")

                data = conn.recv(decode_data0)
                if not data:
                    break
                bytes = bytearray(data)
                print(f"longitud de bytes es:{len(bytes)}")
                numpyarray = np.asarray(bytes, dtype=np.ubyte)
                print(f"longitud de numpyarray es:{len(numpyarray)}")
                bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_GRAYSCALE)
                print(f"longitud de bgrImage es:{len(bgrImage)}")
                arr1 = bgrImage.shape
                print(f"printeamos bgr {bgrImage}")
                print(f"shape de bgr es {arr1}")
                im = Image.fromarray(bgrImage)

                im.save("Imagen_original.jpeg")
                array_flatten = bgrImage.flatten()    
                print(f"longitud de array_flatten {len(array_flatten)}")
                """628*564 = 35492"""
                T = len(array_flatten)
                array_result_py = np.zeros((len(array_flatten),1),dtype=np.ubyte)
                negativo_im(array_flatten,T,array_result_py)
                im_py_neg = array_result_py.tobytes()
                print(f"longitud de bytes de imagen {len(im_py_neg)}")
                im_py = Image.fromarray(array_result_py.reshape(arr1))
                im_py.save("Imagen_negativa_Py.jpeg") 
            print("Finalizando conexiones")                
            n+=1                              