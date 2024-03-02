# this script cleans up step files in the working dir with the following actions:

# rename objects and file info
# perform brute force replacement of values that contain floating point errors
# perform range replacement of same (planned)
# remove unused lines (planned)
# condense duplicate lines such as points and vectors (planned)
# sort lines (planned)
#   look for ADVANCED_BREP_SHAPE_REPRESENTATION, may be multi-line

# output = (strl).step

import os


def FixFloatingPoint(oldstring):
    newstring = oldstring
    fix = {
        """'Administrator'""":               """''""",
        """'Managed by Terraform'""":        """''""",
        """'SolidWorks 2017'""":             """''""",
        """'SwSTEP 2.0'""":                  """''""",
    }
    numberpairs = [
        ['1.000000000000000000',    '1.0'    ],
        ['1.0000000000000000000',   '1.0'    ],
        ['0.000000000000000000',    '0.0'    ],
        ['0.0000000000000000000',   '0.0'    ],
        ['1000.000000000000000',    '1000.0' ],
    ]
    for numberpair in numberpairs:
        fix[numberpair[0]+','] = numberpair[1]+','
        fix[numberpair[0]+' '] = numberpair[1]+' '
        fix[numberpair[0]+')'] = numberpair[1]+')'
    # print(fix)
    for k in fix:
        newstring = newstring.replace(k, fix[k])
    return newstring
# End FixFloatingPoint


def AnalyzeFiles(exts, suffix, funcs):
    formatted_suffix = ' (' + suffix + ')'  # add space and parentheses
    filelist = []  # start with empty list
    for f in os.listdir():  # get all files
        for ext in exts:
            if f.endswith(ext):
                length = len(ext)
                if f[:-length].endswith(formatted_suffix):
                    pass  # skip this file since it's an output of this converter
                else:
                    filelist.append([f, f[:-length] + formatted_suffix + ext])
    # print(filelist)
    for fpair in filelist:
        oldname = fpair[0]
        newname = fpair[1]
        with open(oldname, 'r') as oldfile:
            oldstring = oldfile.read()
            newstring = oldstring
            for func in funcs:
                newstring = func(newstring)
            with open(newname, 'w') as newfile:
                newfile.write(newstring)
# End AnalyzeFiles


# --- Start of script ---

AnalyzeFiles(['.STEP', '.STP', '.step', '.stp'], 'strl', [FixFloatingPoint,])

print()
# os.system('PAUSE')

#EOF