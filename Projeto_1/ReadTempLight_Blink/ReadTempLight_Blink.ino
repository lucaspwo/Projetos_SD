#include <avr/io.h>

int main (void){
  float steinhart;          //inicializacao das variaveis
  float ldrLum;
  uint16_t amostras[5];
  float media;

  ADCSRA |= 0b10000111;     //setando o ADEN em 1 e o prescaler em 111 (ADPS1..0)
  DDRB |=_BV(DDB5);         //setando o pino B5 como saida (pino 13 no Arduino)

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
    
    for(uint8_t i = 0; i<5; i++){
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
    steinhart -= 273.15;

    if(ldrLum >= 3500 && steinhart >= 25)     //condicao de acionamento do LED
      PORTB |= _BV(PORTB5);                   //acionando o LED no pino B5
    else
      PORTB &= ~_BV(PORTB5);                  //desligando o LED no pino B5
  }
}
