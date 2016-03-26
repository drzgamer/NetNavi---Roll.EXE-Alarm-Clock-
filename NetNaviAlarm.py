import os
import time
import dateutil.parser
from alarms import alarms
from GetAlarm import GetAlarm
from button import button

import sys, pygame
from pygame.locals import *
import pygame.gfxdraw

import datetime

alarmInit = None
alarmList = None
mainAlarm = None

def main():
    #Global variables
    global alarmInit
    global alarmList
    global mainAlarm


    #Init alarm and place into list and create main alarm
    alarmInit = GetAlarm()
    alarmList = alarmInit.getAlarm()
    mainAlarm = alarms(alarmList[0].summary, alarmList[0].time)

    #Print to see output
    for obj in alarmList :
        date_object = str(obj.time)
        print (obj.summary + " " + date_object)

def mainPage():

    #Raw alarm 
    currentAlarmRaw = datetime.datetime.strptime(str(mainAlarm.time), '%Y-%m-%d %H:%M:%S')
    
    #Weekday conversion
    week   = ['Mon', 
              'Tues', 
              'Wed', 
              'Thur',  
              'Fri', 
              'Sat',
              'Sun']
    currentAlarmDow = week[currentAlarmRaw.weekday()]


    
    #Seperate each value from time
    currentAlarmMonth = currentAlarmRaw.strftime("%m")
    currentAlarmDay = currentAlarmRaw.strftime("%d")
    currentAlarmHour = int(currentAlarmRaw.strftime("%I"))
    currentAlarmMinute = currentAlarmRaw.strftime("%M")
   

    #Figure out current time
    currentTime = datetime.datetime.now().strftime("%I:%M")
    #Current hour for background image if satement
    currentHourRaw = int(datetime.datetime.now().strftime("%H"))

    #Split for time display
    currentHour = int(datetime.datetime.now().strftime("%H"))
    currentMinute = datetime.datetime.now().strftime("%M")

    #Convert 24hour to 12hour
    if currentHour > 12:
        currentHour = currentHour - 12
    elif currentHour == 0:
        currentHour = currentHour + 12

    #Combine to display time
    currentTime = str(currentHour) +":"+ currentMinute
    currentAlarm = currentAlarmDow + " " + str(currentAlarmHour) + ":" + currentAlarmMinute + currentAlarmRaw.strftime("%p")
    

    #If statement to change background and font color depending on time of day
    if currentHourRaw >= 6 and currentHourRaw <= 10:
        DISPLAYSURF.blit(dawnImg, (0, 0))
        displayTime = clockFont.render(currentTime , True, (0,0,0))
        displayAlarm = alarmFont.render(currentAlarm , True, (0,0,0))
    elif currentHourRaw >= 11 and currentHourRaw <= 16:
        DISPLAYSURF.blit(dayImg, (0, 0))
        displayTime = clockFont.render(currentTime , True, (0,0,0))
        displayAlarm = alarmFont.render(currentAlarm , True, (0,0,0))
    elif currentHourRaw >= 17 and currentHourRaw <= 21:
        DISPLAYSURF.blit(eveImg, (0, 0))
        displayTime = clockFont.render(currentTime , True, (0,0,0))
        displayAlarm = alarmFont.render(currentAlarm , True, (0,0,0))
    elif currentHourRaw >= 22 or currentHourRaw <= 5:
        DISPLAYSURF.blit(nightImg, (0, 0))
        displayTime = clockFont.render(currentTime , True, (255,255,255))
        displayAlarm = alarmFont.render(currentAlarm , True, (255,255,255))

    #Center time and print on screen
    displayTimeX = displayTime.get_rect().width
    displayTimeX = (displayWidth - displayTimeX)/2    
    DISPLAYSURF.blit(displayTime, (displayTimeX, 50))

    #Place alarm to also be a certain length away from right side
    displayAlarmX = displayAlarm.get_rect().width
    displayAlarmX = (displayWidth - displayAlarmX)-10
    DISPLAYSURF.blit(displayAlarm, (displayAlarmX, 0))



    #Navigation
    pygame.gfxdraw.box(DISPLAYSURF, pygame.Rect(0,displayHeight-80,800,80), (0,0,0,175))

def soundAlarm():
    #Figure out current time
    currentTime = datetime.datetime.now().strftime("%I:%M")

    #Split for time display
    currentHour = int(datetime.datetime.now().strftime("%H"))
    currentMinute = datetime.datetime.now().strftime("%M")

    #Convert 24hour to 12hour
    if currentHour > 12:
        currentHour = currentHour - 12
    elif currentHour == 0:
        currentHour = currentHour + 12

    #Combine to display time
    currentTime = str(currentHour) +":"+ currentMinute

    displayTime = clockFont.render(currentTime , True, (0,0,0))
    displayTimeX = displayTime.get_rect().width
    displayTimeX = ((alarmWidth - displayTimeX)/2) + alarmLeft   

    

    pygame.gfxdraw.box(DISPLAYSURF, pygame.Rect(0,0,800,400), (0,0,0,175))
    pygame.gfxdraw.box(DISPLAYSURF, pygame.Rect(alarmLeft,alarmTop,alarmWidth,alarmHeight), (255,255,255))
    DISPLAYSURF.blit(displayTime, (displayTimeX, 100))
    disarmAlarm.draw()
    snoozeAlarm.draw()





#Run time

if __name__ == '__main__':
    main()

#Init pygame and window
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.music.load('Early_Morning_May ringtone.mp3')
displayWidth = 800
displayHeight = 480
# ,pygame.FULLSCREEN
# You need to fix the background images.
DISPLAYSURF = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('NetNave Alarm Clock')


#Set Frames per second
FPS = 30 
fpsClock = pygame.time.Clock()

#AlarmSet
alarmWidth = 400
alarmHeight = 300
alarmTop = 50
alarmLeft = 200


snoozeAlarm = button(370,35,(alarmLeft + 15), (alarmTop + 5) ,pygame.image.load('snoozeImg.png'),DISPLAYSURF)
disarmAlarm = button(370,35, (alarmLeft + 15), (alarmTop + alarmHeight) - 35 ,pygame.image.load('disarmImg.png'),DISPLAYSURF)

#Load images
dawnImg = pygame.image.load('NYCDawn.png')
dayImg = pygame.image.load('NYCDay.png')
eveImg = pygame.image.load('NYCEve.png')
nightImg = pygame.image.load('NYCNight.png')
#Load fonts
clockFont = pygame.font.Font("Roboto-Black.ttf", 80)
alarmFont = pygame.font.Font("Roboto-Black.ttf", 40)

#Create test alarm(always current time plus 1 minute)
testAlarm = datetime.datetime.now()
testAlarm = testAlarm + datetime.timedelta(minutes = 1)

#Current page state
page = "Home"
alarm = "Deactive"
playAlarm = True

#timer for auto snooze
autoSnooze = 420 * FPS #time in seconds


# the main game loop
while True: 

    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()

    if page == "Home":
        mainPage()
    if alarm == "Active":
        soundAlarm()
        if (playAlarm):
            pygame.mixer.music.play(-1)
            playAlarm = False

    if datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") == datetime.datetime.strptime(str(mainAlarm.time), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S"):
        alarm = "Active"
    
    
    if(disarmAlarm.buttonListener(click, mouse) and alarm == "Active"):
        alarm= "Deactive"
        alarmList = alarmInit.getAlarm()
        mainAlarm = alarms(alarmList[0].summary, alarmList[0].time)
        testAlarm = datetime.datetime.now() + datetime.timedelta(minutes = 1)
        autoSnooze = 420 * FPS
        pygame.mixer.music.stop()
        playAlarm = True

    if(snoozeAlarm.buttonListener(click,mouse) and alarm == "Active"):
        alarm = "Deactive"
        mainAlarm.time = datetime.datetime.strptime(str(mainAlarm.time), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes = 7)
        autoSnooze = 420 * FPS
        pygame.mixer.music.stop()
        playAlarm = True

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    
    
    #Auto Snooze     
    if autoSnooze == 0:
        alarm = "Deactive"
        mainAlarm.time = datetime.datetime.strptime(str(mainAlarm.time), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes = 7)
        autoSnooze = 420 * FPS #420 is 7 minutes in seconds
    if autoSnooze > 0 and alarm == "Active":
        autoSnooze -= 1



    pygame.display.update()
    fpsClock.tick(FPS)