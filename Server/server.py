import pymysql
import socket
import hashlib
import pickle

# 데이터베이스 및 소켓 설정 상수화
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'library',
    'user': 'lib',
    'password': 'rmaWhrdlemf',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
SERVER_IP = "192.168.10.53"
SERVER_PORT = 2255

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client {client_address} is connected.")
            handle_client(client_socket)
    finally:
        server_socket.close()

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode("utf-8")
        if data:
            user_id, user_password = data.split("&&")
            print(f"ID: {user_id}")
            print(f"PW: {user_password}")

            if user_id == "admin":
                if user_password == hashlib.sha256("addBook".encode()).hexdigest():
                    addBook(client_socket)
                    return
                
                elif user_password == hashlib.sha256("addUser".encode()).hexdigest():
                    addUser(client_socket)
                    return
            
            if user_password == "Rental":
                rentBook(client_socket)
                return


            response = authenticate_user(user_id, user_password)
            client_socket.send(response.encode("utf-8"))
            if response == "Password is correct.":
                send_book(client_socket)
            elif response == "Administrator":
                send_book(client_socket)
                print("send book done.")

                data = client_socket.recv(4).decode("utf-8")
                print(f"recv data: {data}")
                send_rental(client_socket)

                data = client_socket.recv(4).decode("utf-8")
                print(f"recv data: {data}")
                send_users(client_socket)
    finally:
        client_socket.close()

def authenticate_user(user_id, user_password):
    if user_id == "admin" and hashlib.sha256("admin".encode()).hexdigest() == user_password:
        return "Administrator"

    with pymysql.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Passwd FROM USERS WHERE Id = %s", user_id)
            result = cursor.fetchone()
            if result and user_password == result['Passwd']:
                return "Password is correct."
            else :
                return "Password is incorrect or user not found."

def send_book(client_socket):
    with pymysql.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT B.ISBN, B.name, B.publisher, B.writer, B.category, B.lib_row, B.lib_cal, B.created_at, (COUNT(BO.ISBN) - COUNT(R.Books_ISBN)) AS available_copies FROM BOOK B LEFT JOIN BOOKS BO ON B.ISBN = BO.ISBN LEFT JOIN RENTAL R ON BO.Id = R.Books_Id AND BO.ISBN = R.Books_ISBN AND R.return_flag = 0 GROUP BY B.ISBN;")
            books = cursor.fetchall()

    data = pickle.dumps(books)
    client_socket.sendall(data)

def send_rental(client_socket):
    with pymysql.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT u.name AS user_name, u.Id AS user_id, b.Id AS book_id, bk.name AS book_name, b.ISBN AS book_isbn, r.rental_at, r.return_at, r.return_flag FROM RENTAL r JOIN USERS u ON r.Users_Id = u.Id JOIN BOOKS b ON r.Books_Id = b.Id AND r.Books_ISBN = b.ISBN JOIN BOOK bk ON b.ISBN = bk.ISBN;")
            rental = cursor.fetchall()

    data = pickle.dumps(rental)
    client_socket.sendall(data)


def send_users(client_socket):
    with pymysql.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM USERS")
            users = cursor.fetchall()

    data = pickle.dumps(users)
    client_socket.sendall(data)

def addBook(client_socket):
    print("addBook RUN")
    data = client_socket.recv(1024)
    book_info = pickle.loads(data)
    print(book_info)

    query = f"INSERT INTO BOOK (ISBN, name, publisher, writer, category, lib_row, lib_cal, created_at) VALUES ('{book_info[0]}', '{book_info[1]}', '{book_info[2]}', '{book_info[3]}', '{book_info[4]}', {book_info[5]}, {book_info[6]}, '{book_info[7]}');"

    with pymysql.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    msg = "Administrator"
    client_socket.send(msg.encode("utf-8"))
    send_book(client_socket) 
    print("send book done.")

    ch = client_socket.recv(4).decode("utf-8")
    print(f"recv data: {ch}")
    send_rental(client_socket)

    ch = client_socket.recv(4).decode("utf-8")
    print(f"recv data: {ch}")
    send_users(client_socket)

def addUser(client_socket):
    print("addUser RUN")
    data = client_socket.recv(1024)
    user_info = pickle.loads(data)
    print(user_info)

    query = f"INSERT INTO USERS (Id, Passwd, name, created_at) VALUES ('{user_info[0]}', SHA2('{user_info[1]}', 256), '{user_info[2]}', CURDATE())"

    with pymysql.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    msg = "Administrator"
    client_socket.send(msg.encode("utf-8"))
    send_book(client_socket) 
    print("send book done.")

    ch = client_socket.recv(4).decode("utf-8")
    print(f"recv data: {ch}")
    send_rental(client_socket)

    ch = client_socket.recv(4).decode("utf-8")
    print(f"recv data: {ch}")
    send_users(client_socket)

def rentBook(client_socket):
    print("rentBook run")
    data = client_socket.recv(1024)
    rent_info = pickle.loads(data)
    print(rent_info)

    query = f"INSERT INTO RENTAL (Users_Id, Books_Id, Books_ISBN, rental_at, return_at, return_flag) SELECT {rent_info[0]}, MIN(b.Id), '{rent_info[1]}', NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY), 0 FROM BOOKS b WHERE b.ISBN = '{rent_info[1]}';"

    with pymysql.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    msg = "Administrator"
    client_socket.send(msg.encode("utf-8"))
    send_book(client_socket) 
    print("send book done.")

    ch = client_socket.recv(4).decode("utf-8")
    print(f"recv data: {ch}")
    send_rental(client_socket)

    ch = client_socket.recv(4).decode("utf-8")
    print(f"recv data: {ch}")
    send_users(client_socket)

if __name__ == "__main__":
    start_server()
