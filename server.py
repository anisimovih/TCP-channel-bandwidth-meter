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
            sock.listen(1)

            while global_variables.thread_1_active:
                conn, addr = sock.accept()  # кортеж с двумя элементами: новый сокет и адрес клиента
                print('Connected by', addr)

                with conn:
                    data = bytearray(int(size))

                    """начало приема данных"""
                    while global_variables.thread_1_active:
                        buf = memoryview(data)
                        save_size = size
                        start_time = time.time()

                        """буфер"""
                        while save_size:
                            buf_len = conn.recv_into(buf, save_size)
                            buf = buf[buf_len:]
                            save_size -= buf_len
                            if not global_variables.thread_1_active:  # Выход из бесконечного цикла при отключении клиента.
                                break
                        end_time = time.time()

                        """Выход до завершения цикла для предотвращения лишнего вывода в консоль."""
                        if not global_variables.thread_1_active:
                            break

                        """выход на ожидание новых данных при отсутствии передачи"""
                        if not data:
                            break

                        """рассчет основных параметров"""
                        delta = format(end_time - start_time, '8f')
                        speed = size / (end_time - start_time)
                        number = data[0] + data[1] * 255 + data[2] * 65025

                        graph_append_y(speed)  # Обычный график.
                        # graph_append_y_average(start_time, size)  # Усредненный график.

                        print('start_time = {st}, end_time = {end}, delta = {dell}, number = {num}, size = {sz}, speed = {sp}'.
                              format(st=start_time, end=end_time, dell=delta, num=number, sz=size, sp=speed))
                        results = [start_time, end_time, delta, number, size, speed]  # Переменная для записи в CSV.

                        writer.writerow(results)  # Вывод в файл.
                        time.sleep(0.5)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        conn.send(data)  # Отвечаем клиенту.

        #sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        global_variables.termination_reason = "Прием данных остановлен"
        print("server closed")


def graph_append_y(speed):
    """Создание массива для нового графика."""
    global_variables.graph_y.append(speed)


def graph_append_y_average(start_time, size):
    """Создание массива для нового графика."""
    global_variables.time_stack.append(float(start_time))
    global_variables.time_stack_end.append(float(start_time))

    if len(global_variables.time_stack) > global_variables.time_stack_length:
        global_variables.time_stack.pop(0)
        global_variables.time_stack_end.pop(0)

    if len(global_variables.time_stack) == global_variables.time_stack_length:
        stack_speed = global_variables.time_stack_end[global_variables.time_stack_length - 1] - \
                      global_variables.time_stack[0]

        # Проверка работы графика, в условиях переодического прибывания большого колличества пакетов.
        '''for i in range(0, 9):
            global_variables.graph_y.append((size / stack_speed * global_variables.time_stack_length) + i)
        time.sleep(2)'''

        global_variables.graph_y.append(size / stack_speed * global_variables.time_stack_length)


if __name__ == '__main__':
    print("Started...")
    connect_to_client(10002, 1000, "server.csv")
