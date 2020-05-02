import sys
import random
import time
import errno
import os
import subprocess
import json
import re
import ast
from subprocess import Popen, PIPE 
from multiprocessing import Pool, Lock
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from subprocess import Popen, PIPE
import pandas as pd


deviceName = "emulator-5554"
#main_activity ='com.oristats.habitbull.activities.CalendarActivity'
appPackage = 'com.duolingo'
wait_activity = 'com.duolingo.app.LoginActivity'
app_path_string = '../senior/apps/duolingo.apk'
app_path = os.path.abspath(app_path_string)

desired_caps = {
            "deviceName" : deviceName,
            "platformName": "Android",
            "udid": deviceName,
            "version": "8.1.0",
            "appActivity" : wait_activity,
            "appPackage" : appPackage,
            "app" : app_path,
            "autoGrantPermissions" : "true",
            "gpsEnabled" : "true",
            "noReset": "true",
            "fullReset" :"false"
        }
result = {}
def appium(appium_port,desired_caps):

    #Setup PI
    Unique_username = "Sylphsgt098VWE"
    Unique_password = "u8zvTBYNnnGn"
    Email = "boomngongseniorproject@gmail.com"
    Unspecified_text = "YaaKcuMEgEsr"
    PhoneNo = "+66825999999"
    firstname = "iBvAdkFi"
    lastname = "eTJexjgnzPGS"
    Country = "Thailand"
    Province = "Bangkok"
    Day = "29"
    Month = "02"
    Year = "1990"
    FULLNAME = firstname + " " + lastname
    Card = "5105105105105100"
    Expir = "1225"
    CVV = "122"
    Postal = "10530"
    
    key = 0
    #search bar
    Search = "Mark"

    PII = {"email" : Email,
    "username" : Unique_username,
    "pass" : Unique_password,
    "pwd" : Unique_password,
    "pword" : Unique_password,
    "phone" : PhoneNo,
    "firstname" : firstname,
    "lastname" : lastname,
    "country" : Country, 
    "province" : Province, 
    "day" : Day,
    "month" : Month,
    "year" : Year,
    "search" : Search,
    "fullname" : FULLNAME,
    "gender" : "1",
    "card" : Card,
    "expir" : Expir,
    "cvc":CVV,
    "cvv":CVV,
    "post" : Postal}
    start_time = time.time()
    end_time = start_time + 1347
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    driver.reset()
    time.sleep(3)
    count = 0 
    
    while (time.time() < end_time):
        try:
            window_size = driver.get_window_size() 
            Clickable_Elements = driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
            Textinput_Elements = []
            for element in Clickable_Elements:
                if element.get_attribute("class") == "android.widget.EditText" and element.get_attribute("focusable") == "true":
                    Textinput_Elements.append(element)
                    Clickable_Elements = list(set(Clickable_Elements) - set(Textinput_Elements))
            #iMonkey
            #random action  1 - 100
            if (len(Clickable_Elements) == 0):
                random_action = random.randrange(81,101)
            elif (len(Textinput_Elements) == 0):
                random_action = random.randrange(21,101)
            else:
                random_action = random.randrange(1,101)
                            
            currentAct = driver.current_activity
            
            #0, filled a random text field | or fill all ? 20 %
            if(random_action < 21):
                temp = random.randrange(len(Textinput_Elements))
                for text_field_element in Textinput_Elements:
                    resource_id = text_field_element.get_attribute("resource-id")
                    for pii in PII:
                        if pii in resource_id.lower():
                            text_field_element.click(); 
                            text_field_element.send_keys(PII[pii]);

                    #1 randomly click on clickable element 60%
            elif (random_action >= 21 and random_action < 81):
                temp = random.randrange(len(Clickable_Elements))
                Clickable_Elements[temp].click()
            #Monkey
            # 15 % swipe randomly (4 direction)
            elif (random_action >= 81 and random_action < 96 ):
                height = window_size["height"]
                width = window_size["width"]
                temp = random.randrange(4)
                #driver.swipe(startX, startY, endX, endY, duration)
                if temp == 0:
                    try:
                        driver.swipe(width/2, height/2, width/2, height/4, 400)
                    except:
                        #driver.swipe(height/2, width/2, height/2, width/4, 400)
                        pass
                elif temp == 1:
                    try:
                        driver.swipe(width/2, height/2, width/2, height*3/4, 400)
                    except:
                        #driver.swipe(height/2, width/2, height/2, width*3/4, 400)
                        pass      
                elif temp == 2:
                    try:
                        driver.swipe(width/2, height/2, width/4, height/4, 400)
                    except:
                        #driver.swipe(height/2, width/2, height/4, width/4, 400)
                        pass

                elif temp == 3:
                    try:
                        driver.swipe(width/2, height/2, width*3/4, height/4, 400)
                    except:
                        #driver.swipe(height/2, width/2, height*3/4, width/4, 400)
                        pass
                                
            # 5% monkey
            elif (random_action >= 96): 
                temp = random.randrange(2)
                if temp == 0:
                    temp_x = random.randrange(100)
                    temp_y = random.randrange(100)
                    coor_x = window_size["width"] * temp_x /100
                    coor_y = window_size["height"] * temp_y/100
                    TouchAction(driver).press(x=coor_x, y=coor_y).perform()
                elif temp == 1:
                    driver.press_keycode(4)

            print (driver.current_activity)
            if (driver.current_package != appPackage): 
                driver.reset()
                time.sleep(3)
            time.sleep(0.5)

            print ("currentActivity =  " +str(currentAct))
            print ("No. of Clickable elements =  " + str(len(Clickable_Elements)))
            print ("No. of Textinput elements =  " + str(len(Textinput_Elements)))

            result[key] = (currentAct, len(Clickable_Elements), len(Textinput_Elements))
            if currentAct == driver.current_activity :
                count += 1

            if count > 15 : 
                #driver.reset()
                driver.close_app()
                driver.launch_app()
                count = 0
            key += 1
            timeStep = time.time()
            print ('time = ' + str(timeStep - start_time))
        except: 
            print('clashed')
            driver.reset()
    printResult()

def printResult():
    st = pd.DataFrame.from_dict(result, orient = "index")
    if not os.path.exists('monkeyresult.csv'):
        st.to_csv("monkeyresult.csv")
    else: # else it exists so append without writing the header
        y = 1
        yy = "("+ str(y) +")monkeyresult.csv"
        while os.path.exists(yy):
            y += 1
            yy = "("+ str(y) +")monkeyresult.csv"
            st.to_csv(yy)
     

appium(4723,desired_caps)