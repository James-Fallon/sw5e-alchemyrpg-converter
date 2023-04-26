# sw5e-alchemyrpg-converter

Python script to convert SW5e character JSONs into AlchemyRPG compatible JSONs.

NOTE: This is still very much a WIP. See all the TODOs in convert.py to see what I have left to port. 

But for the (small? large? am I the only one?) number of ppl who love SW5e and Alchemy, enjoy!

## 1. Equip All Your Weapons in SW5e

In your character sheet on the SW5e site, go to your equipment tab and ensure all of your weapons are equipped. This will ensure that the attacks from these weapons will be migrated to Alchemy too.

## 2. Export SW5e JSON in Roll20 Format

From your character sheet, hit the MENU button and then hit EXPORT TO ROLL 20.
This will download a `.json` file of your character which will be used as the input to this script. 

![SW5e Export](https://raw.github.com/James-Fallon/sw5e-alchemyrpg-converter/master/media/sw5e-screen.png)

## 3. Update and run the script

Update `convert.py` by plugging in the path to the json you downloaded in step 2. Now you can run the script:

`python convert.py` or `python3 convert.py`


## 4. Upload JSON to Alchemy

Step 4 will have generated a new `alchemy-character.json` file in the repo. In Alchemy under Characters hit 'Import JSON' and choose this file. 

And thats it!
