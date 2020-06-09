import json

def writeKanjiDataToJson(data):
    with open('output/kanjis.json', 'w', encoding='utf-8')   as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
