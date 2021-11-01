# TextHTMLPress
A command-line static site generator to generate a complete 
HTML website from raw data and files (txt files or MarkDown files).

## Features

- [x] Name: TextHTMLPress
- [x] [Github Repo](https://github.com/Qiwen-Yu/TextHTMLPress)
- [x] [MIT License](https://github.com/Qiwen-Yu/TextHTMLPress/blob/main/LICENSE)
- [x] README.md
- [x] requirements.txt
- [x] title of .html file
- [x] customized output destination
- [x] CSS stylesheet
- [x] customized option from config file 

## Dependencies
This tool is written by `Python 3.9`, with `pip 21.1.2`.

Check the `requirements.txt`.


## How To Use
1. Download the code ([the TextHTMLPress folder](https://github.com/Qiwen-Yu/TextHTMLPress))
2. Using a command line tool (CLI) such as `Windows cmd`, `git bash`, 
   `Unix shell` or `MaxOS Terminal`.
3. In the CLI:

```shell
# install requirements
pip install -r requirements.txt
# redirect into the package folder
cd ~/yourpath/TextHTMLPress

# check help
# it might be python3 __main__.py --help on your machine
# python3 instead of python

python __main__.py --help
# generate .html from a .txt file
python __main__.py -i ./tests/Silver\ Blaze.txt
# generate .html files from a folder 
python __main__.py -i ./tests/
# use multiple options
python __main__.py -i ./tests/Silver\ Blaze.txt -s https://cdn.jsdelivr.net/npm/water.css@2/out/water.css
# use config file
# or python __main__.py -c config.yml
# 
python __main__.py --config config.yml
# specify the lang attribute in root element of HTML, default en-CA
python __main__.py -i ./tests/ -l fr

```
## Example Output

Please find [here](https://github.com/Qiwen-Yu/TextHTMLPress/tree/main/Example_Output).

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

