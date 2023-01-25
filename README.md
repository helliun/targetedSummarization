# Targeted Summarization with TextReducer
TextReducer is a tool for summarization and information extraction powered by the SentenceTransformer library. Unlike many techniques for extractive summaries, TextReducer has the option for a "target" around which the summary will be focused. This target can be any text prompt, meaning that a user can specify the type of information that they would like to find or summarize, and ignore everything else.

One of the key benefits of TextReducer is that rather than extracting the sentences for the summary, it carves away at the original text, removing unnecessary sentences. This leads to more fluent summarizations, and preserves grammatical features like coreference that are often lost in traditional extractive summarization. For instance, in the sentences "Mark lives in Chicago with his family. He has a dog.", it is imporant that these sentences stay linked together. Otherwise, the coreferent of the word "he" in the second sentence is lost. TextReducer is much better at preserving such related sentences, and is thus a valuable tool for fast, but fluent summarizations of large texts.

The class has several methods:
- `reduce(huge_text, target, num_sents=5, filter=False)` - this method takes in a large text and a target text, and returns a summary of the input text that is most similar to the target text. It first encodes the input text and the target text using the SentenceTransformer's embedding model, then it calculates the cosine similarity between the embeddings of the input text and the target text. It then finds the top `num_sents` most similar sentences and returns them as a string.
- `summarize(text, num_sents=5)` - this method takes in a text and returns a summary of the input text that is most similar to the overall meaning of the text. It first encodes the input text using the SentenceTransformer's embedding model, then it calculates the cosine similarity between the embeddings of the sentences and the text as a whole. It then finds the top `num_sents` most similar sentences and returns them as a string.
- `reduce_pdf(pdf_path, target, num_sents=5)` - this method takes in a pdf file's path, a target text and a number of sentences to be returned, it then reads the pdf, extract the text from it, calls the summarize method and returns the summary.

## Installation
To install TextReducer, use "pip install targeted_sum"

## Demo
A Google Colab demo can be found [here](https://colab.research.google.com/drive/1Bnl4e9JmFYoTSAF2FlBVPAUQ1lC0EpjE?usp=sharing)