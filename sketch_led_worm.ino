/* LED worm animation via serial communication */

#define ROW1  2
#define ROW2  9
#define ROW3  17
#define ROW4  3
#define ROW5  10
#define ROW6  16
#define ROW7  11
#define ROW8  12

#define COL1  6
#define COL2  13
#define COL3  14
#define COL4  4
#define COL5  15
#define COL6  5
#define COL7  7
#define COL8  8

#define ROW_LENGTH  8
#define COL_LENGTH  8
#define BUFFER_LENGTH  64
//#define BUFFER_LENGTH 256

boolean matrix[BUFFER_LENGTH] = { 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0};
boolean matrix_tmp[BUFFER_LENGTH];
int row_pin[8] = { 10,15,9,13,2,8,3,6};
int col_pin[8] = { 14,4,5,11,7,12,16,17};

int serial_index = 0;

void setup() {
  int i=0;
  for(i=2;i<=17;i++){
    pinMode(i,OUTPUT);
  }

  for(i=0; i<8; i++){
    digitalWrite(row_pin[i], LOW);
    digitalWrite(col_pin[i], LOW);
  }
  //Serial.begin(9600);
  Serial.begin(115200);
  
}

void loop() {

  for (int index=0;index<BUFFER_LENGTH;index++){
    int blink_row = (index / COL_LENGTH) % ROW_LENGTH;
    int blink_col = index % COL_LENGTH;
    for (int row=0;row<ROW_LENGTH;row++){
      if (blink_row != row) {
        digitalWrite(row_pin[row], LOW);
      } else {
        digitalWrite(row_pin[row], HIGH);
        for (int col=0;col<COL_LENGTH;col++){
          if ( (blink_col == col) && (matrix[index] == 1) ) {
            digitalWrite(col_pin[col], LOW);
          } else {
            digitalWrite(col_pin[col], HIGH);
          }
        }
      }
    }
    delayMicroseconds(2);
  }
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();

    if (incomingByte != 10) {    //Ignore LF
      if (incomingByte == '1') {
        matrix[serial_index] = 1;
      } else if (incomingByte == '0') {
        matrix[serial_index] = 0;
      } else {
        matrix[serial_index] = 1;
      }
      serial_index++;
      if (serial_index >=  BUFFER_LENGTH) {
        serial_index = 0;
      }
    }
  }

}
