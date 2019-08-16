"""
This module is used for naming convention stuff.
"""


GROUP = "grp"
BLENDCOLORS = "bcn"
JOINT = "jnt"
NULL = "nul"
CONTROL = "ctrl"
GUIDE = "guide"
DECOMPOSEMATRIX = "dcm"
VECTORPRODUCT = "vpn"
BIND = "bind"
IK = "ik"
FK = "fk"
HANDLE = "hdl"
REVERSE = "rvr"

# sides
LEFT = "l"
RIGHT = "r"
CENTER = "c"


# locations


# Color
LIGHTGREY = 0
BLUE = 6
DARKRED = 12
RED = 13
WHITE = 16
YELLOW = 17

SIDES = {"left" : LEFT, "right": RIGHT, "center": CENTER}

SIDECOLOR = {LEFT:BLUE,RIGHT:RED,CENTER:YELLOW}

# location, number
NAMETEMPLATE = "side:location:description:number:type"
DELIMITER = "_"

def getSide(name):
    """
    """

    nameTemplateSplit = NAMETEMPLATE.split(":")
    nameSplit = name.split(DELIMITER)

    side = nameSplit[nameTemplateSplit.index("side")]

    if side in SIDES.values():
        return side


