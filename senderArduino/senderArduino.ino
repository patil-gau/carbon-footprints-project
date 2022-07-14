#include "CO2Sensor.h"
#include<SoftwareSerial.h> 

SoftwareSerial mySerial(6,5);//RX,TX

#define temp_sensor_pin  A1 
#define co2_sensor_pin  A0

#define buzzer_pin 13
#define alert_co2_led_pin 12 
#define alert_temp_led_pin 11

#define MAX_CO2_VALUE 1000
#define MAX_TEMP_VALUE 50

float a[]={0.0,0.0}; 

CO2Sensor co2Sensor(co2_sensor_pin, 0.99, 100);



float readTemperatureSensor()
   {
    int temp_adc_val;
    float temp_val;
    temp_adc_val = analogRead(temp_sensor_pin); 
    float calculated_value = (temp_adc_val/1024.0)*5000; 
    temp_val = (calculated_value/10);
    Serial.print("Temp value : ");
    Serial.print(temp_val);
    Serial.println(""); 
     return temp_val; 
    
   }
   


int readCo2Sensor()
  {
   int co2_val = co2Sensor.read(); 
   Serial.print("Co2 value : ");
   Serial.print(co2_val);
   Serial.println(""); 
    return co2_val;
  }

void senddata(float co2value,float tempvalue){
   int i;
   mySerial.print("<");
   mySerial.print(co2value);
   mySerial.print(",");
   mySerial.print(tempvalue);
   mySerial.print(">");
}



void setup() {

  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(buzzer_pin,OUTPUT);
  pinMode(alert_co2_led_pin,OUTPUT);
  pinMode(alert_temp_led_pin,OUTPUT);
  co2Sensor.calibrate();
  

}

void loop() {

  float co2value = readCo2Sensor();
  float tempvalue = readTemperatureSensor();
  delay(100); 
  senddata(co2value,tempvalue);  
  
  
  if(tempvalue>MAX_TEMP_VALUE)
      {
         digitalWrite(alert_temp_led_pin,HIGH);
         digitalWrite(buzzer_pin,HIGH);
         delay(2000);
         digitalWrite(buzzer_pin,LOW);
      }
    else 
      {
         digitalWrite(alert_temp_led_pin,LOW);
         digitalWrite(buzzer_pin,LOW); 
      }

      
  if(co2value>MAX_CO2_VALUE)
    {
      digitalWrite(alert_co2_led_pin,HIGH);
      digitalWrite(buzzer_pin,HIGH);
      delay(2000);
      digitalWrite(buzzer_pin,LOW);
    }
   else
    {
      digitalWrite(alert_co2_led_pin,LOW);
      digitalWrite(buzzer_pin,LOW);
    }    
  delay(10000);

}
