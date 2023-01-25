# Targeted Summarization with TextReducer
TextReducer is a Python class that can be used to summarize large amounts of text and extract relevant information from it. It uses the SentenceTransformer library to generate embeddings of the input text and the target text, which enables it to accurately compare the similarity between the two texts. It also uses the spaCy library to tokenize text into sentences and Wikipedia library to fetch articles by title.

The class has several methods:
- `reduce(huge_text, target, num_sents=5, filter=False)` - this method takes in a large text and a target text, and returns a summary of the input text that is most similar to the target text. It first encodes the input text and the target text using the SentenceTransformer's embedding model, then it calculates the cosine similarity between the embeddings of the input text and the target text. It then finds the top `num_sents` most similar sentences and returns them as a string.
- `summarize(text, num_sents=5)` - this method takes in a text and returns a summary of the input text that is most similar to the overall meaning of the text. It first encodes the input text using the SentenceTransformer's embedding model, then it calculates the cosine similarity between the embeddings of the sentences and the text as a whole. It then finds the top `num_sents` most similar sentences and returns them as a string.
- `reduce_pdf(pdf_path, target, num_sents=5)` - this method takes in a pdf file's path, a target text and a number of sentences to be returned, it then reads the pdf, extract the text from it, calls the summarize method and returns the summary.

## Installation
To install TextReducer, use "pip install targeted_sum"

## Demo
A Google Colab demo can be found [here](https://colab.research.google.com/drive/1Bnl4e9JmFYoTSAF2FlBVPAUQ1lC0EpjE?usp=sharing)