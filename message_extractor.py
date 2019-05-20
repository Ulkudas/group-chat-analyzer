import os, re, json
import editdistance

from emoji_extractor import EmojiExtractor
from pprint import pprint 

class EnglishLang():
    current_path = os.path.dirname(os.path.abspath(__file__))
    en_corpus_path = os.path.join(current_path, 'data', 'en_words.txt')
    
    with open(en_corpus_path, 'r', encoding='utf-8') as corpus_file:
        vocabulary = { word.lower() for word in corpus_file.read().split() }
    
class TurkishLang():
    current_path = os.path.dirname(os.path.abspath(__file__))
    tr_corpus_path = os.path.join(current_path, 'data', 'tr_word_stems_freqs.txt')
    
    skiprow = 6
    word_freqs = {}

    with open(tr_corpus_path, 'r', encoding='utf-8') as corpus_file: 
        for row in range(skiprow): 
            next(corpus_file) 
        for row in corpus_file: 
            parts = row.split() 
            word_freqs[parts[0]] = parts[3] 
        
    vocabulary = set(word_freqs.keys())
    unified_vocabulary = EnglishLang.vocabulary.union(vocabulary)

class MessageExtractor():
    def __init__(self, data_path, name):
        with open(data_path, 'r', encoding='utf-8') as in_file:
            self.raw_text = in_file.read()

        self.name = name
        self.__extract_messages(name)
        self.__create_vocabulary()
        self.__find_word_freqs()
        self.__find_links()
        self.__find_typo_rate()

    def __extract_messages(self, name):      
        regex_string = r'\b(\d+[/]\d+[/]\d+), (\d+:\d+) - {}: (.+)\n'.format(name)
        results = re.findall(regex_string, self.raw_text)

        self.message_data = [
            {
                "date": date,
                "time": time,
                "message": message
            } 
            for (date, time, message) in results if message not in \
                {'You deleted this message.', 'this message was deleted.', '<Media omitted>'}
        ]

        self.messages = [
            element["message"] for element in self.message_data
        ]

        self.text = " ".join(self.messages)
    
    def __create_vocabulary(self):
        self.personal_vocabulary = set(self.text.lower().split())  
    
    def __find_word_freqs(self):
        all_words = self.text.lower().split()
        
        self.word_freqs = {}
        
        for word in all_words:
            if word not in self.word_freqs:
                self.word_freqs[word] = 1
            else:
                self.word_freqs[word] += 1
        
        self.most_frequent_words = sorted(self.word_freqs.items(), key=lambda item: item[1], reverse=True)
    
    def get_most_used_words(self, limit):
        if limit > len(self.most_frequent_words):
            limit = len(self.most_frequent_words)

        return [ item[0] for item in self.most_frequent_words[0:limit]]  

    # gives you the closest bahadir word, a typoed one if typo option is True 
    def find_closest_word(self, given_word, typo=False): 
        min_edit_dis = int(1e9)

        for word in self.personal_vocabulary:
            if typo and word in TurkishLang.unified_vocabulary:
                continue
            
            edit_dis = editdistance.eval(word, given_word)
            
            if edit_dis < min_edit_dis:
                min_edit_dis = edit_dis
                closest_word = word

        return closest_word
    
    def __find_links(self):
        regex_string = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.links = re.findall(regex_string, self.text)


    def __find_typo_rate(self):
        all_words = self.text.lower().split()
        
        count = 0
        for word in all_words:
            if word not in TurkishLang.unified_vocabulary:
                count += 1

        if not all_words:
            self.typo_rate = 0
        else:
            self.typo_rate = count / len(all_words)
    
    def dump_data(self, folder_path):
        with open(os.path.join(folder_path, 'message_data.json'), 'w', encoding='utf-8') as out_file:
            json.dump(self.message_data, out_file)

    def find_emoji_freqs(self):
        pass


