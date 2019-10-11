import time
import random
import csv
import socket

from src import global_variables


def connect_to_server(ip, port, size, filename):
    with open(filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["start_time", "end_time", "delta", "number", "size", "speed"])

        b = bytearray(size)

        try:
            with socket.create_connection((ip, port)) as sock:
                while global_variables.thread_1_active:
                    for i in range(3, size):
                        b[i] = random.randint(0, 255)

                    """номер пакета"""
                    b[0] += 1
                    if b[0] == 255:
                        b[1] += 1
                        b[0] = 0
                        if b[1] == 255:
                            b[2] += 1
                            b[1] = 0

                    sock.sendall(b)

                    check_packet_limit()  # Проверка на ограничение по пакетам.

                    '''start_time = time.time()
                    sock.sendall(b)
                    end_time = time.time()

                    check_packet_limit()  # Проверка на ограничение по пакетам.

                    """рассчет основных параметров"""
                    delta = format(end_time - start_time, '8f')
                    speed = float(size) / (end_time - start_time)
                    number = b[0] + b[1] * 255 + b[2] * 65025

                    """Вывод в консоль."""
                    print('start_time = {st}, end_time = {end}, delta = {dell}, '
                          'number = {num}, size = {sz}, speed = {sp}'.
                          format(st=start_time, end=end_time, dell=delta, num=number, sz=size, sp=speed))
                    results = [start_time, end_time, delta, number, size, speed]

                    """Вывод в файл."""
                    writer.writerow(results)'''

                '''except socket.timeout:
                    print("send data timeout")
                except socket.error as ex:
                    print("send data error:", ex)'''
        except ConnectionRefusedError:
            print("wrong port")
            global_variables.termination_reason = "Подключение не удалось!"
            global_variables.thread_1_active = False


def check_packet_limit():
    if global_variables.packet_limit is not None:  # Проверяем галку.
        if global_variables.packet_limit > 1:
            global_variables.packet_limit -= 1
        else:
            global_variables.thread_1_active = False
