#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>        // Importando funcao delay
#define BAUDRATE 9600

// Funcao pra facilitar a setagem dos registradores pra setar a baudrate, formula eh dada no datasheet
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)

int main(void) {
  Serial.begin(9600);                     // ---> REMOVER DEPOIS <---
  ADC_init();
  while (1){
    // main code here;
  }
}

ISR(ADC_vect) {
  uint8_t lowADC = ADCL;                  // save lowADC       
  uint16_t x = ADCH<<8 | lowADC;          // highADC + lowADC 
  uint8_t num = uint8_t(x>>2);            // use the 8 MSB
  ADCSRA |= 1<<ADSC;                      // start ADC
  Serial.println(num,BIN);                // ---> REMOVER DEPOIS <---
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
  UBRR0H = (uint8_t)(BAUD_PRESCALLER>>8); // config 
  UBRR0L = (uint8_t)(BAUD_PRESCALLER);    // UBRR
  UCSR0B = (1<<RXEN0)|(1<<TXEN0);         // Ativando TX e RX
  UCSR0C = ((1<<UCSZ00)|(1<<UCSZ01));     // 8 bits
}

/* Funcao para enviar um dado pela USART */
void USART_send(unsigned char data){
  while(!(UCSR0A & (1<<UDRE0)));          // Checa se ha espaco no ATMega, se sim ele envia pro buffer
  UDR0 = data;
}

/* Funcao para receber um dado pela USART */
unsigned char USART_receive(void){
  while(!(UCSR0A & (1<<RXC0)));           // Faz-se tipo um polling no registrador de recebimento

  /* Teste Pocelatto */
    digitalWrite(LED_BUILTIN, HIGH);      // Teste pra ver se o USART esta funcionando, liga o LED do Arduino
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);       // Entender o porque o led nao desliga depois q manda outro comando
  /* --- END ------ */
  return UDR0;
  
}
