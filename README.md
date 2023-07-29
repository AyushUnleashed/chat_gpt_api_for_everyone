# ChatGPT api for everyone

* Modified code from unofficial chatgpt to make it work with latest ui
* It uses playwright and chromium to open browser and parse html.
* It is an unoffical api for development purpose only.


# How to install

* Make sure that python and virual environment is installed.

* Create a new virtual environment

```python
For Linux:

# one time
virtualenv -p $(which python3) env

# everytime you want to run the server
source env/bin/activate
```

```python
For Windows:

# one time
python -m venv env

# everytime you want to run the server
env/Scripts/activate
```

* If you get error for windows while activating environment:
```shell
if you get error:
    cannot be loaded because running scripts is disabled on this system.
    
    Solution:
1. Type Powershell and hit Enter. This will open the PowerShell interface.
2. Now, to change the Execution Policy, type Set-ExecutionPolicy RemoteSigned -Scope CurrentUser and hit Enter. This will allow scripts downloaded from the internet which are signed by a trusted publisher to be run.
3. PowerShell will ask for your confirmation. Type Y and hit Enter to confirm the policy change.
4. Try running your script again after this. It should work if the error was related to execution policy.
```

* Now install the requirements

```
pip install -r requirements.txt
```

* If you are installing playwright for the first time, it will ask you to run this command for one time only.

```
playwright install
```

* Now run the server, login with details, press enter on terminal.

```
python server.py
```

* once your login details is cached locally, you can change headless=True, to run it in headlesss mode.

* The server runs at port `5001`. If you want to change, you can change it in server.py


# Api Documentation

* There is a single end point only which is working right now. It is available at `/chat`

```shell
For Windows (Powershell), the command will be:

Invoke-RestMethod -Uri "http://localhost:5001/chat" -Method Post -Body '{"message":"Hello GPT"}' -ContentType 'application/json'
```
```shell
For Linux, the command will be:

curl -X POST -H "Content-Type: application/json" -d '{"message":"Hello GPT"}' "http://localhost:5001/chat"
```


# Credit

* I modified script to work with latest Openai UI & windows, added documentation for running on windows, originally from [Daniel Gross's whatsapp gpt](https://github.com/danielgross/whatsapp-gpt) package which was documented by [Taranjeet ](https://github.com/taranjeet/unofficial-chatgpt-api/) for easy use.

# Disclaimer

Please note that this project is a personal undertaking and not an official OpenAI product. It is not affiliated with OpenAI in any way, and should not be mistaken as such.
