#include <avr/io.h>
#include <avr/interrupt.h>

#define DHT11_PIN 1         // define anlog  port 1

int cont = 0;               //inicializacao da variavel que vai contar os overflows

ISR(TIMER1_OVF_vect){       //funcao que e chamada a cada overflow do TIMER1
  cont++;
}

byte read_dht11_dat(){
  byte i = 0;
  byte result=0;
  for(i=0; i< 8; i++){
    while(!(PINC & _BV(DHT11_PIN))) {};  // wait  forever until anlog input port 0 is '1'   (NOTICE: PINC reads all the analog input ports
    //and  _BV(X) is the macro operation which pull up positon 'X'to '1' and the rest positions to '0'. it is equivalent to 1<    delayMicroseconds(30);
    delayMicroseconds(30);
    if(PINC & _BV(DHT11_PIN))  //if analog input port 0 is still '1' after 30 us
      result |=(1<<(7-i));     //this position is 1
    while((PINC & _BV(DHT11_PIN)));  // wait '1' finish
  }
  return result;
}

void readDHT(){
  byte dht11_dat[5];   
  byte dht11_in;
  byte i;// start condition
  
  PORTC &= ~_BV(DHT11_PIN);    // 1. pull-down i/o pin for 18ms
  delay(18);
  PORTC |= _BV(DHT11_PIN);     // 2. pull-up i/o pin for 40us
  delayMicroseconds(1);
  DDRC &= ~_BV(DHT11_PIN);     //let analog port 0 be input port
  delayMicroseconds(40);     
  
  dht11_in = PINC & _BV(DHT11_PIN);  // read only the input port 0
  if(dht11_in){
    Serial.println("dht11 start condition 1 not met"); // wait for DHT response signal: LOW
    delay(1000);
    return;
  }
  delayMicroseconds(80);
  dht11_in = PINC & _BV(DHT11_PIN); // 
  if(!dht11_in){
    Serial.println("dht11 start condition 2 not met");  //wair for second response signal:HIGH
    return;
  }
  
  delayMicroseconds(80);// now ready for data reception
  for (i=0; i<5; i++){
    dht11_dat[i] = read_dht11_dat();
  }  //recieved 40 bits data. Details are described in datasheet
  
  DDRC |= _BV(DHT11_PIN);      //let analog port 0 be output port after all the data have been received
  PORTC |= _BV(DHT11_PIN);     //let the  value of this port be '1' after all the data have been received
  byte dht11_check_sum = dht11_dat[0]+dht11_dat[1]+dht11_dat[2]+dht11_dat[3];// check check_sum
  if(dht11_dat[4]!= dht11_check_sum){
    Serial.println("DHT11 checksum error");
  }
  Serial.print("Current humdity = ");
  Serial.print(dht11_dat[0], DEC);
  Serial.print(".");
  Serial.print(dht11_dat[1], DEC);
  Serial.print("%  ");
  Serial.print("temperature = ");
  Serial.print(dht11_dat[2], DEC);
  Serial.print(".");
  Serial.print(dht11_dat[3], DEC);
  Serial.println("C  ");
  delay(2000);  //fresh time
  return;
}

void setup(){
  DDRC |= _BV(DHT11_PIN);   //let analog port 0 be output port
  PORTC |= _BV(DHT11_PIN);  //let the initial value of this port be '1'
  Serial.begin(9600);
  Serial.println("Ready");
}

int main (void){
  //float steinhart;          //variavel responsavel por armazenar a temperatura
  float ldrLum;             //variavel responsavel por armazenar a taxa de luz
  uint16_t amostras[5];     //variavel para armazenar 5 leituras consecutivas para calculo de media
  float media;              //variavel para armazenar a media
  
  TCCR1B |= _BV(CS12);      //setando os bits CS12 e CS10 (clk/1024)
  TCCR1B |= _BV(CS10);
  TIMSK1 |= _BV(TOIE1);     //habilitando a interrupcao de overflow

  ADCSRA |= 0b10000111;     //setando o ADEN em 1 e o prescaler em 111 (ADPS1..0)
  DDRB |=_BV(DDB5);         //setando o pino B5 como saida (pino 13 no Arduino)

  sei();                    //ativando interrupcoes
  
  while(true){
    for(uint8_t i = 0; i<5; i++){
      ADMUX &= 0;                                   //zerando ADMUX
      ADMUX |= 0b01000000;                          //setando o AREF para 5V e setando MUX3..0 para ler o ADC0 (A0 no Arduino)
      ADCSRA |= 0b01000000;                         //iniciando a conversao
      while(!(ADCSRA & 0b00010000));                //esperando pelo ADIF = 1
      amostras[i] = ADC;                            //armazenando o resultado
    }
    
    media = 0;
    for(uint8_t i = 0; i<5; i++){                   //tirando a media dos valores
      media += amostras[i];
    }
    media /= 5;
    
    ldrLum = media;                                 //convertendo de nivel para "lumens"
    ldrLum = 4*ldrLum + 1000;

    readDHT();
    
    /*for(uint8_t i = 0; i<5; i++){
      ADMUX &= 0;                                   //zerando ADMUX
      ADMUX |= 0b01000001;                          //setando o AREF para 5V e setando MUX3..0 para ler o ADC1 (A1 no Arduino)
      ADCSRA |= 0b01000000;                         //iniciando a conversao
      while(!(ADCSRA & 0b00010000));                //esperando pelo ADIF = 1
      amostras[i] = ADC;                            //armazenando o resultado
    }

    media = 0;
    for(uint8_t i = 0; i<5; i++){                   //tirando a media dos valores
      media += amostras[i];
    }
    media /= 5;
    
    media = 1023 / media -1;                        //obtendo a resistencia medida pelo sensor
    media = 4700 / media;
    
    steinhart = media / 4700;                       //realizando o calculo de conversao de resistencia em graus celsius
    steinhart = log(steinhart);
    steinhart /= 3950;
    steinhart += 1.0 / (25 + 273.15);
    steinhart = 1.0 / steinhart;
    steinhart -= 273.15;*/

    /*if((ldrLum >= 3500 && steinhart >= 25) || cont >= 7)      //condicao de acionamento do LED
      PORTB |= _BV(PORTB5);                                   //acionando o LED no pino B5
    else
      PORTB &= ~_BV(PORTB5);*/                                  //desligando o LED no pino B5
  }
}
