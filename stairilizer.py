# this script cleans up step files in the working dir with the following actions:
#   rename objects and file info
#   perform brute force replacement of values that contain floating point errors
#   perform range replacement of same (planned)
#   remove unused lines (planned)
#   condense duplicate lines such as points and vectors (planned)
#   sort lines (started)


import os


def SplitSTEP(oldstring):
    char = ';'  # set this to whatever character indicates the end of a line
    newstring = oldstring.replace('\n', ' ')  # replace all newlines with space
    newstring = newstring.replace('\r', ' ')  # replace all carriage returns with space
    newlist = newstring.split(char)  # split into list based on char
    strippedlist = []
    for s in newlist:
        strippedlist.append(s.strip())
    return ';\n'.join(strippedlist)  # return list joined back into string
# End Function


def FixFloatingPoint(oldstring):
    newstring = oldstring
    fix = {
        """'Administrator'""":               """''""",
        """'Managed by Terraform'""":        """''""",
        """'SolidWorks 2017'""":             """''""",
        """'SwSTEP 2.0'""":                  """''""",
        '95836A524_NO THREADS_Black-Oxide 18-8 Stainless Steel Pan Head Phillips Screws': 'Screw',
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
# End Function


def SortSTEP(oldstring):
    newlist = oldstring.split('\n')  # split into list
    header = []
    first = [  # list of items to be output first
        ['APPLICATION_PROTOCOL_DEFINITION',[]],
        ['APPLICATION_CONTEXT',[]],
        ['DESIGN_CONTEXT',[]],
        ['MECHANICAL_CONTEXT',[]],
        ['ADVANCED_BREP_SHAPE_REPRESENTATION',[]],
        ['MANIFOLD_SOLID_BREP',[]],
        ['CLOSED_SHELL',[]],
        ['ADVANCED_FACE',[]],
        ['FACE_OUTER_BOUND',[]],
        ['EDGE_LOOP',[]],
        ['ORIENTED_EDGE',[]],
        ['EDGE_CURVE',[]],
        ['VERTEX_POINT',[]],
        ['CARTESIAN_POINT',[]],
        ['DIRECTION',[]],
        # garbage:
        ['CC_DESIGN_DATE_AND_TIME_ASSIGNMENT',[]],
        ['CC_DESIGN_PERSON_AND_ORGANIZATION_ASSIGNMENT',[]],
        ['CC_DESIGN_SECURITY_CLASSIFICATION',[]],
        ['CALENDAR_DATE',[]],
        ['DATE_TIME_ROLE',[]],
        ['DATE_AND_TIME',[]],
        ['LOCAL_TIME',[]],
        ['PERSON_AND_ORGANIZATION',[]],
        ['PERSON',[]],
        ['ORGANIZATION',[]],
        ['SECURITY_CLASSIFICATION_LEVEL',[]],
        ['SECURITY_CLASSIFICATION',[]],
        ['PRODUCT_RELATED_PRODUCT_CATEGORY',[]],
        ['PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE',[]],
        ['PRODUCT_DEFINITION_SHAPE',[]],
        ['PRODUCT_DEFINITION',[]],
        ['PRODUCT',[]],
        ]
    lines = []
    foundpound = False
    for line in newlist:
        found_first = False  # line is not first by default
        for i in range(len(first)):  # iterate over indices in first
            if first[i][0] in line and found_first == False:  # if keyword is in line, skip if match already found
                first[i][1].append(line)  # add line to that keyword's list
                found_first = True
        if found_first:
            pass  # line already added elsewhere
        elif line.startswith('#') or foundpound == True:
            lines.append(line)
            foundpound = True
        else:
            header.append(line)
    for linelist in first:  # iterate over first again
        header = header + linelist[1]  # add list portion
    return '\n'.join(header + [] + lines)  # return list joined back into string
# End Function


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
# End Function


# --- Start of script ---
# pass list of extensions, keyword to modify filenames, and list of functions to manipulate file contents
AnalyzeFiles(['.STEP', '.STP', '.step', '.stp'], 'strl', [SplitSTEP, FixFloatingPoint, SortSTEP])

# print()
# os.system('PAUSE')

#EOF
