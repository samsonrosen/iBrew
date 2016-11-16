        """
            print "  YEAR80"
            print "    00..FF  YEAR = YEAR80 + 1980"
            print
       

        elif id == Smarter.ResponseWirelessNetworks:
            print "  DB is the signal strength in dBm format."
            print
            print "  Response: <PAYLOAD>"
            print
            print "  PAYLOAD:  <SSID>{0,32}<\",\"><DB>{3}>"
            print
            print "  SSID:     Name in text"
            print
            print "  DB:       <\"-\"><dBm>"
            print
            print "  Examples: MyWifi,-56}"
            print "            MyWifi,-56}OtherWifi,-82}"
            
            
        elif id == Smarter.CommandHeat:
            print "  If no arguments are given it uses its default."
            print
            print "  Arguments: <[<TEMPERATURE><[KEEKWARMTIME]>]>"
            print
            Temperature()
            Keepwarm()
            print "  Examples: 21 50 05 7e"
            print "            21 44 7e"
            print "            21 7e"
            print
            print "  Heat up till 90 if default is 80"

        
        elif id == Smarter.ResponseCoffeeHistory:
            print "  The payload is generated everytime the coffee machine brews. The actioncounter increases with every brewing?"
            print
            print "  Payload maximum is 8. So if 8 check again, if there is more history"
            print "  month checked only accepts value from 1..0c"
            print
            print "  Response: <COUNTER> [<PAYLOAD>{COUNTER}]"
            print
            print "  COUNTER"
            print "    00..08"
            print
            print "  PAYLOAD"
            print "    <??><??><??><DEFAULT/CUPS?><DEFAULT/CUPS?><SECONDS??>"
            print "    <HOURS???><MINUTES???><DAY??><MONTH><YEAR80???><STATE><??>{19}"
            print
            Cups()
            History()
            print "  Example: 47 02 01 00 00 02 02 00 19 00 01 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d"
            print "                 01 00 00 0c 0c 00 19 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e"
           
        elif id == Smarter.ResponseKettleHistory:
            print "  The payload is generated everytime the kettle stops heating. The actioncounter increases with every heating?"
            print "  Formula temperature is above 0 then it was heated with formula temperature enabled. There seems to be some"
            print "  packed time available."
            print
            print "  Payload maximum is 8. So if 8 check again, if there is more history"
            print "  month checked only accepts value from 1..0c"
            print
            print "  Response: <COUNTER> [<PAYLOAD>{COUNTER}]"
            print
            print "  PAYLOAD"
            print "    <??><TEMPERATURE><KEEPWARMTIME><FORMULATEMPERATURE><ACTIONCOUNTER>"
            print "    <SECONDS??><HOURS?><MINUTES?><DAY?><MONTH><YEAR80?><STATE><??>{19}"
            print
            print "  COUNTER"
            print "    00..08"
            print
            Temperature()
            Keepwarm()
            Formula()
            print "  ACTIONCOUNTER"
            print "    00..ff  Amount of heatings before off base"
            History()
            print "  Example: 29 02 01 5f 00 00 0f 00 09 03 15 0a 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d"
            print "                 01 64 19 32 10 00 09 0e 15 0a 19 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e"
        
        elif id == Smarter.CommandStoreBase:
            print "  This can contain the tail 7e, so check for length here!"
            print
            print "  Arguments: <BASELHIGHBITS><BASELOWBITS>"
            print
            print "  BASE = BASELHIGHBITS * 256 + BASELOWBITS [0..4095]"
            print
            print "  Example: 2a 04 03"


        elif id == Smarter.ResponseBase:
            print "  This can contain the tail 7e, so check for length here!"
            print
            print "  Response: <BASELHIGHBITS><BASELOWBITS>"
            print
            print "  BASE = BASELHIGHBITS * 256 + BASELOWBITS [0..4095]"

        elif id == Smarter.Command30:
            print "  Arguments: <[UNKNOWN]>{?}"
            print
            print "  Example: 30 7e"
    
  

        elif id == Smarter.ResponseTimers:
            print "  Arguments: <PAYLOAD>{1 or 4}"
            print
            print "  PAYLOAD  <UNKNOWN><MINUTES><HOURS><??><DAY><MONTH><CENTURY><YEAR>"
            print
            print "  UNKNOWN (COUNTER?)"
            print "    00 Happended"
            print "    01 Not happened"
            print
            Timers()
    """
