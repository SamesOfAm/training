# new test

import json
import io
import re
from xdtools import XDFile

def parse_name(child, placeOfNextDot, subKey):
    if child.name[:4] == "$T$ ":
        noBreakHyphens = re.sub(r"-\n", "", child.raw_text)
        if noBreakHyphens != child.raw_text:
            print "!!! Attention !!! Is this correct? " + noBreakHyphens
        formattedText = re.sub(r"\n", " ", noBreakHyphens)
        firstKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
        placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
        if firstKey in database and firstKey != "":
            secondKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
            if secondKey in database[firstKey] and secondKey != "":
                placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                thirdKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                if thirdKey in database[firstKey][secondKey] and thirdKey != "":
                    placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                    fourthKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                    if fourthKey in database[firstKey][secondKey][thirdKey] and fourthKey != "":
                        placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                        fifthKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                        database[firstKey][secondKey][thirdKey][fourthKey][fifthKey] = formattedText
                        print "Added to translations: " + formattedText
                    elif fourthKey != "" and fourthKey != None:
                        placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                        fifthKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                        if fifthKey != None and fifthKey != "":
                            database[firstKey][secondKey][thirdKey][fourthKey] = {fifthKey: formattedText}
                            print "Added to translations: " + formattedText
                        else:
                            database[firstKey][secondKey][thirdKey][fourthKey] = formattedText
                            print "Added to translations: " + formattedText
                    else:
                        database[firstKey][secondKey][thirdKey] = formattedText
                        print "Added to translations: " + formattedText
                elif thirdKey != "" and thirdKey != None:
                    placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                    fourthKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                    if fourthKey != None and fourthKey != "":
                        placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                        fifthKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                        if fifthKey != None and fifthKey != "":
                            database[firstKey][secondKey][thirdKey] = {fourthKey: {fifthKey: formattedText}}
                            print "Added to translations: " + formattedText
                        else:
                            database[firstKey][secondKey][thirdKey] = {fourthKey: formattedText}
                            print "Added to translations: " + formattedText
                    else:
                        database[firstKey][secondKey][thirdKey] = formattedText
                        print "Added to translations: " + formattedText
                else:
                    database[firstKey][secondKey] = formattedText
                    print "Added to translations: " + formattedText
            elif secondKey != "" and secondKey != None:
                placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                thirdKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                if thirdKey != None and thirdKey != "":
                    placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                    fourthKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                    if fourthKey != None and fourthKey != "":
                        placeOfNextDot = child.name.find('.', placeOfNextDot) + 1
                        fifthKey = child.name[placeOfNextDot:child.name.find(".", placeOfNextDot)]
                        if fifthKey != None and fifthKey != "":
                            database[firstKey][secondKey] = {thirdKey: {fourthKey: {fifthKey: formattedText}}}
                            print "Added to translations: " + formattedText    
                        else:
                            database[firstKey][secondKey] = {thirdKey: {fourthKey: formattedText}}
                            print "Added to translations: " + formattedText
                    else:
                        database[firstKey][secondKey] = {thirdKey: formattedText}
                        print "Added to translations: " + formattedText
                else:
                    database[firstKey][secondKey] = formattedText
                    print "Added to translations: " + formattedText
            else:
                database[firstKey] = formattedText
                print "Added to translations: " + formattedText

def look_for_texts(array):
    for child in array:
        if child.type == 'text':
            parse_name(child, 4, None)
        elif child.type == 'group':
            look_for_texts(child.children)
            
jsonFile = open("db.json").read()
database = json.loads(jsonFile)

with XDFile('test4.xd', 'r') as xd:
    for artboard in xd.artboards:
        for child in artboard.artwork:
            if child.type == 'text':
                parse_name(child, 4, None)
            elif child.type == 'group':
                look_for_texts(child.children)
    # look_for_texts(xd.artworks)

with io.open('output.json', 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(database, indent=4, ensure_ascii=False)))