#include <SoftwareSerial.h>

#include <Servo.h>

#include <XBee.h>

Servo myservo1;
Servo myservo2;
Servo myservo3; 

//int pos = 0;

//SoftwareSerial ssRxTx1(19,18); // RX, TX
//SoftwareSerial ssRxTx2(17,16); // RX, TX
//SoftwareSerial ssRxTx3(15,14); // RX, TX

XBee xbee1 = XBee();
XBee xbee2 = XBee();
XBee xbee3 = XBee();
XBeeResponse response = XBeeResponse();
Rx16Response rx16 = Rx16Response();
//Rx64Response rx64 = Rx64Response();
uint16_t addr16 = 0;
uint16_t x = 0;
void setup(){
  Serial.begin(9600);
//  ssRxTx1.begin(9600);
//  ssRxTx2.begin(9600);
//  ssRxTx3.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
  xbee1.setSerial(Serial1);
  xbee2.setSerial(Serial2);
  xbee3.setSerial(Serial3);
  myservo1.attach(2);
  myservo2.attach(3);
  myservo3.attach(4);
  myservo1.write(90);
  myservo2.write(90);
  myservo3.write(90);

}

void loop(){
  //CDA1
  xbee1.readPacket();
  // Receiver Code
  if(xbee1.getResponse().isAvailable()){
    Serial.println("I received something 1");
      xbee1.getResponse().getRx16Response(rx16);
      addr16= rx16.getRemoteAddress16();
      if (addr16 == 51966){
        //move servo
        myservo1.write(170);
        Serial.println("Manual Override initiated 1");
        delay(3000);
        myservo1.write(90);
        }
       else{
        Serial.println("not my coordinator 1");
        }
        }
  else{
    }
    
   //CDA2
  xbee2.readPacket();
  // Receiver Code
  if(xbee2.getResponse().isAvailable()){
    Serial.println("I received something 2");
      xbee2.getResponse().getRx16Response(rx16);
      addr16= rx16.getRemoteAddress16();
      if (addr16 == 51966){
        //move servo
        myservo2.write(170);
        Serial.println("Manual Override initiated 2");
        delay(3000);
        myservo2.write(90);
        }
       else{
        Serial.println("not my coordinator 2");
        }
        }
  else{
    }

    //CDA3
  xbee3.readPacket();
  // Receiver Code
  if(xbee3.getResponse().isAvailable()){
    Serial.println("I received something 3");
      xbee3.getResponse().getRx16Response(rx16);
      addr16= rx16.getRemoteAddress16();
      if (addr16 == 51966){
        //move servo
        myservo3.write(170);
        Serial.println("Manual Override initiated 3");
        delay(3000);
        myservo3.write(90);
        }
       else{
        Serial.println("not my coordinator 3");
        }
        }
  else{
    } 
    
    }
