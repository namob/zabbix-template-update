from pyzabbix import ZabbixAPI, ZabbixAPIException
import os
import codecs
import sys
import configparser
from glob import glob


def print_log(log):
    from datetime import datetime

    curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{curtime}] - {log}")


config = configparser.ConfigParser()
config.read("config.ini")

# Validate all fields in config
if (
    (
        (all(key in config["server"] for key in ("username", "password", "hostname")))
        or (key in config["server"] for key in ("apitoken", "hostname"))
    )
    and (all(key in config["templates"] for key in ("recursive",)))
    and (
        all(
            key in config["rules"]
            for key in ("createMissing", "updateExisting", "deleteMissing")
        )
    )
):
    print_log("All config values present")
else:
    print_log("Missing config values. Check config.sample.ini")

username = config["server"]["username"]
password = config["server"]["password"]
hostname = config["server"]["hostname"]
apitoken = config["server"]["apitoken"]
path = config["templates"]["path"]
recursive = config["templates"].getboolean("recursive")
createMissing = config["rules"].getboolean("createMissing")
updateExisting = config["rules"].getboolean("updateExisting")
deleteMissing = config["rules"].getboolean("deleteMissing")

# Validation
if not hostname:
    print_log(f"Hostname must be set")
    sys.exit()
if username and password:
    try:
        zapi = ZabbixAPI(hostname)
        zapi.login(username, password)
    except:
        print_log(f"Unable to connect to {hostname} with username and password")
elif apitoken and (apitoken != "" or apitoken == "apitoken"):
    try:
        zapi = ZabbixAPI(hostname)
        zapi.login(api_token=apitoken)
    except:
        print_log(f"Unable to connect to {hostname} with apitoken")
else:
    print_log(f"Username and password or apitoken must be set")
    sys.exit()

if path == "":
    path = os.getcwd() + "/"
else:
    path = os.getcwd() + "/" + path
print_log("Connected to Zabbix API Version %s" % zapi.api_version())


from pyzabbix import ZabbixAPI, ZabbixAPIException

rules = {
    "discoveryRules": {
        "createMissing": True,
        "updateExisting": True,
        "deleteMissing": True,
    },
    "graphs": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
    "host_groups": {"createMissing": True, "updateExisting": True},
    "template_groups": {"createMissing": True, "updateExisting": True},
    "hosts": {"createMissing": True, "updateExisting": True},
    "httptests": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
    "images": {"createMissing": True, "updateExisting": True},
    "items": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
    "maps": {"createMissing": True, "updateExisting": True},
    "mediaTypes": {"createMissing": True, "updateExisting": True},
    "templateLinkage": {
        "createMissing": True,
        "deleteMissing": True,
    },
    "templates": {"createMissing": True, "updateExisting": True},
    "templateDashboards": {
        "createMissing": True,
        "updateExisting": True,
        "deleteMissing": True,
    },
    "triggers": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
    "valueMaps": {"createMissing": True, "updateExisting": True},
}

for rule in rules:
    crule = rules[rule]
    if "deleteMissing" in crule:
        if not deleteMissing and crule["deleteMissing"]:
            crule["deleteMissing"] = False
    elif "updateExisting" in crule:
        if not updateExisting and crule["updateExisting"]:
            crule["updateExisting"] = False
    elif "createMissing" in crule:
        if not createMissing and crule["createMissing"]:
            crule["createMissing"] = False

print_log(
    f"Rules created with global config: createMissing: {createMissing}, updateExisting: {updateExisting}, deleteMissing: {deleteMissing}"
)

if os.path.isdir(path):
    if recursive:
        files = glob(path + "**/*.xml", recursive=True)
        files += glob(path + "**/*.yaml", recursive=True)
        files += glob(path + "**/*.json", recursive=True)
    else:
        files = glob(path + "*.xml")
        files += glob(path + "*.yaml")
        files += glob(path + "*.json")

    for file in files:
        print_log(f"Importing {file}")
        ext = file.split(".")[-1].lower()
        if ext == "xml" or ext == "json" or ext == "yaml":
            with codecs.open(file, encoding="utf-8") as f:
                template = f.read()
                try:
                    zapi.configuration["import"](
                        format=ext, source=template, rules=rules
                    )
                    print_log(f"Successfully imported {file}")
                except ZabbixAPIException as e:
                    print_log(f"Error importing {file}. Error:")
                    print_log(e)
        else:
            print_log(
                f"Unable to import {file}. Invalid extension {ext}. Allowed extensions: xml, json, yaml"
            )
            continue

else:
    print(f"No templates found in {path}")
