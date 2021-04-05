
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

display.clearDisplay();
display.setTextSize(2);
display.setTextColor(WHITE);
}
 
void loop() {

display.setCursor(0,10);
display.print("HR: #");
display.display();
delay(3000);
display.clearDisplay();

display.setCursor(30,30);
display.print("YIKES!");
display.display();
delay(1000);
display.clearDisplay();

display.setCursor(5,25);
display.print("Breathe In");
display.display();
delay(1000);
display.clearDisplay();

breathingExercise();
display.clearDisplay();

display.setCursor(48,30);
display.print("OUT");
display.display();

display.clearDisplay();
delay(1000);

breathingExercise();
display.clearDisplay();

}

//create function to print text

void printText(){

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,10);
  display.print("Breathe");
  display.display();
}

void breathingExercise(){
 
  display.fillCircle(64,32,10,WHITE);
  display.display();
  delay(250);
  display.fillCircle(64,32,20,WHITE);
  display.display();
  delay(250);
  display.fillCircle(64,32,30,WHITE);
  display.display();
  delay(250);
  display.fillCircle(64,32,50,WHITE);
  display.display();
  delay(250);
  display.fillCircle(64,32,60,WHITE);
  display.display();
  delay(250);
  display.clearDisplay();
  display.fillCircle(64,32,50,WHITE);
  display.display();
  delay(250);
  display.clearDisplay();
  display.fillCircle(64,32,40,WHITE);
  display.display();
  delay(250);
  display.clearDisplay();
  display.fillCircle(64,32,30,WHITE);
  display.display();
  delay(250);
  display.clearDisplay();
  display.fillCircle(64,32,20,WHITE);
  display.display();
  delay(250);
  display.clearDisplay();
  display.fillCircle(64,32,10,WHITE);
  display.display();
}
