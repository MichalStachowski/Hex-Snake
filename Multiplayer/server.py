import socket
from _thread import *
from snake import Snake
import pickle


def threaded_client(conn, player, players):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Rozlaczono")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Odebrano: ", data)
                print("Wyslano : ", reply)
                # print(player)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Utracono polaczenie")
    conn.close()


def main():
    server = input("Podaj adres IP komputera: ")
    # server = "192.168.1.30"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen()
    print("Serwer oczekuje na polaczenie")

    players = [Snake([2, 2]), Snake([17, 17])]

    currentPlayer = 0
    while True:
        conn, addr = s.accept()
        print("Nawiazano polaczenie z:", addr)

        start_new_thread(threaded_client, (conn, currentPlayer, players))
        currentPlayer += 1


if __name__ == '__main__':
    main()
