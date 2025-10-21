import json, math

def calculate():
    file = open("data.json", "r")
    data = json.load(file)

    allPurples = {}
    allCheapest = {}

    for colInfo in data:
        collection = colInfo[1]
        blues = []
        purples = []
        cheapest = {"Battle-Scarred": [1000000, []], "Well-Worn": [1000000, []], "Field-Tested": [1000000, []], "Minimal Wear": [1000000, []], "Factory New": [1000000, []]}
        #            bs,            ww,            ft,            mw,            fn
        #cheapest = [[1000000, []], [1000000, []], [1000000, []], [1000000, []], [1000000, []]]
        for skin in collection:
            if skin[0][2] == "Mil-Spec Grade":
                blues.append(skin)
            elif skin[0][2] == "Restricted":
                purples.append(skin)
        for blue in blues:
            for key in blue[1]:
                if blue[1][key] < cheapest[key][0]:
                    cheapest[key][0] = blue[1][key]
                    cheapest[key][1] = blue

        testFloats = {"Battle-Scarred": (0.44+1)/2, "Well-Worn": (0.37+0.44)/2, "Field-Tested": (0.15+0.37)/2, "Minimal Wear": (0.07+0.15)/2, "Factory New": (0+0.07)/2}

        purpleTally = {"Battle-Scarred": [0, 0], "Well-Worn": [0, 0], "Field-Tested": [0, 0], "Minimal Wear": [0, 0], "Factory New": [0, 0]}
        for purple in purples:
            for inputFloat in testFloats:
                estimatedFloat = ((purple[0][3]['max_float'] + purple[0][3]['min_float']) * testFloats[inputFloat]) + purple[0][3]['min_float']
                if estimatedFloat > 0.44:
                    if "Battle-Scarred" in purple[1]:
                        purpleTally["Battle-Scarred"][0] += purple[1]["Battle-Scarred"]
                        purpleTally["Battle-Scarred"][1] += 1
                elif estimatedFloat > 0.37:
                    if "Well-Worn" in purple[1]:
                        purpleTally["Well-Worn"][0] += purple[1]["Well-Worn"]
                        purpleTally["Well-Worn"][1] += 1
                elif estimatedFloat > 0.15:
                    if "Field-Tested" in purple[1]:
                        purpleTally["Field-Tested"][0] += purple[1]["Field-Tested"]
                        purpleTally["Field-Tested"][1] += 1
                elif estimatedFloat > 0.07:
                    if "Minimal Wear" in purple[1]:
                        purpleTally["Minimal Wear"][0] += purple[1]["Minimal Wear"]
                        purpleTally["Minimal Wear"][1] += 1
                else:
                    if "Factory New" in purple[1]:
                        purpleTally["Factory New"][0] += purple[1]["Factory New"]
                        purpleTally["Factory New"][1] += 1
        

        for wear in purpleTally:
            if purpleTally[wear][1] != 0 and cheapest[wear][0] * 10 < math.floor(purpleTally[wear][0] / purpleTally[wear][1] / 1.15):
                print(f"{cheapest[wear][1][0][0]} | {cheapest[wear][1][0][1]} ({wear}) - ${cheapest[wear][0]/100}:")
                print(f"${cheapest[wear][0] / 10} < ${math.floor(purpleTally[wear][0] / purpleTally[wear][1] / 1.15)/100}")


    file.close()