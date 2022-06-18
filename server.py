import socket
import numpy as np
from PIL import Image
import cv2
import ctypes

def negativo_im(array_in,T,array_out):
    for i in range(T):
        array_out[i] = 255-array_in[i]

if __name__ == "__main__":
    HOST = '127.0.0.1'  # (localhost)
    PORT = 5005      # Puerto a     escuchar
    # libfile = './negativo.so'
    # lib = ctypes.CDLL(libfile)
    # lib.negativo_im_c.argtypes = [np.ctypeslib.ndpointer(dtype=np.ubyte),
    #     ctypes.c_int, np.ctypeslib.ndpointer(dtype=np.ubyte)]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        n = 0
        while n<1:
            conn, addr = s.accept()
            with conn:
                print('Conectado por', addr)
                data = conn.recv(32768)
                if not data:
                    break
                bytes = bytearray(data)
                numpyarray = np.asarray(bytes, dtype=np.ubyte)
                bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_GRAYSCALE)
                im = Image.fromarray(bgrImage)
                im.save("Imagen_original.jpeg")
                array_flatten = bgrImage.flatten()
                
                T = len(array_flatten)
                array_result_py = np.zeros((len(array_flatten),1),dtype=np.ubyte)
                # array_result_C = np.zeros((len(array_flatten),1),dtype=np.ubyte)
                
                negativo_im(array_flatten,T,array_result_py)
                im_py_neg = array_result_py.tobytes()
                
                conn.sendall(im_py_neg)
                im_py = Image.fromarray(array_result_py.reshape(256,256))
                im_py.save("Imagen_negativa_Py.jpeg")
                # lib.negativo_im_c(array_flatten,T,array_result_C)
                # im_C_neg = array_result_C.tobytes()
                # conn.sendall(im_C_neg)

                # im2 = Image.fromarray(array_result_C.reshape(256,256))
                # im2.save("Imagen_negativa_C.jpeg")
                n = n+1                

