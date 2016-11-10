function calibrate(ip)          { $.getJSON( '/api/' + ip + '/calibrate'); }

var wait_update = 1000;
var wait_joke   = 60000;

// auto joke timer is not synchronized with the click event (wow that's some sufisasactating... stuff
function process_joke(joke)     { $('#quote').html( joke.question + '<br>' + joke.answer ); }
function joke()                 { $.getJSON( '/api/joke', process_joke); }
function auto_joke()            { joke(); setTimeout(auto_joke, wait_joke);}

function process_update_kettle(status) { if ( status.sensors.base == "On") {
                                           $('#kettle').attr('src','{{ static_url('icons/kettle/kettle.png')}}');
                                           if ( status.default.temperature.prefered == 'celsius' ) {
                                             $('#temperature').html( status.sensors.temperature.raw.celsius + " ºC" ); }
                                           else
                                             $('#temperature').html( status.sensors.temperature.raw.fahrenheid + " ºF" );
                                           $('#water').html( status.sensors.waterlevel.raw-status.sensors.waterlevel.base );
                                           }
                                           else {
                                                $('#water').html( "" );
                                                $('#temperature').html( "" );
                                                $('#kettle').attr('src','{{ static_url('icons/kettle/offbase.png')}}');
                                                
                                           }
                                        }


    
function update_kettle(ip)             { $.getJSON( '/api/' + ip + '/status', process_update_kettle); }
function auto_update_kettle(ip)        { update_kettle(ip); setTimeout(auto_update_kettle, wait_update, ip); }


function process_update_coffee(status) { }

function update_cofee(ip)             { $.getJSON( '/api/' + ip + '/status', process_update_cofee); }
function auto_update_coffee(ip)        { update_cofee(ip); setTimeout(auto_update_cofee, wait_update, ip); }



// Coffee machine control
function cups(ip,cups)              { $.getJSON( '/api/' + ip + '/cups/' + cups); }
function weak(ip)                   { $.getJSON( '/api/' + ip + '/weak'); }
function medium(ip)                 { $.getJSON( '/api/' + ip + '/medium'); }
function strong(ip)                 { $.getJSON( '/api/' + ip + '/strong'); }
function onecupmode(ip,state)       { $.getJSON( '/api/' + ip + '/mode/carafe'); }
function carafemode(ip,state)       { $.getJSON( '/api/' + ip + '/mode/cup'); }
function filter(ip,state)           { $.getJSON( '/api/' + ip + '/filter'); }


function start(ip)              { $.getJSON( '/api/' + ip + '/start'); }
function stop(ip)               { $.getJSON( '/api/' + ip + '/stop'); }

var wait_update = 30000;

function process_update_scan(wirelessnetworks) {

x = wirelessnetworks.networks

keys = Object.keys(x),
keys.sort();

$('#wifi').html('')
$('#wifi').append('<div class="tRow"><div class="wirelessTitleCell">Wireless Networks</div><div class="wirelessSignalCell"></div></div><br>');

for (i = 0; i < keys.length; i++) {
   key = keys[i];
   item = x[key];
    $('#wifi').append('<div class="tRow">');
    $('#wifi').append('<div class="wirelessNameCell"><a href="javascript:join(\''+key+'\')">' + key + '</a></div>');
    $('#wifi').append('<div class="wirelessSignalCell">');
 
    icon = '{{  static_url('icons/wifi/') }}';
    if ( item.quality >= 0 && item.quality < 10) {
        $('#wifi').append('<img id="signal" src="' + icon + 'signal0.png">')
    }
    if ( item.quality >= 10 && item.quality < 30 ) {
        $('#wifi').append('<img class="signal" src="' + icon + 'signal1.png">')
    }

    if ( item.quality >= 30 && item.quality < 50 ) {
        $('#wifi').append('<img class="signal" src="' + icon + 'signal2.png">')
    }

    if ( item.quality >= 50 && item.quality < 70 ) {
        $('#wifi').append('<img id="signal" src="' + icon + 'signal3.png">')
    }
    
    if ( item.quality >= 70 && item.quality <= 100 ) {
        $('#wifi').append('<img class="signal" src="' + icon + 'signal4.png">')
    }
    
    $('#wifi').append('</div>');
    $('#wifi').append('</div>');
}

if (!wirelessnetworks.directmode) {
$('#wifi').append('<div class="tRow">' );
$('#wifi').append('<div class="wirelessNameCell"><a href="javascript:leave(\'{{ client.host }}\')">{{ Smarter.device_to_string(client.deviceId) }} Direct</a></div>');
$('#wifi').append('<div class="wirelessSignalCell"></div></div>');
}
        
}

function leave(ip)              { $.getJSON( '/api/' + ip + '/leave'); }
function update_scan(ip)        { $.getJSON( '/api/' + ip + '/scan', process_update_scan); }
function auto_update_scan(ip)   { update_scan(ip); setTimeout(auto_update_scan, wait_update, ip); }

$(document).ready(              function() {
                                             auto_update_scan('{{ client.host }}'); }
                 );


$(document).ready(function()    {
                                setTimeout(auto_joke, wait_joke);
                                {% for ip in clients %}
                                {% if clients[ip].isKettle %}
                                    setTimeout(auto_update_kettle, wait_update, '{{ ip }}');
                                {% elif clients[ip].isCoffee %}
                                    setTimeout(auto_update_coffee, wait_update, '{{ ip }}');
                                {% end %}
                                {% end %}
                  
                  
                                $("#toggle").click(function(){
                                    $("#settings").toggle();
                                });
                                
                                });

