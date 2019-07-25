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

first start the server using the following command

```python
python multiconn-server.py <ip address> <port>
```
then start the client use the following command and the client has a Gui that has a console located at the bottom of the main window

```python
python client-gui.py
```

Once the main windows is displayed then type "Help" for the help windows or type "connect" for the connection dialog.

the server is set to automatically start on port '12345" and the user will have to increase the num_conns each time they connect.


Thank you and anyone can contribute to this project. 
