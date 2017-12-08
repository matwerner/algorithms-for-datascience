import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('pt')

# Process whole documents
text = "Oi, meu nome é Daniel Menezes."
doc = nlp(text)

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)

## Determine semantic similarities
#doc1 = nlp(u'the fries were gross')
#doc2 = nlp(u'worst fries ever')
#doc1.similarity(doc2)

# Hook in your own deep learning models
#nlp.add_pipe(load_my_model(), before='parser')
