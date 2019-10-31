# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 20:07:32 2019

@author: Vassili Privalihhin
"""

from re import compile

def hex_to_rgb(hexColor):
    colors = []
    for i in range(1, len(hexColor), 2):
        colors.append(int(hexColor[i:i + 2], 16))
    return colors

def rgb_to_cmyk(rgb):
    cmyk = []
    # calculates rgb divided lights for subsequent calculations
    dividedLights = []
    for light in rgb:
        dividedLights.append(light / 255)
    
    # calculates 'k' for 'cmyk'
    k = 1 - max(dividedLights)

    # calculates 'c', 'm' and 'y'
    for light in dividedLights:
        try:
            element = 100 * (1 - light - k) / (1 - k)
        except ZeroDivisionError:
            print("I can't convert rgb to cmyk because of zeros")
            return None
        cmyk.append(round(element))
    
    # adds 'k' as the last element of 'cmyk'
    # ! All elements of cmyk should be multiplied by 100 (cmyk scale) and rounded !
    cmyk.append(round(k * 100))
    return cmyk

color = input("Enter input color: ")
HEX_COLOR_RE = compile(r'^#[a-fA-F0-9]{6}$') # regular expression which will be used to check if the input above is correct
# checks whether entered color matches the 'rules' of regular expression or not
if HEX_COLOR_RE.match(color) is None:
    print('Oops, “{}” is not a valid color code'.format(color))
else:
    rgbColor = hex_to_rgb(color)
    cmyk = rgb_to_cmyk(rgbColor)
    
    # just prints the representations of the hexademical color with formatting
    print('"{}" = rgb({},{},{})'.format(color, rgbColor[0], rgbColor[1], rgbColor[2]))
    if not cmyk is None: 
        print('"{}" = cmyk({},{},{},{})'.format(color, cmyk[0], cmyk[1], cmyk[2], cmyk[3]))