// USART usa 3 fios (1 de tx, 1 de rx e outro terra)
// Informacao eh enviada em blocos de 1 byte com 2 bits de header (1 start e outro stop bit)

#define F_CPU 16000000UL       // Dizer ao compilador qual eh a freq. do clock, deixa as funcoes de delay mais precisas
#include <avr/io.h>
#include <util/delay.h>        // Importando funcao delay

#define BAUDRATE 9600

// Funcao pra facilitar a setagem dos registradores pra setar a baudrate, formula eh dada no datasheet
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)

// Declarando as funcoes
void USART_init(void);
unsigned char USART_receive(void);
void USART_send( unsigned char data);


int main(void){
  char dadoASerEnviado = "o";
  // Inicializa a USART
  USART_init();
  while(1) {
    USART_send(dadoASerEnviado);
    //USART_receive(dadoASerEnviado);
    _delay_ms(2000);
  }
   // Como usual, todas as funcoes q sao non-void precisam de um return
  return 0;
}


// Funcao para inicializar a USART
void USART_init(void){
  UBRR0H = (uint8_t)(BAUD_PRESCALLER>>8);
  UBRR0L = (uint8_t)(BAUD_PRESCALLER);
  
  // Ativando tx e rx
  UCSR0B = (1<<RXEN0)|(1<<TXEN0);
  // Configura o data bits lgenth, parity check e numero de stop bits
  UCSR0C = ((1<<UCSZ00)|(1<<UCSZ01));
}


// Funcao para enviar um dado pela USART
void USART_send(unsigned char data){
  // Checa se ha espaco no ATMega, se sim ele envia pro buffer
  while(!(UCSR0A & (1<<UDRE0)));
  UDR0 = data;
}


// Funcao para receber um dado pela USART
unsigned char USART_receive(void){
  // Faz-se tipo um polling no registrador de recebimento
  while(!(UCSR0A & (1<<RXC0)));
  return UDR0;
  
}
