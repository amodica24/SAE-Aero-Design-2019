#include <SoftwareSerial.h>

#include <Servo.h>

Servo myservo; 

int pos = 0;

SoftwareSerial XBee(10, 11); // RX, TX

void setup(){
  Serial.begin(9600);
  XBee.begin(9600);
  myservo.attach(2);
  myservo.write(90);

  //pinMode(7, OUTPUT);
  }

void loop(){
  // Receiver Code
  if(XBee.available())
  { 
    char XBEEOUTPUT = XBee.read();
    //Serial.print(XBEEOUTPUT);
    Serial.print((char)XBEEOUTPUT);
  //CW
  if (char(XBEEOUTPUT) == 'R') 
  {
      myservo.write(0);
  }
  //CCW  
  else if (char(XBEEOUTPUT) == 'L') 
  { 
      myservo.write(180);
  }
  //Neutral
  else
  {
     myservo.write(90);
  }
 }
}
