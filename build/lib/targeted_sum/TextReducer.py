import torch
from sentence_transformers import SentenceTransformer, util
import spacy
import PyPDF2

class Reducer:
    def __init__(self, model_name='msmarco-MiniLM-L-6-v3', device="cpu"):
        self.device = device if torch.cuda.is_available() else "cpu"
        self.embmodel = SentenceTransformer(model_name).to(self.device)
        self.nlp = spacy.load("en_core_web_sm")
        if self.device != "cpu":
          spacy.require_gpu()
        
    def batch(self, iterable, n=1):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]
        
    def reduce_small(self, text, target_embedding, num_sents=5):
        sentences = [sent.text for sent in self.nlp(text).sents]
        new_texts = []
        for sent in sentences:
            new_text = [s for s in sentences]
            new_text.remove(sent)
            new_texts.append(new_text)
        new_texts = [" ".join(new_text) for new_text in new_texts]
        new_text_embeddings = self.embmodel.encode(new_texts, convert_to_tensor=True, show_progress_bar=False)
        cos_scores = util.cos_sim(target_embedding, new_text_embeddings)[0]
        top_indices = torch.topk(cos_scores, k=len(new_texts))[1]
        top_texts = [new_texts[i] for i in top_indices]
        top_text = top_texts[0]
        top_sentences = [sent.text for sent in self.nlp(top_text).sents]
        if len(top_sentences)<=num_sents:
            return top_text
        else:
            return self.reduce_small(top_text, target_embedding, num_sents)
        
    def reduce_large(self, big_text, target_embedding, num_sents=5):
        big_sentences = [sent.text for sent in self.nlp(big_text).sents]
        parts = []
        for part in self.batch(big_sentences, 10):
            parts.append(self.reduce_small(' '.join(part), target_embedding, num_sents))
        new = ' '.join(parts)
        if len([sent.text for sent in self.nlp(new).sents])<=num_sents:
            return new
        elif len(parts)==1:
            return self.reduce_small(new, target_embedding, num_sents)
        else:
            return self.reduce_large(new, target_embedding, num_sents)
        
    def reduce(self, huge_text, target, num_sents=5):
        target_embedding = self.embmodel.encode(target, convert_to_tensor=True, show_progress_bar=False)
        #huge_sentences = [sent.text for sent in self.nlp(huge_text).sents]
        huge_sentences = [x+"." for x in huge_text.split(". ")]
        parts = []
        for part in self.batch(huge_sentences, 4):
            parts.append(" ".join(part))
        new_text_embeddings = self.embmodel.encode(parts, convert_to_tensor=True, show_progress_bar=False)
        cos_scores = util.cos_sim(target_embedding, new_text_embeddings)[0]
        top_indices = torch.topk(cos_scores, k=len(parts))[1]
        top_texts = [parts[i] for i in top_indices][:3]
        chronological = []
        for part in parts:
            if part in top_texts:
                chronological.append(part)
        reduction = self.reduce_large(" ".join(chronological), target_embedding, num_sents)
        return reduction  

    def summarize(self, text, num_sents=5):
        return self.reduce(text, text, num_sents=num_sents)
        
    def reduce_pdf(self, pdf_path, target, num_sents=5):
        with open(pdf_path, 'rb') as f:
            pdf = PyPDF2.PdfFileReader(f)
            text = ""
            for page in pdf.pages:
                text += page.extractText()
        reduction = self.reduce(text, target, num_sents)
        return reduction