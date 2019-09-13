import socket
import time
import csv
import global_variables


def connect_to_client(port, size, filename):
    with open(filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["start_time", "end_time", "delta", "number", "size", "speed"])

        """ожидание подключения"""
        with socket.socket() as sock:
            sock.bind(("", port))
            sock.listen()

            while global_variables.thread_1_active:
                conn, addr = sock.accept()  # кортеж с двумя элементами: новый сокет и адрес клиента
                print('Connected by', addr)

                with conn:
                    data = bytearray(int(size))

                    """Начало приема данных."""
                    while global_variables.thread_1_active:
                        buf = memoryview(data)
                        save_size = size

                        """Буфер (нужен для обхода разделения пакетов TCP)."""
                        start_time = time.time()
                        if global_variables.very_first_time is None:
                            global_variables.very_first_time = start_time
                        while save_size:
                            buf_len = conn.recv_into(buf, save_size)
                            buf = buf[buf_len:]
                            save_size -= buf_len
                            if global_variables.thread_1_active == False:
                                break
                            # print('received ', 100/size*(size-save_size),'%')
                        end_time = time.time()

                        """Выход на ожидание новых данных при отсутствии передачи."""
                        if not data:
                            break

                        """Рассчет основных параметров."""
                        delta = format(end_time - start_time, '8f')
                        size = size
                        number = data[0] + data[1] * 255 + data[2] * 65025
                        #speed = graph_append_y_only(number, start_time, end_time, size)
                        speed = graph_all_y(number, start_time, end_time, size)

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

        #sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        global_variables.termination_reason = "Прием данных остановлен"


'''def graph_append_y_only(number, start_time, end_time, size):
    delta = end_time - global_variables.very_first_time
    recv_amount = number * size
    speed = recv_amount / delta
    if (end_time - start_time) > 0.01:
        global_variables.graph_y_only.append([number, speed])
        print(global_variables.graph_y_only)
    return speed'''


def graph_all_y(number, start_time, end_time, size):
    delta = end_time - global_variables.very_first_time
    recv_amount = number * size
    speed = recv_amount / delta
    global_variables.graph_y.append(delta)
    #global_variables.graph_y.append(speed)
    return speed


def graph_all_y_2(number, start_time, end_time, size):
    delta = end_time - global_variables.very_first_time
    recv_amount = number * size
    speed = recv_amount / delta
    return speed


if __name__ == '__main__':
    print("Started...")
    connect_to_client(10002, 1000, "server.csv")
