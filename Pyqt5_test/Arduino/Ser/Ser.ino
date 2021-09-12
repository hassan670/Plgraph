String data; 
bool flag = false;
 String id = "39999";

void setup() {
 Serial.begin(115200);
 while(!Serial){;}
 Serial.flush();
 Serial.println("ready");

 while (true){
   while(Serial.available()==0){} //do nothing until serial input
   data = Serial.readString();    //Read incoming serial data
   data.trim();                   //Remove unwanted characters on input string
  
   if(data == "id"){              // print device id if requested
    Serial.println("id"+id);      //attach id identifier on device id
   }
   if (data == "start"){          // starting condition
    flag = true;
    break;
   }
 }
}

void loop() { 
  if (flag == true){
    Serial.println("in loop");
  }
}
