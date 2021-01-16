# Generate Combined Ranklist

This script/app can be used to generate combined ranklist from various online judges. This might be useful to the competitive programming community who needs to arrange team forming contests and later combine them to form best teams possible.

This is a web application with a very basic user interface on the frontend made with **Bootstrap and JQuery**. Under the hood, it uses python's ASGI framework, **Quart** along with **Firebase**.

Live on [Heroku](https://rrii.herokuapp.com)

This webapp is currently in beta version. Needs a lot more improvement and bug fixes.

#### Currently Supported OJs
- Codeforces
- Atcoder
- VJudge

[Contribute](#contributing) to make other OJs available.

## Dependencies

- Quart
- Firebase's Admin SDK
- Google Spreadsheet
- Selenium with headless chrome

## Installation

To install, you need to clone/download this repository. To clone, write on your terminal,
```bash
$ git clone https://github.com/joynahid/combinedranklist.git
```
and change to the `combinedranklist` directory.
Make sure you've Python 3.7+ installed. If not, install or update it and then create a virtual environment by writing,
```bash
$ python3 -m venv env
$ source env/bin/activate
```

If you're in windows, activate virtual environment by,
```bash
$ .\env\Scripts\activate
```

Now install the requirements,
```bash
$ pip3 install requirements.txt
```
Before running the web app, please configure it properly.

To actually run the web app, you need to specify the path of `QUART_APP` to `main:app` in your environment variables.

Then following command will serve the app on your local machine.
```bash
$ quart run
```

## Configuration

You need to have accounts on VJudge and Atcoder as they do not provide API services. Configure it in your environment variables. You will get all environment variables in the `.env` file in the root dir of this repo.

Also you need firestore and storage credentials. You can find them in [firebase.com](https://firebase.com) by creating a new web project. Credentials are need to be written in environment variables.

To configure google spreadsheet, please see their [official documentation](https://developers.google.com/sheets/api)

To configure Selenium, referring to [Selenium's Installation](https://selenium-python.readthedocs.io/installation.html)

Again, all the configuration is about environment variables. You can check the `.env` file to know what you actually need to configure.

## Known Issues

Currently it uses a preset algorithm (Standard ICPC) to generate combined ranklist. Custom algorithm could make it more useful. That means the user will get access to the data and he/she will create him/her own algorithm to combine/merge ranklists.

Other issues are in [Github's Issue](https://github.com/joynahid/combinedranklist/issues)

## Getting Help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's [Issue Tracker](https://github.com/joynahid/combinedranklist/issues).

## Contributing

Contributions are always welcome and encouraged. Please send clean Pull Request, if you want to make it more useful. Here are some quick steps to do so.
- Fork it to get your own copy of this repo.
- Commit updates/ features/ bug fixes to your forked repo.
- Make Pull Request with proper title and description

See more details on **actually**  [contributing to a github repository](https://www.dataschool.io/how-to-contribute-on-github/)
