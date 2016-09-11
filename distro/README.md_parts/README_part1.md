# iBrew: Brewing on the 7th day

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface


## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, command line interface, web interface and rest api. You can also use it in your own code. iKettle 2.0 v19 and SmarterCoffee v20 tested at the moment. Please share any other discoveries you made! 

This means your machine is free! You can connect it yourself and do whatever you want with it. Like interface it with your favorite smarthome controller!

   Signed Me!

#### Brewing on the 7th day 

Since the console it nearly done, protocol almost fully mapped out. It is time to focus on the webpage... the framework is working, it auto reconnect, keeps some stats and you can even preform some actions with it.


#### Update

I decided to quit... I have no coffee machine to test it on, and I am not doing test sessions to remote coffee machines again. And I learned enough python. I think its a terrible language, I never had an app crash and not quit on me, or calling sys.exit() and it does NOTHING even in the main thread. utf-8 vs ascii.... wtf... and after the windows debacle I was really done with it. Then the webpage designs. css wtf... how dificult is it so have the correct font size with different screen sizes. Or stay on the same posision. 

It's not my cup of tea. 

So have phun! You can make the web functional yourself (almost all is there to do so and its almost functionally, you can say I quit before the finish line) or just use the command line. Check out the webserver anyway if you want protocol information, every argument and message is clickable, and shows information (well almost all, except wat was left to convert, still in iBrewHelp.py)!  

Well it have been fun. Signed 09/11/2016.


#### Contact
[Bugs or issues](https://github.com/Tristan79/iBrew/issues). Donations & other questions <tristan@monkeycat.nl>
If you have jokes on coffee, tea, hot chocolade, coffee machines or kettles, please post in the issues.

Still no coffee machine (so no web for that)! I could like to thank Ju4ia for letting me access his coffee machine remotely, and get more Smarter Coffee missing protocol bits, and... that I could test the client code. And thanks for jkellerer for supplying coffee codes!

 
#### Downloads & Setup
  * [MacOS]  (https://github.com/Tristan79/iBrew/blob/master/release/iBrew.dmg) 
  * [Windows](https://github.com/Tristan79/iBrew/blob/master/release/iBrew.zip) (unavailable use source, see note)

Other systems running python see download from source section.


### Download from source

You can run iBrew on systems that run python 2.7 

You can download and unpack the [source](https://github.com/Tristan79/iBrew/archive/master.zip) or download it from github using [Github Desktop](https://desktop.github.com) or manually:

```
git clone https://github.com/Tristan79/iBrew.git
```

Run `make` or use the requirements files.

On windows download the additional [win32 package](https://sourceforge.net/projects/pywin32/files/pywin32/).
Start iBrewUI with python to get a taskbar icon. 

I failed to create a package, I gave up after 8 hours, I just can not get it to work. And windows is fighting me
every step of the way, with its disaster of an user interface (who designs this? Even getting the theme to a bright color took 30 minutes of my time with some hack, are the persons responsible for choosing the color depressed? And then the jumping windows in the taskbar. I give it a try if I find an old windows xp iso. But not going to touch Win7/8/10/... ever again. I get annoyed when software is working against me. But it is almost never the os usually a stand alone app. But in windows 10 its windows itself fighting me on every step. wtf. It doubles the amount of time spend not coding. After 7 years without it, lets make the rest of my life.

 
#### Versions
 * PHASE 1: [BRAINSTORMING] v0.0 Bean Grinder Pack 
 * PHASE 2: [PROTOTYPE]     v0.1 White Tealeaf Edition 
 * PHASE 3: [PROTOCOL]      v0.2 Tea Noire Sweet 
 * PHASE 4: [CONSOLE]       v0.3 Kettle Rattle 
 * PHASE 5: [WEB]           v0.4 Brewing on the 7th day 
 * PHASE 6: [PRERELEASE]    v0.5 Dumb Dump Limited Collector Edition (numbered, signed by author)
 * PHASE 7: [FINALCUT]      v1.0 Out of order!
 
#### Upcoming for the last 3 versions  
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
 * watersensor to something usefull
 * Currently the default values in fast mode are not initalized use slow or give all values
 * filter out wrong responses... of know commands??? or atleast acknowledge them, (03 responses)
 * have not looked at single cup... needs a remote coffee machine session ;-)
 * strip zero from ip


## Usage

### Command Line

See the console section for the commands
 
```
