#include <avr/io.h>

void pwmInitD6(int pwm){
  OCR0A = pwm;
  TCCR0A |= (1 << COM0A1) | (1 << WGM01) | (1 << WGM00);      //fast PWM
  TCCR0B |= (1 << CS01);      //clk/8
}

void pwmInitD5(int pwm){
  OCR0B = pwm;
  TCCR0A |= (1 << COM0B1) | (1 << WGM01) | (1 << WGM00);
  TCCR0B |= (1 << CS01) | (1 << CS00);  //clk/64
}

int main (void){
  ADCSRA |= 0b10000111;   //ADEN em 1 e prescaler em 111
  DDRB |= _BV(DDB5);      //saida LED L1
  DDRB |= _BV(DDB4);      //saida LED L2
  DDRB |= _BV(DDB3);      //saida LED L3
  DDRD |= _BV(DDD6);      //saida PWM1 S1
  DDRD |= _BV(DDD5);      //saida PWM2 S2
  
  while(true){
    if(PINB & (1 << PB4)){    //se chave CH1 acionada
      ADMUX &= 0;             //zerando ADMUX
      ADMUX |= 0b01000000;    //setando AREF para 5V e setando leitura do ADC0 (A1, entrada)
      ADCSRA |= 0b01000000;   //iniciando a conversao
      while(!(ADCSRA & 0b00010000));  //esperando pelo ADIF = 1
      int tempA1 = ADC;
      ADMUX &= 0;             //zerando ADMUX
      ADMUX |= 0b01000001;    //setando AREF para 5V e setando leitura do ADC1 (A2, saida)
      ADCSRA |= 0b01000000;   //iniciando a conversao
      while(!(ADCSRA & 0b00010000));  //esperando pelo ADIF = 1
      int tempA2 = ADC;
      if(tempA1 <= 102){       //ADC = 102 => temp = 20C
        PORTB |= _BV(PORTB5);
        PORTB |= ~_BV(PORTB4);
        PORTB |= ~_BV(PORTB3);
      }
      if(tempA2 >= 614){      //ADC = 614 => temp = 120C
        PORTB |= ~_BV(PORTB5);
        PORTB |= _BV(PORTB4);
        PORTB |= ~_BV(PORTB3);
      }
      if((tempA1 > 102) && (tempA2 < 614)){    //funcionamento normal
        PORTB |= ~_BV(PORTB5);
        PORTB |= ~_BV(PORTB4);
        PORTB |= _BV(PORTB3);
        ADMUX &= 0;             //zerando ADMUX
        ADMUX |= 0b01000010;    //setando AREF para 5V e setando leitura do ADC2 (sensor de umidade)
        ADCSRA |= 0b01000000;   //iniciando a conversao
        while(!(ADCSRA & 0b00010000));  //esperando pelo ADIF = 1
        int umidade = ADC;
        while(umidade > 128){   //umi = 128 => umi = 25%
          if(umidade == 512){   //umi = 512 => umi = 100%
            pwmInitD6(43);      //PWM para sinal S1 (11.25KHz - 25CFM)
            pwmInitD5(12);      //PWM para sinal S2 (5KHz - 100W)
          }
          if((umidade >= 256) && (umidade < 512)){     //umi = 256 => umi 50%
            pwmInitD6(21);      //PWM para sinal S1 (22.5KHz - 50CFM)
            pwmInitD5(24);      //PWM para sinal S2 (2.5KHz - 50W)
          }
          if((umidade >= 128) && (umidade < 256)){
            pwmInitD6(10);      //PWM para sinal S1 (45KHz - 100CFM)
            pwmInitD5(49);      //PWM para sinal S2 (1.25KHz - 25W)
          }
          ADMUX &= 0;             //zerando ADMUX
          ADMUX |= 0b01000010;    //setando AREF para 5V e setando leitura do ADC2 (sensor de umidade)
          ADCSRA |= 0b01000000;   //iniciando a conversao
          while(!(ADCSRA & 0b00010000));  //esperando pelo ADIF = 1
          umidade = ADC;
        }
      }
    } else{
      PORTB |= ~_BV(PORTB5);
      PORTB |= ~_BV(PORTB4);
      PORTB |= ~_BV(PORTB3);
      pwmInitD6(0);
      pwmInitD5(0);
    }
  }
}
