from polyglot.text import Text
import polyglot
import json
import spacy

nlp = spacy.load('pt')

def structureText(text):
    """ Removes literals \n \t \r"""
    return text.replace("\n","").replace("\t","").replace("\r","")    

# input example: {"title":"geologo" }
def getEntities(stringDict):
    entitiesByModel = {}

    for key1, func in NerModels.items():
        entitiesByModel[key1] = {}
        for key2, text in stringDict.items():
            entitiesByModel[key1][key2] = func(text)
    return entitiesByModel 


def NerPolyglot(sentence):
    entities = {"Person":[],"Organisation":[],"Place":[]}

    polyglotAnnotation = Text(sentence, hint_language_code='pt')    
    for entity in polyglotAnnotation.entities:
        entityStr = list(polyglotAnnotation.words[entity.start:entity.end])
        if entity.tag == "I-PER":
            entities["Person"].append(entityStr)
        if entity.tag == "I-LOC":
            entities["Place"].append(entityStr)
        if entity.tag == "I-ORG":
            entities["Organisation"].append(entityStr)

    return entities

def NerSpacy(sentence):
    entities = {"Person":[],"Organisation":[],"Place":[]}
    doc = nlp(sentence)

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        if entity.label_ == "PER":
            entities["Person"].append(entity.text)
        if entity.label_ == "LOC":
            entities["Place"].append(entity.text)
        if entity.label_ == "ORG":
            entities["Organisation"].append(entity.text)

    return entities

if __name__ == '__main__':
    global NerModels 
    NerModels = {"Spacy":NerSpacy}


    with open("../datasets/development.json","r") as f:
        vagas = json.load(f)
        output = {}

        for vaga in vagas:            
            title = structureText(vaga["title"])
            description = structureText(vaga["description"])

            entidadesVaga = getEntities({"title":title,"description":description})
            
            # Indexa os resultados pelo id da vaga
            output[vaga["id"]] = entidadesVaga
            print (vaga["id"])

        with open("entities.json","w") as entities:
            entities.write(json.dumps(output))

