from PySide6.QtCore import QThread,Signal
import socket
import random as rnd
""" 
Thread - класс основным потоком отрабатывающим основную логику сервера
В данном потоке реализована передача данных в основное окно и связь между сервером и клиентом.
Добавлена функции завершения основного цикла для отключения заранее самого потока.
"""
class Thread(QThread):
    max_number = 1000
    max_attempts = 10
    NEWLINE = '\r\n'
    data_to_process = None
    client_conn  = None
    client_addr = None
    sig_Chat = Signal(str)
    

    def __init__(self,flag):
        super().__init__()
        self.running = flag

    def run(self):
        counter = 0
        server = socket.socket()
        server.bind(('127.0.0.1', 7777))
        server.listen()
        secret_number = rnd.randint(0, self.max_number)
        self.client_conn, self.client_addr = server.accept()
        self.client_conn.send((f'Я выбрал целое число между 0 и {self.max_number}. '
                    f'Сможешь ли ты его угадать{self.NEWLINE}Присылай мне свои попытки. '
                    f'У тебя осталось {self.max_attempts - counter} попыток.{self.NEWLINE}').encode())
        while self.running:

            data = ''
            msg = ''
            skip = False
            data = self.client_conn.recv(1024)
            if data:
                msg += data.decode()
            self.sig_Chat.emit(f"Игра обработала ввод: {msg}") 
            if msg == "стоп\r\n":
                skip = True
                self.stop()
            elif msg =="\r\n":
                msg = f'Вы не прислали ничего.Введите число.{self.NEWLINE}'
                self.sig_Chat.emit(f" {msg}")
                skip = True
            else:
                try:
                    guess = int(msg)
                except ValueError as verr:
                    msg = f'Вы ввели {msg} что не явлется подходящим числом. Пробуйте еще раз.{self.NEWLINE}'
                    skip = True
                except Exception as ex:
                    msg = f'Была совершена ошибка при вводе {msg}. Игра остановлена.{self.NEWLINE}'
                    skip = True
                    self.stop()
            if not skip:
                counter += 1
                if guess == secret_number:
                    msg = f'Победа! Вы угадали число за {counter} попытки(ок). Число было {secret_number}.{self.NEWLINE}'
                    self.stop()
                else:
                    if guess < secret_number:
                        msg = f'Число больше, чем введенное! У вас осталось {self.max_attempts - counter} попыток.{self.NEWLINE}'
                    else:
                        msg = f'Число меньше, чем введенное! У вас осталось {self.max_attempts - counter} попыток.{self.NEWLINE}'

                if self.running and counter >= self.max_attempts:
                    self.stop()
                    msg = f'Извините, но вы потратили все {self.max_attempts} попыток и так и не угадали число верно.' \
                            f'{self.NEWLINE}Число было {secret_number}. Удачи в следующий раз!{self.NEWLINE}'

            self.client_conn.send(msg.encode())
        self.sig_Chat.emit("Игра остановлена.")
        self.client_conn.close() 
    def stop(self):
        self.running = False