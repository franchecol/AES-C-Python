# 1) without using with statement
file = open('file_path', 'w')
file.write('hello world !')
file.close()
# using with statement

with open('file_path', 'w') as file:
    file.write('hello world !')
    

print("hola")

"""    
Notice that unlike the first two implementations, there is no need to call 
file.close() when using with statement. The with statement itself ensures
proper acquisition and release of resources.  
  
  The with statement is popularly used with file streams,
as shown above and with Locks, sockets, subprocesses and telnets etc.
"""