import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
import requests
import serial
import time, sys
import datetime

TOKEN = "A1E-0rxa5NT8UljyPhWLqhfNP9FmjPJZHq"  # Put your TOKEN here
DEVICE_LABEL = "agri"  # Put your device label here 
VARIABLE_LABEL_1 = "moisture"  # Put your first variable label here
VARIABLE_LABEL_2 = "status"  # Put your second variable label here
VARIABLE_LABEL_3 = "mode"  # Put your second variable label here
VARIABLE_LABEL_4 = "motor_control"  # Put your second variable label here
VARIABLE_LABEL_5 = "motor_status"  # Put your second variable label here

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering

PUMP = 11
SWITCH = 22
SOIL_MOISTURE = 7
RELAY = 15
mode = 1

GPIO.setup(PUMP, GPIO.OUT, initial=GPIO.LOW)   #
GPIO.setup(RELAY, GPIO.OUT, initial=GPIO.LOW)   #
GPIO.setup(SWITCH, GPIO.IN)   #
GPIO.setup(SOIL_MOISTURE, GPIO.IN)   #
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button) 
SERIAL_PORT = "/dev/ttyS0"    # Raspberry Pi 3

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 1)
ser.write('AT+CMGF=1\r') # set to text mode
sleep(3)
ser.write('AT+CMGDA="DEL ALL"\r') # delete all SMS
sleep(3)
reply = ser.read(ser.inWaiting()) # Clean buf
print "Listening for incomming SMS..."

sms_flag = 1
power_flag = 1
soil = 0
calibrate = 1
wet_flag  = False
def build_payload(variable, value):
    # Creates two random values for sending data
    payload = {variable: value}
    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://app.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def get_var(device, variable):
    try:
        url = "http://app.ubidots.com/"
        url = "{0}api/v1.6/devices/{1}/{2}/".format(url, device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except:
        pass
    
def auto_mode():
    global soil
    global sms_flag
    if soil == 1:
        sms_flag=1
        GPIO.output(PUMP, GPIO.HIGH)
        payload = build_payload(VARIABLE_LABEL_5, 1)
        post_request(payload)
    else:
        GPIO.output(PUMP, GPIO.LOW)
        payload = build_payload(VARIABLE_LABEL_5, 0)
        post_request(payload)

def manual_mode():
    global soil
    global sms_flag
    global calibrate
    global wet_flag
    
    control = get_var(DEVICE_LABEL, VARIABLE_LABEL_4)
    print("control: {}".format(control))
    control = int(control)
    if calibrate == 1:
        print("please calibrate the soil sensor");
        
    if control == 1:
        GPIO.output(PUMP, GPIO.HIGH)
        payload = build_payload(VARIABLE_LABEL_5, 1)
        post_request(payload)
        if soil == 0 and wet_flag == True and sms_flag == 0:
            calibrate = 0    
            ser.write('AT+CMGS="+918919745605"\r')
            sleep(3)
            msg = "SOIL WET : SWITCH OFF THE MOTOR"
            print("Sending SMS with status info:" + msg)
            ser.write(msg + chr(26))
            sms_flag = 1
            sleep(3)
            
    elif control == 0:
        GPIO.output(PUMP, GPIO.LOW)
        payload = build_payload(VARIABLE_LABEL_5, 0)
        post_request(payload)
        if soil == 1 and wet_flag == False and sms_flag == 1:
            ser.write('AT+CMGS="+918919745605"\r')
            sleep(3)
            msg = "SOIL DRY : SWITCH ON THE MOTOR"
            print("Sending SMS with status info:" + msg)
            sms_flag = 0
            ser.write(msg + chr(26))
            sleep(3)
                
def power_checker():
    global power_flag
    switch = GPIO.input(SWITCH)
    if switch == 1 and power_flag == 0:
        power_flag = 1 
        print("Power Failure");
        GPIO.output(RELAY, GPIO.LOW)
        payload = build_payload(VARIABLE_LABEL_2, 0)
        post_request(payload)
        sleep(1)
        ser.write('AT+CMGS="+918919745605"\r')
        sleep(3)
        msg = "Power OFF :from GSM Agri"
        print("Sending SMS with status info:" + msg)
        ser.write(msg + chr(26))
        sleep(3)
    elif switch == 0 and power_flag == 1:
        power_flag = 0
        print("Power ON Condition")
        GPIO.output(RELAY, GPIO.HIGH)
        payload = build_payload(VARIABLE_LABEL_2, 1)
        post_request(payload)  

if __name__ == "__main__":
    while True:
        soil = GPIO.input(SOIL_MOISTURE)
        if soil == 0:
            wet_flag = True
        elif soil == 1:
            wet_flag = False
        print("Soil :" + str(soil))
        payload = build_payload(VARIABLE_LABEL_1, soil)
        post_request(payload)
        mode = get_var(DEVICE_LABEL, VARIABLE_LABEL_3)
        print(mode)
        mode = int(mode)
        print("Mode :{}".format(mode))
        if mode == 1:
            auto_mode()
            #power_checker()
        elif mode == 0:
            manual_mode()
        power_checker()    
        sleep(0.5)
        
            
