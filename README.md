# Perseus Lexica to JSON

## Purpose
The Perseus team at Tufts has done such valuable work in digitizing *Lewis and Short* and *Liddell and Scott* and making them available under a Creative Commons license.
However, the lexica are in XML, while it would be useful to have a version of them in JSON to make them easier to integrate into modern web applications.
This repo contains scripts to convert the XML versions of these works into JSON.
JSON will not be able to act as direct digital representations of the print dictionaries as well as XML can, due to limitations in the JSON format.
Instead, the point of these scripts is to enable the production of JSON versions that reuse the information contained in the dictionaries in a hacker-friendly way, even if the data ends up as a bit of an exquisite corpse.

## Already compiled JSON
A JSON version of Lewis and Short already compiled by the scripts here is available at https://github.com/IohannesArnold/lewis-short-json

## Get Started
(All of these instructions are only suggestions; if you want to use these scripts in other ways, go ahead.)

1. Pull the Perseus Database with `git submodule update --recursive --init`.
2. Make sure you have the Python packages in `requirements.txt` installed, either globally or in a virtualenv.
3. Change to the `./lat` directory.
4. Run `sed -f macrons.txt lat.ls.perseus-eng1.xml > ls.with.macrons.xml`.
5. Run `./alphabetize.py ls.with.macrons.xml`/
6. Run `./tojson.py ls_*.xml`.


## Credits

Text provided by Perseus Digital Library, with funding from The National Endowment for the Humanities. 

Original version available for viewing and download at http://www.perseus.tufts.edu/