# What's this?
It's a Python library for controlling split-flap displays!

# Supported devices
This library currently supports the following devices:

* KRONE / MAN "FBM" split-flap modules with ZiLOG microcontroller (in combination with the "FBUE" address board)
* KRONE / MAN "HLST" heater and light control boards

Support is planned for:

* KRONE / MAN "FBK" split-flap group controller boards
* OMEGA split-flap units with RS-485 data protocol

# Relevant info
Probably most relevant is the pinout of the various devices.
Here's a short, incomplete summary:

![Pinout of 10-pin FBM pin header](/images/pinout_fbm.png?raw=true)

Pinout of the 10-pin header on KRONE / MAN "FBM" modules. You will need the "FBUE" address board to go with it.

![Pinout of 20-pin FBUE pin header](/images/pinout_fbue.png?raw=true)

Pinout of the 20-pin KRONE / MAN split-flap bus header. This is what you will most likely encounter when dealing with this type of display.

# Installation
`pip install pysplitflap`