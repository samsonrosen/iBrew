
```

### Relay

Start a relay server on port 2081, it acts as an man in the middle passing messages between the appliance and
the clients like the Smarter app or another iBrew instances. It can be configured to block and/or modify/patch certain messages. And as there is only one connection needed to the appliances. Good riddense of the annoying beep when the wireless network disconnects due to overload of connections. Also statistics are now possible.


__Advantages__
 * No annoying beep. Only one connection to the appliance needed
 * A lot faster!
 * History and statistics possible!
 * Works with Smarter app!
 * Works with iBrew as client!?
 * Message blocking
 * Message patching

```ibrew dump relay 10.0.0.99```


### Simulation

* Simulates iKettle 2.0 ```ibrew coffee simulate```
* Simulates Smarter Coffee machine ```ibrew kettle simulate```

You can use to dump actionto see more info...

### Web

This is a build in progress, please contribute!

Start the web interface 

```
ibrew web
```

and surf to:

```
http://ip:port/
```

#### Replacement for the Smarter app

Yeah I know the start and stop icons look terrible... and it is partly functional but you get no visual indicator it worked. Work in progress!

![devices](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/devices.png)

#### Build in JSON Rest API

For bridging smarthome controllers or use it to integrate your appliance in your own website!

![rest](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/api.png)

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


### JSON REST API

You can find information on the iBrew JSON REST API in the Web Interface under:

```
http://ip:port/info/api
```

The default port is 2080

#### Example JSON return

http://localhost:2080/api/10.0.0.99/status

```
{"device": {"directmode": false, "connected": true, "host": "10.0.0.99", "firmware": {"version": 19, "certified": "iBrew certified firmware"}, "type": {"desciption": "iKettle 2.0", "id": 1}}, "default": {"formula": {"use": false, "temperature": {"fahrenheid": 32, "celsius": 0}}, "keepwarm": 0, "temperature": {"fahrenheid": 212, "celsius": 100, "prefered": "celsius"}}, "sensors": {"status": "ready", "base": "On", "temperature": {"raw": {"fahrenheid": 68, "celsius": 20}, "stable": {"fahrenheid": 68, "celsius": 20}}, "waterlevel": {"raw": 2005, "base": 920, "stable": 2004}}}
```

### JavaScript

Work in progress! Help would be nice!

JavaScript for use with iBrew JSON REST API [Javascript iBrew interface](https://github.com/Tristan79/iBrew/blob/master/resources/ibrew.js) 
 
### Python

The [Python Smarter Interface](https://github.com/Tristan79/iBrew/blob/master/smarter/) to the iKettle 2.0 and the Smarter Coffee is located in the Smarter folder. Use __pydoc__ or any other python doc app to see the help on [SmarterInterface.py](https://github.com/Tristan79/iBrew/blob/master/smarter/SmarterInterface.py) and [SmarterProtocol.py](https://github.com/Tristan79/iBrew/blob/master/smarter/SmarterProtocol.py). There are a lot of options and functions you can use!

#### Basic Example

```
from smarter.SmarterInterface import *
from smarter.SmarterProtocol import *

appliance = SmarterClient()
appliance.host = "10.0.0.99"
appliance.connect()
if appliance.isKettle() and not appliance.heaterOn:
    appliance.kettle_heat_default()
appliance.disconnect()

```

#### Smarthome controller software

You can always patch or hack in your favorite Smarthome controller (if they have a python interface) into the following functions of SmarterInterface.py. 

```
def __read(self)
def __send(self)
def __monitor_device(self)
```

And start up the monitor with a command like ```ibrew dump monitor 10.0.0.99```  ;-) 

#### Domoticz

Link to old [domoticz alpha python interface](https://github.com/Tristan79/iBrew/tree/6014cbf0a8cd551e74cbc8bfcf3f0f97389359c2/domoticz). This link contains old example [code](https://github.com/Tristan79/iBrew/blob/927c43e347b7c8aa1c2d897936ac51c34fa80e7e/iBrewTerminal.py) for a monitor (look for domoticz) which can be reused


## Guides

### Domoticz

Coming soon!

### HomeKit ~ HomeBridge 

Yes, you can! Connect your iKettle or Smarter Coffee to HomeKit... just follow the following steps!

#### Software

Install the following software to bridge iBrew with HomeKit

 * [Homebridge](https://github.com/nfarina/homebridge)
 * [cmdSwitch2](https://github.com/luisiam/homebridge-cmdswitch2)

#### Setup

Part of config file relevant to iKettle 2.0 or Smarter Coffee

Fill in your own device host (either IP address or hostname) and location to iBrew, 

 * If you use an IP address: PLEASE use a static IP address! (assign in your router)
 * If you are the lucky owner of a router that assigns dynamic IP addresses with hostnames attached (usually in the form of device.local or device.lan) you can use that. If you are lucky, else use a static IP.
 * If you only have ONE device: you can use autodetection (and leave out the ip or hostname) but it adds a 2 seconds time penalty.

#### HomeBridge example config iKettle 2.0
  
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

#### HomeBridge example config Smarter Coffee

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
### Other

Have any links, info or help on other Smarthome controller software, please post in the issues!

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
 * PROTOCOL: History message is not finished
 * PROTOCOL: Modifiers/patches!!! 
 * PROCOCOL: Script or url events
 * PROCOCOL: Time arguments (have not figured that out)
 * PYTHON: Better error handling
 * PYTHON: There is no length check on message... could crash thing :-)
 * IKETTLE20: Fahrenheid not finished, please to not use.
 * IKETTLE20: Watersensor to something usefull (like the stupid left or right side handle, cuz the kettle weight balance is off, its inaccurate as fuck even in the smarter app :-/)
 * SMARTER COFFEE: Have not looked at single cup... needs a remote coffee machine session ;-)
 * SMARTER COFFEE: Did I accidently switch carafe required bit?
 * SMARTER COFFEE: Cups from the status and cups from the display setting is differen 
 * SMARTER COFFEE: Timers protocol
 * SMARTER COFFEE: v0.5 Missing Coffee Smarter codes (working bit only?)
 * SMARTER COFFEE: Descaling data bit? (the smarter app has it...)
 * HELP: Add the missing pieces
 * SIMULATOR: Add carafe removal and water filling
 * SIMULATOR: Fix waterlevel and fix cups?

Interfaces
 * PYTHON: Better error handling
 * PYTHON: Make the print stuff more general
 * PYTHON: Strip zero from ip
 * PYTHON: fix wireless with the same name
 * PYTHON: filter out wrong responses... of know commands??? or atleast acknowledge them, (03 responses)
 * CLI: make on/off true/false universal with string_to_bool
 * CLI: relay has no port neither has ibrew, we need port numbers...
 * CLI: Fix Simulation command and relay...
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


## LICENSE

The author has no contact with or support from Smarter, and is not affiliated in any way with the company that produces the appliances.

