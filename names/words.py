import uuid
import random

def removeWhitespace(string: str) -> str:
    return string.strip().capitalize()
    
# Esta función lee un archivo con una lista de adjetivos y otro con una lista de de sustantivos, después elige
# un adjetivo y tres sustantivos al azar y los retorna en formato de string. Si los archivos no se encuentran
# se retorna un GUID
def GetName() -> str:
    try:
        adjectivesFile = open("names\\adjectives.txt", 'r')
        nounsFile = open("names\\words.txt", 'r')

        adjectiveList = adjectivesFile.readlines()
        adjectiveList = list(map(removeWhitespace, adjectiveList))

        nounList = nounsFile.readlines()
        nounList = list(map(removeWhitespace, nounList))

        adjectivesFile.close()
        nounsFile.close()

        adjective = random.choice(adjectiveList)
        
        nouns =  random.sample(nounList, 3)

        return adjective+nouns[0]+nouns[1]+nouns[2]
    except FileNotFoundError:
        print("No se encontraron los archivos con nombres, se utilizarán GUIDs")
        return str(uuid.uuid4())


