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
        if global_variables.connection_type == "TCP":
            tcp_connection(ip, port, size, b)
        else:
            udp_connection(ip, port, size, b)


def tcp_connection(ip, port, size, b):
    try:
        with socket.create_connection((ip, port)) as sock:
            while global_variables.thread_1_active:
                for i in range(3, size):
                    b[i] = random.randint(0, 255)

                increment_packet_number(b)

                sock.sendall(b)

                check_packet_limit()  # Проверка на ограничение по пакетам.

    except ConnectionRefusedError:
        print("wrong port")
        global_variables.termination_reason = "Подключение не удалось!"
        global_variables.thread_1_active = False


def udp_connection(ip, port, size, b):
    time_limit = time.time()
    try:
        with socket.socket(type=socket.SOCK_DGRAM) as sock:
            while global_variables.thread_1_active:
                for i in range(3, size):
                    b[i] = random.randint(0, 255)

                number = increment_packet_number(b)

                '''Ограничение скорости передачи'''
                udp_time = time.time() - time_limit
                while (size / udp_time) > global_variables.udp_speed:
                    time.sleep(0.001)
                    udp_time = time.time() - time_limit

                #print(size / udp_time, " > ", global_variables.udp_speed)
                sock.sendto(b, (ip, port))
                time_limit = time.time()
                print("Отправил ", number, " пакет.")
                check_packet_limit()  # Проверка на ограничение по пакетам.

    except ConnectionRefusedError:
        print("wrong port")
        global_variables.termination_reason = "Подключение не удалось!"
        global_variables.thread_1_active = False


def increment_packet_number(b):
    b[0] += 1
    if b[0] == 255:
        b[1] += 1
        b[0] = 0
        if b[1] == 255:
            b[2] += 1
            b[1] = 0
    return b[0] + b[1] * 255 + b[2] * 65025


def check_packet_limit():
    if global_variables.packet_limit is not None:  # Проверяем галку.
        if global_variables.packet_limit > 1:
            global_variables.packet_limit -= 1
        else:
            global_variables.thread_1_active = False
