import socket
import time
import csv

import numpy as np

from src import global_variables
from src.graph import Graph


def connect_to_client(port, size, filename, graph):
    with open(filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["start_time", "end_time", "delta", "number", "size", "speed"])

        # tcp_reception(port, size, writer)
        udp_reception(port, size, writer)


def tcp_reception(port, size, writer):
    first = True
    """ожидание подключения"""
    with socket.socket() as sock:
        sock.bind(("", port))
        sock.listen(1)

        while global_variables.thread_1_active:
            conn, addr = sock.accept()  # кортеж с двумя элементами: новый сокет и адрес клиента
            print('Connected by', addr)

            with conn:
                data = bytearray(int(size))

                """Начало приема данных."""
                while global_variables.thread_1_active:
                    buf = memoryview(data)

                    """Определяем время начала приема, начиная со второго пакета."""
                    if not first:
                        if global_variables.very_first_time is None:
                            global_variables.very_first_time = time.time()

                    start_time, end_time = save_buffer(buf, size, conn)

                    first = False

                    """Выход на ожидание новых данных при отсутствии передачи."""
                    if not data or global_variables.server_break:
                        break

                    """Рассчет основных параметров."""
                    delta = format(end_time - start_time, '8f')
                    number = data[0] + data[1] * 255 + data[2] * 65025
                    if global_variables.very_first_time is not None:
                        speed = smoothing_graph(number, start_time, end_time, size)

                        """Вывод в консоль."""
                        print('start_time = {st}, '
                              'end_time = {end}, '
                              'delta = {dell}, '
                              'number = {num}, '
                              'size = {sz}, '
                              'speed = {sp}'.
                              format(st=start_time,
                                     end=end_time,
                                     dell=delta,
                                     num=number,
                                     sz=size,
                                     sp=speed))
                        results = [start_time, end_time, delta, number, size, speed]
                        writer.writerow(results)  # Вывод в файл.

                    '''if number == size:
                        Graph.draw_graph(graph)
                        global_variables.thread_1_active = False
                        global_variables.termination_reason = "Прием данных завершен."'''

    sock.close()
    if global_variables.termination_reason == '':
        global_variables.termination_reason = "Прием данных прерван!"


def save_buffer(buf, save_size, conn):
    """Буфер (нужен для обхода разделения пакетов TCP)."""
    start_time = time.time()
    while save_size:
        buf_len = conn.recv_into(buf, save_size)
        buf = buf[buf_len:]
        save_size -= buf_len
        if not global_variables.thread_1_active:  # Выход из бесконечного цикла при отключении клиента.
            global_variables.server_break = True
            break
        # print('received ', 100/size*(size-save_size),'%')
    end_time = time.time()
    return start_time, end_time


def udp_reception(port, size, writer):
    first = True
    real_number = -1

    """ожидание подключения"""
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
        sock.bind(("", port))
        while global_variables.thread_1_active:

            start_time = time.time()
            if not first:
                if global_variables.very_first_time is None:
                    global_variables.very_first_time = time.time()
            message, address = sock.recvfrom(size)
            end_time = time.time()
            first = False

            number = message[0] + message[1] * 255 + message[2] * 65025 - 1
            real_number += 1
            # speed = number * size / (time.time() - global_variables.very_first_time) * 8
            # print("Скорость на ", number, " пакете: ", speed, " бит/сек")

            if global_variables.very_first_time is not None:
                udp_smoothing_graph(number, real_number, start_time, end_time, size)

    sock.close()
    if global_variables.termination_reason == '':
        global_variables.termination_reason = "Прием данных прерван!"


def smoothing_graph(number, start_time, end_time, size):
    total_delta = end_time - global_variables.very_first_time
    total_amount = number * size
    speed = total_amount / total_delta * 8
    instant_speed = size / (end_time - start_time)
    '''if number % 10 == 0:
        speed = 20000'''

    if instant_speed < Graph.speed_limit:
        Graph.graph_x = np.append(Graph.graph_x, number)
        Graph.graph_y = np.append(Graph.graph_y, speed)
        Graph.normal_speeds_quantity += 1
    return speed


def udp_smoothing_graph(number, real_number, start_time, end_time, size):
    total_delta = end_time - global_variables.very_first_time
    total_amount = real_number * size
    speed = total_amount / total_delta * 8
    instant_speed = size / (end_time - start_time) * 8
    print("Пакет ", number, " средняя скорость: ", speed, "единичная скорость:", instant_speed, " (бит/сек)")
    print("speed = ", speed)
    print("instant_speed = ", instant_speed)
    '''if number % 10 == 0:
        speed = 20000'''

    if instant_speed < Graph.speed_limit:
        Graph.graph_x = np.append(Graph.graph_x, number)
        Graph.graph_y = np.append(Graph.graph_y, speed)
        Graph.normal_speeds_quantity += 1
    return speed
