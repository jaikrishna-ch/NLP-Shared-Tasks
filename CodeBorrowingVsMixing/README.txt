To run the code
output generated in output.csv

python SharedTask2.py

In this project, based on the tweets scraped from twitter which consists of hindi-english tweets, we predicted how likely
a word is borrowed or mixed from the other language and ranked a set of test words.

For example : "Aaj raat ko movie chalenge" in this, movie is a word from english language, which is borrowed to Hindi sentence.

The links to the twitter data required to train are given in the Datasheet.csv file, scrape the tweets using tweepy.
The scraping process took approx 3 days on AWS ec2 console. And approximately 2,40,000 tweets were scraped along with their user
id and tweet id. 

The tweet composition is mentioned in the Datasheet.csv file.

data consists of all the tweet text.

input.txt consists of data to be ranked.

output consists of the ranked data.


