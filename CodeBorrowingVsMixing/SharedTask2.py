from nltk.tokenize import word_tokenize
import csv
import string
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
from collections import defaultdict

PUNCT_LIST = list(string.punctuation)
STOPWORDS_LIST = list(stopwords.words('english'))

STEMMER = PorterStemmer()
templist = ['EN', 'CMEQ', 'CME', 'HI', 'CMH']

def parse_datasheet(file):
    important_data = defaultdict()
    meta = defaultdict()
    tweet_types = defaultdict()
    f = open(file, 'r')
    # with open(file,'r') as f:
    try:
        for x in f:
            tuples=x.split(',')
            t='None'

            data = []
            en = 0
            total = 0
            hi = 0

            for i in range(1, len(tuples)) :
                r = tuples[i].split(':')

                data.append((int(r[0]),int(r[1]),str(r[2])))
                
                if str(r[2]) == 'HI' :
                    hi = hi + 1
                    total = total+1
                elif str(r[2]) == 'EN':
                    en = en + 1
                total = total + 1

            total=en+hi
            en_ratio = float(en)/float(total)
            temp = (en_ratio,1-en_ratio,data)
            # temp = get_ratios(tuples)
            en_ratio = temp[0]
            hi_ratio = temp[1]
            important_data[temp[0]] = temp[1]
            meta[tuples[0]] = temp[2]
            if 1 < en_ratio / .9:
                t=templist[0]
            elif en_ratio/.5 == 1:
                t=templist[1]
            elif en_ratio/.5 > 1:
                t=templist[2]     
            elif hi_ratio/.9 > 1:
                t=templist[3]
            elif hi_ratio > .5:
                t=templist[4]
            tweet_types[tuples[0]]= t
        f.close()
        return (tweet_types, meta)
    except:
        return (tweet_types, meta)    
    
HI_STRING = 'HI'
def parse_tweet_in_data(file):
    non_filtered = []
    filtered=defaultdict()
    f = open(file, 'r')
    total = 0
    try:
        csvReader = csv.reader(f, delimiter=',')
        for t_id,tweet,_ in csvReader:
            filtered_words = []
            for s,e,t in meta[t_id]:
                word = tweet[s-1:e]


                if not (t!=HI_STRING or not word.upper().lower().startswith("main")):
                    non_filtered.append(word)
                    continue
                total = total + 1
                filtered_words.append(word)

            filtered[t_id]=' '.join(filtered_words)
        f.close()
        return filtered
    except:
        return None

PUNCT = set(PUNCT_LIST)
STOPWORDS = set(stopwords.words('english'))


def tokenize(text):
    punc_removed = []
    lowercased = []
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    
    tokens = word_tokenize(text)
    lowercased = [t.lower() for t in tokens]

    for word in lowercased:

        processedWord = []
        for letter in word:
            if letter not in PUNCT:
                processedWord.append(letter)
        punct_removed = ''.join(processedWord)

        punc_removed.append(punct_removed)
    
    stopwords_removed = []
    for w in punc_removed:
        if w in STOPWORDS:
            continue
        stopwords_removed.append(w)

    stem = []
    for w in stopwords_removed:
        stem.append(STEMMER.stem(w))

    return [w for w in stem if w]


def get_stem_words(file):
    csvReader = csv.reader(open(file,'r'))
    stem_words = []
    key_words = []
    for key_word, in csvReader:
        key_words.append(key_word)
        try:
            tokens = tokenize(key_word)
            stem_words.append(tokens[0])
        except:
            print tokens
    return stem_words,key_words


def read_hashes(file):
    key_hashes=set()
    csvReader = csv.reader(open(file,'r'), delimiter=',')
    for t_id,tweet,u_id in csvReader:
        hash_tags = []
        words = tweet.split(" ")
        for word in words:
            if word.startswith('#'):
                hash_tags.append(word.lower())
            
        if len(hash_tags)==0:
            continue
        words = tokenize(tweet)
        try:
            for word in words:
                if word not in stem_words:
                    continue
                if word in stem_words:
                    for hash_tag in hash_tags:
                        key_hashes.add(hash_tag)
                    break
        except:
            print "Word not present!!"
    return key_hashes

def has_hash(tweet):
    words = tweet.split(" ")
    count = 0
    for word in words:
        if(word.startswith('#')) and word in key_hashes:
            count += 1
    if count > 0:
        return True
    return False

def read_data1(datafile):
    word_user_data = defaultdict(lambda: defaultdict(lambda: set([])))
    skip_types = ['HI', 'CMH']  
    f = open(datafile, 'r')
    csvReader = csv.reader(f, delimiter=',')
    for t_id,tweet,u_id in csvReader:
        tweet_type = tweet_types[t_id]
        # Heuristic Condition 2
        if tweet_type not in skip_types and has_hash(tweet) == False:
            continue
        
        words = tokenize(filtered[t_id])
        
        for word in words:
            if word in stem_words :
                word_user_data[word][tweet_type].add(u_id)

    return word_user_data


def read_data2(datafile):
    word_tweets_data = defaultdict(lambda: defaultdict(lambda: set([])))
    f = open(datafile, 'r')
    skip_types = ['HI', 'CMH']       
    csvReader = csv.reader(f, delimiter=',')
    for t_id,tweet,u_id in csvReader:
        tweet_type = tweet_types[t_id]

        # Heuristic Condition 2
        if tweet_type not in skip_types and has_hash(tweet) == False:
            continue
        
        words = tokenize(filtered[t_id])
        
        for word in words:
            if word in stem_words :
                word_tweets_data[word][tweet_type].add(t_id)

    return word_tweets_data

def get_unique_ratio(counts):
    en = 1
    hi = 0
    cmh = 0

    if 'EN' in counts:
        en = len(counts['EN'])
    if 'HI' in counts:
        hi = len(counts['HI'])
    if 'CMH' in counts:
        cmh = len(counts['CMH'])

    ratio = (1.0*(hi+cmh)/en)
    return ratio

def get_final_ranks():
    final_ranks = []
    for key_word in key_words:
        try:
            final_metric = (user_metric[tokenize(key_word)[0]]+tweet_metric[tokenize(key_word)[0]])/2.0
        except:
            final_metric = 0
        final_ranks.append((key_word,final_metric))
    return final_ranks
    
def generate_metrics():
    user_metric = defaultdict()
    for word,type_counts in word_user_data.items():
        user_metric[word] = get_unique_ratio(type_counts)

    tweet_metric = defaultdict()
    for word,type_counts in word_tweets_data.items():
        tweet_metric[word] = get_unique_ratio(type_counts)
    return user_metric, tweet_metric

tweet_types,meta = parse_datasheet("Datasheet.csv")
filtered  = parse_tweet_in_data("data.csv")
stem_words,key_words = get_stem_words("input.txt")
key_hashes = read_hashes("data.csv")

word_user_data = read_data1("data.csv")
word_tweets_data = read_data2("data.csv")

user_metric, tweet_metric = generate_metrics()

final_ranks = get_final_ranks()

list_fin_sorted = sorted(final_ranks,key=lambda l:l[1],reverse=True)
list_fin_word_rank = [(s[0],s[1]) for s in list_fin_sorted]

if len(list_fin_word_rank)==0:
    print "No tweet with hashes!"

for i in list_fin_word_rank:
    print i

f = open("output.csv",'w')
csvWriter = csv.writer(f)
csvWriter.writerows([(data[0],i+1) for i,data in enumerate(list_fin_word_rank)])
f.close()