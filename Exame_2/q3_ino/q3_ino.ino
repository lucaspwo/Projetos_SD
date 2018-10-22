#include <SoftwareSerial.h>             //Importando a biblioteca

SoftwareSerial mySerial(10, 11);        // 10 = RX, 11 = TX

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; 
  }

  mySerial.begin(115200);               //Inicializando a serial
}

void loop() { 
  if (mySerial.available()) {           //Caso haja envio da Galileo
    String rx = mySerial.readString();
    Serial.println(rx);                 //Exibindo o texto na tela
    if(rx == "X"){                      //Caso venha um X...
      mySerial.write("Sim, mestre!");   //... envie uma string especial
    }
  }
}
