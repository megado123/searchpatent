#Script intended for debugging in Azure only
import nltk
import  urllib.request
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
nltk.download('stopwords') # nice to bring up everything to download

from patentsearch.models  import  User, Search, SearchData


class Data():
    def __init__(self, textdata):
        self.text = textdata
        self.counts = []
        self.words = []

    def bow(self):
        tokens = [t for t in self.text.split()]
        clean_tokens = tokens[:]
        sw = stopwords.words('english')
        for token in tokens:
            if token in stopwords.words('english'):
                clean_tokens.remove(token)
        freq = nltk.FreqDist(clean_tokens)

        for key, val in freq.items():
            self.counts.append(val)
            self.words.append(key)
 


x = Data("This is my cool example")
x.bow()
print (x.counts)
print (x.words)
print(x.text)

print('checking out class')
data = {'Machine Name': hostname}
searchData = SearchData(s, jsonData= data)
print(searchData.frequency_list)
