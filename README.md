## What
Python script to dynamically change the fps cap of a game based on idleness.

## Why
Saves power, also reduce heat in the room (summer is too darn hot)
AMD does this perfectly fine with Radeon Chill, but NVDIA doesn't care

## How
### Requirements :
- Python & [Pynput](https://pypi.org/project/pynput/)
- [RTSS](https://www.guru3d.com/page/rivatuner-rtss-homepage/)
- [rtss-cli](https://github.com/xanderfrangos/rtss-cli)

1. set the name of the app (so the same as the rtss profile) or use "Global"
2. set rtss-cli.exe path
3. change config if you like
4. run the script (& rtss)

### How idleness is decided
- Uses max fps on high activity or if a configurable "active_key" is pressed
- Reduces to a lower fps otherwise
- After a period of no input, reduces fps further
- After another period of no input, reduces fps even further

### Limitations
- Made with a specific use case in mind (ff14)
- Does not care whether inputs are made on the game window or elsewhere
- Does not care for mouse movements or scroll
- You'll have to automate script startup on your own
