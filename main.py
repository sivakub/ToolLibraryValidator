import os
import lib.lib as lib
import argparse

# Press the green button in the gutter to run the script.

parser = argparse.ArgumentParser(description='Merge posts utility')
parser.add_argument('--file', type=str, help='Tool library file to check.')
args = parser.parse_args()

file_ = args.file
print("")
if os.path.isfile(file_):
    tool = lib.Tool(file_)

    if tool.isValidLib():
        print("The file contains {} tool's'".format(tool.getNumberOfTools()))
        print("")
        for toolItem in range(tool.getNumberOfTools()):
            if not tool.hasValidToolType(toolItem):
                lib.msg("Tool type is not valid must be one of " + (
                    str(lib.fusionToolTypes()).replace('[', '').replace(']', '')))

            if not tool.hasValidUnit(toolItem):
                lib.msg("Unit should be either 'millimeters' or 'inches'")

            tool.hasValidBMC(toolItem)

            # Grade is not used anymore
            # if not tool.hasValidGrade(toolItem):
            #     lib.msg("GRADE should be must be one of " + (str(lib.vaildGrades()).replace('[', '').replace(']', '')))

            tool.hasValidGeometry(toolItem)

            tool.hasValidPostProcess(toolItem)

            if len(lib.getMsg()) > 0:
                print("Tool {} has following issues:".format(toolItem + 1))
                for j in lib.getMsg():
                    print(j)
                lib.clearMsg()
                print("")
            else:
                print("Tool {} is a Valid Tool".format(toolItem + 1))
    else:
        print("File is not a valid tool library 'data' object not found")

else:
    print("File Name is not valid")
