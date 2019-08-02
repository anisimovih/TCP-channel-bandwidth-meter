"""
python3.6 lexius_client.py --p 10002 --f client.csv --s 1000 --ip 192.168.10.196
python3.6 server.py --p 10002 --f server.csv --s 10000
"""

import socket
import time
import csv
import global_variables


"""функция тестирования скорости сети с графиками"""
def connect_to_client(port, size, filename):
    with open(filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["start_time", "end_time", "delta", "number", "size", "speed"])

        """ожидание подключения"""
        with socket.socket() as sock:
            sock.bind(("", port))
            sock.listen()
            while True:
                conn, addr = sock.accept()  # кортеж с двумя элементами: новый сокет и адрес клиента
                print('Connected by', addr)

                """переменные дляя графики"""
                '''line = []
                graph = plt.subplot()
                graph.set_xlabel('Номер пакета')
                graph.set_ylabel('скорость(Байт/сек)')'''

                with conn:
                    data = bytearray(int(size))
                    #with open(filename, "a", newline='') as csv_file:

                    """начало приема данных"""
                    while True:
                        buf = memoryview(data)
                        save_size = size
                        start_time = time.time()

                        """буфер"""
                        while save_size:
                            buf_len = conn.recv_into(buf, save_size)
                            buf = buf[buf_len:]
                            save_size -= buf_len
                            # print('received ', 100/size*(size-save_size),'%')

                        """выход на ожидание новых данных при отсутствии передачи"""
                        end_time = time.time()
                        if not data:
                            break

                        """рассчет основных параметров"""
                        delta = format(end_time - start_time, '8f')
                        speed = size / (end_time - start_time)
                        global_variables.graph_y.append(speed)
                        size = size
                        number = data[0] + data[1] * 255 + data[2] * 65025

                        """график
                        line.append(speed)
                        graph.plot([number-1, number], [line[number-2], line[number-1]], color='blue', dash_joinstyle='round', dash_capstyle='round', antialiased=True)
                        plt.xlim([number - 50, number])
                        plt.pause(0.00001)"""

                        """вывод в консоль"""
                        print('start_time = {st}, end_time = {end}, delta = {dell}, number = {num}, size = {sz}, speed = {sp}'.format(st=start_time, end=end_time, dell=delta, num=number, sz=size, sp=speed))
                        results = [start_time, end_time, delta, number, size, speed]

                        """вывод в файл"""
                        #with open(filename, "a", newline='') as csv_file:
                        #writer = csv.writer(csv_file, delimiter=';')
                        writer.writerow(results)

                        '''if global_variables.what_to_join == 'c':
                            print("lvl 1")
                            if global_variables.thread_1_active == False:
                                print("lvl 2")
                                sock.shutdown(socket.SHUT_RDWR)
                                sock.close()
                                break
                break
                print("End of fiel")'''


if __name__ == '__main__':
    print("Started...")
    connect_to_client(10002, 1000, "server.csv")
