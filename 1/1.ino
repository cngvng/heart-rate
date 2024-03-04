#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

const char* ssid = "cngvng";
const char* password = "11111111";
const char* serverIP = "172.20.10.4";
const uint16_t serverPort = 2024;
 
WiFiClient client;
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Đang kết nối Wi-Fi...");
  }
  Serial.println("Đã kết nối Wi-Fi.");

  Wire.begin();
  mpu.begin();

  // Thiết lập cấu hình cho cảm biến MPU6050
  mpu.setHighPassFilter(MPU6050_HIGHPASS_0_63_HZ);
  mpu.setMotionDetectionThreshold(1);
  mpu.setMotionDetectionDuration(20);
  mpu.setInterruptPinLatch(true);  // Giữ nó kẹp. Sẽ tắt khi khởi tạo lại.
  mpu.setInterruptPinPolarity(true);
  mpu.setMotionInterrupt(true);

  delay(100);

  // Kết nối đến máy chủ Python
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Đã kết nối đến máy chủ Python.");
  } else {
    Serial.println("Không thể kết nối đến máy chủ Python.");
  }
}

void loop() {
  if (mpu.getMotionInterruptStatus()) {
    /* Lấy giá trị đọc từ cảm biến */
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    if (client.connected()) {
      // Gửi dữ liệu đến máy chủ Python
      String data = String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z) + "," + String(g.gyro.x) + "," + String(g.gyro.y) + "," + String(g.gyro.z);
      client.println(data);
    }
  }

  delay(500);
}
