import json
import os
import pickle
import argparse
from multiprocessing.dummy import Pool as ThreadPool
#First run wikiextractor to get wikipedia text:
#python WikiExtractor.py -o OUTPUT_DIRECTORY --no-templates --json --processes 16 arwiki/arwiki-20190201-pages-articles-multistream.xml
#Now this script will produce a big dictionary pickled to access wikipedia

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input-dir', help='Directory where the output of WikiExtractor is and only', required=True)
parser.add_argument('-o','--output-dir', help='Where to place the pickled wiki', required=True)

arwiki = {} #global variable across processors
total = 0 # count

def get_file_wiki(filename):
    global arwiki
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            json_article = json.loads(line)
            article_title = json_article['title']
            article_text = [par for par in json_article['text'].split('\n')[1:] if par != ""]
            arwiki[article_title]= article_text
    global total
    total +=1


def get_pickled_wiki(inp, out):
    global arwiki
    file_names = []
    for root, dirs, files in os.walk(inp):
        for file in files:
            if file[:5] == "wiki_":
                if file[-5:] != ".json":
                    os.rename(os.path.join(root, file),os.path.join(root, file + ".json"))
                    file_names.append(os.path.join(root, file + ".json"))
                else:
                    file_names.append(os.path.join(root, file))
    pool = ThreadPool(100)
    pool.map(get_file_wiki, file_names)
    pickle.dump(arwiki,open(out+"/arwiki.p","wb"))

def test_read_wiki(out):
    wiki = pickle.load(open(out+"/arwiki.p","rb"))
    print(wiki["لبنان"])

def main():
    args = parser.parse_args()
    get_pickled_wiki(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
