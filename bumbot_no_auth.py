#BumBot v1 This bot's account was taken from Backup Ref since CTS didn't want the bot.

from ttapi import Bot
from printnesteddictionary import print_dict
import re
import random
from time import localtime, strftime
import sys
import os
import unicodedata
import threading
import pickle

bumbot_auth       = 'auth+live+xxxxxxxx'
bumbot_userid     = '4fdca143aaa5cd1e79000315'

lsk_userid        = '4e7c70bc4fe7d052ef034402'
babyshoe_userid   = '4e3f5465a3f7512f10015692'

speakeasy_id      = '4e8a63d614169c39fb79b09a'

AUTH   = bumbot_auth
USERID = bumbot_userid
ROOM   = speakeasy_id

bbot = Bot(AUTH,USERID,ROOM)

welcList = [] # Welcome list
userList = []
snags = 0

beerme = ['Ok /name, I\'ll add it to your tab.','Of course!','Coming right up! Here you go!','Whoah there /name, slow down with the drinks there! I\'ll give you one for now though.','Sure, but when are you going to hand over the dough, /name?','Ok, just don\'t make eyes to the bull!','Trying to get an edge are ya?','Gettin a bit spifflicated are ya?','Ok, /name, just warning you, you have to clean the upchuck!']

def speak(data):
   global userList,beerme
   name = data['name']
   userid = data['userid']
   text = data['text']
   userid = data['userid']
   print(strftime('%I:%M:%S %p',localtime())+'  '+strpAcc(name) + ':'+ ' '*(21-len(strpAcc(name)))+ strpAcc(text))
   if re.match('/((h(ello|i|ey))|(sup))', strpAcc(text)):
      bbot.speak('Hey! How are you %s?' % atName(name))
   if re.match('(.+)?( have )?(.)?/round( )?of( )?beer(s)?',text.lower()):
      bbot.speak('Round of %d beers coming right up! Hold on just a minute!' % (len(userList)-1))
      beerTmr = threading.Timer(random.randint(7,20),serveBeers) # We wait for a random amount of 7-20 seconds to "fill" the beers
      beerTmr.start()
   if re.match('/beer(( )?me)?',text.lower()):
      bbot.speak('%s *gives a :beer: to %s*' % (beerme[random.randint(0,len(beerme)-1)].replace('/name',atName(name)),atName(name)))
   if re.match('/menu(.+)?',text.lower()):
      bbot.speak('Here\'s our menu: :beer::cocktail::sake::coffee::hamburger::spaghetti::ramen::cake::icecream::apple::watermelon::eggplant:')


def userReg(data):
   global welcList
   userid = data['user'][0]['userid']
   name   = data['user'][0]['name']
   print '%s  %s has entered the room. %s' % (strftime('%I:%M:%S %p',localtime()),name,userid)
   if strftime('%w',localtime()) == '3':
      if len(welcList)==0 and not(userid == bumbot_userid):
         wTmr = threading.Timer(5,welcomeUsers) #Welcome users wait 5 seconds to welcome
         wTmr.start()
      if not(userid == bumbot_userid):
         welcList.append(atName(name))
   if not(userid == bumbot_userid):
      userList.append({'name':data['user'][0]['name'],'userid':data['user'][0]['userid'],'avatarid':data['user'][0]['avatarid']})

def serveBeers():
   global userList
   bbot.speak('Here are the beers! Cheers! ' + (':beer:'*(len(userList)-1)))

def welcomeUsers():
   global welcList,userList
   bbot.speak('Hey, %s, have a cold one on the house :beer:' % ', '.join(welcList)) # We can welcome 2 people at once if they come within the same 5 secs
   welcList = []

def roomChanged(data):
   print 'Moderators:      %s' % (', '.join(data['room']['metadata']['moderator_id']))
   global userList
   for i in range(len(data['users'])):
      userList.append({'name':data['users'][i]['name'],'userid':data['users'][i]['userid'],'avatarid':data['users'][i]['avatarid']})
   print '\nCurrent Users:'
   for i in range(len(userList)):
      print(strpAcc(userList[i]['name'])+ ' '*(30-len(strpAcc(userList[i]['name']))) + userList[i]['userid']) #when we enter the room we print the current users in the I/O
   print '\nCurrent DJs:'
   for i in range(len(userList)):
      if userList[i]['userid'] in data['room']['metadata']['djs']:
         print strpAcc(userList[i]['name'])
   print '\n'

def newSong(data):
   global snags
   snags = 0

def userDereg(data):
   userid = data['user'][0]['userid']
   name   = data['user'][0]['name']
   print '%s  %s has left the room. %s' % (strftime('%I:%M:%S %p',localtime()),strpAcc(name),userid)
   for i in range(len(userList)):
      if userList[i]['userid']==userid: userList.remove(userList[i])
      
def songEnd(data):
   global snags
   md = data['room']['metadata']
   bbot.speak(numEmote('%d:arrow_up: %d:arrow_down: %d:heart:' % (int(md['upvotes']),int(md['downvotes']),int(snags))))
   
def atName(name):
   if name[0]=='@':
      return name
   else:
      return '@%s' % name

def recSnag(data):
   global snags
   snags += 1

def strpAcc(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def numEmote(s): # changing the numbers into emoticon numbers
   return s.replace('0',':0:').replace('1',':1:').replace('2',':2:').replace('3',':3:').replace('4',':4:').replace('5',':5:').replace('6',':6:').replace('7',':7:').replace('8',':8:').replace('9',':9:')

bbot.on('snagged',recSnag)
bbot.on('newsong',newSong)
bbot.on('endsong',songEnd)
bbot.on('deregistered',userDereg)
bbot.on('speak',speak)
bbot.on('roomChanged',roomChanged)
bbot.on('registered',userReg)
bbot.start()