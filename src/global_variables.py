ip = ''
port = ''
filename = ''
size = ''
packet_limit = None
connection_type = 'TCP'
udp_speed = 1200

# TODO: по возможности перенести в соответствующие классы
thread_1_active = False  # Активность потока сервера/клиента.
server_break = False
what_to_join = 's'
termination_reason = ''
very_first_time = None  # Время приема самого первого пакета.

# TODO: удалить
graph_smooth_y = [0]  # Массивы для тестового графика
graph_smooth_x = [0]
