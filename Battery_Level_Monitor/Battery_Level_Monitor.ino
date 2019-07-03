#include <LiquidCrystal.h>


const int rs = 12, en = 13, d0 = A0, d1 = A1, d2 = A2, d3 = A3;
const int analogPin = A4;
LiquidCrystal lcd(rs, en, d0, d1, d2, d3);
float analogValue;
float input_voltage;

int ledPins[] = { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 }; // an array of pin numbers to which LEDs are attached
int pinCount = 10;           // the number of pins (i.e. the length of the array)

void setup()
{
   Serial.begin(9600);     //  opens serial port, sets data rate to 9600 bps
   lcd.begin(16, 2);       //// set up the LCD's number of columns and rows: 
   pinMode(A0,OUTPUT);
   pinMode(A1,OUTPUT);
   pinMode(A2,OUTPUT);
   pinMode(A3,OUTPUT);
   pinMode(A4,INPUT);
   lcd.print("Voltage Level");
}

void LED_function(int stage)
{
    for (int j=2; j<=11; j++)
    {
    digitalWrite(j,LOW);
    }
    for (int i=1, l=2; i<=stage; i++,l++)
    {
    digitalWrite(l,HIGH);    //delay(30);
    }
   
}
void loop()
{
//  Conversion formula for voltage
  analogValue = analogRead (A4);
  Serial.println(analogValue);
  delay (1000); 
  input_voltage = (analogValue * 5.0) / 1024.0;
  lcd.setCursor(0, 1);
  lcd.print("Voltage= ");
  lcd.print(input_voltage);
  Serial.println(input_voltage);
  delay(100);

  if (input_voltage < 0.50 && input_voltage >= 0.00 )
    {
    digitalWrite(2, HIGH);
    delay (30);
    digitalWrite(2, LOW);
    delay (30);
    }
  else if (input_voltage < 1.00 && input_voltage >= 0.50)
    {
    LED_function(2);
    }
  else if (input_voltage < 1.50 && input_voltage >= 1.00)
    {
    LED_function(3);
    }
  else if (input_voltage < 2.00 && input_voltage >= 1.50)
    {
    LED_function(4);
    }
  else if (input_voltage < 2.50 && input_voltage >= 2.00)
    {
    LED_function(5);
    }
  else if (input_voltage < 3.00 && input_voltage >= 2.50)
    {
    LED_function(6);
    }
  else if (input_voltage < 3.50 && input_voltage >= 3.00)
    {
    LED_function(7);
    }
  else if (input_voltage < 4.00 && input_voltage >= 3.50)
    {
    LED_function(8);
    }
  else if (input_voltage < 4.50 && input_voltage >= 4.00)
    {
    LED_function(9);
    }
  else if (input_voltage < 5.00 && input_voltage >= 4.50)
    {
    LED_function(10);
    }
}
