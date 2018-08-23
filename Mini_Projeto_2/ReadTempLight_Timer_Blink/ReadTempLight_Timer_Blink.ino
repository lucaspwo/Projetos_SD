#include <avr/io.h>
#include <avr/interrupt.h>

int cont = 0;               //inicializacao da variavel que vai contar os overflows

ISR(TIMER1_OVF_vect){       //funcao que e chamada a cada overflow do TIMER1
  cont++;
}

int main (void){
  float steinhart;          //variavel responsavel por armazenar a temperatura
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

    if((ldrLum >= 3500 && steinhart >= 25) || cont >= 7)      //condicao de acionamento do LED
      PORTB |= _BV(PORTB5);                                   //acionando o LED no pino B5
    else
      PORTB &= ~_BV(PORTB5);                                  //desligando o LED no pino B5
  }
}
