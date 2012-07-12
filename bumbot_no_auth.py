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

banlistDir = 'hidden'
bl = open(banlistDir,'r')
banlist = pickle.load(bl)
bl.close()

welcList = [] # Welcome list
userList = []
snags = 0
songData = {}
closedMsg = 'Sorry, the speakeasy isn\'t open right now (it opens on Wednesdays) and this is where I sleep.'


avatars = [{'id':1,'desc':'Brunette girl'},{'id':2,'desc':'Green-haired girl'},{'id':3,'desc':'Red hair pigtails'},{'id':4,'desc':'Blonde chick'},{'id':5,'desc':'Brown mohawk guy'},{'id':6,'desc':'Light brown pigtails'},{'id':7,'desc':'Light brown haired guy'},{'id':8,'desc':'Ginger'},{'id':34,'desc':'African-American kid'},{'id':9,'desc':'Brown bear'},{'id':10,'desc':'Voodoo/Acupuncture bear'},{'id':12,'desc':'Alien bear'},{'id':13,'desc':'Aquamarine bear'},{'id':14,'desc':'Purple bear'},{'id':15,'desc':'Orange bear'},{'id':16,'desc':'Goth bear'},{'id':17,'desc':'Blue bear'},{'id':18,'desc':'Gray mouse/cat'},{'id':19,'desc':'Green mouse/cat'},{'id':121,'desc':'Pink mouse/cat'},{'id':20,'desc':'Blonde superhero'},{'id':21,'desc':'Pink haired superhero'},{'id':22,'desc':'Viking/Devil'},{'id':23,'desc':'Gorilla'},{'id':36,'desc':'Butler monkey'},{'id':37,'desc':'Pink monkey'},{'id':27,'desc':'Ginger space man'},{'id':28,'desc':'Blue-eyed space man'},{'id':29,'desc':'Green glasses space man'},{'id':30,'desc':'Brown haired space kid'},{'id':31,'desc':'African-American space man'},{'id':32,'desc':'Black haired space kid'},{'id':33,'desc':'Blonde space kid'},{'id':218,'desc':'Pink space monkey'},{'id':219,'desc':'Purple space monkey'},{'id':220,'desc':'Red space monkey'},{'id':221,'desc':'Yellow space monkey'},{'id':222,'desc':'Blue alien'},{'id':223,'desc':'Pink alien chick'},{'id':224,'desc':'Green bearded alien'},{'id':225,'desc':'Green monocle alien'},{'id':226,'desc':'Green alien pink hair chick'},{'id':227,'desc':'Ginger alien chick'},{'id':228,'desc':'Purple monocle alien'},{'id':229,'desc':'Purple bearded alien'},{'id':230,'desc':'Redhead chick alien with hat'},{'id':26,'desc':'Superuser robo helmet'},{'id':35,'desc':'Superuser rainbow helmet'},{'id':58,'desc':'Wooooo'}]

beerme = ['Ok /name, I\'ll add it to your tab.','Of course!','Coming right up! Here you go!','Whoah there /name, slow down with the drinks there! I\'ll give you one for now though.','Sure, but when are you going to hand over the dough, /name?','Ok, just don\'t make eyes to the bull!','Trying to get an edge are ya?','Gettin a bit spifflicated are ya?','Ok, /name, just warning you, you have to clean the upchuck!']

def speak(data):
   global userList,beerme,songData,banlistDir,banlist
   name = data['name']
   userid = data['userid']
   text = data['text']
   userid = data['userid']

   if re.match('/((h(ello|i|ey))|(sup))', strpAcc(text)):
      bbot.speak('Hey! How are you %s?' % atName(name))
   if re.match('(.+)?( have )?(.)?/round( )?of( )?beer(s)?',text.lower()):
      bbot.speak('Round of %d beers coming right up! Hold on just a minute!' % (len(userList)-1))
      beerTmr = threading.Timer(random.randint(7,20),serveBeers)
      beerTmr.start()
   if re.match('/beer(( )?me)?',text.lower()):
      bbot.speak('%s *gives a :beer: to %s*' % (beerme[random.randint(0,len(beerme)-1)].replace('/name',atName(name)),atName(name)))
   if re.match('/menu(.+)?',text.lower()):
      bbot.speak('Here\'s our menu: :beer::cocktail::sake::coffee::hamburger::spaghetti::ramen::cake::icecream::apple::watermelon::eggplant:')

   if re.match('/ban( )?list',text.lower()):
      nameBans = []
      for i in range(len(banlist)):
         nameBans.append(banlist[i]['name'])
      bbot.speak('Ban list: %s' % ', '.join(nameBans))

   if re.match('/cover( )?art',text.lower()):
      bbot.speak(songData['metadata']['coverart'])

   if re.match('/album',text.lower()):
      if songData['metadata']['album'] != '':
         bbot.speak('This song appears to be from the album "%s".' % songData['metadata']['album'])
      else:
         bbot.speak("The album name couldn't be identified.")
         
   if re.match('/genre',text.lower()):
      if songData['metadata']['genre'] != '':
         bbot.speak('This song is classified as %s.' % songData['metadata']['genre'])
      else:
         bbot.speak("The genre couldn't be identified.")
         
   if re.match('bumbot ban (.+)',text.lower()):
      def checkMod(data):
         if userid in data['room']['metadata']['moderator_id']:
            def getId(userdata):
                     if userdata['success']:
                        if userdata['userid'] in data['room']['metadata']['moderator_id']:
                              bbot.speak("I can't ban mods!")
                        else:
                              bbot.bootUser(userdata['userid'],'You have been banned by %s!' % name)
                              def getName(namedata):
                                 global banlistDir
                                 banlist.append({'userid':userdata['userid'],'name':namedata['name']})
                                 bl = open(banlistDir,'w')
                                 pickle.dump(banlist,bl)
                                 bl.close()
                                 print 'Wrote new banlist: %s' % str(banlist)
                                 bbot.speak('Banned %s!' % namedata['name'])
                              bbot.getProfile(userdata['userid'],getName)
                     else:
                        bbot.speak("I couldn't find the user!")
            bbot.getUserId(text[11:],getId)
      bbot.roomInfo(False,checkMod)

   if re.match('bumbot unban (.+)',text.lower()):
      def checkMod(data):
            if userid in data['room']['metadata']['moderator_id']:
               beginLen = len(banlist)
               for i in range(len(banlist)):
                  if banlist[i]['name'].lower()==text[13:].lower():
                        bbot.speak('Unbanned %s.' % banlist[i]['name'])
                        banlist.remove(banlist[i]) #remove that current value
                        global banlistDir
                        bl = open(banlistDir,'w')
                        pickle.dump(banlist,bl)
                        bl.close()
                        print 'Wrote new banlist: %s' % str(banlist)                        
                        break
               if beginLen-1 != len(banlist):
                  bbot.speak('Couldn\'t remove the user from the ban list.')
      bbot.roomInfo(False,checkMod)
      
   print(strftime('%I:%M:%S %p',localtime())+'  '+strpAcc(name) + ':'+ ' '*(21-len(strpAcc(name)))+ strpAcc(text))
         
def newSong(data):
   global snags,songData
   snags = 0
   songData = data['room']['metadata']['current_song']

def userReg(data):
   global welcList,bbot_
   userid = data['user'][0]['userid']
   name   = data['user'][0]['name']
   print '%s  %s has entered the room. %s' % (strftime('%I:%M:%S %p',localtime()),name,userid)
   if roomOpen():
      if len(welcList)==0 and not(userid == bumbot_userid):
         wTmr = threading.Timer(5,welcomeUsers) #Welcome users
         wTmr.start()
      if not(userid == bumbot_userid):
         welcList.append(atName(name))
   else:
      def getMods(data):
         if not(userid in data['room']['metadata']['moderator_id'] or userid == lsk_userid or userid == bumbot_userid):
            bbot.speak('Booting...')
            bbot.bootUser(userid,closedMsg)
      bbot.roomInfo(getMods)
   if not(userid == bumbot_userid):
      userList.append({'name':data['user'][0]['name'],'userid':data['user'][0]['userid'],'avatarid':data['user'][0]['avatarid']})

def serveBeers():
   global userList
   bbot.speak('Here are the beers! Cheers! ' + (':beer:'*(len(userList)-1)))

def welcomeUsers():
   global welcList,userList
   bbot.speak('Hey, %s, have a cold one on the house :beer:' % ', '.join(welcList))
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
   if roomOpen():
      for i in range(len(userList)):
         if not(userList[i]['userid'] in data['room']['metadata']['moderator_id'] or userid == lsk_userid or userid == bumbot_userid):
            bbot.bootUser(userList[i]['userid'],closedMsg)
   newSong(data)

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

def numEmote(s):
   return s.replace('0',':zero:').replace('1',':one:').replace('2',':two:').replace('3',':three:').replace('4',':four:').replace('5',':five:').replace('6',':six:').replace('7',':seven:').replace('8',':eight:').replace('9',':nine:')

def roomOpen():
   return strftime('%w',localtime()) == '3' or (strftime('%w',localtime())==4 and int(strftime('%H',localtime()))<6)

bbot.on('newsong',newSong)
bbot.on('snagged',recSnag)
bbot.on('newsong',newSong)
bbot.on('endsong',songEnd)
bbot.on('deregistered',userDereg)
bbot.on('speak',speak)
bbot.on('roomChanged',roomChanged)
bbot.on('registered',userReg)
bbot.start()