import pandas as pd
import numpy as np
import re

# open cv
recipes = pd.read_csv('./RAW_recipes.csv')
print("opened cv")

# get the columns
columns = recipes.columns.to_numpy()

recipesDict = recipes.to_dict()
print("made recipe dict")

print(recipesDict["nutrition"])


# add a new key for the data that is going to be vectorized
recipesDict['vectorized'] = {
    i: re.sub(
        r"'([^']*)'",
        r"\1",
        recipesDict['ingredients'][i][1:-1] + ', ' + recipesDict['tags'][i][1:-1]
    ) # combine the ingrdients and the tags and then just format it to be "word, word, ..."
    for i in range(len(recipesDict["name"])) # lenth should be same in all column
}