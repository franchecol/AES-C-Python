import socket
import numpy as np
from PIL import Image

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5005
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        im = open("lena.jpg","rb")
        l = im.read(256*256)
        s.sendall(l)
        images_t = []
        while True:
            #im_rx recibe datos del servidor
            im_rx = s.recv(32768)
            if not im_rx:
                break
            else:
                im1 = bytearray(im_rx)
                #extend agrega a la lista images_t el arreglo im1
                images_t.extend(im1)
                
        array_Py = np.asarray(images_t[0:256*256], dtype=np.ubyte)
        im_py_rx = Image.fromarray(array_Py.reshape(256,256))
        im_py_rx.save("RX_neg_lena_Py.jpeg")
        
        array_C = np.asarray(images_t[256*256:], dtype=np.ubyte)
        im_py_rx = Image.fromarray(array_C.reshape(256,256))
        im_py_rx.save("RX_neg_lena_C.jpeg")
        