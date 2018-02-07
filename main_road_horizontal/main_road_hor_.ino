#include <SoftwareSerial.h>
#include <SparkFunESP8266WiFi.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include "RTClib.h"

RTC_DS3231 rtc;
int count=0;int val=0;int ir1=0;
int ir2=0;

/* This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
   which provides a common 'type' for sensor data and some helper functions.
   
   To use this driver you will also need to download the Adafruit_Sensor
   library and include it in your libraries folder.

   You should also assign a unique ID to this sensor for use with
   the Adafruit Sensor API so that you can identify this particular
   sensor in any data logs, etc.  To assign a unique ID, simply
   provide an appropriate value in the constructor below (12345
   is used by default in this example).
   
   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3V DC
   Connect GROUND to common ground

   I2C Address
   ===========
   The address will be different depending on whether you leave
   the ADDR pin floating (addr 0x39), or tie it to ground or vcc. 
   The default addess is 0x39, which assumes the ADDR pin is floating
   (not connected to anything).  If you set the ADDR pin high
   or low, use TSL2561_ADDR_HIGH (0x49) or TSL2561_ADDR_LOW
   (0x29) respectively.
    
   History
   =======
   2013/JAN/31  - First version (KTOWN)
*/

#define IRSens1Pin 52
#define IRSens2Pin 50
#define IRSens3Pin 48
#define IRSens4Pin 46

#define STLight1 2
#define STLight2 3
#define STLight3 4
#define STLight4 5
#define STLight5 6
#define STLight6 7
#define STLight7 8
#define STLight8 9
#define STLight9 10
#define STLight10 11
#define STLight11 12
#define STLight12 13

//////////////////////////////
// WiFi Network Definitions //
//////////////////////////////
// Replace these two character strings with the name and
// password of your WiFi network.
const char mySSID[] = "CS-RESEARCH";
const char myPSK[] ="marthogidhe";

int i=0;
int j, ctrl_var=0;

//////////////////////////////
// ESP8266Server definition //
//////////////////////////////
// server object used towards the end of the demo.
// (This is only global because it's called in both setup()
// and loop()).
ESP8266Server server = ESP8266Server(80);

Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

//////////////////
// HTTP Strings //
//////////////////
const char destServer[] = "example.com";
const String htmlHeader = "HTTP/1.1 200 OK\r\n"
                          "Content-Type: text/html\r\n"
                          "Connection: close\r\n\r\n"
                          "<!DOCTYPE HTML>\r\n"
                          "<html>\r\n"
                          "<head></head>\r\n"
                          "<body>\r\n";

const String httpRequest = "GET / HTTP/1.1\n"
                           "Host: example.com\n"
                           "Connection: close\n\n";

int light;
String light1;

/*void displaySensorDetails(void)
{
  sensor_t sensor;
  tsl.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" lux");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" lux");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" lux");  
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}*/                 

void configureSensor(void)
{
  /* You can also manually set the gain or enable auto-gain support */
  // tsl.setGain(TSL2561_GAIN_1X);      /* No gain ... use in bright light to avoid sensor saturation */
  // tsl.setGain(TSL2561_GAIN_16X);     /* 16x gain ... use in low light to boost sensitivity */
  tsl.enableAutoRange(true);            /* Auto-gain ... switches automatically between 1x and 16x */
  
  /* Changing the integration time gives you better sensor resolution (402ms = 16-bit data) */
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);      /* fast but low resolution */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_101MS);  /* medium resolution and speed   */
  // tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_402MS);  /* 16-bit data but slowest conversions */

  /* Update these values depending on what you've set above! */  
  Serial.println("------------------------------------");
  Serial.print  ("Gain:         "); Serial.println("Auto");
  Serial.print  ("Timing:       "); Serial.println("13 ms");
  Serial.println("------------------------------------");
}

// All functions called from setup() are defined below the
// loop() function. They modularized to make it easier to
// copy/paste into sketches of your own.
void setup() 
{
  // Serial Monitor is used to control the demo and view
  // debug information.
  Serial.begin(115200);

  pinMode(IRSens1Pin, INPUT);
  pinMode(IRSens2Pin, INPUT);
  pinMode(IRSens3Pin, INPUT);
  pinMode(IRSens4Pin, INPUT);

  pinMode(STLight1, OUTPUT);
  pinMode(STLight2, OUTPUT);
  pinMode(STLight3, OUTPUT);
  pinMode(STLight4, OUTPUT);
  pinMode(STLight5, OUTPUT);
  pinMode(STLight6, OUTPUT);
  pinMode(STLight7, OUTPUT);
  pinMode(STLight8, OUTPUT);
  pinMode(STLight9, OUTPUT);
  pinMode(STLight10, OUTPUT);
  pinMode(STLight11, OUTPUT);
  pinMode(STLight12, OUTPUT);

  
  /*for(int i = 0; i < 255; i++)
  {
    analogWrite(STLight1, i); 
    analogWrite(STLight2, i); 
    analogWrite(STLight3, i); 
    analogWrite(STLight4, i); 
    delay(50);
    Serial.println(i);
  }*/
  

  if(!tsl.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.print("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  //displaySensorDetails();
  configureSensor();
  
  // initializeESP8266() verifies communication with the WiFi
  // shield, and sets it up.
  initializeESP8266();

  // connectESP8266() connects to the defined WiFi network.
  connectESP8266();

  // displayConnectInfo prints the Shield's local IP
  // and the network it's connected to.
  displayConnectInfo();
  
  serverSetup();
}

void loop() 
{
  serverDemo();
  /* Get a new sensor event */ 
  DateTime now=rtc.now();
  sensors_event_t event;
  tsl.getEvent(&event);
  light = event.light;
  Serial.println(event.light);
  light1=String(light);
  
  
  Serial.println(digitalRead(IRSens2Pin));
  Serial.print(now.hour(),DEC);
  Serial.print(":");
  Serial.println(now.minute(),DEC);
 // hour=now.hour();
 // Serial.print(hour);
 
// val=digitalRead(STLight1);
Serial.println(val); 
  if(ctrl_var == 0)
  {
        /* Display the results (light is measured in lux) */
    if (event.light)
    {
      Serial.print(event.light); Serial.println(" lux");
    }
    else
    {
      /* If event.light = 0 lux the sensor is probably saturated
         and no reliable data could be generated! */
      Serial.println("Sensor overload");
    }
    
    if(event.light>=700)
    {
      //for(j=i;j>=0;j--)
      //{
    
        analogWrite(STLight1, 0);
        analogWrite(STLight2, 0);
        analogWrite(STLight3, 0);
        analogWrite(STLight4, 0);
        analogWrite(STLight5, 0);
        analogWrite(STLight6, 0);
        analogWrite(STLight7, 0);
        analogWrite(STLight8, 0);
        analogWrite(STLight9, 0);
        analogWrite(STLight10, 0);
        analogWrite(STLight11, 0);
        analogWrite(STLight12, 0);
          delay(1000);
          //loop();
          val=0;count=1;
          serverDemo();count=0;
          loop();
          
      //}
      //i=0;
    }
     if(now.hour()>=10 && !(int(digitalRead(IRSens1Pin))) && !(int(digitalRead(IRSens2Pin))) && count!=1){
      
     
    
      //for(j=i;j<131;j++)
     // {
    
        analogWrite(STLight1, 50);Serial.println("midway");
        analogWrite(STLight2,50);
        analogWrite(STLight3,50);
        analogWrite(STLight4,50);
        analogWrite(STLight5,50);
        analogWrite(STLight6,50);
        analogWrite(STLight7,50);
        analogWrite(STLight8,50);
        analogWrite(STLight9,50);
        analogWrite(STLight10,50);
        analogWrite(STLight11,50);
        analogWrite(STLight12,50);
        val=1;light=event.light;
        serverDemo();
          delay(25);
        }
     
      //i=131;
      if(int(digitalRead(IRSens1Pin)))
      
      {
        analogWrite(STLight1, 250);
        analogWrite(STLight2,250);delay(500);
        analogWrite(STLight3,250);
        analogWrite(STLight4,250);delay(500);
        analogWrite(STLight5,250);
        analogWrite(STLight6,250);delay(500);
        analogWrite(STLight7,250);
        analogWrite(STLight8,250);delay(500);
        analogWrite(STLight9,250);
        analogWrite(STLight10,250);delay(500);
        analogWrite(STLight11,250);
        analogWrite(STLight12,250);val=2;
        serverDemo();light=event.light;ir1=1;
        count=1;
      }
       if(int(digitalRead(IRSens2Pin)))
      
      {
        /*analogWrite(STLight12, 0);
        analogWrite(STLight11,0);
        analogWrite(STLight10,0);
        analogWrite(STLight9,0);*/
        analogWrite(STLight8,250);
        analogWrite(STLight7,250);delay(500);
        analogWrite(STLight6,250);
        analogWrite(STLight5,250);delay(500);
        analogWrite(STLight4,250);
        analogWrite(STLight3,250);delay(500);
        analogWrite(STLight2,250);
        analogWrite(STLight1,250);val=2;
        serverDemo();light=event.light;ir2=1;
        count=1;
      }
    if(count==1){
      for(int i=0;i<20;i++){
       if(int(digitalRead(IRSens1Pin))){
        
        i=0;light=event.light;
        serverDemo();
       }
       if(int(digitalRead(IRSens1Pin))){
          analogWrite(STLight9, 250);
          analogWrite(STLight10,250);
          analogWrite(STLight11,250);
          analogWrite(STLight12,250);
          serverDemo();
          i=0;
        }light=event.light;
       serverDemo();
       delay(1000); 
      }count=0;ir1=0;ir2=0;
    }
    Serial.write(int(event.light));
    if(event.light<800 && now.hour()<10)
    { 
     // for(j=i;j<256;j++)
     // {
    
        analogWrite(STLight1, 255);
        analogWrite(STLight2, 255);
        analogWrite(STLight3, 255);
        analogWrite(STLight4, 255);
        analogWrite(STLight5, 255);
        analogWrite(STLight6, 255);
        analogWrite(STLight7, 255);
        analogWrite(STLight8, 255);
        analogWrite(STLight9, 255);
        analogWrite(STLight10, 255);
        analogWrite(STLight11, 255);val=2;
        analogWrite(STLight12, 255);
          delay(25);
      //}
     i=255;
    }}
  if(val=1){for(int c=1;c<13;c++){
    
  }}
  
  delay(1000);
  
}

void initializeESP8266()
{
  // esp8266.begin() verifies that the ESP8266 is operational
  // and sets it up for the rest of the sketch.
  // It returns either true or false -- indicating whether
  // communication was successul or not.
  // true
  int test = esp8266.begin();
  if (test != true)
  {
    Serial.println(F("Error talking to ESP8266."));
    errorLoop(test);
  }
  Serial.println(F("ESP8266 Shield Present"));
}

void connectESP8266()
{
  // The ESP8266 can be set to one of three modes:
  //  1 - ESP8266_MODE_STA - Station only
  //  2 - ESP8266_MODE_AP - Access point only
  //  3 - ESP8266_MODE_STAAP - Station/AP combo
  // Use esp8266.getMode() to check which mode it's in:
  int retVal = esp8266.getMode();
  if (retVal != ESP8266_MODE_STA)
  { // If it's not in station mode.
    // Use esp8266.setMode([mode]) to set it to a specified
    // mode.
    retVal = esp8266.setMode(ESP8266_MODE_STA);
    if (retVal < 0)
    {
      Serial.println(F("Error setting mode."));
      errorLoop(retVal);
    }
  }
  Serial.println(F("Mode set to station"));

  // esp8266.status() indicates the ESP8266's WiFi connect
  // status.
  // A return value of 1 indicates the device is already
  // connected. 0 indicates disconnected. (Negative values
  // equate to communication errors.)
  retVal = esp8266.status();
  if (retVal <= 0)
  {
    Serial.print(F("Connecting to "));
    Serial.println(mySSID);
    // esp8266.connect([ssid], [psk]) connects the ESP8266
    // to a network.
    // On success the connect function returns a value >0
    // On fail, the function will either return:
    //  -1: TIMEOUT - The library has a set 30s timeout
    //  -3: FAIL - Couldn't connect to network.
    retVal = esp8266.connect(mySSID, myPSK);
    if (retVal < 0)
    {
      Serial.println(F("Error connecting"));
      errorLoop(retVal);
    }
  }
}

void displayConnectInfo()
{
  char connectedSSID[24];
  memset(connectedSSID, 0, 24);
  // esp8266.getAP() can be used to check which AP the
  // ESP8266 is connected to. It returns an error code.
  // The connected AP is returned by reference as a parameter.
  int retVal = esp8266.getAP(connectedSSID);
  if (retVal > 0)
  {
    Serial.print(F("Connected to: "));
    Serial.println(connectedSSID);
  }

  // esp8266.localIP returns an IPAddress variable with the
  // ESP8266's current local IP address.
  IPAddress myIP = esp8266.localIP();
  Serial.print(F("My IP: ")); Serial.println(myIP);
}

/*void clientDemo()
{
  // To use the ESP8266 as a TCP client, use the 
  // ESP8266Client class. First, create an object:
  ESP8266Client client;

  // ESP8266Client connect([server], [port]) is used to 
  // connect to a server (const char * or IPAddress) on
  // a specified port.
  // Returns: 1 on success, 2 on already connected,
  // negative on fail (-1=TIMEOUT, -3=FAIL).
  int retVal = client.connect(myIP, 80);
  if (retVal <= 0)
  {
    Serial.println(F("Failed to connect to server."));
    return;
  }

  // print and write can be used to send data to a connected
  // client connection.
  client.print(httpRequest);

  // available() will return the number of characters
  // currently in the receive buffer.
  while (client.available())
    Serial.write(client.read()); // read() gets the FIFO char
  
  // connected() is a boolean return value - 1 if the 
  // connection is active, 0 if it's closed.
  if (client.connected())
    client.stop(); // stop() closes a TCP connection.
}*/

void serverSetup()
{
  // begin initializes a ESP8266Server object. It will
  // start a server on the port specified in the object's
  // constructor (in global area)
  server.begin();
  Serial.print(F("Server started! Go to "));
  Serial.println(esp8266.localIP());
  Serial.println();
}

void serverDemo()
{
  // available() is an ESP8266Server function which will
  // return an ESP8266Client object for printing and reading.
  // available() has one parameter -- a timeout value. This
  // is the number of milliseconds the function waits,
  // checking for a connection.
  ESP8266Client client = server.available(500);
  
  if (client) 
  {
    Serial.println(F("Client Connected!"));
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) 
    {
      
      if (client.available()) 
      {
        String request = client.readString();
        Serial.print("Received: ");
        Serial.println(request);
        client.flush();
        if (request.indexOf("LED=AUTO") != -1)
        {
          ctrl_var=0;
          loop();
        }
        if (request.indexOf("LED=ON") != -1)
        {
          ctrl_var=1;
          digitalWrite(STLight1, HIGH);
          digitalWrite(STLight2, HIGH);
          digitalWrite(STLight3, HIGH);
          digitalWrite(STLight4, HIGH);
          digitalWrite(STLight5, HIGH);
          digitalWrite(STLight6, HIGH);
          digitalWrite(STLight7, HIGH);
          digitalWrite(STLight8, HIGH);
          digitalWrite(STLight9, HIGH);
          digitalWrite(STLight10, HIGH);
          digitalWrite(STLight11, HIGH);
          digitalWrite(STLight12, HIGH);
          Serial.println("LED ON");val=2;
        } 
        if (request.indexOf("LED=OFF") != -1)
        {
          ctrl_var=1; val=0;
          digitalWrite(STLight1, LOW);
          Serial.println("LED OFF");
          digitalWrite(STLight2, LOW);
          digitalWrite(STLight3, LOW);
          digitalWrite(STLight4, LOW);
          digitalWrite(STLight5, LOW);
          digitalWrite(STLight6, LOW);
          digitalWrite(STLight7, LOW);
          digitalWrite(STLight8, LOW);
          digitalWrite(STLight9, LOW);
          digitalWrite(STLight10, LOW);
          digitalWrite(STLight11, LOW);
          digitalWrite(STLight12, LOW);
        }
        if (request.indexOf("L1") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight1, LOW);
          delay(3000);
          Serial.println("LED1 OFF");
        }
        if (request.indexOf("L2") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight2, LOW);
          Serial.println("LED2 OFF");
        }
        if (request.indexOf("L3") != -1){
          ctrl_var=0;
          digitalWrite(STLight3, LOW);
          Serial.println("LED3 OFF");
        }
        if (request.indexOf("L4") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight4, LOW);
          Serial.println("LED4 OFF");
        }
        if (request.indexOf("L5") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight5, LOW);
          Serial.println("LED5 OFF");
        }
        if (request.indexOf("L6") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight6, LOW);
          Serial.println("LED1 OFF");
        }
        if (request.indexOf("L7") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight7, LOW);
          Serial.println("LED1 OFF");
        }
        if (request.indexOf("L8") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight8, LOW);
          Serial.println("LED1 OFF");
        }
        if (request.indexOf("L9") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight9, LOW);
          Serial.println("LED9 OFF");
        }
        if (request.indexOf("L10") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight10, LOW);
          Serial.println("LED10 OFF");
        }
        if (request.indexOf("L11") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight11, LOW);
          Serial.println("LED11 OFF");
        }
        if (request.indexOf("L12") != -1)
        {
          ctrl_var=0;
          digitalWrite(STLight12, LOW);
          Serial.println("LED12 OFF");
        }
        /*if(c == 'z')
          Serial.println("Hi");
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) 
        {*/
          Serial.println(F("Sending HTML page"));
          // send a standard http response header:
          client.print(htmlHeader);
          String htmlBody;
          /*htmlBody +=" <p class=\"lux\">";
          htmlBody += String(light);
          htmlBody+="</p>";*/
          htmlBody +="<p class =\"l8\">";
          
          htmlBody+=val;
          htmlBody+="</p>";  
          /*htmlBody +="<p class =\"l2\">";
          htmlBody+=val;
          htmlBody +="</p>";
          htmlBody +="<p class =\"l3\">";
          htmlBody +=val;
          htmlBody +="</p>";
         htmlBody +="<p class =\"l4\">";
         htmlBody +=val;
         htmlBody +="</p>";
         
         htmlBody +="<p class =\"l5\">";
          htmlBody+=val;
          htmlBody+="</p>";  
          htmlBody +="<p class =\"l6\">";
          htmlBody+=val;
          htmlBody +="</p>";
          htmlBody +="<p class =\"l7\">";
          htmlBody +=val;
          htmlBody +="</p>";
          htmlBody +="<p class =\"l8\">";
          htmlBody +=val;
          htmlBody +="</p>";
          htmlBody +="<p class =\"l9\">";
          htmlBody+=val;
          htmlBody+="</p>";  
          htmlBody +="<p class =\"l10\">";
          htmlBody+=val;
          htmlBody +="</p>";
          htmlBody +="<p class =\"l11\">";
          htmlBody +=val;
          htmlBody +="</p>";
         htmlBody +="<p class =\"l12\">";
         htmlBody +=val;
         htmlBody +="</p>";
          /*htmlBody += "</br>Sensor 1: ";*/
          htmlBody +="<p class =\"IR1\">";
          htmlBody += digitalRead(IRSens1Pin);
          htmlBody +="</p>";
          htmlBody +="<p class =\"IR2\">";
          htmlBody += digitalRead(IRSens2Pin);
          htmlBody +="</p>";

          /*htmlBody += "</br>Sensor 2: ";
          htmlBody += digitalRead(IRSens2Pin);*/

          /*htmlBody += "</br>Sensor 3: ";
          htmlBody += digitalRead(IRSens3Pin);*/
          /*
          htmlBody += "</br>IR: ";
          htmlBody += digitalRead(IRSens2Pin);*/
          
          
          /*for (int a = 0; a < 6; a++)
          {
            htmlBody += "A";
            htmlBody += String(a);
            htmlBody += ": ";
            htmlBody += String(analogRead(a));
            htmlBody += "<br>\n";
          }*/

          htmlBody += "</body>\n";
          htmlBody += "</html>\n";
          client.print(htmlBody);
          break;
        //}
        /*if (c == '\n') 
        {
          // you're starting a new line
          currentLineIsBlank = true;
        }
        else if (c != '\r') 
        {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }*/
      }
    }
    // give the web browser time to receive the data
    delay(10);
   
    // close the connection:
    client.stop();
    Serial.println(F("Client disconnected"));
  }
  
}

// errorLoop prints an error code, then loops forever.
void errorLoop(int error)
{
  Serial.print(F("Error: ")); Serial.println(error);
  Serial.println(F("Looping forever."));
  for (;;)
    ;
}

// serialTrigger prints a message, then waits for something
// to come in from the serial port.
void serialTrigger(String message)
{
  Serial.println();
  Serial.println(message);
  Serial.println();
  while (!Serial.available())
    ;
  while (Serial.available())
    Serial.read();
}
