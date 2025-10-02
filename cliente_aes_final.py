#cliente_aes_final.py
import socket
import numpy as np
import cv2
import time
import ctypes
from ctypes import *
from PIL import Image
import aes_lib
import statistics
from statistics import mean
import matplotlib.pyplot as plt
from numpy import asarray
import os
aes_c = CDLL(os.path.join(os.path.dirname(__file__), "aes_c_lib.so"))
# Declare ctypes signatures explicitly to avoid ABI/FFI issues
aes_c.make_key.restype = None
aes_c.encrypt.argtypes = [POINTER(c_ubyte)]
aes_c.encrypt.restype = c_ubyte
aes_c.decrypt.argtypes = [POINTER(c_ubyte)]
aes_c.decrypt.restype = c_ubyte
"CLiente encripta la imagen y envía la imagen encriptada al servidor"
aes_c.make_key()

# Simple binary framing helpers
def send_u64(sock, value:int):
    sock.sendall(int(value).to_bytes(8, 'big'))

def send_u32(sock, value:int):
    sock.sendall(int(value).to_bytes(4, 'big'))

def filtro_mediana(sign, ventana):
    signc = []
    tam = len(sign)
    offs = int((ventana-1)/2)
    for i in range(tam):
        inicio = i - offs if (i - offs > 0) else i
        fin = i + offs if (i + offs < tam) else tam
        signc.append(statistics.median(sign[inicio:fin]))
    return signc



# llave de 16 bits
master_key = 0x6672616e636f67656e61726f78617669

llave = aes_lib.make_key(master_key)   

if __name__ == "__main__":
    
    llave = aes_lib.make_key(master_key)
        
    tot_encrypted = []
    tot_encrypted_c = []
    encrypted_to_bytes = []	
    encrypted_to_bytes_c = []	
    header_to_bytes = []
    
    time_encrypt_py = []
    time_encrypt_c = []
    time_py_median = []
    time_c_median = []
    HOST = "127.0.0.1"
    PORT = 5005
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))        
        im = open("tux.bmp","rb")
        l = im.read()
        lenght_image = len(l)
        print(f"longitud de la imagen {lenght_image}")
 
        # "Convertimos la imagen de formato byte a hexadecimal"        
        # hexadecimal_string = l.hex()
        # "Convertimos de formato hexadecimal a integer"
        # str_to_int = int(hexadecimal_string, 16)        
        "Separamos la data de la imagen en Bits de Headers y Bits de data(píxeles)"
        
        "Bits de headers"
        header_bits = l[:54]
        "Bits de data(píxeles)"
        image_bits = l[54:]
        
        
        

        
        "Convertimos los píxeles a a integer"
        image_int = int.from_bytes(image_bits, "big")  
        "El formato AES encripta en bloques de 128 bits"
        data_split =aes_lib.split_bits(image_int,128)
        len_data_split = str(len(data_split)).encode("utf-8")
        "Envíamos la cantidad de bloques de 128 bits que se encriptarán de la imagen"            
        send_u32(s, len(data_split)) #1 (binary, robust)
        "Tenemos un arreglo de int de datos encriptados"
        
        # Initialize C key once before encryption loop
        aes_c.make_key()

        for i in range(len(data_split)):
            
            data_split_8= aes_lib.split_bits(data_split[i],8)
            vectorx = np.asarray(data_split_8).astype('int32')
            arr = (ctypes.c_ubyte * len(vectorx))(*vectorx)
            start1 = time.time()
            res1 = aes_c.encrypt(arr)
            end1 = time.time()
            tiempo1 = end1 - start1
            time_encrypt_c.append(tiempo1)
            # Read encrypted block bytes directly from ctypes buffer
            encrypt_c = int.from_bytes(bytearray(arr), 'big')
            start2 = time.time()
            encrypted = aes_lib.encrypt(data_split[i],llave)
            end2 = time.time()
            tiempo2 = end2 - start2
            time_encrypt_py.append(tiempo2)
            tot_encrypted.append(encrypted)
            tot_encrypted_c.append(encrypt_c)    

        " arreglo de bytes de datos encriptados"
        for i in range(len(tot_encrypted)):
            encrypted_to_bytes.append(tot_encrypted[i].to_bytes(16, 'big')) 
            encrypted_to_bytes_c.append(tot_encrypted_c[i].to_bytes(16, 'big'))
        image_encrypted_bits = (b''.join(encrypted_to_bytes))
        image_encrypted_bits_c = (b''.join(encrypted_to_bytes_c))
        "enviamos datos encriptados en python" 
        inicio= time.perf_counter()
        s.sendall(image_encrypted_bits) #2
        fin=time.perf_counter()
        
        "enviamos datos encriptados en c"
        s.sendall(image_encrypted_bits_c) #3
        print(f"Tiempo para enviar datos encriptados: \n{fin-inicio}")

        "enviamos la informacion del header"

        
        s.sendall(header_bits) #4
       
        index = range(len(data_split))
        "join header con datos encriptados"
        image_total_encrypted = b''.join([header_bits,image_encrypted_bits])
        bytes_encripted = bytearray(image_total_encrypted)
        
        image_total_encrypted_c = b''.join([header_bits,image_encrypted_bits_c])
        bytes_encripted_c = bytearray(image_total_encrypted_c)
        print(f"longitud de bytes en Python: {len(bytes_encripted)}")
        print(f"longitud de bytes en C : {len(bytes_encripted_c)}")

           
        "guardamos la imagen encriptada (raw bytes, no decodificar)"
        inicio1=time.perf_counter()
        # Save encrypted data directly as BMP files (header + encrypted pixel data)
        with open("Imagen_encriptada_cliente_py.bmp", "wb") as f:
            f.write(bytes_encripted)
        with open("Imagen_encriptada_cliente_c.bmp", "wb") as f:
            f.write(bytes_encripted_c)
        fin1=time.perf_counter()
        print(f"Tiempo de recibir e imprimir la imagen encriptada: \n{fin1-inicio1}")    
       
    ltb2 = (filtro_mediana(time_encrypt_py[:100],4))

    plt.plot(index[:100],ltb2[:100],label = 'tiempos en py')
    plt.plot(index[:100],time_encrypt_c[:100],label = "tiempos en c")
    plt.xlabel("ejecuciones")
    plt.ylabel("tiempos")
    plt.tight_layout()
    plt.legend()    
    plt.savefig("tiempos_encryptacion.png",dpi = 500)
    plt.close
    

    plt.plot(mean(time_encrypt_py[100:])/mean(time_encrypt_c[100:]),'-ro',label='speedup')
    plt.xlabel('N')
    plt.ylabel('Speedup')
    plt.legend()
    plt.savefig("tiempos_promedios de encriptacion3.png",dpi = 500)      
     
