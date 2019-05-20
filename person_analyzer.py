import os, re 

from message_extractor import MessageExtractor

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'data', 'ozcs.txt')

class PersonAnalyzer(): 
    def __init__(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as in_file:
            self.raw_text = in_file.read()
        self.__extract_names()

        self.extractors = [ MessageExtractor(data_path, name) for name in self.names ]

        for extractor in self.extractors:
            print(extractor.name, extractor.get_most_used_words(5))
        

    def __extract_names(self):
        regex_string = r'\b\d+[/]\d+[/]\d+, \d+:\d+ - ([^:]+): .+\n'
        self.names = set(re.findall(regex_string, self.raw_text))

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'data', 'ozcs.txt')
analyzer = PersonAnalyzer(data_path)



