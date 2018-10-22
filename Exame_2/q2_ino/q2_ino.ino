#include <SPI.h>                        //Importando a biblioteca SPI

byte rx = 0;                            //Definindo a variavel global que lidara
                                        // com a entrada e a saida
void SlaveInit(void) {                  //Funcao responsavel por setar os pinos da
  pinMode(SCK, INPUT);                  // comunicacao SPI
  pinMode(MOSI, INPUT);
  pinMode(MISO, INPUT);
  pinMode(SS, INPUT);
  SPCR = (1 << SPE);                    //Definindo o Arduino como slave
}

byte SPItransfer(byte value) {          //Funcao responsavel por receber e enviar
  SPDR = value;
  while(!(SPSR & (1<<SPIF)));
  delay(10);
  return SPDR;
}

void setup() {
  Serial.begin(9600);
  SlaveInit();                          //Inicializacao do bus SPI
  Serial.println("Iniciando Slave");
}

void loop() {
  if(!digitalRead(SS)){                 //Se houver intencao de envio do mestre...
    pinMode(MISO, OUTPUT);              //... habilitar a entrada de dados...
    Serial.println("Slave Ativado");
    Serial.println("tx:" + String(rx)); //... imprimir o que sera enviado...
    rx = SPItransfer(rx);               //... enviar o valor existente na variavel rx e salvar o recebido...
    Serial.println("rx:" + String(rx)); //... imprimir o valor recebido
  }
}
