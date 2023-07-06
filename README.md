# zabbix-template-update
Python script to update Zabbix templates


## Usage
- Copy config.sample.ini to config.ini
- Edit config.ini and input configuration values
- Copy templates or folders of templates to templates/ or any other specified template folder in the config
- Run script

You can get the default Zabbix templates from Zabbix git repo found [here](https://git.zabbix.com).


## Configuration
### Server
| Name    | Required                                   | Default                   | Description                          |
| --------| ------------------------------------------ | ------------------------- | ------------------------------------ |
| hostname| **Yes**                                    | https://your.hostname.tld | Hostname to use to connect to Zabbix |
| username| **Yes** (if not using api token)           | username                  | Username used to connect to Zabbix   |
| password| **Yes** (if not using api token)           | password                  | Password used to connect to Zabbix   |
| apitoken| **Yes** (if not using username & password) | apitoken                  | API token used to connect to Zabbix  |

### Templates
| Name    | Required | Default    | Description                                                                     |
| --------| -------- | ---------- | ------------------------------------------------------------------------------- |
|path     | No       | templates/ | Path used to read templates. If not specified, path where script is run is used |
|recursive| No       | False      | Recurse through folders looking for *.xml, *.json or *.yaml files               |
  

### Rules
| Name           | Required | Default | Description |
| -------------- | -------- | ------- | ----------- |
| createMissing  | No       | True    | -           |
| updateExisting | No       | True    | -           |
| deleteMissing  | No       | False   | -           |  

Settings for global rules. If any option is set to True, all possible settings will be true  

createMissing: `discoveryRules, graphs, host_groups, template_groups, hosts, httptests, images, items, maps, mediaTypes, templateLinkage, templates, templateDashboards, triggers, valueMaps`  
updateExisting: `discoveryRules, graphs, host_groups, template_groups, hosts, httptests, images, items, maps, mediaTypes, templates, templateDashboards, triggers, valueMaps`  
deleteMissing: `discoveryRules, graphs, httptests, items, templateLinkage, templateDashboards, triggers, valueMaps`  
  
See [Zabbix API Docs](https://www.zabbix.com/documentation/current/en/manual/api/reference/configuration/import) for more information

