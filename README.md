# iBrew: Intermezzo!

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface


## Introduction
iBrew is an interface to the iKettle 2.0 and Smarter Coffee devices. 

_Stand alone, no internet or Smarter app needed!_

It features!

For smarthome fans! 
 * Support unlimited iKettle 2.0 or Smarter Coffee appliances! As many as you like!
 * Usage statistics
 
iBrew Bridges 
 * Command Line 
 * Web (almost finished, help appreciated!)
 * JSON Rest 
 * [Javascript iBrew interface](https://github.com/Tristan79/iBrew/blob/master/resources/ibrew.js) (almost finished :-)
 * [Python Smarter] (https://github.com/Tristan79/iBrew/tree/master/smarter) 

Connection Guides
 * __HomeKit__ (using HomeBridge)
 * [Domoticz](http://www.domoticz.com/) (coming soon!)
 * Please share your favorite smarthome controller setup!

_No tracking of you or your appliances usage!_
 
For the domotics interface experts!
 * Kettle and coffee machine simulation (works with Smarter app!)
 * Console for Smarter protocol debugging
 * Monitor
 * Message blocking and patching
 * Message relay (works with Smarter app!)
 * Smarter protocol description (start web interface for a clickable web version :-)

Tested on iKettle 2.0 v19 and SmarterCoffee v20 & v22. 

Written enterly lying down... (sick in bed for months and months :-/) 

__Donations welcome! Tea, jokes, smarthome stuff, apple cakes, indian food, hugs... or new stuff to play with!__

<tristan@monkeycat.nl>

Please share any bugs, jokes, problems, discoveries you made! 

## News

__Please post links, information or help on interfacing with smarthome controllers software in the issues! There are too many out there for me to test and write guides for them all!__

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

Once you start the app from the MacOS package (drag it to your application folder first) it will auto link iBrew in your terminal.
Open a terminal and run ```ibrew``` and you're all set, good to go!

_it creates a soft symlink to /usr/local/bin/ibrew,... :-)_

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

Interfaces
 * RELAY: simulate brew or heating process if not connected.
 * PYTHON: Better error handling
 * PYTHON: Strip zero from ip
 * PYTHON: fix wireless with the same name
 * PYTHON: filter out wrong responses... of know commands??? or atleast acknowledge them, (03 responses)
 * CLI: Currently the default values in fast mode are not initalized use slow or give all values
 * CLI: Sometimes it does not quit :-)
 * CLI: Connecting in console mode... fails sometimes, and after reconnect is had strange data... stupid threads... missing...
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

  iBrew Web Server

  Usage: ibrew (energy) (dump) (fahrenheid) web (port) (rules) (modifiers) (host)

    energy                 energy saver (stats not possible)
    dump                   dump message enabled
    fahrenheid             use fahrenheid
    web                    start web interface & rest api
    port                   optional port number, default 2082
    rules                  blocking rules
    modifiers              patches
    host                   host address of device (format: ip4, ip6, fqdn)


  iBrew Command Line

  Usage: ibrew (energy) (dump) (shout|slow) (coffee|kettle) (fahrenheid) [command] (host)

    dump                   dump message enabled
    energy                 NOT IMPLEMENTED energy saver (stats not possible)
    shout                  sends commands and quits not waiting for a reply
    slow                   fully inits everything before action
    coffee                 assumes coffee machine
    kettle                 assumes kettle
    fahrenheid             PARTLY WORKING use fahrenheid
    command                action to take!
    host                   host address of device (format: ip4, ip6, fqdn)

  If you do not supply a host, it will try to connect to the first detected device
  Thus if you have more then one device supply a host (if its not in direct mode)


```

### Console
Start the console with the command `iBrew console`. The following commands are available within the console,
you can also use them on the command line as arguments, note that [] are manditory arguments and () are optional arguments.

```

  iKettle 2.0 & Smarter Coffee  Commands
    default                set default settings
    info                   device info
    list                   list detected devices
    reset                  reset device to default
    shortstatus            show status
    start                  start the device
    status                 show full status
    settings               show user settings
    stop                   stop the appliance

  iKettle 2.0 Commands
    base                   show watersensor base value
    base [base]            store watersensor base value
    boil                   heat till 100°C (coffee level)
    calibrate              calibrates watersensor
    celsius                use celsius °C [console only]
    fahrenheid             use fahrenheid °F [console only]
    formula (temperature (keepwarm))] heat kettle in formula mode
    heat (temperature)(keepwarm))    heat kettle
    settings [temperature] [keepwarm] [formula] [formulatemperature] store kettle user settings
    tea [white,green,black,oelong] warms water for tea

  Smarter Coffee  Commands
    beans                  use beans for coffee
    brew (cups (hotplate (grind (strength)))) brew coffee
    brew default           brew coffee with default settings
    carafe                 returns if carafe is required
    carafe [state]         set carafe is required [on or off]
    cups [number]          set number of cups [1..12]
    descaling              descale coffee machine
    filter                 use pregrind beans in filter for coffee
    hotplate off           turn hotplate off
    hotplate on (minutes)  turn hotplate on (time in minutes)
    mode                   return which mode: cup or carafe mode
    mode [mode]            set mode: [cup] or [carafe] mode
    pregrind               use pregrind beans in filter for coffee
    (strength) [strength]  set strength coffee [weak, medium or strong]
    settings [cups] [hotplate] [grind] [strength] store user settings

  Wireless Network Commands
    direct                 enable direct mode access
    join [net] [pass]      connect to wireless network
    rejoin                 rejoins current wireless network [not in direct mode]
    scan                   scan wireless networks

  Smarter Network Commands [console only]
    connect (host) (rules&modifiers) connect to device
    block [rules]          block messages with groups or ids
    disconnect             disconnect connected device
    unblock [rules]        unblock messages groups or ids
    relay (port)           start relay device
    relay stop             stop relay device
    rules (full)           show blocking rules
    stats                  show traffic statistics

  Block Rules
    Consists of rules, in: is for outgoing connection to the device, out: is for incomming connection from relay client.

    [in:|out:]rule(,[in:|out:]rule)*

    rule:
      message id
      group name

  Debug Commands
    time [time]            set the device time
    firmware               show firmware Wifi
    history                action history
    [hexdata]              send raw data to device (e.g. '64 7e')
    dump                   toggle 'dump raw messages'
    monitor                monitor incomming traffic
    modify (modifiers)     patch or unpatch messages
    sweep (id)             [developer only] try (all or start with id) unknown command codes

  NOT IMPLEMENTED Modifiers Rules
    [in:|out:]var=(value)(,[in:|out:]var=(value))*

    VAR           VALUE
    version       [00..FF]               override device firmware version
    heater        disable                coffee machine or kettle heater disabled

    base          [00..4000]             override default calibration base
    formula       [0..100]               override default formula temperature
    temperature   [0..100]               override default temperature
    keepwarm      off or [5..?]          override default keepwarm time
    formula       disable/enabled        override formula mode

    carafe        optional or required   override carafe detection
    cups          [1..12]                override default number of cups
    grind         beans or filter        override default grind
    hotplate      off or [5..?]          override default hotplate time
    mode          carafe or cup          override mode
    strength      weak, medium or strong override default strength
    water                                correct cups according to water level
    limit         [1..12]                limit the number of cups to be selected
    grinder       disable                force use of filter
    hotplate      disable                coffee machine hotplate disabled
    child         lock                   kettle can not heat above 45 degrees

    if no value it clears the patch

  NOT IMPLEMENTED Debug Coffee Timer
    timer [index] (erase|[time]) set/erase timer
    timers                 show timers

  Help Commands
    examples               show examples of commands
    groups                 show all groups
    group                  show messages in group
    messages               show all known protocol messages
    message [id]           show protocol message detail of message [id]
    notes                  show developer notes on the devices
    protocol               show all protocol information available
    structure              show protocol structure information

  iBrew Commands
    console (rules) (modifiers) start console [command line only]
    joke                   show joke
    license                show license
    license disagree       stop using license [command line only]
    quit                   quit console [console only]


```

#### Examples

```

  Example command line:
    ibrew shout 21 30 05 7e  Send kettle raw heat without waiting for reply
    ibrew weak 10.0.0.1      Set coffee strength to weak
    ibrew strength weak      Set coffee strength to weak but do not toggle filter/beans
    ibrew dump coffee relay out:GOD Simulates coffee machine messages

  Example console:
    off                      Stop heating/brewing
    messages                 Show all protocol messages
    message 3e               Show protocol message 3a, turn hotplate on
    167E                     Send kettle raw stop
    21 30 05 7e              Send kettle raw heat
    weak                     Set coffee strength to weak
    strength weak            Set coffee strength to weak but do not toggle filter/beans
    cups 3                   Set number of cups to brew
    mode cup                 Set cup mode
    block in:wifi,in:02          Block wifi and [Set device time] command to device
    patch relay out:version=12] Patches [Device info] Argument version to clients
    brew 4 10 beans strong   Brew 4 cups of strong coffee using the beans keeping the hotplate on for 10 minutes
    join MyWifi p@ssw0rd     Joins MyWifi wireless network using p@ssw0rd as credential
    settings 100 20 True 75  Set default user settings for the kettle to...


```

## HomeKit ~ Homebridge 

### Software

Use the following software to bridge iBrew with HomeKit

 * [Homebridge](https://github.com/nfarina/homebridge)
 * [cmdSwitch2](https://github.com/luisiam/homebridge-cmdswitch2)

### Config

Part of config file relevant to iKettle 2.0 or Smarter Coffee

#### Homebridge config iKettle 2.0
  
```
	"platforms": [{
		"platform": "cmdSwitch2",
		"switches": [{
			"name": "iKettle 2",
			"on_cmd": "/Users/Tristan/Coding/iBrew/ibrew start 10.0.0.99",
			"off_cmd": "/Users/Tristan/Coding/iBrew/ibrew stop 10.0.0.99",
			"state_cmd": "/Users/Tristan/Coding/iBrew/ibrew shortstatus 10.0.0.99 | grep 'heating'"
		}]
```

#### Homebridge config Smarter Coffee

```
	"platforms": [{
		"platform": "cmdSwitch2",
		"switches": [{
			"name": "Smarter Coffee",
			"on_cmd": "/Users/Tristan/Coding/iBrew/ibrew start 10.0.0.89",
			"off_cmd": "/Users/Tristan/Coding/iBrew/ibrew stop 10.0.0.89",
			"state_cmd": "/Users/Tristan/Coding/iBrew/ibrew shortstatus 10.0.0.89 | grep 'grinding\|brewing'"
		}]
```

#### Notes 

Fill in your own device host (either IP address or hostname) and location to ibrew, 

 * If you use an ip address: PLEASE use a static IP address! (assign in your router)
 * If you are the lucky owner of a router that assigns dynamic IP addresses with hostnames attached (usually in the form of device.local or device.lan) you can use that. If you are lucky, else use a static IP.
 * If you only have ONE device: you can use autodetection (and leave out the ip or hostname) but it adds a 2 seconds time penalty.

#### Example HomeBridge config file

If you do not use any other HomeBridge devices, you can use and alter the following 
example config file for iKettle 2.0. 

```
{
	"bridge": {
		"name": "Homebridge",
		"username": "CC:22:3D:E3:CE:30",
		"port": 51826,
		"pin": "031-45-154"
	},

	"description": "Homebridge",

	"platforms": [{
		"platform": "cmdSwitch2",
		"switches": [{
			"name": "iKettle 2",
			"on_cmd": "/Users/Tristan/Coding/iBrew/ibrew start 10.0.0.99",
			"off_cmd": "/Users/Tristan/Coding/iBrew/ibrew stop 10.0.0.99",
			"state_cmd": "/Users/Tristan/Coding/iBrew/ibrew shortstatus 10.0.0.99 | grep 'heating'"
		}]

	}]
}
```

### Web Interface

This is a build in progress, please contribute!

Start the web interface and surf to:

```
http://ip:port/
```

#### Replacement for the Smarter app

Yeah I know the start and stop icons look terrible... and it is partly functional but you get no visual indicator it worked. Work in progress!

![devices](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/devices.png)

#### Build in JSON Rest API

For bridging smarthome controllers or use it to integrate your appliance in your own website!

![rest](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/rest.png)

#### Setup

You can setup your appliance without the Smarter app. Default settings, calibration, descaling or wifi setup... it does it all! No internet required. This means you can use and setup the kettle and the smarter coffee even if smarters servers disappears (chance of no smarter servers in 5 years 97%, I seen it before :-/)

![settings](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/settings.png)

#### Statistics

It keeps stats for you, and you only! It does NOT send them (or anything else) to Smarter like the Smarter app does and definitly not to me...
Keep your appliance usage to yourself, will you!

![stats](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/stats.png)

#### Protocol description is fully interactive!

Cuz my code sucks... :-) 

![protocol](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/protocol.png)


### REST API

You can find information on the rest api in the web interface under:

```
http://ip:port/info/api
```

The default port is 2080

##### Example JSON return

http://localhost:2080/api/10.0.0.99/status

```
{"device": {"directmode": false, "connected": true, "host": "10.0.0.99", "firmware": {"version": 19, "certified": "iBrew certified firmware"}, "type": {"desciption": "iKettle 2.0", "id": 1}}, "default": {"formula": {"use": false, "temperature": {"fahrenheid": 32, "celsius": 0}}, "keepwarm": 0, "temperature": {"fahrenheid": 212, "celsius": 100, "prefered": "celsius"}}, "sensors": {"status": "ready", "base": "On", "temperature": {"raw": {"fahrenheid": 68, "celsius": 20}, "stable": {"fahrenheid": 68, "celsius": 20}}, "waterlevel": {"raw": 2005, "base": 920, "stable": 2004}}}
```
 
### Python Interface

The Smarter interface to the iKettle 2.0 and the Smarter Coffee is located in the Smarter folder. Use pydoc or any other python doc app to see the help on SmarterInterface.py and SmarterProtocol.py.


## LICENSE

The author has no contact with or support from Smarter, and is not affiliated in any way with the company that produces the appliances.


Copyright (c) 2016, Tristan Crispijn
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. You may not use source, binary forms or derivative work, with or without modification, for commercial purposes. 

4. Written consent of the original author with his/her signature on paper.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. YOU AGREE TO NOT USE THIS SOFTWARE IN ANY WAY. SMARTER EMPLOYEES OR SMARTER AFFILIATED PEOPLE ARE NOT ALLOWED TO USE THIS SOFTWARE OR DERIVATIVE WORK. YOU AGREE THAT THE SOFTWARE CAN MONITOR THE USAGE OF THE SOFTWARE ITSELF AND OR THE DEVICES ATTACHED TO THE SOFTWARE, AND SEND IT BACK TO A MONITOR SERVER FOR BETTER SUPPORT. ENJOY!
               
