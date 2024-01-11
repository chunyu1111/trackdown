#include <Servo.h>   //載入函式庫，這是內建的，不用安裝ㄗ
Servo myservo;  // 建立SERVO物件
int state=0;
int counter=0;
String res="";
int angle=0;
void setup(){
  Serial.begin(9600);myservo.attach(6);  // 設定要將伺服馬達接到哪一個PIN腳
}
void loop()
{
  if(state==0)
  {
    Serial.println("req:"+String(counter++));
    state = 1;
  }
  else
  {
    while(Serial.available())
    {
      char c=Serial.read();
      res+=c;
      if(res.endsWith("\n"))
      {
        Serial.println("echo:"+res);
        res.trim();
        angle = res.toInt();
        myservo.write(angle);  //旋轉到0度，就是一般所說的歸零
        delay(1000);
        state = 0;
        res="";
      }
    }
  }
}
