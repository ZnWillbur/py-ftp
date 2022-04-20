import socket
from socket import SOL_SOCKET,SO_REUSEADDR
import json
import struct



s = socket.socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #就是它，在bind前加
s.bind(('0.0.0.0',8080))  #把地址绑定到套接字
s.listen()          #监听链接

while True:
    conn,addr = s.accept() #接受客户端链接

    head_len_bytes=conn.recv(4) #先收报头4个bytes,得到报头长度的字节格式
    x=struct.unpack('i',head_len_bytes)[0] #提取报头的长度

    head_bytes=conn.recv(x) #按照报头长度x,收取报头的bytes格式
    header=json.loads(str(head_bytes, encoding="utf8")) #提取报头

    # 获取报头数据
    file_size = header["file_size"]
    file_name = header["file_name"]
    # 获取并保存文件数据
    
    with open(file_name, "wb") as f:
        n = 0
        while True:
            n += 1
            data = conn.recv(file_size)
            if not data:
                print('接收完毕！')
                break
            f.write(data)
            f.flush()
            print(f"写入{n}次")

    conn.close()

