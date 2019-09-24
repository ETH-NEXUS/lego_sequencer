# LEGO Sequencer

## Installation: 

To run this project, you'll need the following:

- Python 3.x + pipenv
- A LEGO Mindstorms ev3 unit with Minipython installed

Follow these instructions to set up your device with rpyc
- https://www.ev3dev.org/docs/tutorials/
- https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/rpyc.html

Check out the source code to a directory of your choosing, e.g.:

```
# creates a folder called lego_sequencer under the current directory.
git clone https://github.com/ETH-NEXUS/lego_sequencer.git
```

We'll refer to this folder, `lego_sequencer`, as the source directory below.

## Usage

The LEGO Sequencer consists of two components:
- the Mindstorms unit, which handles moving the tray and scanning bricks, and
- the webserver, which communicates with the Mindstorms unit to get the bricks that were scanned, convert them
  to a sequence, then send the sequence to NCBI's BLAST API for determining the species to which it might belong.

## LEGO Mindstorms Setup

Ensure that the device is plugged in both to power and to a USB port on your computer.

To turn the unit on, press the dark gray center button on the unit's face. You'll see some text scroll by on the display
as the brick boots up Linux. This can take up to a minute, so be patient. (In the unlikely case that it freezes, you can
hold down the left, center, and right buttons, then press the back button to reboot the unit.)

Eventually, you'll see a menu appear with a number of options. The option "File Browser" should be selected; press
the center button to activate it, at which point you'll see a list of files. The first file, `rpyc_server.sh`, should
also already be selected. To run it, press the center button again. At this point the screen will go blank, but the 
unit is ready to accept commands from the webserver which you'll soon launch on your computer.

When you're done with your demo, press the back button (the top-left button on the unit's face, separate from the other
buttons). You'll again see the file browser. Hold down the back button until a popup menu appears with power options
(i.e., "Power Off", "Reboot", and "Cancel"); press the center button again to turn the unit off.

## Webserver Setup

Inside the source directory, run the following to install the required Python libraries for the project:

```pipenv install```

Finally, run the following script to start the webserver:

`./run_site.sh`

If you're using Windows, you'll probably want to run the webserver via [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/), like so:

`run_site.bat`

The site should be accessible at [http://localhost:5000](http://localhost:5000).

### Alternate Docker Setup

If you prefer to use Docker, inside the source directory you can build the project as an image like so:

```docker build -t lego-sequencer .```

Then, you can launch the image as a container:

```docker run --rm -d -p 5000:50000 lego-sequencer```

As before, you should be able to access the site at [http://localhost:5000](http://localhost:5000).