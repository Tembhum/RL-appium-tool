#appium script.py
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

# print(sys.argv)

#add unlocking devices here also !!!!!!!!!!!!!!!!!!!1


start_time = time.time()

def download_from_gcloud(url,data):
	apk_folder = data[4]
	# print(apk_folder)
	temp_download_cmd = gsutil+" cp " + url + " " + apk_folder
	# print(temp_download_cmd)
	p_xx =  os.system(temp_download_cmd)


def appium(appium_port,desired_caps,log,adb_path,device_name,apk_path,appium_actions):


	
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

	# 3 attemp to run the application
	try:
		driver = webdriver.Remote("http://0.0.0.0:"+str(appium_port)+"/wd/hub", desired_caps)
	except:
		#print("################ cannot testing the app retry : 1 ###################")
		try:
			Error_handle(adb_path,device_name)
			driver = webdriver.Remote("http://0.0.0.0:"+str(appium_port)+"/wd/hub", desired_caps)
		except:
			try:
				reboot(adb_path,device_name,proxy_host,mitmPort)
				time.sleep(2)

				Error_handle(adb_path,device_name)
				driver = webdriver.Remote("http://0.0.0.0:"+str(appium_port)+"/wd/hub", desired_caps)
				# driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)
			except:
				return True
	window_size = ""
	temp_count = 0

	#loading appliaction 
	time.sleep(10)

	#Checking screen is available and get screen size()
	try:
		window_size = driver.get_window_size()
	except:
		time.sleep(2)
		try:
			# driver.quit()
			window_size = driver.get_window_size()
		except:
			time.sleep(2)
			try:
				driver.quit()
				Error_handle(adb_path,device_name)
				driver = webdriver.Remote("http://0.0.0.0:"+str(appium_port)+"/wd/hub", desired_caps)
				window_size = driver.get_window_size()
			except:
				return True

		
	activity_count = 0
	package_count = 0 
	for count in range(appium_actions):		
		p_XX = os.system("echo '########### "+str(count)+" ###########' >> "+log + package_name+".log ")
		package = driver.current_package

		if(package != package_name and package_count >=  10 ):
			activity_count = 0
			try:
				driver.launch_app()
			except:
				# print("################ cannot testing the app retry : 3 ###################")
				driver.quit()
				Error_handle(adb_path,device_name)
				driver = webdriver.Remote("http://0.0.0.0:"+str(appium_port)+"/wd/hub", desired_caps)
				# driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)
			
		else:
			#allow pop-up, browser and default application for 10 actions
			if(package != package_name):
				package_count += 1

			if (activity_count >= 50):
				activity_count = 0
				try:
					driver.launch_app()
				except:
					driver.quit()
					Error_handle(adb_path,device_name)
					driver = webdriver.Remote("http://0.0.0.0:"+str(appium_port)+"/wd/hub", desired_caps)
					# driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)
			else:
				try:
					prev_activity = driver.current_activity
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
								driver.swipe(height/2, width/2, height/2, width/4, 400)
						if temp == 1:
							try:
								driver.swipe(width/2, height/2, width/2, height*3/4, 400)
							except:
								driver.swipe(height/2, width/2, height/2, width*3/4, 400)
								
						if temp == 2:
							try:
								driver.swipe(width/2, height/2, width/4, height/4, 400)
							except:
								driver.swipe(height/2, width/2, height/4, width/4, 400)

						if temp == 3:
							try:
								driver.swipe(width/2, height/2, width*3/4, height/4, 400)
							except:
								driver.swipe(height/2, width/2, height*3/4, width/4, 400)
					
					# 5% monkey
					elif (random_action >= 96): 
						temp = random.randrange(2)
						if temp == 0:
							temp_x = random.randrange(100)
							temp_y = random.randrange(100)
							coor_x = window_size["width"] * temp_x /100
							coor_y = window_size["height"] * temp_y/100
							TouchAction(driver).press(x=coor_x, y=coor_y).perform()
						if temp == 1:
							driver.press_keycode(4)
				except:
					try:
						driver.launch_app()
					except:
						driver.quit()
						Error_handle(adb_path,device_name)
						driver = webdriver.Remote("http://0.0.0.0:"+str(appium_port)+"/wd/hub", desired_caps)
						# driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)		


				curr_activity = driver.current_activity

				if(curr_activity == prev_activity):
					activity_count+= 1

		if time.time() - start_time >= 1500 : 
			return False
				
	driver.quit()




def init_mitm(mitm,appium_actions,package_name,mitm_port,har_dump,result):
	mitm_cmd = mitm + " -p "+ str(mitm_port) +" -s "+har_dump+" --set hardump="+result + package_name +".har > /dev/null &"
	p_03 = os.system(mitm_cmd)
	# print(mitm_cmd)


def reboot(adb_path,device_name,proxy_host,mitm_port):
	is_device_online = False
	#check that device is connect to comp?
	while not is_device_online:

		p = Popen([adb_path,"devices"], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
		output, err = p.communicate() 
		rc = p.returncode
		output = output.decode("utf-8")
		check_device = output.strip().split("\n")
		for line in check_device:
			if device_name in line and "device" in line:
				is_device_online = True
		time.sleep(2)
	#reboot device
	reboot_device_cmd = adb_path +" -s "+ device_name + " reboot "
	p_06 =  os.system(reboot_device_cmd)

	

	is_device_online = False
	count = 0
	#wait for rebooting
	while not is_device_online:
		p = Popen([adb_path,"devices"], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
		output, err = p.communicate() 
		rc = p.returncode
		output = output.decode("utf-8")
		check_device = output.strip().split("\n")
		for line in check_device:
			if device_name in line and "device" in line:
				is_device_online = True
				# print(line)
	time.sleep(10)
	if(device_name == "0123456789ABCDEF" ):
		time.sleep(25)

	#unlock
	unlockcmd = adb_path + " -s " + device_name+" shell input keyevent KEYCODE_WAKEUP && " + adb_path +" -s " + device_name+" shell input keyevent 26 && " + adb_path +" -s " + device_name+" shell input keyevent 26"
	p8 = os.system(unlockcmd)
	time.sleep(1)

	#for now
	if device_name == "cff690c5":
		unlockcmd2 =adb_path + " -s " + device_name+ " shell input swipe 360 1600 360 1000 100 && "+adb_path+ " -s "+device_name+" shell input text 1234 && adb -s "+device_name+" shell input keyevent 66 && "+adb_path+" -s "+device_name+" shell input keyevent KEYCODE_BACK"
		p18 = os.system(unlockcmd2)

	else:
		unlockcmd2 =adb_path + " -s " + device_name+ " shell input swipe 360 700 360 200 && "+adb_path+ " -s "+device_name+" shell input text 1234 && adb -s "+device_name+" shell input keyevent 66 && "+adb_path+" -s "+device_name+" shell input keyevent KEYCODE_BACK"
		p18 = os.system(unlockcmd2)


	wificmd = adb_path+ " -s " +device_name+" shell svc wifi enable"
	p18 = os.system(wificmd)

	time.sleep(3)

	#join wifi network
	join_wifi_command = adb_path+ " -s " +device_name+ " shell am start -n com.steinwurf.adbjoinwifi/.MainActivity \
	-e ssid 'Male_Mond_2.4G' -e password_type WPA -e password 'Male2499'"


	temp_cmd = adb_path+" -s "+device_name+" shell input keyevent KEYCODE_BACK"
	p18 = os.system(temp_cmd)
	p18 = os.system(temp_cmd)




	is_device_online = False
	count = 0
	#wait for rebooting
	while not is_device_online:
		p = Popen([adb_path,"devices"], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
		output, err = p.communicate() 
		rc = p.returncode
		output = output.decode("utf-8")
		check_device = output.strip().split("\n")
		for line in check_device:
			if device_name in line and "device" in line:
				is_device_online = True
				# print(line)

	# print("reboot done for " + device_name)

	

	# appium_cmdddd = adb_path +  " -s "+device_name+ " uninstall io.appium.uiautomator2.server"
	# p_xx = os.system(appium_cmdddd)
	# appium_cmdddd = adb_path +  " -s "+device_name+ " uninstall io.appium.uiautomator2.server.test"
	# p_xx = os.system(appium_cmdddd)

# reset adb server will cause servier problems in parallel
def Error_handle(adb_path,device_name):

	is_device_online = False
	count = 0

	while not is_device_online:

		p = Popen([adb_path,"devices"], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
		output, err = p.communicate() 
		rc = p.returncode
		output = output.decode("utf-8")
		check_device = output.strip().split("\n")
		for line in check_device:
			if device_name in line and "device" in line:
				is_device_online = True
				# print(line)
	time.sleep(5)
	# appium_cmdddd = adb_path +  " -s "+device_name+ " uninstall io.appium.uiautomator2.server.test"
	# p_xx = os.system(appium_cmdddd)
	
	
	

########### var setup ############

temp = "temp/"
finished_apk = "finished_apk.txt"
error_apk = "error_apk.txt"

#error handle after
error_apk_file = open(error_apk, "r", encoding= "ISO-8859-1")

set_error_apk = set()

for line_temporal in error_apk_file:
	set_error_apk.add(line_temporal.strip())


appium_actions = 300

device_name = sys.argv[2]
line = sys.argv[3]

proxy_host = "192.168.1.50"



# print(line)

line_temp = line.strip().split(',')
apk_url = line_temp[1]
temp_str = apk_url.split('/')
apk = temp_str[-1]
package_name = apk[:-4]

gsutil = "google-cloud-sdk/bin/gsutil"

temp_design_caps = temp + device_name + "/" + device_name+".txt"
design_cap_file = open(temp_design_caps, "r" , encoding= "ISO-8859-1")
data = design_cap_file.read()
data = ast.literal_eval(data)

desired_caps = data[0]
appium_port = data[1]
mitmPort = data[2]
systemPort = data[3]
temp  = data[4]
log = data[5]
result = data[6]
apk_path = temp + apk


desired_caps['systemPort'] = data[3]
desired_caps['app'] = apk_path


adb_path = "adb"
emulator_path = "emulator"
har_dump = "mitmproxy/har_dump.py"
mitm = "mitmproxy/osx/mitmdump"




if line.strip() not in set_error_apk:

	kill_appium_cmd = "pkill -f 'appium -p " + str(appium_port)+"'"
	p_xx = os.system(kill_appium_cmd)


	kill_mitm_cmd = "pkill -f 'mitmdump -p " +str(mitmPort)+"'"
	p_xx = os.system(kill_mitm_cmd)

	# print(kill_mitm_cmd)

	init_mitm(mitm,appium_actions,package_name,mitmPort,har_dump,result)


	####################### running appium and mitmproxy ########################

	#start appium
	appium_cmd = "appium -p "+str(appium_port)+" >> " + log + package_name+".log &"
	p_xx = os.system(appium_cmd)



	#donwload apk file
	download_from_gcloud(apk_url,data)

	reboot(adb_path,device_name,proxy_host,mitmPort)

	


	#install apk
	adb_install_cmd = adb_path +" -s "+ device_name + " install -r " + apk_path
	p_04 = os.system(adb_install_cmd)



	Error = appium(appium_port,desired_caps,log,adb_path,device_name,apk_path,appium_actions)
			
	if not Error:
		temp_str =" : test time using "+str(time.time() - start_time)+" seconds -- appium_action :" + str(appium_actions) +" "+ device_name
		p_XX = os.system("echo '"+package_name  +temp_str + "' >> result.txt")
		temp_cmd = "echo '"+ line + "' >> "+finished_apk  
		p_04 = os.system(temp_cmd)
		temp_cmd = "rm " + log + package_name+".log"
		p_04 = os.system(temp_cmd)

	else:
		temp_str = " an activity does not exist"
		p_XX = os.system("echo 'Error"+ " "+package_name +" " +temp_str + " " + device_name+"' >> result.txt")
		error_temp = "echo '" + line + "' >> "+error_apk
		p_XX = os.system(error_temp)


	# kill all running process

	kill_appium_cmd = "pkill -f 'appium -p " + str(appium_port)+"'"
	p_xx = os.system(kill_appium_cmd)

	kill_mitm_cmd = "pkill -f 'mitmdump -p " +str(mitmPort)+"'"
	p_xx = os.system(kill_mitm_cmd)

	delete_cmd = "rm " + apk_path
	p_XX = os.system(delete_cmd)

	#uninstall 
	adb_uninstall_cmd = adb_path +" -s "+ device_name + " uninstall " + package_name
	p_04 = os.system(adb_uninstall_cmd)

	time.sleep(20)


	#update finished apk file






