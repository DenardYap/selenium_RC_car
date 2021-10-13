#include <nRF24L01.h>
#include <RF24.h>
#include <SPI.h>


#define CE_PIN  9
#define CSN_PIN 10

const uint64_t pipe = 0xE8E8F0F0E1LL;
RF24 radio(CE_PIN, CSN_PIN);


void setup() {
  pinMode(A0, INPUT_PULLUP); //debug mode
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(pipe);
}

String msg = "";
//String data = "";

char data[5];
char a = 'a';

void loop() {

  if (Serial.available()) {
    char a = (char)Serial.read();
    if (a != '\n') {
      msg += a;
    }
    else {
      //data = msg.toCharArray;
      msg.toCharArray(data, 4);
      msg = "";
      radio.write(&data, sizeof(data));
      Serial.println(data);
      delay(10);
    }
  }

  //reserved for debuggeing
  //debug mode: Jumper A0 to GND
  if (!digitalRead(A0)) {
    radio.write("0", 1);
    delay(500);
    radio.write("50", 2);
    delay(500);
    radio.write("100", 3);
    delay(500);
    radio.write("101", 3);
    delay(500);
    radio.write("102", 3);
    delay(500);
    radio.write("103", 3);
    delay(500);
    radio.write("104", 3);
    delay(500);
    radio.write("105", 3);
    delay(500);
    radio.write("106", 3);
    delay(500);
    radio.write("201", 3);
    delay(500);
    radio.write("202", 3);
    delay(500);
    radio.write("203", 3);
    delay(500);
    radio.write("204", 3);
    delay(500);
    radio.write("205", 3);
    delay(500);
    radio.write("206", 3);
    delay(500);
  }
}
