#!/usr/bin/env python2
# -*-coding:UTF-8 -*
"""
    Game module 
"""

import time
import re
from pubsublogger import publisher
from packages import Paste
from Helper import Process
from pubsublogger import publisher


def search_game(message):
	#We recover the paste
	paste= Paste.Paste(message)
	content=paste.get_p_content()
	#We open the file with all game word and the stock for all paste found
	filetoopen=open("corpus.txt","r")
	filetowrite=open("stock.txt","a")
	count=0 #Number of game word found in 1 file
    	for line in filetoopen:
		linestrip=line.strip() #Must do because it takes all the line and not just the word
		reg=re.compile(r'{}'.format(linestrip))#we create the regex
		results=re.findall(reg,content)#we find the occurences
		if(len(results)>0):
			count=count+1
		re.purge()
	if count>5:
		print results
		publisher.warning('{} contains Game related conversations+{} occurences of a game related word '.format(paste.p_name,count))#warning for the logs
		filetowrite.write('{} contains Game related conversations+{} occurences of a game related word \n'.format(paste.p_name,count))#For stock.txt
		to_print = 'GameConv;{};{};{};{} Terms related;{}'.format(paste.p_source, paste.p_date, paste.p_name, count, paste.p_path)#To see on the webinterface
		publisher.warning(to_print)
		filetoopen.close()
		filetowrite.close()	

if __name__ == '__main__':
    # If you wish to use an other port of channel, do not forget to run a subscriber accordingly (see launch_logs.sh)
    # Port of the redis instance used by pubsublogger
    publisher.port = 6380
    # Script is the default channel used for the modules.
    publisher.channel = 'Script'

    # Section name in bin/packages/modules.cfg
    config_section = 'Game'

    # Setup the I/O queues
    p = Process(config_section)

    # Sent to the logging a description of the module
    publisher.info("Run detection of Game based conversation")
    
    
    
    # Endless loop getting messages from the input queue
    while True:
        # Get one message from the input queue
        message = p.get_from_set()
        if message is None:
            publisher.debug("{} queue is empty, waiting".format(config_section))
            time.sleep(1)
            continue

        search_game(message)
 	

