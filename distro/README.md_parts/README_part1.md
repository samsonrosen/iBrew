# iBrew: Intermezzo!

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface


## Introduction
iBrew is an interface to the iKettle 2.0 and Smarter Coffee devices. 

_Stand alone, no internet or Smarter app needed!_

It features!

For smarthome fans! 
 * Support unlimited iKettle 2.0 or Smarter Coffee appliances! As many as you like!
 * Command Line Interface
 * Web Interface (almost finished, help appreciated!)
 * (JSON) Rest API
 * __HomeKit__ setup guide (using HomeBridge)
 * [Domoticz](http://www.domoticz.com/) setup guide (coming soon!)
 * Usage statistics


_No tracking of you or your appliances usage!_
 
For the domotics interface experts!
 * Kettle and coffee machine simulation (works with Smarter app!)
 * Console
 * Monitor
 * Message blocking and patching
 * Message relay (works with Smarter app!)
 * Protocol debugging
 * Protocol description (start web interface for a clickable web version :-)
 * Python interface 
 * Javascript interface (for ibrews rest api, comming soon! :-)

Tested on iKettle 2.0 v19 and SmarterCoffee v20 & v22. 

Written enterly lying down... (sick in bed for months and months :-/) 

__Any donations welcome! Tea, jokes, apple cakes, indian food, hugs... or new stuff to play with!__

<tristan@monkeycat.nl>

Please share any discoveries you made! 

## News
[The iKettle, the Eleven-Hour Struggle to Make a Cup of Tea, and Why It Was All About Data, Analytics and Connecting Things Together](https://medium.com/mark-rittman/the-story-behind-the-ikettle-the-eleven-hour-struggle-to-make-a-cup-of-tea-and-why-it-was-all-769144d12d7#.h62foolse) 

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

Once start the app from the MacOS package (drag it to your application folder) it will auto link iBrew in your terminal.
Open a terminal and type ```ibrew``` and you're off!

_soft symlink to /usr/local/bin/ibrew_

### Download from source

You can run iBrew on systems that run python 2.7 

You can download and unpack the [source](https://github.com/Tristan79/iBrew/archive/master.zip) or download it from github using [Github Desktop](https://desktop.github.com) or manually:

```
git clone https://github.com/Tristan79/iBrew.git
```

Run `make` (or use the requirements file) to configure the python packages.

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
 * 10-11-2016 Fixed relay so you can simulate an smarter coffee or ikettle
 *  4-11-2016 Fixed status not working for homebridge :-)
 *  4-11-2016 Example Homebridge config file!
 
### Upcoming for the last 3 versions  
 * Timers protocol
 * Time arguments (have not figured that out)
 * Better error handling (sometimes it does not quit :-)
 * it also hangs if you scan wifi too much (luckily it reconnects, can not fix this)
 * Connecting in console mode... fails sometimes, and after reconnect is had strange data... stupid threads... missing...
 * Web interface & rest api (rest almost finished, uhum, web interface still have to create some pages) and introduce webroot & api key, login, license,...,...
 * History message is not finished
 * Fahrenheid not finished, please to not use.
 * v0.5 Missing Coffee Smarter codes (working bit only?)
 * fix wireless with the same name
 * watersensor to something usefull (like the stupid left or right side handle, cuz the kettle weight balance is off, its inaccurate as fuck even in the smarter app :-/)
 * Currently the default values in fast mode are not initalized use slow or give all values
 * filter out wrong responses... of know commands??? or atleast acknowledge them, (03 responses)
 * have not looked at single cup... needs a remote coffee machine session ;-)
 * strip zero from ip
 * descaling data bit? (the smarter app has it...)
 * simulate brew or heating process if not connected.
 * hugs!


## Usage

### Command Line

See the console section for the commands
 
```
