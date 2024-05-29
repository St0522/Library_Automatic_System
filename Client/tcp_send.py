# 클라이언트 프로그램
# 서버 프로그램은 주피터, 이것은 파이참으로 실행 - 동시에 두개 프로그램 실행을 위해서.
import socket

server_ip = '192.168.10.53' # 위에서 설정한 서버 ip
server_port = 2255 # 위에서 설정한 서버 포트번호

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

msg = input('msg:') # 서버로 보낼 msg 입력
socket.sendall(msg.encode(encoding='utf-8'))

# 서버가 에코로 되돌려 보낸 메시지를 클라이언트가 받음
data = socket.recv(100)
msg = data.decode() # 읽은 데이터 디코딩
print('echo msg:', msg)

socket.close()