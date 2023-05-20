# Weggo Community. V1.0 Beta.

The purpose of this project is to create a new version of the existing platform. A version totally focused on user experience, with a very defined branding.
The pre-existing code has been reduced in order to focus, in this second version, on one main service: the supply and demand of camper vehicles.

# LET TO MODIFY
## Ways to work with the code

1. Perform the relevant configuration on your computer:

    - git init
    - git config --global user.name "YOUR_USER"
    - git config --global user.email "YOUR_EMAIL"
    - git remote add origin https://github.com/Weggosp/Develop.git

2. Download the code and manage it locally

    - git pull origin <branch>

3. Create a branch to work on it. Communicate with the team to know the changes in other branches.

    - git branch -M "NEW_BRANCH"
    - If all is ok: git push -u origin NEW_BRANCH

4. Communicate changes and code uploading for review.

### Prerequisites

You will need the following to work:

```
Visual Studio Code (or similar), Python > 2.7, Sass and have installed the dependencies described in the file requirements.txt
```
## Start application

1. Install dependencies

	`pip install -r requirements.txt`

2. Run application

	* On Windows

		`python application.py`

	* On Linux / macOS

		`python3 application.py`

_Note: It's recommended to work on isolated environment when you work with Python's apps to avoid problems with other global dependencies. You can use this [simple guide](#enable-a-virtual-environment-on-python) to configure your virtual environment._


### Enable a virtual environment on Python

#### On Windows

1. Create virtual environment

	`python -m venv .venv`

2. Activate environment

    `.\.venv\Scripts\activate.ps1`

#### On Linux / macOS

1. Create virtual environment

	`python3 -m venv .venv`

2. Activate environment

	`. ./.venv/bin/activate`

Once you have activated your virtual environment, you'll see __`(.venv)`__ in your command prompt. While your virtual environment it's activated, you can install dependencies and start the application in isolated way.

[More info about virtual environments](https://docs.python.org/3/library/venv.html)

### Configure Sass Compile

The css compiled files should be place on `/static/css`.

If you are using 'Live Sass Compiler' extension for VS Code, edit your settings.json 

> VS Code User Settings -> Extensions -> Live Sass Compile Config -> edit in settings.json

and paste the next:

```
"liveSassCompile.settings.formats": [
        {
            "format": "expanded",
            "extensionName": ".css",
            "savePath": "~/../css/"
        }
    ]
```

## Built with

* [Python 2.7](https://www.python.org//) - The programming language used
* Flask 1.1.2 Framework
* VIPER - Design Pattern
* External libraries were used in this project

## Main implementation

* Stripe payment gateway

## Authors

* **Weggo España** - [weggo.es](https://weggo.es)

See also the list of [contributors](https://github.com/Weggosp/Develop/contributors) who participated in this project. All contributors belong to the Weggo development team.

## License

This is a private business project, closed to any public outside the company and, specifically, to the technological development area. Any inappropriate or unauthorized use without the consent of the company's management will be considered illegal and against all the rules of this company. - All rights of this project and its authorship are held by Weggo España S.L.
