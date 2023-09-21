#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
From Anki's web site:
                    
height (cozmo.util.Distance): The height of the lift above the ground. 
ratio (float): The ratio from 0.0 to 1.0 that the lift is raised from the ground. 
angle (cozmo.util.Angle): The angle of the lift arm relative to the ground.

This link might be helpful (it should still work):
https://data.bit-bots.de/cozmo_sdk_doc/cozmosdk.anki.com/docs/index.html

'''

import cozmo
import socket
import errno
from socket import error as socket_error

#need to get movement info
from cozmo.util import degrees, distance_mm, speed_mmps

def parseMessage(message):
    l = list(message.split(";"))
    newl = []
    for i in l:
            if i.isdigit() == True:
                i = int(i)
            newl.append(i)
    return newl

def turnRight(robot):
    robot.say_text("I will turn right").wait_for_completed()
    robot.turn_in_place(cozmo.util.degrees(-90)).wait_for_completed()
    return
def turnLeft(robot):
    robot.say_text("I will turn left").wait_for_completed()
    robot.turn_in_place(cozmo.util.degrees(90)).wait_for_completed()
    return

def cozmo_program(robot: cozmo.robot.Robot):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket_error as msg:
        robot.say_text("socket failed" + msg).wait_for_completed()
    ip = "10.0.1.10"
    port = 5000
    
    try:
        s.connect((ip, port))
    except socket_error as msg:
        robot.say_text("socket failed to bind").wait_for_completed()
    cont = True
    
    robot.say_text("ready").wait_for_completed()    
    
    #SET COZMO's NAME
    myName = 'Zeek'
    
    while cont:
        bytedata = s.recv(4048)
        #need to decode the bytedata: 
        data = bytedata.decode('utf-8')
        #do we need access to data as a string?  Is this necessary?
        #theData = str(data)
        if not data:
            cont = False
            s.close()
            quit()
        else:
            msg = parseMessage(data)
            #print(msg[3])
            #print(msg[4])

            #only want my name for both msgs
            if msg[0] == myName:
                #first message 
                if len(msg) == 5:
                    #want to go forward and backwards. if F just go forward 
                    #but if B turn 180 degrees
                    #turn will only take place if distX is not 0
                    if msg[3] > 0 and msg[1] == 'B':
                        robot.turn_in_place(cozmo.util.degrees(180)).wait_for_completed()
                        robot.drive_straight(cozmo.util.distance_mm(msg[3]),cozmo.util.speed_mmps(90)).wait_for_completed()
                    elif msg[3] > 0 and msg[1] == 'F':
                        robot.drive_straight(cozmo.util.distance_mm(msg[3]),cozmo.util.speed_mmps(100)).wait_for_completed()

                    #want to turn left or right. Right if R and left if L
                    #but turn will only happen if distY is not 0
                    if msg[4] > 0 and msg[2] == 'R':
                        turnRight(robot)
                        robot.drive_straight(cozmo.util.distance_mm(msg[4]),cozmo.util.speed_mmps(100)).wait_for_completed()

                    if msg[4] > 0 and msg[2] == 'L':
                        turnLeft(robot)
                        robot.drive_straight(cozmo.util.distance_mm(msg[4]),cozmo.util.speed_mmps(100)).wait_for_completed()

                #second msg
                elif len(msg) == 3:
                    robot.set_head_angle(msg[1])
                    robot.set_lift_height(msg[2])


           

                    

                    

cozmo.run_program(cozmo_program)
