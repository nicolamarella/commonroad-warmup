# Common Road "warmup" task

### Specifications
the idea is that we want to implement a simple python script to load a Common Road scenario and later on use that same script from a C++ program which will pass some variables (i.e. position, velocity, etc) to create or update an object in the scenario and get the state of an arbitrary object. Basically:
1. Make python work with CommonRoad_io library to load a scenario
2. Call that script with the right parameters and read output from C++

### Python setup
I am currently working on a Linux system, so I'm not using Conda but rather python virtual enviroments.

1. create python env: `python -m venv venv`
2. enable env: `source venv/bin/activate`
3. install deps: `pip install -r requirements.txt` this will automatically install also commonroad-io and some very useful tool like `pudb` for debug and testing
4. you can test python script direcly with something like `python simple_reader.py 123 1 2 3 5 --get-state 11434`

Note that you can call `python simple_reader.py -h` to see the help:
```
usage: simple_reader.py [-h] [--get-state ID] ID X Y Ψ v

positional arguments:
  ID              ID of the new object
  X               Position X of the new object
  Y               Position Y of the new object
  Ψ               Orientation Ψ of the new object
  v               Velicty v of the new object

optional arguments:
  -h, --help      show this help message and exit
  --get-state ID  Specify the ID of an Object to get the state back
```

### C++ setup
Nothing much to say, just use g++ compiler to build the program or use [compileAndRun.sh](src/compileAndRun.sh) to automatically compile and run from console.

**Important:** C++ programm will call python interpreter based on the ENV variables, so it must be executed from inside the Python virutal env (or just make C++ code better :smile: ).

### Final notes
Project is heavily improvised and can be improved A LOT. Also communication with Python could (should?) be implemented with the [Python embedding library](https://docs.python.org/2/extending/embedding.html). If I'll have time I'll branch and do it. 

Furthermore specifications were not so strict on how to make Python and C++ communicate, there are plenty of ways. It would have been so much fun running python while listening to a socket and use that to communicate in realtime with one or more C++ instances moving objects in the scenario. Again, if time, I'll branch and do it :smile: