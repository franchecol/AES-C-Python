#servidor_aes_final.py
import socket
import numpy as np
import cv2
import time
import ctypes
from ctypes import *
from PIL import Image
import aes_lib
import os
aes_c = CDLL(os.path.join(os.path.dirname(__file__), "aes_c_lib.so"))
aes_c.make_key()
from statistics import mean
import matplotlib.pyplot as plt
import statistics
master_key = 0x6672616e636f67656e61726f78617669
llave = aes_lib.make_key(master_key)


tot_decrypted = []
tot_decrypted_c = []
decrypted_to_bytes = [] 
decrypted_to_bytes_c = []
n = 0
SOCK_BUFFER = 32768

def filtro_mediana(sign, ventana):
    signc = []
    tam = len(sign)
    offs = int((ventana-1)/2)
    for i in range(tam):
        inicio = i - offs if (i - offs > 0) else i
        fin = i + offs if (i + offs < tam) else tam
        signc.append(statistics.median(sign[inicio:fin]))
    return signc

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
                "recibe longitud de imagen"
                print(f'Conectado por{addr}')
                data0 = conn.recv(SOCK_BUFFER)#0
                decode_data0 = int(data0.decode("utf-8"))
                SOCK_BUFFER = decode_data0

                "Recibimos  la cantidad de bloques de 128 bits que se encriptarán de la imagen"
                data1 = conn.recv(SOCK_BUFFER)#1
                len_encrypted = data1
                
                "recibimos los datos encriptados en python"
                inicio=time.perf_counter()
                data2 = conn.recv(SOCK_BUFFER)#2
                fin=time.perf_counter()
                print(f"Tiempo para recibir los datos encriptados: \n {fin-inicio}")
                print("data2",len(data2))
                
                "recibimos los datos encriptados en c"
                data3 = conn.recv(SOCK_BUFFER)#3
                print("data3",len(data3))
                
                # Debug: Check if data2 and data3 are identical
                if data2 == data3:
                    print("✓ Python and C encrypted data match")
                else:
                    print(f"✗ WARNING: Encrypted data mismatch! Diff bytes: {sum(1 for a,b in zip(data2,data3) if a!=b)}")

                time_decrypt_py = []
                time_decrypt_c = []

                
                "bits to int"
                "split into 128 bits blocks"
                image_int = int.from_bytes(data2, "big")  
                data_split =aes_lib.split_bits(image_int,128)   
                image_int_c = int.from_bytes(data3, "big") 
                data_split_c = aes_lib.split_bits(image_int_c,128)
                
                print(f"Number of blocks to decrypt: {len(data_split)} (Python), {len(data_split_c)} (C)")          
                "Desencriptamos los datos recibidos"
                # Initialize C key once before decryption loop
                aes_c.make_key()
                inicio1=time.perf_counter() 
                for i in range(len(data_split)):
                    # For C decryption: convert encrypted block to byte array
                    data_split_8_c = aes_lib.split_bits(data_split_c[i], 8)
                    vectory = np.asarray(data_split_8_c).astype('int32')
                    arr1 = (ctypes.c_ubyte * len(vectory))(*vectory)
                    start1 = time.time()
                    res2 = aes_c.decrypt(arr1)
                    end1 = time.time()
                    tiempo1 = end1-start1
                    time_decrypt_c.append(tiempo1)
                    
                    # Convert decrypted bytes to int
                    decrypt_c_str = ','.join(map(str, arr1))
                    decrypt_c = aes_lib.str_to_int(decrypt_c_str)
                    
                    # Debug: print first few blocks
                    if i < 3:
                        print(f"C decrypt block {i}: {hex(decrypt_c)}, expected: {hex(data_split_orig[i]) if 'data_split_orig' in dir() else 'N/A'}")

                    start2 = time.time()
                    decrypted = aes_lib.decrypt(data_split[i],llave)  
                    end2 = time.time()
                    tiempo2 = end2 - start2
                    time_decrypt_py.append(tiempo2)
                    tot_decrypted.append((decrypted))          
                    tot_decrypted_c.append((decrypt_c))      
                fin1=time.perf_counter()
                print(f"Tiempo para desencriptar los datos recibidos: \n{fin1-inicio1} "  )
              
                " arreglo de bytes de datos desencriptados"
                for i in range(len(tot_decrypted)):
                    decrypted_to_bytes.append(tot_decrypted[i].to_bytes(16, 'big')) 
                    decrypted_to_bytes_c.append(tot_decrypted_c[i].to_bytes(16,'big'))
                image_decrypted_bits = (b''.join(decrypted_to_bytes))
                image_decrypted_bits_c = (b''.join(decrypted_to_bytes_c))
                
                
                
                "recibimos los datos de los headers en bits"
                
                data4 = conn.recv(SOCK_BUFFER)#4
                header_bits = data4 
                index = range(len(data_split))
                "join header con datos desencriptados"
                image_total_decrypted = b''.join([header_bits,image_decrypted_bits])
                image_total_decrypted_c = b''.join([header_bits,image_decrypted_bits_c])
                bytes_decrypted = bytearray(image_total_decrypted)                
                bytes_decrypted_c = bytearray(image_total_decrypted_c)
                print(f"longitud de bytes: {len(bytes_decrypted)}")
                print(f"longitud de bytes_c: {len(bytes_decrypted_c)}")

                "guardamos la imagen desencriptada (raw bytes con header BMP)"
                inicio2=time.perf_counter()
                # Save decrypted data directly as BMP files (header + decrypted pixel data)
                with open("Imagen_desencriptada_servidor_tux_py.bmp", "wb") as f:
                    f.write(bytes_decrypted)
                with open("Imagen_desencriptada_servidor_tux_c.bmp", "wb") as f:
                    f.write(bytes_decrypted_c)
                fin2=time.perf_counter()    
                print(f"Tiempo para imprimir la imagen desencriptada: \n{fin2-inicio2}")         
                ltb2 = (filtro_mediana(time_decrypt_py[:100],3))

                plt.plot(index[:100],ltb2[:100],label = 'tiempos en py')
                plt.plot(index[:100],time_decrypt_c[:100],label = "tiempos en c")
                plt.xlabel("ejecuciones")
                plt.ylabel("tiempos")
                plt.tight_layout()
                plt.legend()    
                plt.savefig("tiempos_desencriptación.png",dpi = 500)
                plt.close


                plt.plot(mean(time_decrypt_py[100:])/mean(time_decrypt_c[100:]),'-ro',label='speedup')
                plt.xlabel('N')
                plt.ylabel('Speedup')
                plt.legend()
                plt.savefig("tiempos_promedios de desencriptacion3.png",dpi = 500)  
            n+=1                              