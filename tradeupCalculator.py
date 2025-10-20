import json

def calculate():
    file = open("tmpdata.json", "r")
    data = json.load(file)

    for collection in data:
        blues = []
        purples = []
        #            bs,            ww,            ft,            mw,            fn
        cheapest = [[1000000, []], [1000000, []], [1000000, []], [1000000, []], [1000000, []]]
        for skin in collection:
            if skin[0][2] == "Mil-Spec Grade":
                blues.append(skin)
            elif skin[0][2] == "Restricted":
                purples.append(skin)
        for blue in blues:
            if blue[1]['Battle-Scarred'] < cheapest[0][0]:
                cheapest[0][0] = blue[1]['Battle-Scarred']
                cheapest[0][1] = blue
            if blue[1]['Well-Worn'] < cheapest[1][0]:
                cheapest[1][0] = blue[1]['Well-Worn']
                cheapest[1][1] = blue
            if blue[1]['Field-Tested'] < cheapest[2][0]:
                cheapest[2][0] = blue[1]['Field-Tested']
                cheapest[2][1] = blue
            if blue[1]['Minimal Wear'] < cheapest[3][0]:
                cheapest[3][0] = blue[1]['Minimal Wear']
                cheapest[3][1] = blue
            if blue[1]['Factory New'] < cheapest[4][0]:
                cheapest[4][0] = blue[1]['Factory New']
                cheapest[4][1] = blue
        print(cheapest)


    file.close()