import serial
import pandas as pd
import pickle
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Received data from ESP32 throught wifi
host = '1'

port = '172.20.10.4:2024'  # Tên cổng Serial, thay đổi tùy theo hệ thống của bạn
baudrate = 115200  # Baud rate, phải giống với Arduino

ser = serial.Serial(port, baudrate)
df = pd.DataFrame()
model = pickle.load(open('logistic_model_d.pkl', 'rb'))

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()  # Đọc dữ liệu từ cổng Serial
        # print(data)
        # print(data.split(','))
        # df = df.append({'AccX': data[0], 'AccY': data[1], 'AccZ': data[2], 'GyroX': data[3], 'GyroY': data[4], 'GyroZ': data[5]}, ignore_index=True)
        # Save to Acc to 6 columns
        df = pd.concat([df, pd.DataFrame([x.split(',') for x in data.split(';')], columns=['AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ'])], ignore_index=True)
        print("The predicted value is: ", np.where(model.predict(df)==1, 'Falling', 'Not Falling'))
        # df.to_csv('running_data.csv', index=False)
