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
  * [MacOS]  (https://dl.dropboxusercontent.com/u/12474226/iBrew.dmg) (note that the web interface is NOT finished, only the rest api is, I hope :-)

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

#### Troubleshooting

Please post any bug or [issues](https://github.com/Tristan79/iBrew/issues) here on github!
The error handling is still kinda broken... :-) now use dump to see more. Will revert to debug, info, logging (wip)

### Log location

 * macOS ```~/Library/Application Support/iBrew/logs```
 * unix  ```~/.iBrew/logs```
 * windows ```~%APPDATA%\iBrew\logs```

### Unable to connect to iKettle 2.0 or Smarter Coffee appliance

```
MoonTwo:iBrew Tristan$ ./ibrew list
[10.0.0.3:2016-11-13 12:38:24] Found iKettle 2.0 (iBrew certified firmware v19)
[10.0.0.98:2016-11-13 12:38:24] Found Smarter Coffee (iBrew certified firmware v20)
[10.0.0.99:2016-11-13 12:38:24] Found iKettle 2.0 (iBrew certified firmware v19)
```
Some hints
* Did you download, clone or pull iBrew from git to get the latest version with all the bug fixes?

Network trouble
 * Does the Smarter app autodetects it?
 * Is a firewall blocking port 2081 on your computer (or on your router)?
 * Does ```./ibrew list``` work?
 * Make sure that your kettle/coffee machine is on the same network and subnet as your pc and your phone.
 * It could be that your router is blocking utp broadcast messages (some do, so it never auto detects). 

Static IP address
 * Look up the IP address of the appliance in your router (dhpc server)
 * Set up a static IP address in your router (dhpc server) for your appliance

Reset wireless network
 * Reset appliance (iKettle is longer then 10 seconds button hold on base, coffee machine, eeuh I forgot which button but you can use the smarter app to reset your appliance wireless network to direct mode [FIX])
 * If the appliance is reset. Try connect with your wifi of your pc (if it has wifi) to the appliance its wireless network access point iKettle:?? or SmarterCoffee:?? try if iBrew works.
 * Reconnect to your wifi network (and if you are lucky and could connect with iBrew in direct mode, the command is ./ibrew join namewireless password) else use your phone app.



## Usage

### Command Line

See the console section for the commands.
 
```
