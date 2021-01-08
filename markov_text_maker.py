import sys, re, random
from typing import Dict, List

#MARKOV_WORDS: number of words in dictionary keys. 
MARKOV_WORDS = 2

def file_parse(file:str) -> str:
    text1 = ""
    space = True
    with open(file,'r') as f:
        for line in f:
            if line.rstrip() == "":
                pass
            elif line.rstrip() =="Free eBooks at Planet eBook.com":
                pass
            elif line.rstrip() =="The Great Gatsby":
                #print(f"top of page found. {line.rstrip()}")
                pass
            elif re.fullmatch(r"([0-9]*)",line.rstrip()):
                #print(f"new page found: {line.rstrip()}")
                pass
            elif re.fullmatch(r"chapter (\w*)",line.rstrip().lower()):
                #print(f"new chapter found: {line.rstrip()}")
                pass
            elif line.rstrip()[-1] == "-":
                text1 += " "+line.rstrip()[:len(line.rstrip()) -1]
                #print(f'line ended in "-": {line}')
                space = False
            else:
                if space:
                    text1 +=" "+line.rstrip()
                else:
                    text1 += line.rstrip()
                    space = True
    return text1

def markov_builder(text2) -> Dict[str,List[str]]:
    markov_dict: Dict[str,List[str]] = {}
    sentences = text2.split(".")
    for sent in sentences:
        words = sent.split()
        i = 0
        if (len(words)) <= 1:
            pass
        else:
            #Choose a random words.
            location = random.randint(0,len(words)-MARKOV_WORDS)
            selected_words = " ".join(words[location:location+MARKOV_WORDS])
            if selected_words in markov_dict:
                markov_dict[selected_words].append(sent[sent.find(selected_words,i):]+".")
            else:
                markov_dict[selected_words] = [sent[sent.find(selected_words,i):]+"."]
        
    return markov_dict

def main(args) -> int:

    text1 = file_parse(args[1])
    text2 = file_parse(args[2])
    text1_sentences = text1.split(".")
    markov_dict = markov_builder(text2)
    next_great_americian_novel = []
    for sentence in text1_sentences:

        if random.choice([True,False]):
            i = 0
            sent_changes = []
            words = sentence.split()
            for i in range(len(words)-MARKOV_WORDS):
                check = " ".join(words[i:i+MARKOV_WORDS])
                if  check in markov_dict:
                    markov_split = random.choice(markov_dict[check])
                    #print(f"'{sentence[:sentence.find(check,i)]}' paired with:'{markov_split}' ")
                    sent_changes.append(sentence[:sentence.find(check,i)]+markov_split)
                i += len(check)

            if len(sent_changes) > 0:
                next_great_americian_novel.append("*** "+random.choice(sent_changes))
                #print(f'chose:\n {next_great_americian_novel[-1]}\n')
            else:
                next_great_americian_novel.append(sentence +".")
        else:
            next_great_americian_novel.append(sentence +".")
    #Time to assemble this great work:
    para_length = random.randint(4,8)
    new_masterpiece = ""
    for i in range(len(next_great_americian_novel)):
        new_masterpiece += next_great_americian_novel[i]
        if i%para_length == 0:
            new_masterpiece +="\n\n"
            para_length = random.randint(4,8)
    
    print(new_masterpiece)
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))