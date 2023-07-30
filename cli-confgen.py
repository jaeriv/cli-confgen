import click
from modules import get_current_var_files, file_exists, CURRENT_DIR
from pprint import pprint
import yaml
from jinja2 import Environment, FileSystemLoader


variable_file_argument = click.argument("variable_file", nargs=1)
site_argument = click.argument("site_name", nargs=1)
device_argument = click.argument("device", nargs=1)

# To-do
# Setup logging and log under except statements and add command to view logs.

@click.group()
def cli():
    """
    \b
****************************************************************************
 ##   #     ###                      ##                 #    ##               
#  #  #      #                      #  #               # #  #  #              
#     #      #                      #      ##   ###    #    #      ##   ###   
#     #      #          ####        #     #  #  #  #  ###   # ##  # ##  #  #  
#  #  #      #                      #  #  #  #  #  #   #    #  #  ##    #  #  
 ##   ####  ###                      ##    ##   #  #   #     ###   ##   #  #  
****************************************************************************                                                                                  
    """
    pass

@cli.command()
def list_variable_files():
    """List available variable files."""
    try:
        click.echo("")
        click.echo("Current variable files in /variables:")
        for file in get_current_var_files():
            click.echo(file)
        click.echo("")
    except FileNotFoundError as error:
        return click.echo("The 'variables' directory is missing.")
@cli.command()
@variable_file_argument
def list_sites(variable_file):
    """List sites or groups within a variable file."""
    if not file_exists(file=f"{CURRENT_DIR}/variables/{variable_file}"): 
        return click.echo(f"Variable file '{variable_file}' not found, please create a YAML variable file in 'variables' directory.")
    try:
        with open(f"{CURRENT_DIR}/variables/{variable_file}", "r") as f:
            data = yaml.safe_load(f)
            for key, value in data.items():
                click.echo(key)
    except AttributeError as error:
        return click.echo(f"The file '{variable_file}' is either empty, not formatted correctly, or not a YAML file.")

@cli.command()
@variable_file_argument
@site_argument
@click.option("--iv", is_flag=True, show_default=True, default=False, help="Include variables for each site.")
def list_devices(variable_file, site_name, iv):
    """List all devices within a site."""
    if not file_exists(file=f"{CURRENT_DIR}/variables/{variable_file}"): 
        return click.echo(f"Variable file '{variable_file}' not found, please create a YAML variable file in 'variables' directory.")
    try:
        with open(f"{CURRENT_DIR}/variables/{variable_file}", "r") as f:
            data = yaml.safe_load(f)
            if iv:
                for device in data[site_name].items():
                    if None in device:
                        click.echo(f"WARNING: {device[0]} has no variables set.")
                    else:
                        pprint(device)
            else:
                for key,value in data[site_name].items():
                    click.echo(key)
    except AttributeError as error: 
        return click.echo(f"The site/group '{site_name}' is either empty or not formated correctly.")
    except TypeError as error:
        return click.echo(f"The file '{variable_file}' is either empty, not formatted correctly, or not a YAML file.")
    except KeyError as error:
        return click.echo(f"The site '{site_name}' does not exist in file.")

@cli.command()
@variable_file_argument
@site_argument
@device_argument
def generate_config(variable_file, site_name, device):
    """Generate configuration file by specifying variable file, site/group, and device."""
    if not file_exists(file=f"{CURRENT_DIR}/variables/{variable_file}"): 
        return click.echo(f"Variable file '{variable_file}' not found, please create a YAML variable file in 'variables' directory.")
    try:
        with open(f"{CURRENT_DIR}/variables/{variable_file}", "r") as f:
            data = yaml.safe_load(f)
            try:
                config_file_name = data[site_name][device]["config_file"]
                if config_file_name == "" or config_file_name == None:
                    return click.echo(f"The value for 'config_file' is empty.")
            except KeyError as error:
                if "config_file" in error.args:
                    return click.echo(f"The variable 'config_file' is not defined or set.")
                elif device in error.args:
                    print(error.args)
                    return click.echo(f"The device '{device}' does not exist in {variable_file}.")
                elif site_name in error.args:
                    return click.echo(f"The site/group '{site_name}' does not exist in {variable_file}.")
            try:
                golden_config = data[site_name][device]["golden_config"]
                if golden_config == "" or golden_config == None:
                    return click.echo(f"The value for 'golden_config' is empty.")
                if not file_exists(file=f"{CURRENT_DIR}/templates/{golden_config}.j2"):
                    return click.echo(f"The file {golden_config}.j2 does not exist. Create a Jinja2 golden template file within the 'templates' directory.")
            except KeyError as error:
                if "golden_config" in error.args:
                    return click.echo(f"The variable 'golden_config' is not defined or set.")
        # GENERATE CONFIG FILE
        template_loader = FileSystemLoader("templates")
        env = Environment(loader=template_loader)
        template = env.get_template(f"{golden_config}.j2")
        new_file = template.render(data[site_name][device])
        with open(f"{CURRENT_DIR}/configs/{config_file_name}", "w+") as f:
            f.write(new_file)
        click.echo(f"Config file generated. Location: './configs/{config_file_name}'")          
    except TypeError as error:
        return click.echo(f"The file '{variable_file}' is either empty, not formatted correctly, missing required variables, or not a YAML file.")


if __name__ == "__main__":
    cli()