#include <avr/io.h>

int main (void){
  int temp = 0;     //inicializacao das variaveis
  int luz = 0;

  ADCSRA |= 0b10000111;     //setando o ADEN em 1 e o prescaler em 111 (ADPS1..0)
  DDRB |=_BV(DDB5);         //setando o pino B5 como saida (pino 13 no Arduino)

  while(true){
    ADMUX &= 0;             //zerando ADMUX
    ADMUX |= 0b01000000;    //setando o AREF para 5V e setando MUX3..0 para ler o ADC0 (A0 no Arduino)
    ADCSRA |= 0b01000000;   //iniciando a conversao
    while(!(ADCSRA & 0b00010000));    //esperando pelo ADIF = 1
    luz = ADC;      //armazenando o resultado
    
    ADMUX &= 0;             //zerando ADMUX
    ADMUX |= 0b01000001;    //setando o AREF para 5V e setando MUX3..0 para ler o ADC1 (A1 no Arduino)
    ADCSRA |= 0b01000000;   //iniciando a conversao
    while(!(ADCSRA & 0b00010000));    //esperando pelo ADIF = 1
    temp = ADC;     //armazenando o resultado

    if(luz >= 700 && temp >= 500)     //condicao de acionamento do LED
      PORTB |= _BV(PORTB5);           //acionando o LED no pino B5
    else
      PORTB &= ~_BV(PORTB5);          //desligando o LED no pino B5
  }
}
