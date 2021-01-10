import sys, re, random
from typing import Dict, List, Tuple
from copy import deepcopy

#MARKOV_WORDS: number of words in markov dictionary key. 
MARKOV_WORDS = 6

#User inputs new names. Used in file_parse.
NEW_NAMES:List[str] = ["Ray","Gatsby","Kanye","West","Kim","Bruce/Caitlyn","Jenner","Kardasian","Kris"]

#Old names replaced in file_parse.
CHARACTER_NAMES = {
                    'Jay':NEW_NAMES[0],'Gatsby':NEW_NAMES[1],
                    'Tom':NEW_NAMES[2],'Buchanan':NEW_NAMES[3],
                    'Daisy':NEW_NAMES[4],
                    'Nick':NEW_NAMES[5], 'Carraway':NEW_NAMES[6],
                    'Baker':NEW_NAMES[8],
                    'Mina':NEW_NAMES[4],'Murray':NEW_NAMES[7],
                    'Johnathan':NEW_NAMES[5],'Harker':NEW_NAMES[6],
                    'Abraham':NEW_NAMES[2],'Van Helsing':NEW_NAMES[3],
                    'Dracula':NEW_NAMES[1]
                    }

NOVEL_LENGTH = 4000 #words in novel.

#Parse incoming text files into a large text string, removing page numbers, headings, and wrapped words.
def file_parse(file:str) -> str:
    text = ""
    space = True
    with open(file,'r') as f:
        for line in f:
            if line.rstrip() == "":
                pass
            elif line.rstrip() =="Free eBooks at Planet eBook.com":
                pass
            elif (line.rstrip() =="The Great Gatsby") or (line.rstrip() == "Dracula"):
                pass
            elif re.fullmatch(r"([0-9]*)",line.rstrip()):
                pass
            elif re.fullmatch(r"chapter (\w*)",line.rstrip().lower()):
                pass
            elif line.rstrip()[-1] == "-":
                text += " "+line.rstrip()[:len(line.rstrip()) -1]
                space = False
            else:
                if space:
                    text +=" "+line.rstrip()
                else:
                    text += line.rstrip()
                    space = True
    for name in CHARACTER_NAMES.keys():
        text = text.replace(name,CHARACTER_NAMES[name])
    return text

#Create a markov chain dictionary using a text file. Change stored list into dictionary with frequencies.
def markov_builder(markov_dict:Dict[Tuple[str,...],Dict[str,float]],text:str) -> Dict[Tuple[str,...],Dict[str,float]]:
    words = text.split()
    #if the text has less words than are required in the key & value raise an exception.
    if (len(words)) <= (MARKOV_WORDS +1):
        raise ValueError(f"text has less than minimum number of words. Text: {text}, words needed: {MARKOV_WORDS + 1}")
    else:
        #store lines in a dictionary.
        for i in range(0,len(words)-MARKOV_WORDS):
            #because slices are just range objects, indexing stops at one prior to the end. for example, [0:2] in [0,1,2] will return [0,1]
            selected_words = tuple(words[i:i+MARKOV_WORDS])
            if selected_words not in markov_dict.keys():
                markov_dict[selected_words]={}
                markov_dict[selected_words][words[i+MARKOV_WORDS]] = 1.0
            else:
                if markov_dict[selected_words].get(words[i+MARKOV_WORDS]) is None:
                    markov_dict[selected_words][words[i+MARKOV_WORDS]] = 1.0
                else:
                    markov_dict[selected_words][words[i+MARKOV_WORDS]] += 1.0
    return markov_dict

#convert key frequencies to probabilities:
def convert_freq_to_prob(markov_dict:Dict[Tuple[str,...],Dict[str,float]]) -> Dict[Tuple[str,...],Dict[str,float]]:
    for key in markov_dict.keys():
        sum_of_tuple_freq = float(sum(markov_dict[key].values()))
        for entry in markov_dict[key].keys():
            #update the entry to be probability instead of frequency.
            markov_dict[key][entry] = round(markov_dict[key][entry]/sum_of_tuple_freq,2)
    return markov_dict

#Find a match using the markov dictionary and return that match.
#TODO: Update this so the key values are dictionaries instead of lists.
def find_match(markov_dict:Dict[Tuple[str,...],Dict[str,float]], novel:List[str] ) -> List[str]:

    #Look at the last two words and pick another word.
    check: Tuple[str,...] = tuple(novel[len(novel)-MARKOV_WORDS:len(novel)])
    if check in markov_dict.keys():
        possible_words = list(markov_dict[check].keys())
        probabilities = list(markov_dict[check].values()) 
        [adding] = random.choices(possible_words, weights = probabilities, k=1)
        novel.append(adding)
        return novel
    else:
        start_of_sentences = []
        #Select a new sentence:
        for key in markov_dict.keys():
            if "." in key[0]:
                start_of_sentences.append(key)
        select_next_sentence = random.choice(start_of_sentences)
        novel.append(select_next_sentence[1])
        for i in range(MARKOV_WORDS):
            for key in markov_dict.keys():
                if novel[-1] in key[0]:
                    novel.append(key[1])
                    break
        return novel
    raise ValueError("something went wrong. check novel: {novel}")


# Calls find_match to concatenate words onto the end of the novel. Returns the new "novel" generated by the Markov chain.
# TODO: Update this so the key values are dictionaries instead of lists.
def next_great_americian_novel(markov_dict:Dict[Tuple[str,...],Dict[str,float]],seed:List[str]) -> str:
    new_masterpiece = ""
    novel:List[str] = seed

    timer = 0
    
    #find matches
    while len(novel) <= NOVEL_LENGTH:
        novel = find_match(markov_dict, novel)

        timer += 1
        if timer > NOVEL_LENGTH:
            raise ValueError("infinite loop reached. {novel}")

    #Put the novel together:
    para_length = random.randint(4,8)
    i = 1
    formatted_novel = []
    for word in novel:
        if "." in word[-1]:
            if word in ["Mrs.","Mr.","Dr.","....",]:
                formatted_novel.append(word)
                pass
            else:
                if i%para_length == 0:
                    word +="\n\n"
                    #print(f'added new paragraph. word was: {word.rstrip()}, paragraph_length = {para_length}')
                    para_length = random.randint(4,8)
                    i = 1
                formatted_novel.append(word)
                i += 1
        else:
            formatted_novel.append(word)
    new_masterpiece += " ".join(formatted_novel)


    return new_masterpiece

def main(args:List[str]) -> int:

    markov_dict:Dict[Tuple[str,...],Dict[str,float]] = {}
    for arg in args[1:]:
        text = file_parse(arg)
        seed = text.split()[0:MARKOV_WORDS]
        markov_dict = markov_builder(markov_dict, text)

    markov_dict = convert_freq_to_prob(markov_dict)
    new_masterpiece = next_great_americian_novel(markov_dict,seed)

    print(new_masterpiece)
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))