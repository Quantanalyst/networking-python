# socket library for establishing a connection to a host on a certain port
import socket
# threading library for using multi-threading capability of our CPU
import threading 
# Queue for creating a queue. This way we can avoid scanning a port multiple times. 
from queue import Queue


# my home's router default gateway
# if you want to know what is yours? in Linux, use `ip route | grep default` command
target = "192.168.0.1"

queue = Queue()
open_ports = []

# This function creates a TCP socket and connects to the host on a certain port
# If socket is able to connect, then it will return True, if not, it returns False
def portscan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target,port))
        return True
    except:
        return False

# This function, puts all the items in the port list into a queue
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

# This function takes one port from the queue and scan its connection
# if the port is open, then it will append it to the open port list
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f'Port {port} is open!')
            open_ports.append(port)

port_list = range(1,1024)
fill_queue(port_list)

thread_list = []

# This for loop, establishes 10 threads. These are only templates and they are not started yet. 
# Each thread will be appended to the thread list. 
for t in range(50):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# This for loop, takes each threads in the thread list and make them to start. 
for thread in thread_list:
    thread.start()

# This for loop is important, it waits for each thread to finish its job. 
for thread in thread_list:
    thread.join()

print(f'Open ports are: {open_ports}')
