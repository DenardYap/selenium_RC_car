import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import time
import serial.tools.list_ports
import serial
ports = list(serial.tools.list_ports.comports())
port = None 
#automatically check which port are in use and connect to that COM PORT
for p in ports:
    if "Arduino" in p.description:
        
        port = p[0]
        break

#set the connection using defauly paras
ser = serial.Serial(port, 9600)
# ~ link = "https://zoom.us/wc/join/7824489172" #replace link here
link = "https://discord.com/login"
# ~ username = "chat-item__sender" #replace class name here
username = "username-1A8OIy.clickable-1bVtEA"
# ~ message = "chat-item__chat-info-msg" #replace class name here
message = "markup-2BOw-j.messageContent-2qWWxC"
    
#these are the codes specified in arduino to make the car reacts in a certain ways
forward1 = "101\n".encode()     
left1 = "102\n".encode()
back1 =  "103\n".encode()
right1 = "104\n".encode()
stop1 = "105\n".encode()    
straight1 = "106\n".encode()
forward2 = "201\n".encode()
left2 = "202\n".encode()
back2 =  "203\n".encode()
right2 = "204\n".encode()
stop2 = "205\n".encode()
straight2 = "206\n".encode()
#the delay for the motors
delay = 0.1
delayed1 = False
delayed2 = False
#using lists to simplify the code
actions = ["W", "A", "S", "D", "X"]
action_list1 = [forward1, left1, back1, right1, stop1]
action_list2 = [forward2, left2, back2, right2, stop2]
action_stop1 = [0, 0, 0, 0, 0]
action_stop2 = [0, 0, 0, 0, 0]
speed_stop = 0
player1 = None
player2 = None
standing_player1 = None
standing_player2 = None
standing_message_len = 0
speed = "100\n".encode()
host = "Makers Club - Bernard Yap"
standing_message = None
middle1_ = True
left1_ = False
right1_ = False
middle2_ = True
left2_ = False
right2_ = False
repeated = False
might_go_left = False
might_go_right = False

def ask_q():
    global player1
    global player2
    global speed
    global speed_stop
    global action_stop1
    global action_stop2
    
    while True:
        try:
            #1 to reset, 2 to set players, 3 to increase speed
            q = input("1 to reset to reset player1, 2 to reset to reset player2, 3 to set players, 4 to increase speed")
            if int(q) == 1:
                player1 = None
                ser.write(stop1)
                ser.write(straight1)
                print("Player 1 is now None")
                action_stop1 = [0, 0, 0, 0, 0]
                #stop player 1
            if int(q) == 2:
                player2 = None
                ser.write(stop2)
                ser.write(straight2)
                print("Player 2 is now None")
                action_stop2 = [0, 0, 0, 0, 0]
                #stop player 2
            if int(q) == 3:
                q_1 = input("Input player1")
                # ~ q_2 = input("Input player2")
                player1 = str(q_1)
                player2 = str(q_2)
            if int(q) == 4:
                s_ = input("Input speed")
                speed_stop = 0
                if int(s_ )<0 or int(s_) >100:
                    print("Please only input 0-100")
                else:
                    speed = str(s_) + "\n"
        except:
            pass

# ~ def delay_for_p1():
    # ~ global delay
    # ~ global delayed1
    # ~ delayed1 = True
    # ~ print("1: Delaying for " + str(delay) + " milliseconds")
    # ~ time.sleep(delay)
    # ~ delayed1 = False
    # ~ return False
    
# ~ def delay_for_p2():
    # ~ global delay
    # ~ global delayed2
    # ~ delayed2 = True
    # ~ print("2: Delaying for " + str(delay) + " milliseconds")
    # ~ time.sleep(delay)
    # ~ delayed2 = False
    # ~ return False
    
driver = webdriver.Chrome()
driver.get(link)

# ~ while True:
    # ~ a = input("this is a pause")
    # ~ user  = driver.find_elements_by_css_selector(username1) #get the last user
    # ~ msg = driver.find_element_by_class_name(message) #get the last message
    # ~ if a == "1":
        # ~ print(user[0].text)
        # ~ time.sleep(1)
    # ~ elif a == "2":
        # ~ print(msg)
        # ~ time.sleep(1)
        
question_tread = threading.Thread(target = ask_q)
question_tread.daemon = True
question_tread.start()
input("This is a pause")

a_and_d = [0, 0] # FIFO for A and D 
ed = False
standby_list = []
while True:
    try:
        user  = driver.find_elements_by_class_name(username)[-1] #get the last user
        msg = driver.find_elements_by_class_name(message)[-1] #get the last message
        msg_raw = driver.find_elements_by_class_name(message)[-2:] #get the last message
        msg_list = [messages.text for messages in msg_raw]   
        if msg_list[0][-1].upper() == msg_list[1][-1].upper():
            if msg_list[0][-1].upper() == "A" or msg_list[0][-1].upper() == "D":
                a_and_d[0] = msg_list[0][-1].upper()
                a_and_d[1] = msg_list[1][-1].upper()
            # ~ print("Repeated")
        elif msg_list[0][-1].upper() != msg_list[1][-1].upper():
            if msg_list[1][-1].upper() == "A" or msg_list[1][-1].upper() == "D":
                # x a 
                # a x 
                # ~ print("ASD")
                if standby_list != msg_list:
                    # ~ print("ZXC")
                    a_and_d.pop(0)
                    a_and_d.append(msg_list[1][-1].upper()) 
            standby_list = msg_list
            # ~ print("Not Repeated")
        if a_and_d[0] == a_and_d[1]:
            repeated = True
        else:
            repeated = False
            
        if user.text == player1:
            standing_player1 = user.text
            standing_player2 = None
            # ~ print("Standing_player1 is : " + str(standing_player1))
            
        elif user.text == player2:
            standing_player2 = user.text
            standing_player1 = None
            # ~ print("Standing_player2 is : " + str(standing_player2))
        
        elif user.text == "":
            # ~ print("List out of range
            print(1)
            pass
            
        else:
            standing_player1 = None
            standing_player2 = None
            
        if standing_player1 == player1:
            # ~ print("Player 1 is recognized")
            for i, b in enumerate(actions):  # W A S D X 
                if msg.text[-1].upper() == b: 
                    if action_stop1[i] == 0: #this is to only send data once
                        if i == 1:
                            print("1 - ed")
                            if left1_ == True:
                                # ~ print("Left1 passed")
                                pass
                                
                            elif (middle1_ == True and right1_ == False and repeated  == True) or (middle1_ == True and left1_ == False and might_go_left  == True):
                                middle1_ = False
                                left1_ = True
                                # ~ print("Left1")
                                ser.write(left1)
                                
                            elif middle1_ == False and right1_ == True:
                                # ~ print("Going straight")
                                might_go_left = False
                                might_go_right = True
                                middle1_ = True
                                right1_ = False
                                ser.write(straight1)
                            
                        elif i == 3:
                            print("3 - ed")
                            if right1_ == True:
                                # ~ print("Right1 Passed")
                                pass
                            elif (middle1_ == True and left1_ == False and repeated  == True) or (middle1_ == True and left1_ == False and might_go_right  == True):
                                # ~ print("Right 1")
                                middle1_ = False
                                right1_ = True
                                ser.write(right1)
                                
                            elif middle1_ == False and left1_ == True:
                                # ~ print("Going straight 2")
                                might_go_left = True
                                might_go_right = False
                                middle1_ = True
                                left1_ = False
                                ser.write(straight1)
                            
                        else:
                            ser.write(action_list1[i])
                            # ~ print("1: Serial written: " + str(action_list1[i]))
                            action_stop1 = [0,0,0,0,0]
                            action_stop1[i] = 1
                    
        elif standing_player2 == player2:
            # ~ print("Player 2 is recognized")
            
            for i, b in enumerate(actions):
                # ~ print("2: Message is: " +str(msg.text[-1].upper()))
                if msg.text[-1].upper() == b:
                    if action_stop2[i] == 0: #this is to only send data once
                        print("2: Action stop: " + str(action_stop2))
                        if i == 1:
                            if left2_ == True:
                                pass
                            elif middle2_ == True and right2_ == False and standing_message != msg.text:
                                middle2_ = False
                                left2_ == True 
                                ser.write(left2)
                                
                            elif middle2_ == False and right2_ == True:
                                middle2_ = True
                                right2_ = False
                                ser.write(straight2)
                            standing_message = msg.text
                        elif i == 3:
                            if right2_ == True:
                                pass
                            elif middle2_ == True and left2_ == False and standing_message != msg.text:
                                middle2_ = False
                                right2_ == True
                                ser.write(right2)
                                
                            elif middle1_ == False and left1_ == True:
                                middle1_ = True
                                left1_ = False
                                ser.write(straight2)
                            standing_message = msg.text
                        else:
                            ser.write(action_list2[i])
                            print("2: Serial written: " + str(action_list2[i]))
                            action_stop2 = [0,0,0,0,0]
                            action_stop2[i] = 1
                    #send bytes
                    
        elif user.text == host: 
            if speed_stop == 0:
                speed_stop = 1
                print("Host is recognized!")
                print("Changing speed to: " + str(speed))
                ser.write(speed.encode())
                #send speed
        
    except Exception as e:
        print("Some errors occured: " + str(e))    
