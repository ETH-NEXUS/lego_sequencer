# LEGO Sequencer

## Installation: 

To run this project, you'll need the following:

- Python 3.5.3 + pipenv
- A LEGO Mindstorms ev3 unit with Minipython installed

Follow these instructions to set up your device with rpyc
- https://www.ev3dev.org/docs/tutorials/
- https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/rpyc.html


## Usage

You should already have the ev3 connected and running the rpyc daemon. First, install the Python requirements like so:

```pipenv install```

Run the following to start the webserver:

`./run_site.sh`

If you're using Windows, you'll probably want to run the webserver via [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/), like so:

`run_site.bat`
