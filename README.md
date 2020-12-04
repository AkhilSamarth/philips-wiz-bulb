# Simple Script to control a Philips Wiz lightbulb

This is a script you can use to easily manipulate a Philips Wiz lightbulb outside of the app (note: you'll still the need the app for first-time setup). The only configuration needed for the script to enter in the IP and MAC addresses of the bulb you want to control. After that, just call the following functions to interface with the bulb:

`setColor(r, g, b, w=0, c=0)` - Sets the color of the bulb. On a full-color bulb, there are 5 LEDs inside the bulb: red, green, blue, warm white, and cool white. The setColor function takes in 5 arguments (warm and cool parameters optional) corresponding to each of these in the range [0, 255].

`setTemp(temp, brightness=100)` - Sets the bulb to white light with the given color temperature and brightness (optional). Temperature is in Kelvin with range [2200, 6000] (warm white to cool white). Brightness ranges [10, 100].

`changeState(state=None)` - Turns the bulb on or off. True turns the bulb on, False turns it off, and None will toggle the bulb.

`smoothTemp(start=4500, end=3000, duration=60)` - Smoothly transitions between the given color temperatures in `duration` minutes. Default parameters will transition from a cool white to a warm white over the course of an hour (useful for a bedroom in which you work).

## Technical Details

These lightbulbs communicate with their apps using a UDP port on port 38899. The communication itself occurs through JSON objects with a few simple parameters. The following is the format of the JSON sent from the app to the bulb:

```
{
	"method":"setPilot",
	"env":"pro",
	"params":{
		"mac":"<BULB MAC ADDRESS HERE>",
		"rssi":-73,
		"src":"",
		"state":true,
		"dimming":100,
		"r":0,
		"g":0,
		"b":0,
		"c":0,
		"w":0
	}
}
```

Note: the last 5 parameters (`r, g, b, c, w`) can be replaced with a single `temp` parameter.

Main parameters:

`state` - turns the bulb on/off

`dimming` - sets the brightness of the bulb

`r`/`g`/`b` - RGB values for full-color models

`c`/`w` - controls the two white LEDs (cool and warm)

`temp` - used to easily set white color temperature rather than manually inputting values for LEDs

## Credits

Thanks to the following source for help in figuring out how these bulbs work:

http://blog.dammitly.net/2019/10/cheap-hackable-wifi-light-bulbs-or-iot.html
