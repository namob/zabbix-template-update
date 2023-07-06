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

print(rules)

createMissing = True
updateExisting = False
deleteMissing = False

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

print(rules)
