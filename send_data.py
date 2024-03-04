import socket
import threading
import pandas as pd
import pickle
import numpy as np
import warnings
import telepot
import re


token = '7147796332:AAFSSsaykxzdZmXmeFOp6yzqKM122P9M-RE'
host = '172.20.10.1'  # Địa chỉ IP của máy tính chạy Python
port = 2024  # Cổng kết nối
model = pickle.load(open('logistic_model_d.pkl', 'rb'))

warnings.filterwarnings("ignore")

bot = telepot.Bot(token)
df = pd.DataFrame()
count = 0
receiver_id = 5678258056

def start_server():
    global df, count

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)

    print("Server listening on {}:{}".format(host, port))

    while True:
        client_socket, addr = server_socket.accept()
        print("Connected with", addr)

        while True:
            data = client_socket.recv(1024)  # Nhận dữ liệu từ ESP32
            if not data:
                break

            data = data.decode('utf-8')
            print(data)
            data = re.sub(r'\\r\\n', '', data)
            print(data)

            split_data = data.split(',')
            # print(split_data)
            df_list = [float(x) for x in split_data if x != ' ' and x != '' and x.strip()]
            print(df_list)
            if df_list:
                df = pd.concat([df, pd.DataFrame([df_list], columns=['AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ'])], ignore_index=True)
            # df = pd.DataFrame([df_list], columns=['AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ'])
            count += 1
            if count == 5:
                print("Received 10 data samples, predicting ...")
                avg = np.array(df.mean()).reshape(1,-1)
                y_pred = model.predict(avg)
                if y_pred == 1:
                    print("Falling")
                    bot.sendMessage(receiver_id, "Kodai Falling")
                else:
                    print("Not Falling")
                df = pd.DataFrame()
                count = 0
        client_socket.close()


if __name__ == '__main__':
    start_server()
