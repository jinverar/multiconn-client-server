# multiconn-client-server

project to help learn how to connect multi-connected clients to a server for incident response. 

I have uploaded a GUI for the client server code

there are two main files to the GUI. 

1. clientPythonCode.py
2. clientApp.py
3. multiconn-client-gui.ui

the ClientApp.py was created with the following command from the .ui file 

```bash
pyuic5 -x -o  clientApp.py  muliconn-client-gui.ui
```
the clientPythonCode.py is my main working file that holds the python code for the program. This file imports the mainwindow code.

Program Usage:

```python
python clientPythonCode.py
```

Thank you and anyone can contribute to this project. 