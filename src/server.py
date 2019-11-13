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

        if global_variables.connection_type == "TCP":
            tcp_reception(port, size, writer)
        else:
            udp_reception(port, size, writer)


def tcp_reception(port, size, writer):
    first = True
    """ожидание подключения"""
    with socket.socket() as sock:
        sock.bind(("", port))
        sock.listen(1)

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

                """Выход из цикла без вывода данных."""
                if global_variables.server_break or not data:
                    break

                """Рассчет основных параметров."""
                delta = format(end_time - start_time, '8f')
                number = data[0] + data[1] * 255 + data[2] * 65025
                if global_variables.very_first_time is not None:
                    speed = smoothing_graph('tcp', start_time, end_time, size, number)

                    save_data(start_time, end_time, delta, number, speed, size, writer)

                '''if number == size:
                    Graph.draw_graph(graph)
                    global_variables.thread_1_active = False
                    global_variables.termination_reason = "Прием данных завершен."'''

    sock.close()
    global_variables.server_break = False
    if global_variables.termination_reason == '':
        global_variables.termination_reason = "Прием данных прерван!"


def save_buffer(buf, save_size, conn):
    """Буфер (нужен для обхода разделения пакетов TCP)."""
    start_time = time.time()
    while save_size:
        try:
            buf_len = conn.recv_into(buf, save_size)
        except socket.error as e:
            print(e)
            global_variables.thread_1_active = False
            global_variables.server_break = True
            break
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
    last_number = 0

    """ожидание подключения"""
    with socket.socket(type=socket.SOCK_DGRAM) as sock:
        sock.bind(("", port))
        while global_variables.thread_1_active:

            start_time = time.time()
            if not first:
                if global_variables.very_first_time is None:
                    global_variables.very_first_time = time.time()
            try:
                message = sock.recv(size)
            except socket.error as e:
                print(e)
                global_variables.thread_1_active = False
                break

            end_time = time.time()
            first = False

            number = message[0] + message[1] * 255 + message[2] * 65025 - 1  # Номер из пакета.
            real_number += 1  # Реальное числополученных пакетов

            if global_variables.very_first_time is not None and global_variables.thread_1_active:
                if number > last_number:  # Если пакет застрял, то мы его не отображаем (график только возрастает по x).
                    delta = format(end_time - start_time, '8f')
                    speed = smoothing_graph('udp', start_time, end_time, size, number, real_number)
                    last_number = number

                    save_data(start_time, end_time, delta, number, speed, size, writer)

    sock.close()
    if global_variables.termination_reason == '':
        global_variables.termination_reason = "Прием данных прерван!"


def smoothing_graph(connection_type, start_time, end_time, size, number, real_number=None):
    total_delta = end_time - global_variables.very_first_time  # Суммарное время.
    if connection_type == 'tcp':
        total_amount = number * size  # Суммарный объем.
    else:
        total_amount = real_number * size  # В случе UDP нужно учитывать только дошедшие пакеты.

    speed = total_amount / total_delta * 8  # Средняя скорость в битах.
    instant_speed = size / (end_time - start_time) * 8  # Скорость по одному пакету.
    # print("Пакет ", number, " средняя скорость: ", speed, "единичная скорость:", instant_speed, " (бит/сек)")

    if instant_speed < Graph.speed_limit:
        Graph.graph_x = np.append(Graph.graph_x, number)
        Graph.graph_y = np.append(Graph.graph_y, speed)
        Graph.normal_speeds_quantity += 1
    return speed


def save_data(start_time, end_time, delta, number, speed, size, writer):
    """Вывод в консоль и сохранение в файл"""
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
                 sz=number,
                 sp=speed))
    results = [start_time, end_time, delta, number, size, speed]
    writer.writerow(results)  # Вывод в файл.
