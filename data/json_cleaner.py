import json

json_new = [ ]

#go through the jsons and check for the "content" element
#if empty, delete the element
for json_file in json_new:
    print(json_file)
    with open("./" + json_file) as file:
        data = json.load(file)
        result = []
        for item in data:
            if len(item['content']) > 0:
                #add
                result.append(item)
        #now I have the result --> write it back
        print("writing...")
        with open("./json/clean_" + json_file,"w") as update_file:
            json.dump(result,update_file)
