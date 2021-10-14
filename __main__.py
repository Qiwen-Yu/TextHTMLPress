"""
python -m entry point to run via python -m
"""
import click
from pathlib import Path
from generator import Generator
# fix issue 7
import sys
#issue 8
import json;

DEFAULT_FILE = '.txt'
# fix issue 6
DEFAULT_LANG = 'en-CA'
# current working directory, a path object
cwd = Path.cwd()
# ADD a relative path
DEFAULT_OUTPUT = cwd / 'dist'


@click.command()
@click.help_option('-h', '--help')
@click.version_option('0.1', '-v', '--version')
@click.option('-i', '--input', 'inp', required=False, type=click.Path(exists=True, file_okay=True, dir_okay=True,
                                                                     readable=True, resolve_path=True,
                                                                     path_type=Path),
              help='Path to an input file/folder')
@click.option('-o', '--output', required=False, default=DEFAULT_OUTPUT, type=click.Path(exists=False,
                                                                                        file_okay=False, dir_okay=True,
                                                                                        readable=True, writable=True,
                                                                                        resolve_path=True,
                                                                                        path_type=Path),
              help='Path to an folder contains all output files')
@click.option('-s', '--stylesheet', required=False, default='', help='URL of a CSS stylesheet')
# fix issue 6
@click.option('-l', '--lang', required=False, default=DEFAULT_LANG, help='Indicates the lang attribute on root html')
@click.option('-c', '--config', 'config_' , required= False,  type=click.Path(exists=True, file_okay=True, dir_okay=True,
                                                                     readable=True, resolve_path=True,
                                                                     path_type=Path),
              help='Path to a config file/folder')
def main(inp: Path, output: Path, stylesheet: str, lang: str , config_:Path) -> None:
    if config_!=None and config_.exists():
        # work with json file
        try:
         with open(config_, "r") as read_file:
          data = json.load(read_file)
        except:
          click.echo("The config file has error")
          sys.exit(1)
        if('input' in data ):
         input= Path(data['input'])
         if 'output' in data:
             output= Path(data['output'])
         else:
             output= DEFAULT_OUTPUT
         if 'stylesheet' in data:
             stylesheet= data['stylesheet']
         else:
             stylesheet= ''
         if 'lang' in data:
             lang= data['lang']
         else:
             lang= DEFAULT_LANG
         #create an instance of Generator
         g= Generator(input, output, stylesheet, lang)
         g.generator_wrapper()
        else:
         click.echo(f"The input file/folder {inp} or config file does not exist.")
         sys.exit(1)
    elif inp !=None and inp.exists():
        # create an instance of the Generator
        g = Generator(inp, output, stylesheet, lang)
        # TODO: or make generator_wrapper() a function, not a method
        g.generator_wrapper()
    else:
        # f string, format string python3
        click.echo(f"The input file/folder {inp} or config file does not exist.")
        
        # fix issue 7
        sys.exit(1)


if __name__ == '__main__':
    main()
