#include <avr/io.h>
#include <avr/interrupt.h>

int main(void) {
  Serial.begin(9600);             // TESTE
  ADCSRA |= 1<<ADPS2;             // prescaler
  ADMUX  |= 1<<REFS0;             // Vref 5V on arduino
  ADCSRA |= 1<<ADIE;              // turn interrupts ON
  ADCSRA |= 1<<ADEN;              // enable ADC 
  sei();                          // enable global interruptions
  ADCSRA |= 1<<ADSC;              // start ADC
  while (1){
    // main code here;
  }
}

ISR(ADC_vect) {
  uint8_t lowADC = ADCL;          // save lowADC       
  uint16_t x = ADCH<<8 | lowADC;  // highADC + lowADC 
  uint8_t num = uint8_t(x>>2);    // use the 8 MSB
  ADCSRA |= 1<<ADSC;              // start ADC
  Serial.println(num,BIN);        // TESTE
} 
