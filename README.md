# iBrew: Brewing on the 7th day

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface

## News 

[The iKettle, the Eleven-Hour Struggle to Make a Cup of Tea, and Why It Was All About Data, Analytics and Connecting Things Together](https://medium.com/mark-rittman/the-story-behind-the-ikettle-the-eleven-hour-struggle-to-make-a-cup-of-tea-and-why-it-was-all-769144d12d7#.h62foolse) 


## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, command line interface, web interface and rest api. You can also use it in your own code. iKettle 2.0 v19 and SmarterCoffee v20 tested at the moment. Please share any other discoveries you made! 

This means your machine is free! You can connect it yourself and do whatever you want with it. Like interface it with your favorite smarthome controller!

   Signed Me!

#### Brewing on the 7th day 

Since the console it nearly done, protocol almost fully mapped out. It is time to focus on the webpage... the framework is working, it auto reconnect, keeps some stats and you can even preform some actions with it.


#### Update

I tested the code and I can simulate a coffee machine (so I can write the web stuff without a coffee machine), still I do not have time till december to finish the web interface (ju4ia tolds me the coffee part is partly working). The command line is fully functional!!! Patches are also not working, and the replay mode does not quit properly... Anyway speeded up the network code and added a message blocking system (firewall)... can take a while for the web interface to be fully functional.

Anyway, as always donate: codes, your own code mods, bugs or other stuff...

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
 * PHASE 5: [WEB]           v0.4 Brewing on the 7th day (rest api is working!!!)
 * PHASE 6: [PRERELEASE]    v0.5 The conundrum struggle
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
    energy                 energy saver (stats not possible)
    shout                  sends commands and quits not waiting for a reply
    slow                   fully inits everything before action
    coffee                 assumes coffee machine
    kettle                 assumes kettle
    fahrenheid             use fahrenheid
    command                action to take!
    host                   host address of device (format: ip4, ip6, fqdn)

  If you do not supply a host, it will try to connect to the first detected device
  Thus if you have more then one device supply a host (if its not in direct mode)


```

### Console
Start the console with the command `iBrew console`. The following commands are available within the console,
you can also use them on the command line as arguments:

```

  iKettle 2.0 & Smarter Coffee  Commands
    default                set default settings
    info                   device info
    list                   list detected devices
    reset                  reset device to default
    start                  start the device
    status                 show status
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
    Consists of rules, > is for outgoing connection to the device, < is for incomming connection from relay client.

    [>|<]rule(,[>|<]rule)*

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

  Example:
    off                      Stop heating/brewing
    messages                 Show all protocol messages
    message 3e               Show protocol message 3a, turn hotplate on
    167E                     Send kettle raw stop
    21 30 05 7e              Send kettle raw heat
    weak                     Set coffee strength to weak
    strength weak            Set coffee strength to weak but do not toggle filter/beans
    cups 3                   Set number of cups to brew
    mode cup                 Set cup mode
    block >wifi,>02          Block wifi and [Set device time] command to device
    patch relay <version=12] Patches [Device info] Argument version to clients
    brew 4 10 beans strong   Brew 4 cups of strong coffee using the beans keeping the hotplate on for 10 minutes
    join MyWifi p@ssw0rd     Joins MyWifi wireless network using p@ssw0rd as credential
    settings 100 20 True 75  Set default user settings for the kettle to...


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

Use pydoc or any other python doc app to see the help on Smarter.py

### LICENSE

The author has no contact with or support from Smarter, and is not affiliated in any way with the company that produces the appliances.


Copyright (c) 2016, Tristan Crispijn
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. You may not use source, binary forms or derivative work, with or without modification, for commercial purposes. 

4. Written consent of the original author with his/her signature on paper.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. YOU AGREE TO NOT USE THIS SOFTWARE IN ANY WAY. SMARTER EMPLOYEES OR SMARTER AFFILIATED PEOPLE ARE NOT ALLOWED TO USE THIS SOFTWARE OR DERIVATIVE WORK. YOU AGREE THAT THE SOFTWARE CAN MONITOR THE USAGE OF THE SOFTWARE ITSELF AND OR THE DEVICES ATTACHED TO THE SOFTWARE, AND SEND IT BACK TO A MONITOR SERVER FOR BETTER SUPPORT. ENJOY!
               
