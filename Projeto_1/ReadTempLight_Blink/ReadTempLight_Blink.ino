#include <avr/io.h>

int main (void){
  int temp = 0;
  int luz = 0;

  ADCSRA |= 0b10000111;
  DDRB |=_BV(DDB5);

  while(true){
    ADMUX &= 0;
    ADMUX |= 0b01000000;
    ADCSRA |= 0b01000000;
    while(!(ADCSRA & 0b00010000));
    luz = ADC;
    
    ADMUX &= 0;
    ADMUX |= 0b01000001;
    ADCSRA |= 0b01000000;
    while(!(ADCSRA & 0b00010000));
    temp = ADC;

    if(luz >= 700 && temp >= 500)
      PORTB |= _BV(PORTB5);
    else
      PORTB &= ~_BV(PORTB5);
  }
}
