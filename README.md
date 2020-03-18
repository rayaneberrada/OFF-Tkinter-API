# Project Title

OpenFoodFacts interface: tkinter interface where you can pick an aliment among the differents categories proposed and get an healthier equivalent for the aliment selected and save them in database..

## Motives

The point of that application was to learn to interact with API's and database using Python.

## Libraries

[Tkinter](https://docs.python.org/3/library/tk.html)

[Requests](http://docs.python-requests.org/en/master/)

[Records](https://pypi.org/project/records/)

[Pymysql](https://github.com/PyMySQL/PyMySQL)

## Screenshots

Main menu:
![Screenshot](OFF.png)


## Installation
1-Create a database named "offdb" using mysql. Make sure to changes variables connection such as "user" and "passow" in Database.py and Interface.py and replace them by ones related to the mysql user you used to create your Database

2-Create a virtual environnement and clone the repository inside

3-move inside the projet_cinq directory

4-run this code to install all the requirements you need to use the program:  
```Bash
pip install -r requirements.txt
```
  followed by this code to install Tkinter: 
  ```Bash
sudo apt-get install python3-tk
  ```
5-You need to run that code to force the creation of the database the first time you launch the program: 
```Bash
python Launcher.py -e 'update'
```
Then you can just launch the program by typing this code or force the update of the database with the previous code : 
```Bash
python Launcher.py 
```
