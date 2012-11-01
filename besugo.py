#!/usr/bin/env python
# Copyright 2012 Matias Surdi
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PORT = 40016
IP="224.0.0.215"
COMM_INT="0.0.0.0"
SOMETHING_TO_SAY=(
    "football",
    "food",
    "Matias having vacations tomorrow",
    "who should win this contest",
    "your stupidity",
    "the weather",
    "money",
    "religion",
    "how I feel",
    "how many drugs toke my programmer",
    "how stupid this conversation is",
    "how beautiful I am",
    "who we should kill",
    "ley Sinde",
    )

YES_NO = (
    "yes",
    "no",
    "usually",
    "sometimes",
    "maybe",
    "I don't know",
    "for sure",
    "of course",
    "no idea dude",
    "I don't get it",
    )

import sys, time
import socket
import Queue
import aiml
import os
import logging
import random
import signal
from threading import Thread



class Sender():
    def __init__(self,name):
        logging.debug("Initializing sender")
        self.name = name
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        self.send_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(COMM_INT))
 
    def send(self,sender,message):
        logging.debug("Sending message: %s" % message)
        send_info = sender+"||"+message 
        self.send_socket.sendto(send_info, (IP, PORT))

    def close(self):
        self.send("bye")
        self.send_socket.close()
    

class Listener(Thread):
    def __init__(self):
        logging.debug("Setting up listener")
        Thread.__init__(self)
        self.must_stop = False
        # Init socket
        self.listen_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM )
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow more than 1 process to bind
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) # Allow more than 1 process to bind
        self.listen_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 1) # ttl=1 means local segment
        self.listen_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1) # Listen our own discoveries
        self.listen_socket.bind(('', PORT))
        self.listen_socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(COMM_INT)) # Send from this iface
        self.listen_socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(IP) + socket.inet_aton(COMM_INT)) # Join a group by informing the kernel of it
        #Init queue
        self.queue = Queue.Queue()

    def run(self):
        logging.debug("Starting listener...")
        while True:
            time.sleep(0.2)
            listen_info=None
            try:
                listen_info, addr = self.listen_socket.recvfrom( 1024 )#,socket.MSG_DONTWAIT) 
            except Exception,e:
                if e.errno != 35:
                    raise e
            if listen_info:
                logging.debug("Got message: %s" % listen_info)
                from_ = addr[0] + "." + str(addr[1])
                sender = ""
                if listen_info.find("||") > -1:
                    sender,listen_info = listen_info.split("||",1)
                self.queue.put({"from":from_,"text":listen_info,"sender":sender})
            if self.must_stop:
                # send unregister packet
                self.listen_socket.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(IP) + socket.inet_aton(COMM_INT))
                self.listen_socket.close()
                break

    def get_message(self):
        message = None
        try:
            message = self.queue.get(block=False,timeout=1)
        except Queue.Empty,e:
            pass
        return message

    def stop(self):
        self.must_stop = True

class Me():
    def __init__(self,name):
        self.brain = aiml.Kernel()
        self.brain.verbose(False)
        self.brain.setBotPredicate("name",name)
        self.name = name
        self.friends = set()
        self.boring_counter = 0
        self.boring_limit = random.randint(60,100)
        if os.path.exists(name+".brain"):
            logging.info("Loading my brain...")
            self.brain.bootstrap(brainFile = name+".brain")
            logging.info("Brain loaded.")
        else:
            books=os.listdir('aiml/');
            for book in books:
                logging.info("Learning from %s" % book)
                self.brain.learn("aiml/"+book)
            self.brain.saveBrain(name+".brain")

    def say_hello(self):
        hello = "Hi everybody!!!, I'm %s" % self.name
        self.type_text(hello)
        return hello

    def say_bye(self):
        bye = "Have to go. See you soon!"
        self.type_text(bye)
        return bye

    def say_something(self):
        return random.choice(SOMETHING_TO_SAY)

    def say_yesno(self):
        return random.choice(YES_NO)

    def get_name(self):
        return self.name

    def type_text(self,message):
        sys.stdout.write("me>")
        sys.stdout.flush()
        for letter in message:
            time.sleep(random.randint(10,20) / 100.0 ) 
            sys.stdout.write(letter)
            sys.stdout.flush()
        sys.stdout.write("\n")
         
    def boring(self):
        self.boring_counter += 1
    
    def reply(self,sender=None,message=None):
        reply = None
        # Send a response or say nothing
        should_i_respond = True
        if len(self.friends) > 0:
            should_i_respond =  (1 / random.randint(1,len(self.friends)) == 1)

        if sender == self.name or not should_i_respond:
            self.boring()
            reply = None
        # Decide if this is boring
        elif self.boring_counter > self.boring_limit:
            reply = "This conversation is boring, let's talk about "+ self.say_something()
            self.boring_counter = 1
        elif message:
            if sender not in self.friends:
                self.friends.add(sender)
            print "%s> %s" % (sender,message)
            logging.info(message)
            if message.find("?") > -1 :
                reply = self.say_yesno()
            else:
                reply = self.brain.respond(message,sender)
            logging.info(reply)
            logging.debug("My reply is: %s" % reply)
            logging.debug("Replying message: '%s' from '%s'" % (message,sender))
        
        if reply:
            self.type_text(reply)
        return reply


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please, provide a name for this character as the first argument"
        sys.exit(1)
    print "Starting Besugo's talk..."
  
    # Initialize logging and parameters
    logging.basicConfig(level=logging.WARNING)
    name = sys.argv[1]
    sender = Sender(name)
    listener = Listener()
    listener.start()
    me = Me(name)
    said_hello = False
    while True:
        try:
            message=""
            message = listener.get_message()
            if message:
                reply = me.reply(message["sender"],message["text"])
                if reply:
                    sender.send(me.get_name(),reply)
            else:
                time.sleep(1)
                if not said_hello:
                    sender.send(me.get_name(),me.say_hello())
                    said_hello = True
                else:
                    me.boring()
        except KeyboardInterrupt:
            logging.info("Stopping...")
            sender.send(me.get_name(),me.say_bye())
            listener.stop()
            listener.join()
            break

