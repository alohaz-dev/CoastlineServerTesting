import socket
from _thread import *
import sys

currentPlayer = 0
server = '192.168.1.66'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print('Waiting for a connection, Server Started')

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

pos = [(0,0),(100,100)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ''
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                #print('Recieved: ', reply)
                #print('Sending: ', reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print('Lost connection')
    currentPlayer -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to:', addr, '\nPlayer: ', currentPlayer+1)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1