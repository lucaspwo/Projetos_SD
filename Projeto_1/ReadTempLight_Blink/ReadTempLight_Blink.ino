#include <avr/io.h>

int main (void){
  int luz = 0;              //inicializacao das variaveis
  uint16_t amostras[5];
  float media;

  ADCSRA |= 0b10000111;     //setando o ADEN em 1 e o prescaler em 111 (ADPS1..0)
  DDRB |=_BV(DDB5);         //setando o pino B5 como saida (pino 13 no Arduino)

  while(true){
    ADMUX &= 0;                                     //zerando ADMUX
    ADMUX |= 0b01000000;                            //setando o AREF para 5V e setando MUX3..0 para ler o ADC0 (A0 no Arduino)
    ADCSRA |= 0b01000000;                           //iniciando a conversao
    while(!(ADCSRA & 0b00010000));                  //esperando pelo ADIF = 1
    luz = ADC;                                      //armazenando o resultado
    float resVolt = (float)luz / 1023 * 5;          //obtendo o valor da tensao no resistor de referencia
    float ldrVolt = 5 - resVolt;                    //obtendo o valor de tensao no LDR
    float ldrRes = ldrVolt/resVolt * 10000;         //obtendo a resistencia no LDR
    float ldrLux = 12518931 * pow(ldrRes, -1.405);  //convertendo a resistencia do LDR em lux
    float ldrLum = ldrLux * 100;                    //convertendo de lux para lumen

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
    
    float steinhart;                                //realizando o calculo de conversao de resistencia em graus celsius
    steinhart = media / 4700;
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
