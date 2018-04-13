# new test

import json
import io
import re
from xdtools import XDFile            
jsonFile = open("output.json").read()
database = json.loads(jsonFile)
prefix = "$T$ "
inputFile = 'test4.xd'
outputFile = 'output.json'

def write_to_key(database, keys, counter, obj):
    if keys[counter+1]:
        database[keys[counter]] = {}
        return write_to_key(database[keys[counter]], keys, counter+1, obj)
    else:
        database[keys[counter]] = obj.raw_text
        print "Added to translation: " + keys[counter] + ": " + obj.raw_text
    return counter

def check_for_key(database, keys, counter, obj):
    if keys[counter] and keys[counter] is not None and not "":
        if keys[counter] in database:
            return check_for_key(database[keys[counter]], keys, counter +1, obj)
        else:
            write_to_key(database, keys, counter, obj)
        return counter
        
def look_for_texts(obj):
    if obj.type == 'text' and obj.name[:len(prefix)] == prefix:
        obj.raw_text = re.sub(r"-\n", "", obj.raw_text)
        obj.raw_text = re.sub(r"\n", " ", obj.raw_text)
        obj.name = re.sub("\$T\$ ", "", obj.name)
        keys = obj.name.split('.')
        check_for_key(database, keys, 0, obj)
    elif obj.type == 'group':
        for child in obj.children:
            look_for_texts(child)

with XDFile(inputFile, 'r') as xd:
    for artboard in xd.artboards:
        for obj in artboard.artwork:
            look_for_texts(obj)

with io.open(outputFile, 'w', encoding='utf-8') as outfile:
    outfile.write(unicode(json.dumps(database, indent=4, ensure_ascii=False)))