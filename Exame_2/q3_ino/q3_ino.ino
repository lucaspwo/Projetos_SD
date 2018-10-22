#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  mySerial.begin(115200);
}

void loop() { 
  if (mySerial.available()) {
    String rx = mySerial.readString();
    Serial.println(rx);
    if(rx == "X"){
      mySerial.write("Yes, master!");
    }
  }
}
