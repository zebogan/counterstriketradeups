import requests, json, time, html_to_json, os, sys

import tradeupCalculator

if os.path.exists("collections.json"):
    print("collection data present")
else:
    print("getting collection data")
    pageLinks = []

    # get list of collections
    totalcsgo1 = requests.get("https://totalcsgo.com/skins/collections")
    totalcsgo2 = requests.get("https://totalcsgo.com/skins/collections/2")
    totalcsgo = [totalcsgo1, totalcsgo2]

    for t in totalcsgo:
        page = html_to_json.convert(t.text)
        # get each tile in the grid from the site
        tiles = page['html'][0]['body'][0]['div'][0]['div'][0]['main'][0]['div'][1]['div'][0]['div'][2]['div'][0]['div'][0]['div']
        for tile in tiles:
            link = tile['div'][0]['a'][0]['_attributes']['href']
            name = tile['div'][0]['a'][1]['h2'][0]['_value']
            # the actual collections (not sticker, graffiti, agent) all have The in the name
            if "The" in name:
                pageLinks.append({'name': name, 'link': link})

    # name, skins
    collectionData = []

    with open("updatedSkins.json", "r") as file:
        us = json.load(file)

        for idx, col in enumerate(pageLinks):
            # gun, skin, rarity
            skins = []
            r = requests.get(f"https://totalcsgo.com{col['link']}")
            page = html_to_json.convert(r.text)
            tiles = page['html'][0]['body'][0]['div'][0]['div'][0]['main'][0]['div'][1]['div'][0]['div'][1]['div'][0]['div'][1]['div'][1]['div']
            for tile in tiles:
                rarity = tile['div'][0]['div'][0]['div'][0]['div'][0]['span'][0]['_value']
                gun = tile['div'][0]['div'][0]['div'][0]['div'][0]['span'][1]['_value']
                skin = tile['div'][0]['div'][0]['a'][2]['h2'][0]['_value']
                for a in us:
                    if a['name'] == f"{gun} | {skin}":
                        minFloat = a["min_float"]
                        maxFloat = a["max_float"]
                
                skins.append([gun, skin, rarity, {"min_float": minFloat, "max_float": maxFloat}])
            collectionData.append([col['name'], skins])
            print(f"Progress: {idx+1}/{len(pageLinks)}")

    with open("collections.json", "w") as file:
        json.dump(collectionData, file, indent=4)

                

if len(sys.argv) == 2 and sys.argv[1] == "update":
    print("updating price data")
    skinData = []

    with open("collections.json", "r") as file:
        allCollections = json.load(file)
        counter = 0
        startTime = time.time()
        #!!!! CHANGE BEFORE RUNNING!!!
        for idx, col in enumerate(allCollections[:2]): # remove [:2]
            colData = []
            for skin in col[1]:
                counter += 1
                if counter % 20 == 0:
                    print("delaying")
                    print(f"progress: {counter}/1357")
                    curTime = time.time()
                    print(f"time elapsed: {round((curTime - startTime)//3600)}h{round((curTime - startTime)%3600)//60}m{round((curTime - startTime)%60)}s")
                    time.sleep(300)
                fixedName = f"\"{skin[0]}+%7C+{skin[1]}\"".replace(" ", "+")
                response = requests.get(f"https://steamcommunity.com/market/search/render/?query={fixedName}&start=0&count=10&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730&norender=1&category_730_Quality%5B%5D=tag_normal")
                results = json.loads(response.text)['results']

                wearData = {}

                for result in results:
                    wearName = result['name'].replace(f"{skin[0]} | {skin[1]} (", "").replace(")", "")
                    price = result['sell_price']
                    wearData[wearName] = price

                colData.append([skin, wearData])
            skinData.append(colData)
            print(f"progress: {idx+1}/{len(allCollections)}")

    #!!!! CHANGE BEFORE RUNNING!!!
    with open("tmpdata.json", "w") as file: #remove tmp
        json.dump(skinData, file, indent=4)
else:
    print("running normally")
    tradeupCalculator.calculate()


