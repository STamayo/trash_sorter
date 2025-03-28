const int pres = A0;
const int led = 2;
int value = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  pinMode(pres, INPUT);  //set A0 as an input pin;
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  value = analogRead(pres);
  Serial.println(value);

  delay(500);
}
