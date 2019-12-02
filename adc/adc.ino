#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#define BAUDRATE 9600
#define F_CPU 16000000UL
#define UBRR (((F_CPU / (BAUDRATE * 16UL))) - 1)

uint8_t value = 0;

int main(void) {
  ADC_init();
  USART_init();
  while (1){
    if(USART_receive() == 116) {
       USART_send(value);
    }
  }
}

ISR(ADC_vect) {
  uint8_t lowADC = ADCL;                  // save lowADC       
  uint16_t x = ADCH<<8 | lowADC;          // highADC + lowADC 
  value = uint8_t(x>>2);                  // use the 8 MSB
  ADCSRA |= 1<<ADSC;                      // start ADC
} 

void ADC_init(void) {
  ADCSRA |= 1<<ADPS2;                     // prescaler
  ADMUX  |= 1<<REFS0;                     // Vref 5V on arduino
  ADCSRA |= 1<<ADIE;                      // turn interrupts ON
  ADCSRA |= 1<<ADEN;                      // enable ADC 
  sei();                                  // enable global interruptions
  ADCSRA |= 1<<ADSC;                      // start ADC
}

void USART_init(void) {
  UBRR0H = (unsigned char)(UBRR>>8);      // config 
  UBRR0L = (unsigned char)(UBRR);         // UBRR
  UCSR0B = (1<<RXEN0)|(1<<TXEN0);         // Ativando TX e RX
  UCSR0B&=~(1<<UDRIE0);                   // Desligando interrupção
  UCSR0C = ((1<<UCSZ00)|(1<<UCSZ01));     // 8 bits
  UCSR0A&=~(1<<U2X0);                     // Bendito registrador
}

void USART_send(unsigned char data){
  while(!(UCSR0A & (1<<UDRE0)));          // Comenta ai alemao
  UDR0 = data;                            // Comenta ai alemao
}

unsigned char USART_receive(void){
  while(!(UCSR0A & (1<<RXC0)));           // Comenta ai alemao
  return UDR0;                            // Comenta ai alemao
}
