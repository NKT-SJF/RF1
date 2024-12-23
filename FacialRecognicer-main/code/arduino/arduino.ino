#include <bufferfiller.h>
#include <enc28j60.h>
#include <EtherCard.h>
#include <net.h>
#include <stash.h>

#define ESTATICA 1

#if ESTATICA
  static byte myip[] = { 10,50,4,205 };
  static byte gwip[] = { 10,50,4,1 };
#endif

static byte mymac[] = { 0x74,0x69,0x69,0x2D,0x30,0x31 };

byte Ethernet::buffer[500]; 

const char page[] PROGMEM =
"HTTP/1.0 200 OK\r\n"
"Content-Type: text/html\r\n"
"\r\n"
"<html>"
  "<head><title>"
    "Control de Puerta"
  "</title></head>"
  "<body>"
  "<h1>Bomba de tiempo</h1>"
  "<p><a href=\"/ON\"><button>Abrir Puerta</button></a></p>"
  "<p><em>"
    "Esto es una prueba.<br />"
    ":)."
  "</em></p>"
  "</body>"
"</html>"
;

const int relayPin = 7;
bool relayState = false;

void setup() {
  Serial.begin(19200);
  Serial.println("\n[Vuelva pronto]");

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // Asegúrate de que el relé está apagado al inicio

  if (ether.begin(sizeof Ethernet::buffer, mymac) == 0) 
    Serial.println("Error al acceder al controlador Ethernet");

  #if ESTATICA
    ether.staticSetup(myip, gwip);
  #else
    if (!ether.dhcpSetup())
      Serial.println("DHCP falló");
  #endif

  ether.printIp("IP:  ", ether.myip);
  ether.printIp("GW:  ", ether.gwip);  
  ether.printIp("DNS: ", ether.dnsip);  
}

void loop() {
  if (ether.packetLoop(ether.packetReceive())) {
    uint8_t* data = ether.tcpOffset(); // Obtener el offset TCP
    if (strstr((char*)data, "GET /ON")) {
      relayState = true;
      digitalWrite(relayPin, HIGH);
      delay(100);
      digitalWrite(relayPin, LOW);
      relayState = false;
    } else if (strstr((char*)data, "GET /OFF")) {
      relayState = false;
      digitalWrite(relayPin, LOW);
    }

    memcpy_P(ether.tcpOffset(), page, sizeof(page));
    ether.httpServerReply(sizeof(page) - 1);
  }
}