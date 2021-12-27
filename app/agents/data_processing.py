from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
import string
from nltk.probability import FreqDist


class CommonWords:
    """ This class tokenize text, extract the most common words in text and build word cloud """

    def __init__(self, quantity: int) -> None:
        self.quantity = quantity
        self.stop = set(stopwords.words('english'))
        self.stop.update(set(stopwords.words('polish')))
        punctuation = list(string.punctuation)
        self.stop.update(punctuation)
        self.text = ''

    def common_words_to_df(self, file) -> dict:
        """
        Tokenize words in text and extract the most common words
        :param self:
        :return: None
        """

        print('## Initzilize NLTK (Natural Language Toolkit)')
        print(f'## Prepering {self.quantity} most common words in text')

        # Open csv file
        df = file

        # Marge text from df to variable (str)
        for word in df.profile_text.values:
            self.text = self.text + word + ' '

        # Tokenize text
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(self.text)

        # Tokenized text
        text = ' '.join(word for word in text)
        tokenized_word = word_tokenize(text)
        tokenized_word = [word.lower() for word in tokenized_word]
        filtered_word = []

        # Filtering text (excluding stopwords)
        for word in tokenized_word:
            if word not in self.stop:
                filtered_word.append(word)

        for word in filtered_word:
            try:
                if isinstance(int(word), int):
                    filtered_word.remove(word)
            except:
                pass

        # Build common words
        fdist = FreqDist(filtered_word)

        # Select n words from dict - n is quantity variable in class
        most_common = fdist.most_common(self.quantity)
        #json_file = json.dumps(dict(most_common))
        #html_content = json2html.convert(json=json_file)
        return dict(most_common)