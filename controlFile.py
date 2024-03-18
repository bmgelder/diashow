import json5


def openCreateControlFile(path):
    try:
        with open(path, "r") as jsonFile:
            controlData = json5.loads(
                jsonFile.read().replace("data = ", "").replace(";", ""))
    except ValueError as e:
        print(f'Error decoding JSON: {e}')
    except FileNotFoundError as e:
        controlData = {"fileList": []}
        with open(path, "x") as jsonFile:
            jsonFile.write(
                "data = " + json5.dumps(controlData, indent=2) + ";")
    return controlData


def saveControlFile(path, controlData):
    with open(path, "w") as jsonFile:
        jsonFile.write(
            "data = " + json5.dumps(controlData, indent=2) + ";")
    return controlData
