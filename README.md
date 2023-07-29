# CLI - ConfGen

CLI - ConfGen is a Python CLI tool created with the purpose of generating configuration files based off a 'golden-config'. It utilizes the Python Click library, YAML files, and Jinja2.

## Installation

    git pull blah blah


```bash
pip install requirements.txt
```

## Usage & Commands

```
cli-confgen
generate-config - Generate configuration file.
list-devices -  List all devices within a site.
list-sites - List sites or groups within a variable file.
list-variable-files - List available variable files.
```
Examples:

Help:
```bash
python cli-confgen.py --help
```

input (list-variable-files):
```bash
python cli-confgen.py list-variable-files
```
output (list-variable-files):
```bash
Current variable files in /variables:
east-hq.yaml
texas.yaml
california.yaml
```
input (list-sites):
```bash
python cli-confgen.py list-sites texas.yaml
```
output (list-sites):
```bash
dallas
waco
```
input (list-devices) - optional flag '--iv' to include variables in output:
```bash
python cli-confgen.py list-devices texas.yaml waco
```
output (list-devices):
```bash
txwac01sw01
txwac02sw01
```
input (generate-config):
```bash
python cli-confgen.py generate-config texas.yaml  waco txwac01sw01
```
output (generate-config):
```bash
Config file generated. Location: './configs/txwac01sw01.txt'
```

## YAML file structure
Each YAML file may represent a state, region, or building. 
Each file will include dictionaries of sites, devices within those sites, and variables for the devices. These files must be located in the 'variables' directory. For each device there are two required variables, 'golden_config' and 'config_file'. The 'golden_config' value should be the Jinja2 file name of the 'golden config'. The 'config_file' value should be whatever you want to name the generated config file. For the 'golden_config' value, don't include the '.j2' extension, it is assumed.

Example: texas.yaml
```yaml
dallas:
  txdal01sw01:
    golden_config: "2960-golden"
    config_file: "txdal01sw01.txt"
    default_gw: "10.8.1.1"
    hostname: "txdal01sw01"
    eth_1_1_ip: "10.8.1.15"
    eth_1_1_subnet_mask: "255.255.255.0"
  txdal02sw01:
    golden_config: "3011-golden"
    config_file: "txdal02sw01.txt"
    default_gw: "10.8.2.1"
    hostname: "txdal02sw01"
    eth_1_1_ip: "10.8.2.15"
    eth_1_1_subnet_mask: "255.255.255.0"
waco:
  txwac01sw01:
    golden_config: "2960-golden"
    config_file: "txwac01sw01.txt"
    default_gw: "10.8.3.1"
    hostname: "txwac01sw01"
    eth_1_1_ip: "10.8.3.15"
    eth_1_1_subnet_mask: "255.255.255.0"
  txwac02sw01:
    golden_config: "3011-golden"
    config_file: "txwac02sw01.txt"
    default_gw: "10.8.4.1"
    hostname: "txwac02sw01"
    eth_1_1_ip: "10.8.4.15"
    eth_1_1_subnet_mask: "255.255.255.0"
```

## Note on golden config file
Each 'golden-config' file should be created as a Jinja2 file - .j2 extension. These files should be located in the 'templates' directory. Each unique value that you want replaced should be surrounded by double brackets {{unique_value}}. These unique values should correspond to the variables under the devices using this template. 

Example: texas-field-2960.j2
```
interface ethernet 1/1
 ip address {{eth_1_1_ip}} {{eth_1_1_subnet_mask}}
 no shutdown
hostname {{hostname}}
ip default gateway {{default_gw}}
```

