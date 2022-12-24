# Welcome to Tic-Tac-Toe API

Hello! This project is an API that is written in **Python** using **Flask** framework. You can integrate this with any frontend of your choice - be it web app client or mobile app. Obviously! you need to host this API on some cloud (e.g. AWS, Azure, etc.) to start using it.

This projects is built entirely on flask framework. You can refer **flask documentation** [here](https://flask.palletsprojects.com/en/2.2.x/) 

## Local Installation and build

Follow below steps to clone this repo to your local system and build locally.

### Git clone
```batch
git clone https://github.com/nkitanand/tictactoe_RestAPI.git
```

### Create virtual environment
Since, your local system might have other python projects that uses the same libraries. Updating one library for the sake of one project might harm or even break other projects. Thus, it is a best practice to use virtual environment in python that helps in managing libraries seperately for different projects. Follow these steps to create virtual environment -
>**Note:** For more details refer [virtual env section](https://flask.palletsprojects.com/en/2.2.x/installation/#virtual-environments)  of flask documentation
```batch
cd go/to/root_directory/of/project/
py -m venv venv
venv\Scripts\activate
```

### Installing necessary Libraries
This project depends on a number of libraries to work. I have put these details in _requirements.txt_ file. You can run a simple **pip** command to install all the libraries. 
> **Note:** Refer python virtual environment section before running this **pip** command
```batch
pip install -r requirements.txt
```

## Run API locally

After installing all the required libraries you are now ready to experience this awesome API that acts as the engine behind the tic-tac-toe game. 
>Go to the root directory of the project before running below command. Make sure root directory contains "app.py" file.
```batch
flask run
```
To Run in debugger mode
```batch
flask --debug run
```
On running this command you should see below output
```batch
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 122-765-911
```
Congratulations! It means API is running successfully in your local system. Hit url - http://127.0.0.1:5000/ in your browser or Postman tool to get below JSON response -
```JSON
{
  "Game": "Tic Tac Toe", 
  "Status": "In Progress", 
  "Winner": null, 
  "GameBoardState": {
    "Box 1": null, 
    "Box 2": null, 
    "Box 3": null, 
    "Box 4": null, 
    "Box 5": null, 
    "Box 6": null, 
    "Box 7": null, 
    "Box 8": null, 
    "Box 9": null
    }
}
```
