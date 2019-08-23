# LEGO Sequencer

## Installation: 

To run this project, you'll need the following:

- Python 3.5.3
- A LEGO Mindstorms ev3 unit with Minipython installed

To set up the webserver, run the following commands:

```bash
popd static
npm install
pushd
```
  
Follow these instructions to set up your device with rpyc
- https://www.ev3dev.org/docs/tutorials/
- https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/rpyc.html


## Usage

You should already have the ev3 connected and running the rpyc daemon.

Run the following to start the webserver:

`FLASK_APP=app.y flask run`
