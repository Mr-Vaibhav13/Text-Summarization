import bs4 as bs
import urllib.request
import re
import heapq
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')


data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Cricket')
article = data.read()

text = bs.BeautifulSoup(article,'lxml')

paragraphs = text.find_all('p')

articleTXT = ""

for p in paragraphs:
    articleTXT += p.text

# Removing Square Brackets and Extra Spaces
articleTXT = re.sub(r'\[[0-9]*\]', ' ', articleTXT)
articleTXT = re.sub(r'\s+', ' ', articleTXT)

# Removing special characters and digits
tokenTXT = re.sub('[^a-zA-Z]', ' ', articleTXT )
tokenTXT = re.sub(r'\s+', ' ', tokenTXT)

sentence_list = nltk.sent_tokenize(articleTXT)

stopwords = nltk.corpus.stopwords.words('english')

frequencies = {}
for word in nltk.word_tokenize(tokenTXT):
    if word not in stopwords:
        if word not in frequencies.keys():
            frequencies[word] = 1
        else:
            frequencies[word] += 1

maximum_frequncy = max(frequencies.values())

for word in frequencies.keys():
    frequencies[word] = (frequencies[word]/maximum_frequncy)


rank = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in rank.keys():
                    rank[sent] = frequencies[word]
                else:
                    rank[sent] += frequencies[word]


outputSentence = heapq.nlargest(7, rank, key=rank.get)


with open('cricket1.txt', 'w') as f:
    f.write('\n'.join(outputSentence))

# print(summary)





