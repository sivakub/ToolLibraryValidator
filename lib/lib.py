import json

msg_ = []


def msg(toPrint):
    msg_.append(str(toPrint))


def getMsg():
    return msg_


def clearMsg():
    msg_ = []


class Tool:
    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        self.jsonData = self.getJsonData()

    def getJsonData(self) -> object:
        try:
            with open(self.jsonFile, 'r') as f:
                return json.load(f)
        except:
            print("Failed to load the file")

    def isValidLib(self):
        if "data" in self.jsonData:
            return True
        else:
            return False

    def getData(self):
        return self.jsonData['data']

    def getNumberOfTools(self) -> int:
        return len(self.getData())

    def getToolData(self, num):
        return self.getData()[num]

    def getToolType(self, num):
        return self.getToolData(num)['type']

    def hasValidToolType(self, num):
        return True if self.getToolType(num) in fusionToolTypes() else False

    def hasValidUnit(self, num):
        unit = self.getToolData(num)['unit']
        if unit == "millimeters" or unit == "inches":
            return True
        return False

    def hasValidGrade(self, num):
        if "GRADE" in self.getToolData(num):
            grade = self.getToolData(num)['GRADE']
            return True if grade in vaildGrades() else False

    def hasValidBMC(self, num):
        bmc = self.getToolData(num)['BMC']
        return True if bmc in fusionBMCs() else False


    def getToolGeometry(self, num):
        if 'geometry' in self.getToolData(num):
            return self.getToolData(num)['geometry']
        else:
            msg("No Geometry Object Found")
            return False

    def hasValidGeometry(self, num):
        self.getToolData(num)
        reqPrams = millRequiredPrams().get(self.getToolType(num))
        reqDataType = []
        for i in self.getToolGeometry(num):
            if i in reqPrams:
                dataType = pramsType().get(type(self.getToolGeometry(num)[i]))
                if i not in dataType:
                    reqDataType.append(i)
                reqPrams.remove(i)

        if len(reqDataType) > 0:
            msg("")
            msg("{} Improper data type for geometry object item".format(len(reqDataType)))
            for k in reqDataType:
                msg("   Data Type is wrong for '{}'".format(k))

        if len(reqPrams) > 0:
            msg("")
            msg("{} Improper geometry data".format(len(reqPrams)))
            for key in reqPrams:
                msg("   geometry object should contain '{}'".format(key))

            return False

        else:
            return True

    def hasValidPostProcess(self, num):
        toolClassification = getToolClassification(self.getToolType(num))
        reqposts = []
        if toolClassification == "milling" or toolClassification == 'hole making':
            reqposts = fusionMillingPostProcess()
            for m in self.getToolData(num)['post-process']:
                reqposts.remove(m)

        if len(reqposts) > 0:
            msg("")
            msg("{} Improper post process data".format(len(reqposts)))
            for pst in reqposts:
                msg("   post process should contain '{}'".format(pst))

            return False
        else:
            return True


def fusionToolTypes():
    return [
        "face mill",
        "bull nose end mill",
        "ball end mill",
        "tapered mill",
        "radius mill",
        "chamfer mill",
        "lollipop mill",
        "slot mill",
        "thread mill",
        "boring bar",
        "counter bore",
        "center drill",
        "spot drill",
        "reamer",
        "counter sink",
        "tap left hand",
        "tap right hand",
        "dovetail mill",
        "flat end mill",
        "drill",
        "turning general",
        "turning boring",
        "turning grooving",
        "turning threading",
        "holder",
        "waterjet",
        "laser cutter",
        "plasma cutter",
        "probe",
        "electric arc wire",
        "laser powder",
        "laser wire"
    ]

def fusionBMCs():
    return [
        "unspecified",
        "hss",
        "ti coated",
        "carbide",
        "ceramics"
    ]


def vaildGrades():
    return {"Mill Generic", "generic"}


def fusionMillingPostProcess():
    return {"break-control", "comment", "diameter-offset", "length-offset", "live", "manual-tool-change", "number",
            "turret"}


def pramsType():
    return {
        int: {"DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "RE", "TA", "tip-diameter", "NT",
              "thread-profile-angle", "tip-length"},
        float: {"DC", "LB", "LCF", "OAL", "SFDM", "shoulder-length", "RE", "TA", "tip-diameter", "NT",
                "thread-profile-angle", "tip-length"},
        bool: {"CSP", "HAND"},
        str: {}

    }


def millRequiredPrams():
    return {
        "flat end mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND"},
        "ball end mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND"},
        "lollipop mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND"},
        "bull nose end mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "RE"},
        "slot mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "RE"},
        "face mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "RE", "TA"},
        "dovetail mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "RE", "TA"},
        "chamfer mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "TA",
                         "tip-diameter"},
        "thread mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "NT", "TP",
                        "thread-profile-angle"},
        "tapered mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "RE", "TA"},
        "radius mill": {"CSP", "DC", "LB", "LCF", "NOF", "OAL", "SFDM", "shoulder-length", "HAND", "RE", "tip-length"}
    }


def getToolClassification(tool):
    milling = ["face mill", "bull nose end mill", "ball end mill", "tapered mill", "radius mill", "chamfer mill",
               "lollipop mill", "dovetail mill", "slot mill", "thread mill", "flat end mill"]
    if tool in milling:
        return 'milling'
    holemaking = ["boring bar", "counter bore", "center drill", "spot drill", "reamer", "counter sink", "tap left hand",
                  "tap right hand", "drill"]
    if tool in holemaking:
        return 'hole making'

    turning = ["turning general", "turning boring", "turning grooving", "turning threading"]
    if tool in turning:
        return 'turning'

    cutting = []
    if tool in cutting:
        return 'cutting'

    if tool == "probe":
        return 'probe'

    if tool == "holder":
        return 'holder'

    deposition = ["electric arc wire", "laser powder", "laser wire"]
    if tool in deposition:
        return 'deposition'

    return 'unspecified'
