
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

![devices](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/devices.png)

![rest](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/rest.png)

![settings](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/settings.png)

![stats](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/stats.png)

![protocol](https://raw.githubusercontent.com/Tristan79/iBrew/master/distro/images/protocol.png)


### REST API

You can find information on the rest api in the web interface under:

```
http://ip:port/info/rest
```

##### Eaxmple json return

http://localhost:2080/api/10.0.0.99/status

```
{"device": {"directmode": false, "connected": true, "host": "10.0.0.99", "firmware": {"version": 19, "certified": "iBrew certified firmware"}, "type": {"desciption": "iKettle 2.0", "id": 1}}, "default": {"formula": {"use": false, "temperature": {"fahrenheid": 32, "celsius": 0}}, "keepwarm": 0, "temperature": {"fahrenheid": 212, "celsius": 100, "prefered": "celsius"}}, "sensors": {"status": "ready", "base": "On", "temperature": {"raw": {"fahrenheid": 68, "celsius": 20}, "stable": {"fahrenheid": 68, "celsius": 20}}, "waterlevel": {"raw": 2005, "base": 920, "stable": 2004}}}
```
 
### Python Interface

The Smarter interface to the iKettle 2.0 and the Smarter Coffee is located in the Smarter folder. Use pydoc or any other python doc app to see the help on SmarterInterface.py and SmarterProtocol.py.


## LICENSE

The author has no contact with or support from Smarter, and is not affiliated in any way with the company that produces the appliances.

