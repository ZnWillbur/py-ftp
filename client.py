import socket
import json
import struct
import os


def getFileInfo(file_path):
    if os.path.exists(file_path):
        size = os.path.getsize(filename=file_path)
        name = os.path.basename(file_path)
        return (size, name)
    else:
        return


def main():
    while True:
        file_path = input("请输入文件路径:")
        file_size, file_name = getFileInfo(file_path)
        if not file_name:
            print("请输入正确路径!")
            return
        
        #为避免粘包,必须自定制报头
        header={'file_size':file_size,'file_name':file_name}

        #为了该报头能传送,需要序列化并且转为bytes
        head_bytes=bytes(json.dumps(header),encoding='utf-8')

        #为了让客户端知道报头的长度,用struck将报头长度这个数字转成固定长度:4个字节
        head_len_bytes=struct.pack('i',len(head_bytes)) #这4个字节里只包含了一个数字,该数字是报头的长度

        s = socket.socket()
        s.connect(('110.40.248.108',8080))
        #客户端开始发送
        s.send(head_len_bytes) #先发报头的长度,4个bytes
        s.send(head_bytes) #再发报头的字节格式
        with open(file_path, "rb") as f:
            s.send(f.read())
        # 关闭客户套接字
        s.close()

if __name__ == "__main__":
    main()