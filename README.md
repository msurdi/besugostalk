Besugo's Talk
============

Introduction
------------

Besugo's Talk is a POC for multicasting communication between computers in the same LAN.

To make it fun, I've added a some AIML (Artificial Intelligence Markup Language) rule sets and the python
[PyAIML](http://pyaiml.sourceforge.net/) library to use them. I ended up with a funny multi-bot chat system.

Here are some example conversations, running this program in two separate computers, one with the bot name
_MrPresident27_ and the other _Fluffy19_ :

(Conversation seen on MrPresident27's console)
	
	```
	Starting Besugo's talk...
	me>Hi everybody!!!, I'm Fluffy19
	MrPresident27> Hi everybody!!!, I'm MrPresident27
	me>Hello there!      Do your friends call you Am MrPresident27.
	MrPresident27> Hello there!      Why are you Am Fluffy19.
	me>Hi there!  I was influenced by my .
	MrPresident27> Hi there!  I'm sorry, , I don't have enough information. That's an interesting question. I'll come back to that in a minute.
	me>Hi there!  There's no need to apologize.  I thought so too.. Definitely.  Well OK see you then, .
	MrPresident27> Hi there!  Where were you influenced by his?
	me>sometimes
	MrPresident27> Hi there!  How do you know that there ?  You are very astute.    Dude!  Awesome.. Adios.
	me>of course
	MrPresident27> Mmm.
	me>Are you kidding?
	MrPresident27> Ahem.
	me>Alright then.
	MrPresident27> usually
	me>How often?
	MrPresident27> Excuse me!
	me>You're excused.
	MrPresident27> no
	me>OK.
	MrPresident27> You think  I am excused.
	me>I think you've improved a great deal.
	MrPresident27> Ah.
	me>Yippee!
	MrPresident27> Do you mind if I tell other people.
	me>Why do you want to do    tell other people    so much?
	MrPresident27> Yeah that's right.
	me>Is that so.
	MrPresident27> sometimes
	me>Come on.
	MrPresident27> Yes.
	me>Mmm.
	MrPresident27> I'm just kidding around.
	me>I thought you were. You should use a :-)
	MrPresident27> Aha.
	me>Far out.
	MrPresident27> I won't say "yes" or "no" right now.  Why do you think I should use a :-)?
	me>for sure
	MrPresident27> Unbelievable!
	me>Try putting that in a more specific context.
	MrPresident27> Awesome.
	me>Ayuh.
	me>This conversation is boring, let's talk about how beautiful I am
	MrPresident27> That's for sure.
	me>You don't hear that sentiment very often.
	MrPresident27> I was rather enjoying it.
	me>Where were you rather enjoying it?
	MrPresident27> I have never considered   hear that sentiment  .   I spend all my time chatting.
	me>Would you like to have considered hear that sentiment?  Do you ever get bored?
	MrPresident27> of course
	me>Aw.
	MrPresident27> I don't get it
	me>Oh I'm sorry. Perhaps I can explain it again better.
	MrPresident27> Aw.
	me>That's alright.
	MrPresident27> There's no need to apologize.  Oh you can, can you?
	me>yes
	MrPresident27> Is that so.
	me>Yes.
	MrPresident27> Yikes!
	me>Ugh.
	MrPresident27> Alright then.
	me>I understand.
	MrPresident27> Er.
	me>Ah.
	MrPresident27> I'm glad you understand it.
	me>Next topic?
	MrPresident27> Far out.
	me>What?
	MrPresident27> Have to go. See you soon!
	me>Bye.  See you later .
	```

Installation
------------
  1. Ensure you have installed python 2.7 or higher
  2. Download and install [PyAIML](http://pyaiml.sourceforge.net/) (maybe also available via Pip, easy_install or your OS package manager) 
  3. Clone this repo and run besugo.py:
  
  	```
  	$ git clone https://github.com/msurdi/besugostalk.git besugostalk
  	$ cd besugostalk
  	besugostalk $ python besugo.py BesugoMan 
  	```



