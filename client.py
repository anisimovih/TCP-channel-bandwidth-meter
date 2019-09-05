import time
import csv
import socket
import global_variables


def connect_to_server(ip, port, size, filename):
    with open(filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["start_time", "end_time", "delta", "number", "size", "speed"])

        b = bytearray(int(size))
        data = bytearray(int(size))

        try:
            with socket.create_connection((ip, port)) as sock:
                # with open(filename, "a", newline='') as csv_file:
                """начало отправки данных"""
                # while True:

                "Отправка системного времени, проблема в неизвестном пинге."
                '''delta_time = str(time.time()).encode('utf-8')
                print(len(delta_time))
                for i in range(3, 21):
                    b[i] = delta_time[i-3]
                sock.sendall(b)'''

                while global_variables.thread_1_active:
                    b[0] += 1

                    time.sleep(5)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                    sock.sendall(b)


                    """Прием ответа от сервера."""
                    buf = memoryview(data)
                    save_size = size
                    start_time = time.time()
                    while save_size:
                        buf_len = sock.recv_into(buf, save_size)
                        buf = buf[buf_len:]
                        save_size -= buf_len
                        if not global_variables.thread_1_active:
                            break
                    end_time = time.time()

                    """Рассчет основных параметров."""
                    delta = format(end_time - start_time, '8f')
                    speed = float(size) / (end_time - start_time)
                    number = b[0] + b[1] * 255 + b[2] * 65025

                    graph_append_y(start_time, size, speed)  # Создание массива для нового графика.


                    """Вывод в консоль."""
                    print('start_time = {st}, end_time = {end}, delta = {dell}, '
                          'number = {num}, size = {sz}, speed = {sp}'.
                          format(st=start_time, end=end_time, dell=delta, num=number, sz=size, sp=speed))
                    results = [start_time, end_time, delta, number, size, speed]

                    """Вывод в файл."""
                    writer.writerow(results)
                    #csv_file.flush

                    '''if number == 50:
                        break'''

                    """номер пакета"""
                    if b[0] == 255:
                        b[1] += 1
                        b[0] = 0
                        if b[1] == 255:
                            b[2] += 1
                            b[1] = 0

                '''except socket.timeout:
                    print("send data timeout")
                except socket.error as ex:
                    print("send data error:", ex)'''
        except ConnectionRefusedError:
            print("wrong port")
            global_variables.termination_reason = "Подключение не удалось"
            global_variables.thread_1_active = False
            #global_variables.termination_reason = "Connection refused"

    print("client stopped")



def graph_append_y(start_time, size, speed):
    """Создание массива для нового графика."""
    '''global_variables.time_stack.append(float(start_time))
    global_variables.time_stack_end.append(float(start_time))

    if len(global_variables.time_stack) > global_variables.time_stack_length:
        global_variables.time_stack.pop(0)
        global_variables.time_stack_end.pop(0)

    if len(global_variables.time_stack) == global_variables.time_stack_length:
        stack_speed = global_variables.time_stack_end[global_variables.time_stack_length - 1] - \
                      global_variables.time_stack[0]

        # Проверка работы графика, в условиях переодического прибывания большого колличества пакетов.
        for i in range(0, 9):
            global_variables.graph_y.append((size / stack_speed * global_variables.time_stack_length) + i)
        time.sleep(2)'''

        #global_variables.graph_y.append(size / stack_speed * global_variables.time_stack_length)

    global_variables.graph_y.append(speed)


if __name__ == '__main__':
    print("Started...")
    connect_to_server("127.0.0.1", 10002, 1000, "client.csv")

