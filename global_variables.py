graph_y = [0]  # Координата Y графика
graph_len = 1  # Координата X !!!отрисованного!!! графика.
graph_active = False  # Активность графика.
ip = ''
port = ''
filename = ''
size = ''
thread_1_active = False  # Активность потока сервера/клиента.
what_to_join = 's'  #
termination_reason = ''  #
time_stack_length = 20  # Размер усреднения.
time_stack = []  # Массив времен начала приема.
time_stack_end = []  # Массив времен конца приема.

packet_limit = None
very_first_time = None

plot_end = 1

graph_y_only = [[0, 0]]  # [x, y] адекватных результатов
last = 0

graph_len_new = 1
