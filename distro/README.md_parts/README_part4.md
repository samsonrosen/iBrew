
```

### HomeKit ~ Homebridge 

Use the following software to bridge iBrew with HomeKit

[Homebridge](https://github.com/nfarina/homebridge)
[cmdSwitch2](https://github.com/luisiam/homebridge-cmdswitch2)

Example homebridge config file for iKettle 2.0 (Smarter Coffee coming soon)

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

#### REST API

You can find information on the rest api under:

```
http://ip:port/info/api
```
 
   
### Python Interface

Use pydoc or any other python doc app to see the help on Smarter*.py


### LICENSE

The author has no contact with or support from Smarter, and is not affiliated in any way with the company that produces the appliances.

