#include <nRF24L01.h>
#include <RF24.h>
#include <RF24_config.h>
#include <SPI.h>

//chip enable and chip select not pins to nrf24l01
#define CE_PIN  9
#define CSN_PIN 10

//reserved for later use
#define SPEED_IN A1
#define DIREC_IN A2
#define BRAKE 2 //interrupt

//connect to motor driver
#define M1 8
#define M2 7
#define EN 6

//steering and delay parameters
//#define oriDir 90
#define turnTime 250

//servo pin
#define ServoPin 5

//player select: No Jumper > Player 1, Jumper to GND > Player 2
#define playerSelect A0

#include <Servo.h>
Servo steering;

RF24 radio(CE_PIN, CSN_PIN);
const uint64_t pipe = 0xE8E8F0F0E1LL;
uint8_t oriDir = 90;
void setup() {
  steering.attach(ServoPin);
  
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(playerSelect, INPUT_PULLUP);
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(1, pipe);
  radio.startListening();
  Serial.println("Beginning");
  analogWrite(EN, 100);
  int alignmentValue = analogRead(A5);
  oriDir = map(alignmentValue, 0, 1023, 80, 100);
  steering.write(oriDir);
}

//initialize default values
uint8_t spd = 255;

uint8_t dirs;
bool fwd = true;
int maxSpd = 100;
char data[20] = "";

void loop() {
  
  //Serial.println(oriDir);
  String msg_string = "";
  int msg;
  if (radio.available() )
  {
    radio.read( data, sizeof(data) );
    msg_string = data;
    msg = msg_string.toInt();
    Serial.print("Command = ");
    Serial.print(msg_string);
    Serial.print("\t >>> ");
    if (msg <= 100) {
      maxSpd = msg;
      Serial.print("Speed Changed. ");
      Serial.print("New Speed = ");
      Serial.print(maxSpd);
      spd = map(maxSpd, 0, 100, 0, 255);
      analogWrite(EN, spd);
    }

    else if (msg > 100) {
      if (!digitalRead(playerSelect)) //checking player 1 or player 2
        msg = msg - 100; //if player 2, minus 100 from the msg command

      switch (msg) {
        //drive forward
        case 101:  //'w'
          fwd = true;
          digitalWrite(M1, fwd);
          digitalWrite(M2, !fwd);
          Serial.print("Forward");
          break;

        //turn left
        case 102:  //'a'
          steering.write(oriDir - 30);
          Serial.print("Turn Left");
          break;

        //drive reverse
        case 103: //'s'
          fwd = false;
          digitalWrite(M1, fwd);
          digitalWrite(M2, !fwd);
          Serial.print("Reverse");
          break;

        //turn right
        case 104: //'d'
          steering.write(oriDir + 30);
          Serial.print("Turn Right");
          break;

        //stop
        case 105: //'x':
          fwd = true;
          digitalWrite(M1, LOW);
          digitalWrite(M2, LOW);
          Serial.print("Stop");
          break;

        //straight
        case 106:
          steering.write(oriDir);
          Serial.print("Straight");
          break;
      }

    }
    Serial.print("\n");
  }
}
