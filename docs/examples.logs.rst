-----------
Logging
-----------

OOPNET allows for logging on different levels. `logging.INFO` provides basic information about what OOPNET is doing,
while `logging.DEBUG` provides for detailed information.

To enable logging, you can either create your own logger and set the logging handlers as you please, or use logger
provided by OOPNET. This logger uses a `RotatingFileHandler` and a `StreamHandler`. The `RotatingFileHandler` writes up
to 5 MB of data to `oopnet.log` before rotating the logs. The default logging level is `logging.INFO` but this behaviour
can be overruled.

To show logging functionality, we first have to import the necessary packages.

.. literalinclude:: /../examples/logs.py
	:language: python
	:lines: 1-4

Now, let's start the logger:

.. literalinclude:: /../examples/logs.py
	:language: python
	:lines: 6

.. note::

	The logger only has to be started once! Don't put this function call in every part of your package/module! Below is
	also an example that describes, how to implement logging in the other parts of your program.


Next, we read the Poulakis model.

.. literalinclude:: /../examples/logs.py
	:language: python
	:lines: 8-10

This leads to a log message in `oopnet.logs` and in the console::

	Reading model from 'data/Poulakis.inp'

If you want more details, you can set the logging level to `logging.DEBUG`

.. literalinclude:: /../examples/logs.py
	:language: python
	:lines: 12

Now, if we reread the Poulakis model, we will get way more information:

.. literalinclude:: /../examples/logs.py
	:language: python
	:lines: 14

And here are the log contents::

	Reading model from 'data/Poulakis.inp'
	Reading Curves
	Reading Patterns
	Reading Junctions section
	Added 30 Junctions
	Reading Reservoirs section
	Added 1 Reservoirs
	Reading Tanks section
	Added 0 Tanks
	Reading Pipes section
	Added 50 Pipes
	Reading Pumps section
	Added 0 Pumps
	Reading Valve section
	Added 0 Valves
	Reading demand section
	Reading Options
	Reading report settings
	Reading times settings
	Reading Controls
	Reading Energy
	Reading Rules
	Reading status section
	Reading mixing section
	Reading quality section
	Reading reactions
	Reading sources section
	Reading Emitters section
	Reading title
	Reading Coordinates section


Now, what if you had a function, that you think might fail and that you want to log? OOPNET provides a decorator for
this purpose, `logging_decorator()`, that needs a logger passed to it.

First, let's pretend that the logger has already been started in another part of you program and you want to add logging,
to a different part of your program (i.e., you don't have to declare logging handlers, that's already taken care of).
To do this, we simply have to get the logger:

.. literalinclude:: /../examples/logs.py
	:language: python
	:lines: 16

We will now use this logger to log a custom function. We want to log a function that tries to add a float and a string.
After declaring the function, we call it and of course an exception is raised:

.. literalinclude:: /../examples/logs.py
	:language: python
	:lines: 19-24

This results in the following logs::

	Error raised by 'do_some_crazy_things'
	Traceback (most recent call last):
	  File "/home/***/oopnet/oopnet/utils/oopnet_logging.py", line 46, in wrapper
		return func(*args, **kwargs)
	  File "/home/***/oopnet_refactor/examples/logs.py", line 21, in do_some_crazy_things
		a += b
	TypeError: unsupported operand type(s) for +=: 'int' and 'str'
	Traceback (most recent call last):
	  File "/home/***/oopnet/examples/logs.py", line 25, in <module>
		do_some_crazy_things()
	  File "/home/***/oopnet/oopnet/utils/oopnet_logging.py", line 46, in wrapper
		return func(*args, **kwargs)
	  File "/home/***/oopnet/examples/logs.py", line 21, in do_some_crazy_things
		a += b
	TypeError: unsupported operand type(s) for +=: 'int' and 'str'



+++++++
Summary
+++++++

.. literalinclude:: /../examples/logs.py
	:language: python