from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk
nltk.data.path.append("C:/Users/satya/AppData/Roaming/nltk_data")


def summarize_text(text: str, language: str = 'english', num_sentences: int = 3):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentences_count=num_sentences)
    return ' '.join(str(sentence) for sentence in summary)

