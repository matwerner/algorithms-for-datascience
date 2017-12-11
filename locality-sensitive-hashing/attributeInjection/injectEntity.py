from polyglot.text import Text
import polyglot
import json
import spacy
nlp = spacy.load('pt')

person ="person"
organisation = "organisation"
place = "place"

def structureText(text):
    """ Removes literals \n \t \r"""
    return ' '.join(text.replace("\n"," ").replace("\t"," ").replace("\r"," ").replace("\v"," ").replace("\n"," ").replace("\f"," ").split())

# input example: {"title":"geologo" }
def getEntities(stringDict):
    entitiesByModel = {}
    for model, func in NerModels.items():
        entitiesByModel[model] = {}
        for key, text in stringDict.items():
            if key != "id" and text != "" :
                entitiesByModel[model][key] = func(text,stringDict["id"])
    return entitiesByModel

def NerPolyglot(text,id):
    entities = {person:[],organisation:[],place:[]}
    polyglotAnnotation = Text(text, hint_language_code='pt')
    for entity in polyglotAnnotation.entities:
        entityStr = list(polyglotAnnotation.words[entity.start:entity.end])
        # if entity.tag == "I-PER":
        #     entities[person].append(entityStr)
        if entity.tag == "I-LOC":
            entities[place].append(entityStr)
        if entity.tag == "I-ORG":
            entities[organisation].append(entityStr)
    return entities

def NerSpacy(text,id):
    entities = {person:[],organisation:[],place:[]}
    doc = nlp( structureText(text))
    # Find named entities, phrases and concepts
    for entity in doc.ents:
    #     if entity.label_ == "PER":
    #         entities[person].append(entity.text)

        if entity.label_ == "LOC":
            entities[place].append(entity.text)

        if entity.label_ == "ORG":
            entities[organisation].append(entity.text)

    return entities

def injectEntities(outputJson,inputJson):
    with open("../datasets/development.json","r") as f:
        vagas = json.load(f)
        output = {}

        for vaga in vagas[9700:]:
            title = structureText(vaga["title"])
            entidadesVaga = getEntities(vaga)
            
            # Indexa os resultados pelo id da vaga
            output[vaga["id"]] = entidadesVaga
            print (vaga["id"])

        with open(outputJson,"w") as entities:
            entities.write(json.dumps(output))

if __name__ == '__main__':
    global NerModels 
    NerModels = {"Spacy":NerSpacy,"Polyglot":NerPolyglot }
    injectEntities("documents_entities.json","../datasets/development.json")