import time
import csv
import socket
import axes


def connect_to_server(ip, port, size, filename):
    with open(filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["start_time", "end_time", "delta", "number", "size", "speed"])

    b = bytearray(int(size))

    try:
        with socket.create_connection((ip, port)) as sock:
            with open(filename, "a", newline='') as csv_file:
                while True:
                    try:
                        b[0] += 1
                        start_time = time.time()

                        sock.sendall(b)
                        time.sleep(0.2)

                        end_time = time.time()
                        delta = format(end_time - start_time, '8f')
                        speed = float(size) / (end_time - start_time)
                        axes.graph_y.append(speed)
                        number = b[0] + b[1] * 255 + b[2] * 65025
                        size = len(b)
                        print('start_time = {st}, end_time = {end}, delta = {dell}, '
                              'number = {num}, size = {sz}, speed = {sp}'.
                              format(st=start_time, end=end_time, dell=delta, num=number, sz=size, sp=speed))
                        results = [start_time, end_time, delta, number, size, speed]

                        writer = csv.writer(csv_file, delimiter=';')
                        writer.writerow(results)

                        if b[0] == 255:
                            b[1] += 1
                            b[0] = 0
                            if b[1] == 255:
                                b[2] += 1
                                b[1] = 0
                    except socket.timeout:
                        print("send data timeout")
                    except socket.error as ex:
                        print("send data error:", ex)
    except ConnectionRefusedError:
        print("wrong port")
