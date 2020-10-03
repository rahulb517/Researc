#include <Ethernet.h> //ethernet lib
#include <EthernetUdp.h> //UDP lib
#include <SPI.h> //SPI lib

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE}; //assign mac address
IPAddress ip(192, 168, 0, 144); //Arduino's IP
unsigned int localPort = 5010; //assign a port
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
int packetSize;
EthernetUDP Udp; //Udp object


void setup() {
  Ethernet.begin(mac, ip); //init ethernet
  Udp.begin(localPort);
  Serial.begin(9600);
  delay(1500);

 

}


void loop() {

  packetSize = Udp.parsePacket(); //read packet size

  if(packetSize > 0){ //check if there has been a request
     Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
     String str = "";
     if(strcmp(packetBuffer, "Data") == 0){
        unsigned int id = 12;
        float temp = random(30, 70)/ 3.0; //replace these with methods to measure temp, no2, and pressre
        float pressure = random(7000, 8000) / 9.0;
        float no2 = random(1000, 1500) / 8.0;
        str = str + String(id) + "," + String(temp) + "," + String(pressure) + "," + String(no2);
        unsigned int len = str.length() + 1;
        char buf[len];
        str.toCharArray(buf, len);
        
        Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()); //init packet send
        Udp.print(buf); //send string back to client
        Udp.endPacket(); //end packet send
     }
     //memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE);
  }
}
