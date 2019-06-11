## Obtaining Wikipedia as a Python dictionary

We adapt the Wikipedia extractor available in https://github.com/attardi/wikiextractor (all code is available in the arwiki folder).
From Wikipedia dumps we will turn it to a Python dictionary to be able to access it as:

```
wikipedia['لبنان'] = ["       
لبنان أو (رسمياً: الجمهوريّة اللبنانيّة)، هي دولة عربية واقعة في الشرق الأوسط في غرب القارة الآسيوية.", ... ]
```
**Steps**:
All scripts here are located in the **arwiki** folder.

*  First download Wikipedia dump available at: https://dumps.wikimedia.org/arwiki/20190520/arwiki-20190520-pages-articles-multistream.xml.bz2 and unzip to .xml (you can use older versions also).
*  Create a temporary **empty** folder, say it's location is  TEMP_DIRECTORY,  Use arwiki/wikiextractor.py to do a first step extraction of the dump to your (if you use Linux instead of '^' write '\'):

**Note:** This command will create a bunch of folders in your TEMP_DIRECTORY named AA, AB, ... and will take up to 10 minutes (there are 660k articles in total).
```shell
python WikiExtractor.py ^
arwiki-20190201-pages-articles-multistream.xml ^
--processes 16 ^
--o . ^
--no-templates ^
--json
```

* Now using the output of WikiExtractor we will build a Python dictionary of Arabic Wikipedia and save it in pickle form  (if you are not familiar with Pickle check https://wiki.python.org/moin/UsingPickle, we will use it extensively here), pick an OUTPUT_DIRECTORY:

```shell
python arwiki_to_dict.py ^
-i TEMP_DIRECTORY ^
-o OUTPUT_DIRECTORY
```
This command will create a file called arwiki.p of size 1.2GB in your output directory and this is your pickled Wikipedia.
*  You can safely now delete your TEMP_DIRECTORY
