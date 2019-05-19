import os, re 

from message_extractor import MessageExtractor

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'data', 'ozcs.txt')

class PersonAnalyzer(): 
    def __init__(self):
        with open(data_path, 'r', encoding='utf-8') as in_file:
            self.raw_text = in_file.read()
        self.__extract_names()

        self.extractors = [ MessageExtractor(name) for name in self.names ]

        max_typo_rate = -1e9
        for extractor in self.extractors:
            if extractor.typo_rate > max_typo_rate:
                max_typo_rate = extractor.typo_rate
                max_typoer = extractor.name
        
        print(max_typoer)

    def __extract_names(self):
        regex_string = r'\b\d+[/]\d+[/]\d+, \d+:\d+ - ([^:]+): .+\n'
        self.names = set(re.findall(regex_string, self.raw_text))

analyzer = PersonAnalyzer()


