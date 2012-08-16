#BumBot v3 This bot's account was taken from Backup Ref since CTS didn't want the bot.

from ttapi_with_stop import Bot
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
voteScore = 50
alreadyVoted = 0
songData = {}
djList = []
closedMsg = 'Sorry, the speakeasy isn\'t open right now (it opens on Wednesdays) and this is where I sleep.'


avatars = [{'id':1,'desc':'Brunette girl'},{'id':2,'desc':'Green-haired girl'},{'id':3,'desc':'Red hair pigtails'},{'id':4,'desc':'Blonde chick'},{'id':5,'desc':'Brown mohawk guy'},{'id':6,'desc':'Light brown pigtails'},{'id':7,'desc':'Light brown haired guy'},{'id':8,'desc':'Ginger'},{'id':34,'desc':'African-American kid'},{'id':9,'desc':'Brown bear'},{'id':10,'desc':'Voodoo/Acupuncture bear'},{'id':12,'desc':'Alien bear'},{'id':13,'desc':'Aquamarine bear'},{'id':14,'desc':'Purple bear'},{'id':15,'desc':'Orange bear'},{'id':16,'desc':'Goth bear'},{'id':17,'desc':'Blue bear'},{'id':18,'desc':'Gray mouse/cat'},{'id':19,'desc':'Green mouse/cat'},{'id':121,'desc':'Pink mouse/cat'},{'id':20,'desc':'Blonde superhero'},{'id':21,'desc':'Pink haired superhero'},{'id':22,'desc':'Viking/Devil'},{'id':23,'desc':'Gorilla'},{'id':36,'desc':'Butler monkey'},{'id':37,'desc':'Pink monkey'},{'id':27,'desc':'Ginger space man'},{'id':28,'desc':'Blue-eyed space man'},{'id':29,'desc':'Green glasses space man'},{'id':30,'desc':'Brown haired space kid'},{'id':31,'desc':'African-American space man'},{'id':32,'desc':'Black haired space kid'},{'id':33,'desc':'Blonde space kid'},{'id':218,'desc':'Pink space monkey'},{'id':219,'desc':'Purple space monkey'},{'id':220,'desc':'Red space monkey'},{'id':221,'desc':'Yellow space monkey'},{'id':222,'desc':'Blue alien'},{'id':223,'desc':'Pink alien chick'},{'id':224,'desc':'Green bearded alien'},{'id':225,'desc':'Green monocle alien'},{'id':226,'desc':'Green alien pink hair chick'},{'id':227,'desc':'Ginger alien chick'},{'id':228,'desc':'Purple monocle alien'},{'id':229,'desc':'Purple bearded alien'},{'id':230,'desc':'Redhead chick alien with hat'},{'id':26,'desc':'Superuser robo helmet'},{'id':35,'desc':'Superuser rainbow helmet'},{'id':58,'desc':'Wooooo'}]

beerme = ['Ok /name, I\'ll add it to your tab.','Of course!','Coming right up! Here you go!','Whoah there /name, slow down with the drinks there! I\'ll give you one for now though.','Sure, but when are you going to hand over the dough, /name?','Ok, just don\'t make eyes to the bull!','Trying to get an edge are ya?','Gettin a bit spifflicated are ya?','Ok, /name, just warning you, you have to clean the upchuck!','Ok, /name just be sure you don\'t handle any of them wooden nickels.']

welcomeDrinks = ['Hi /name, have a nice glass \'o gin imported from Canada :beer:','/name, welcome! Here some of our very own gin from out back! :beer:','Hey! /name, you\'re not allowed here! Beat it! Just joking. Everything is Jake. Have a nice glass of our very own giggle water. :beer:','Oh /name, the big cheese, @babyshoe, has been brewing up something special for us this week. Lemme pull out a glass of that stuff. :beer:','We got this one from straight across the Atlantic. /name, here\'s one special for you. :beer:','Hey /name, straight from out the back. Here, have one. :beer:','/name, one glass of moonshine for you! :beer:','/name, you look a bit spifflicated coming in here. Well that\'s alright. Have another. :beer:','Our finest bathtub gin on the house for this fine citizen, /name. Cheers! :beer:']

def speak(data):
   global userList,beerme,songData,banlistDir,banlist,voteScore,alreadyVoted
   name = data['name']
   userid = data['userid']
   text = data['text']
   userid = data['userid']
   if re.match('/commands',text.lower()):
      bbot.speak(u'Current commands: /hey, /roundofbeers, /beer, /menu, /banlist, /coverart, /album, /genre, /bop (score > or = 60%), /lame (score < or = 45%) Mods: BumBot ban *username*, BumBot unban *username*')
      
   if re.match('/bo(p|b)',text.lower()):
      if not(alreadyVoted == 1 or alreadyVoted == -1):
         if userid != songData['djid']:
            if voteScore >= 60.0:
               bbot.vote('up')
               alreadyVoted = 1
            else:
               bbot.speak('You\'re gonna need the audience to back you up a bit more.')
         else:
            bbot.speak('You can\'t awesome your own song!')
      else:
         if alreadyVoted == 1:
            bbot.vote('up')
         bbot.speak('I already voted!')
            
   if re.match('/lame',text.lower()):
      if not(alreadyVoted == 1 or alreadyVoted == -1):
         if voteScore <= 45.0:
            bbot.vote('down')
            alreadyVoted = -1
         else:
            bbot.speak('You\'re gonna need the audience to back you up a bit more.')
      else:
         if alreadyVoted == -1:
            bbot.vote('down')         
         bbot.speak('I already voted!')

   if re.match('/((h(ello|i|ey))|(sup))', strpAcc(text)):
      bbot.speak('Hey! How are you %s?' % atName(name))
   if re.match('/round( )?of( )?beer(s)?',text.lower()):
      bbot.speak('Round of %d beers coming right up! Hold on just a minute!' % (len(userList)-1))
      beerTmr = threading.Timer(random.randint(7,20),serveBeers)
      beerTmr.start()
   if re.match('/beer(( )?me)?',text.lower()):
      bbot.speak('%s *gives a :beer: to %s*' % (beerme[random.randint(0,len(beerme)-1)].replace('/name',atName(name)),atName(name)))
   if re.match('/menu(.+)?',text.lower()):
      bbot.speak('Here\'s our menu: :beer::cocktail::sake::coffee::hamburger::spaghetti::ramen::cake::icecream::apple::watermelon::eggplant: and we also have shirley temples for those of you non-drinkers. Lemonade is reserved for the raids.')

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
      
   print(strLT()+'  '+strpAcc(name) + ':'+ ' '*(21-len(strpAcc(name)))+ strpAcc(text))
         
def newSong(data):
   global snags,songData,voteScore,alreadyVoted
   snags = 0
   voteScore = 50
   alreadyVoted = 0
   songData = data['room']['metadata']['current_song']
   print '%s  %s started playing "%s" by %s' % (strLT(),strpAcc(songData['djname']),strpAcc(songData['metadata']['song']),strpAcc(songData['metadata']['artist']))
   songData['djid'] = data['room']['metadata']['current_dj']

def pmReply(data):
   text = data['text']
   userid = data['senderid']
   if userid == lsk_userid:
      if text.lower() == 'unicode':
         print 'Unicode speak test'
         bbot.speak(u'\u25B2 \u25BC \u2764')
      if re.match('/say (.+)',text.lower()):
         bbot.speak(text[5:])
      if text.lower()=='dj on':
         bbot.addDj()
      if text.lower()=='dj off':
         bbot.remDj()
      if re.match('dj( )?list',text.lower()):
         print djList
      if text.lower()=='stop':
         bbot.stop()
      if text.lower()=='restart':
         restartWait()
         
def userReg(data):
   global welcList
   userid = data['user'][0]['userid']
   name   = data['user'][0]['name']
   print '%s  %s has entered the room. %s' % (strLT(),name,userid)
   if roomOpen():
      if len(welcList)==0 and not(userid == bumbot_userid):
         wTmr = threading.Timer(5,welcomeUsers) #Welcome users
         wTmr.start()
      if not(userid == bumbot_userid):
         welcList.append(atName(name))
   else:
      def getMods(data):
         if not(userid in data['room']['metadata']['moderator_id'] or userid == lsk_userid or userid == bumbot_userid):
            bbot.bootUser(userid,closedMsg)
      bbot.roomInfo(getMods)
   if not(userid == bumbot_userid):
      userList.append({'name':data['user'][0]['name'],'userid':data['user'][0]['userid'],'avatarid':data['user'][0]['avatarid'],'laptop':data['user'][0]['laptop']})
      
def addedDj(data):
   global djList
   user = data['user'][0]
   djList.append({'name':user['name'],'userid':user['userid'],'avatarid':user['avatarid'],'laptop':user['laptop']})
   print '%s  %s has jumped on the DJ stand.' % (strLT(),strpAcc(user['name']))
   botIsDj = False
   for i in range(len(djList)):
      if bumbot_userid==djList[i]['userid']:
         botIsDj = True
         break
   if len(djList)==1 and not(botIsDj):
      bbot.addDj()
   if len(djList)==3 and botIsDj:
      bbot.remDj()   
   
def removedDj(data):
   global djList
   for i in range(len(djList)):
      if data['user'][0]['userid']==djList[i]['userid']:
         print '%s  %s has jumped off the DJ stand.' % (strLT(),strpAcc(data['user'][0]['name'])) 
         djList.remove(djList[i])
         break
   botIsDj = False
   for i in range(len(djList)):
      if bumbot_userid==djList[i]['userid']:
         botIsDj = True
         break
   if (len(djList)==1) and not(botIsDj):
      bbot.addDj()
   if (len(djList)==1) and botIsDj:
      bbot.remDj()


def serveBeers():
   global userList
   bbot.speak('Here are the beers! Cheers! ' + (':beer:'*(len(userList)-1)))

def welcomeUsers():
   global welcList,userList
   bbot.speak('Hey, %s, have a cold one on the house :beer:' % ', '.join(welcList))
   welcList = []
   
def roomChanged(data):
   print 'Moderators:      %s' % (', '.join(data['room']['metadata']['moderator_id']))
   global userList,djList
   for i in range(len(data['users'])):
      userList.append({'name':data['users'][i]['name'],'userid':data['users'][i]['userid'],'avatarid':data['users'][i]['avatarid'],'laptop':data['users'][i]['laptop']})
   print '\nCurrent Users:'
   for i in range(len(userList)):
      print(strpAcc(userList[i]['name'])+ ' '*(30-len(strpAcc(userList[i]['name']))) + userList[i]['userid']) #when we enter the room we print the current users in the I/O
   print '\nCurrent DJs:'
   djIds = data['room']['metadata']['djs']
   for i in range(len(djIds)):
      for k in range(len(userList)):
         if djIds[i]==userList[k]['userid']:
            djList.append(userList[k])
            print userList[k]['name']
   print '\n'
   if len(djList)==1:
      bbot.addDj()     
   if not(roomOpen()):
      for i in range(len(userList)):
         if not(userList[i]['userid'] in data['room']['metadata']['moderator_id'] or userid == lsk_userid or userid == bumbot_userid):
            bbot.bootUser(userList[i]['userid'],closedMsg)
   newSong(data)
   updateVotes(data)

def userDereg(data):
   userid = data['user'][0]['userid']
   name   = data['user'][0]['name']
   print '%s  %s has left the room. %s' % (strLT(),strpAcc(name),userid)
   for i in range(len(userList)):
      if userList[i]['userid']==userid: userList.remove(userList[i])

def updateVotes(data):
   global voteScore
   up = float(data['room']['metadata']['upvotes'])
   down = float(data['room']['metadata']['downvotes'])
   listeners = float(data['room']['metadata']['listeners'])
   voteScore = 50*(1+(up-down)/listeners)
   #print voteScore

def songEnd(data):
   global snags
   md = data['room']['metadata']
   bbot.speak(u'"%s": %s\u25B2, %s\u25BC, %s\u2764' % (md['current_song']['metadata']['song'],str(md['upvotes']),str(md['downvotes']),str(snags)))
   
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

def uniDesc(s):
   s=unicode(s)
   for i in range(len(s)):
      if ord(s[i])>=128:
         s.replace(s[i],'?')
   return s

def numEmote(s):
   return s.replace('0',':zero:').replace('1',':one:').replace('2',':two:').replace('3',':three:').replace('4',':four:').replace('5',':five:').replace('6',':six:').replace('7',':seven:').replace('8',':eight:').replace('9',':nine:')

def roomOpen():
   return strftime('%w',localtime()) == '3' or (int(strftime('%w',localtime()))==4 and int(strftime('%H',localtime()))<6)

def strLT(): #string local time
   return strftime('%I:%M:%S %p',localtime())
   
def restartWait(retryTime=60):
   threading.Timer(retryTime,restartBegin).start()
   try:
      bbot.stop()
   except AttributeError, err:
      pass # If we get an AttributeError, that just means that we weren't able to close an already closed websocket
   print '%s  BOT DISCONNECTED... BOT WILL TRY TO RECONNECT IN %s SECONDS...' % (strLT(),str(retryTime))
   
def restartBegin():
   global djList,userList
   userList = []
   djList   = []   
   print '%s  ATTEMPTING TO RECONNECT...\n' % strLT()
   try:
      bbot.connect(speakeasy_id)
      bbot.start()
      bbot.updatePresTmr()
   except (AttributeError, URLError):
      disconnect()

def disconnect(data=None):
   restartWait()

bbot.on('rem_dj',removedDj)
bbot.on('add_dj',addedDj)
bbot.on('pmmed',pmReply)
bbot.on('newsong',newSong)
bbot.on('snagged',recSnag)
bbot.on('endsong',songEnd)
bbot.on('deregistered',userDereg)
bbot.on('speak',speak)
bbot.on('roomChanged',roomChanged)
bbot.on('registered',userReg)
bbot.on('update_votes',updateVotes)
bbot.on('disconnect',disconnect)
bbot.start()