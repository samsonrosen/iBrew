# iBrew: Intermezzo!

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface


## Introduction
iBrew is an interface to the iKettle 2.0 and Smarter Coffee devices. 

_Stand alone, no internet or Smarter app needed!_

It features!

For smarthome fans! 
 * Support unlimited iKettle 2.0 or Smarter Coffee appliances! As many as you like!
 * Usage statistics!
 * No tracking!
 * Stand alone or bridge mode!
 
iBrew Interfaces & Bridges 
 * Command Line 
 * Web (almost finished, help appreciated!)
 * JSON REST 
 * [Javascript](https://github.com/Tristan79/iBrew/blob/master/resources/ibrew.js) (almost finished :-)
 * [Python] (https://github.com/Tristan79/iBrew/tree/master/smarter) 
 * Message relay (works with Smarter app!)
 
Connection Guides
 * __HomeKit__ (using HomeBridge)
 * [Domoticz](http://www.domoticz.com/) (coming soon!)
 * Please share your favorite smarthome controller setup!

_No tracking of you or your appliances usage!_
 
For the Smarthome and Domotics Interface experts!
 * Kettle and coffee machine simulation (works with Smarter app!)
 * Console for Smarter protocol debugging
 * Monitor
 * Message blocking and patching
 * Smarter protocol description (start web interface for a clickable web version :-)

Tested on iKettle 2.0 v19 and SmarterCoffee v20 & v22. 

Written enterly lying down... (sick in bed for months and months :-/) 

__Donations welcome! Tea, jokes, smarthome stuff, apple cakes, indian food, hugs... or new stuff to play with!__

<tristan@monkeycat.nl>

Please share any bugs, jokes, problems, discoveries you made! 


## Hot! News
__Please post links, information or help on interfacing with smarthome controllers software in the issues! There are too many out there for me to test and write guides for them all!__.

If you are a plugin coder or scripter and you do not have an iKettle or Smarter Coffee, __just simulate one!__

* Simulates iKettle 2.0 ```ibrew dump coffee relay out:GOD,in:32```
* Simulates Smarter Coffee machine ```ibrew dump kettle relay out:GOD,in:14 ```

        
### iBrew in the Media
[The iKettle, the Eleven-Hour Struggle to Make a Cup of Tea, and Why It Was All About Data, Analytics and Connecting Things Together](https://medium.com/mark-rittman/the-story-behind-the-ikettle-the-eleven-hour-struggle-to-make-a-cup-of-tea-and-why-it-was-all-769144d12d7#.h62foolse) 


### Old :-) News
__Still no coffee machine!__ I would like to thank Ju4ia for letting me access his coffee machine remotely, and get more Smarter Coffee missing protocol bits, and... that I could test the client code. And thanks for jkellerer for supplying coffee codes!

Since the console it nearly done, protocol almost fully mapped out. It is time to focus on the webpage... the framework is working, it auto reconnect, keeps some stats and you can even preform some actions with it.


## Contact
[Bugs or issues](https://github.com/Tristan79/iBrew/issues). 

Donations & other questions <tristan@monkeycat.nl>

If you have jokes on coffee, tea, hot chocolade, coffee machines or kettles, please post in the issues.


 
## Downloads & Setup

Other systems than MacOS running python see download from source section.
  
### MacOS
  * [MacOS]  (https://github.com/Tristan79/iBrew/blob/master/release/iBrew.dmg) (note that the web interface is NOT finished, only the rest api is, I hope :-)

Once you start the app from the MacOS package (drag it to your application folder first) it will auto link iBrew in your terminal.
Open a terminal and run ```ibrew``` and you're all set, good to go!

_it creates a soft symlink to /usr/local/bin/ibrew,... :-)_

### Raspberry Pi Jessy (light)

Tested on a clean Jessy light image (september 2016). 

#### Install 

SSH to the Pi! And use:

```
cd ~
sudo apt-get install git
sudo apt-get install python-setuptools
sudo easy_install pip
git clone https://github.com/Tristan79/iBrew.git
cd ~/iBrew
sudo make setup
sudo ln -s ~/iBrew/ibrew /usr/local/bin/ibrew
```

Now you can start ibrew from anywhere :-) Type in your terminal

```
ibrew
```

Or if you want to start the web interface type 

```
ibrew web
```

And surf to your pi on port 2080!

#### Update 

You can update to the latest version of iBrew with

```
cd ~/iBrew
git pull
```

#### Start web server on pi boot
Coming soon!

### Download from source

You can run iBrew on systems that run python 2.7 

You can download and unpack the [source](https://github.com/Tristan79/iBrew/archive/master.zip) or download it from github using [Github Desktop](https://desktop.github.com) or manually:

```
git clone https://github.com/Tristan79/iBrew.git
```

Run `sudo make setup` (or use the requirements file) to configure the python packages.

#### Update 

You can update to the latest version of iBrew with

```
cd ~/iBrew
git pull
```

### Windows and source
For the requirements either use ```pip install requirements.txt``` or install make from somewhere.
On windows download the additional [win32 package](https://sourceforge.net/projects/pywin32/files/pywin32/).
Start iBrewUI with python to get a taskbar icon. I failed to create a working package :-)

## Versions
 * PHASE 1: [BRAINSTORMING] v0.0 Bean Grinder Pack 
 * PHASE 2: [PROTOTYPE]     v0.1 White Tealeaf Edition 
 * PHASE 3: [PROTOCOL]      v0.2 Tea Noire Sweet 
 * PHASE 4: [CONSOLE]       v0.3 Kettle Rattle 
 * PHASE 5: [WEB]           v0.4 Brewing on the 7th day 
 *                          v0.4.4 Intermezzo! <-- We are here!
 * PHASE 6: [PRERELEASE]    v0.5 The conundrum struggle
 * PHASE 7: [FINALCUT]      v1.0 Out of order!

### Fixes 
 * 13-11-2016 Fixed firewall added coffee machine and kettle simulator
 * 10-11-2016 Fixed relay so you can simulate an smarter coffee or ikettle
 *  4-11-2016 Fixed status not working for homebridge :-)
 *  4-11-2016 Example Homebridge config file!
 
### Upcoming for the last 3 versions  

Protocol
 * Timers protocol
 * v0.5 Missing Coffee Smarter codes (working bit only?)
 * descaling data bit? (the smarter app has it...)
 * Time arguments (have not figured that out)
 * History message is not finished
 * Fahrenheid not finished, please to not use.
 * watersensor to something usefull (like the stupid left or right side handle, cuz the kettle weight balance is off, its inaccurate as fuck even in the smarter app :-/)
 * have not looked at single cup... needs a remote coffee machine session ;-)
 * modifiers/patches!!! 
 * script or url events
 * there is no length check on message... could crash thing :-)


Interfaces
 * RELAY: simulate brew or heating process if not connected.
 * PYTHON: Better error handling
 * PYTHON: Strip zero from ip
 * PYTHON: fix wireless with the same name
 * PYTHON: filter out wrong responses... of know commands??? or atleast acknowledge them, (03 responses)
 * CLI: Currently the default values in fast mode are not initalized use slow or give all values
 * CLI: Sometimes it does not quit :-)
 * CLI: Connecting in console mode... fails sometimes, and after reconnect is had strange data... stupid threads... missing...
 * CLI: # Bug in ./iBrew slow dump calibrate 10.0.0.3
 * WEB: it also hangs if you scan wifi too much (luckily it reconnects, can not fix this)
 * WEB: Web interface 
 * WEB: Auto relay when in web mode
 * WEB: API key, login
 * WEB: Settings iBrew (like blocking, patches, other stuff)
 * JAVASCRIPT: JSON Rest API
 * OTHER: Guides to Smarthome controllers
 * ME: hugs!


## Usage

### Command Line

See the console section for the commands.
 
```
