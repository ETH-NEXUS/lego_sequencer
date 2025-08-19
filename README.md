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

### Network issues
on the macbook the device should appear as a network device. I had issues with the self asisgned IP (yellow dot at the device in the network settings). Setting the IP manually to 192.168.2.1 and the mask to 255.255.255.0 solved the issue

### SSH
For debugging and setup, ssh to the ev3 can be helpful, with usb connected run: `ssh robot@ev3dev.local` default pw:`maker`.

## Webserver Setup

Inside the source directory, run the following to install the required Python libraries for the project.

The communication with the ev3 depends on a legacy version of rpyc which we need to patch to make it compatible with python > 3.6
```bash
# 1) clone old version of rpyc
git clone https://github.com/tomerfiliba-org/rpyc.git
cd rpyc
git checkout v3.3
# Apply local patch
patch -p1 < ../rpyc-v3.3-python3.12-compat.patch 
# install the env (local rpyc is referenced in Pipfile)
cd ..
pipenv install
```


Finally, run the following script to start the webserver:

`./run_site.sh`

If you're using Windows, you'll probably want to run the webserver via [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/), like so:

`run_site.bat`

The site should be accessible at [http://localhost:5000](http://localhost:5000).

## Patch rpyc 3.3
The eve3 runs python 3.5, and the corresponding rpyc module 3.3.0 - which is incompatible with modern python versions, due to the usage of async (keyword since python 3.7)
To make it work with modern python, the function rpyc.utils.helpers.async needs to be renamed to async_, as well as the module rpyc.core.async to async_module. 

## Google custom search API
The web server uses google custom serarch API to fetch images of the species found by blast.
To use this feature, set up a search engine as well as API key as described in  
`https://developers.google.com/custom-search/v1/overview`
and store the credentials in `instance/application.cfg`:
```

GCE_KEY = 'your_key'
GCE_PROJECT_CX = 'your_search_engine_id'
```


### Alternate Docker Setup

Python 3.5 is not available on Mac, so one alternative is to use Docker. 
Inside the source directory you can build the project as an image like so:

```docker build --platform linux/amd64 -t lego-sequencer .```
Then, you can launch the image as a container:


```bash
docker run \
  --platform linux/amd64 \
  -p 5000:5000 \
  -e FLASK_APP=sequencer \
  -e FLASK_ENV=development \
  -v "$(pwd)":/app \
  lego-sequencer

docker ps                      # find the container ID or name
#restart app:
docker kill -s HUP <container_name>
# stop
docker stop <container_id>    # stop the running container
```


As before, you should be able to access the site at [http://localhost:5000](http://localhost:5000).

## Mock mode
To test frontend an webservice calls without the lego hardware there is a mock mode implemented. Activate by setting `MOCK_COMM` in `sequencer/default_settings.py`.

```python
MOCK_COMM =  True
```
