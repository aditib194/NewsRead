import requests
import bs4
import spacy
import pyphen

nlp = spacy.load("en_core_web_trf")

def syllablesCount(word):
	dic = pyphen.Pyphen(lang='en_US')
	return dic.inserted(word).count('-') + 1

def readibility(p):
	words = 0
	sentences = 0
	syllables = 0
	for y in range(0, len(p) - 1):
		paragraphs = p[y].get_text()
		for token in paragraphs.split(" "):
			words += 1
		text = nlp(paragraphs)
		for sent in text.sents:
			sentences += 1
			for token in sent:
				if(not token.is_punct and not token.is_space):
					syllables += syllablesCount(token.text)
	read = 206.835 - (1.015 * words)/sentences - (84.6 * syllables)/words
	if(read < 1):
		return 1
	if(read > 100):
		return 100
	return read


res = requests.get("https://apnews.com")
soup = bs4.BeautifulSoup(res.text, "lxml")
links = soup.select('.Link ')
for x in range(7, 35):
	res = requests.get(links[x]['href'])
	soup = bs4.BeautifulSoup(res.text, "lxml")
	text = soup.select('.RichTextStoryBody p')
	print(readibility(text))

# res = requests.get("https://apnews.com/article/military-academies-sexual-assault-report-8753bdc6ba693836e787ee4dca5194d5")
# soup = bs4.BeautifulSoup(res.text, "lxml")
# link = soup.select('.RichTextStoryBody p')
# # print(link[0].get_text())

# nlp = spacy.load("en_core_web_trf")

# text = link[2].get_text()
# doc = nlp(text)

# for token in doc[0:10]:
# 	print (token)

# for sent in doc.sents:
# 	print(sent)

# sentence1 = list(doc.sents)[0]
# print(sentence1)

# for token in doc[:10]:
# 	print (token)

# token2 = sentence1[2]
# print(token2)