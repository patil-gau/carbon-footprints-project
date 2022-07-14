#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

//last modified one
WiFiClient wifiClient;

String postData;

/* Set these to your desired credentials. */
const char *ssid = "";  //ENTER YOUR WIFI SETTINGS
const char *password = "";
 
String host = "http://192.168.4.247:5000/saveSensorValues"; 




int arrindex = 0;
char recvchars[32];
boolean newdata=false;
String location = "belgavi,karnataka";
char co2value[10];
char tempvalue[10];
char bpvalue[20];
char ecgvalue[30];


void recvdata(){
  static boolean recvinprogress=false;
  int ndx=0;
  char startmarker='<';
  char comma=',';
  char endmarker='>';
  char c;
  int  co2index = 0;
  int tempindex = 0;
  bool  co2reading =  true;
  bool tempreading = false;

 while(!Serial.available() < 0){Serial.println("");}
 
 while(Serial.available()>0 && newdata==false){
    c=Serial.read();
    
    if(c==startmarker)
    {
      recvinprogress=true;
      newdata==false;
      continue;
    }

   if(c==endmarker){
      recvinprogress=false;
      ndx=0;
      break;
    }


    if(recvinprogress==true){
      
      recvchars[ndx]=c;
      ndx++;  
     
      
      if (co2reading==true)
        { 
            if (c==comma)
                {
                  co2reading = false;
                  tempreading= true;  
                  continue;  
                }
            co2value[co2index] = c;
            co2index++;    
       }

       if (tempreading==true)
        { 
           if (c==comma)
                {
                  co2reading = true;
                  tempreading= false;  
                  continue;  
                }
          tempvalue[tempindex] = c;
          tempindex++;    
       }
      
    }

       
   
  }
  newdata = false; 


  
}


void setup() {
  //Serial Begin at 9600 Baud 
  Serial.begin(9600);

  WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA);        //This line hides the viewing of ESP as wifi hotspot
  
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  //If connection successful show IP address in serial monitor
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //IP address assigned to your ESP
  
}

void loop() {
  
HTTPClient http; 

recvdata();

Serial.print("temp value ");
String co2data =  co2value;
Serial.print(co2data);
Serial.println("");
Serial.print("pulse value ");
String tempdata =  tempvalue;
Serial.print(tempdata);
Serial.println("");

Serial.print(recvchars);
Serial.println("");  

String Data = "?Co2Value=" + co2data + "&TempValue=" + tempdata + "&Location=" + location;

String serverPath = host + Data;


http.begin(wifiClient,serverPath.c_str());              
int httpResponseCode = http.GET();
if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
http.end();  //Close connection
delay(10000);  //Post Data at every 5 seconds
  

  
}
