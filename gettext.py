import os
import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize


def split(txt, seps):
    """ 
    Solution pour un split avec de multiples séparateurs, 
    comme spécifié ici https://stackoverflow.com/a/4697047/14320108
    
    Usage :
    >>> split('ABC ; DEF123,GHI_JKL ; MN OP', (',', ';'))
    ['ABC', 'DEF123', 'GHI_JKL', 'MN OP']
    """
    default_sep = seps[0]

    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]

def clear(string):
    """
    Avec une chaîne de caractères en entrée,
        - retire les '--',
        - retire les '\n',
        - retire les '\',
        - remplace les '\'' par des ''',
        - met tous les caractères en minuscule
        - sépare la phrase en une liste de mots
    Retourne la liste de mots.
    """

    return np.char.split( #Séparer les phrases en liste de mots. 
        np.char.lower( #Lowercase
            np.char.replace(
                re.sub(r"\\", '',
                    re.sub(r"\n", '', 
                        re.sub(r"--", '', string))),
                "\'", "'")
        )
    )


def extract_sentences():
    """
    Lit les fichiers dont le nom ressemble à 'epN.txt', extrait les phrases prononcées par Elliot ou Mr. Robot,
        en enlevant le nom du personnage du string et '\n' ; et retourne la liste de String obtenue.
    """
    sentences = []
    re_filename = re.compile("^\w{3}(?:.txt)$") #Noms de fichiers epN.txt
    re_line_Elliot_two_points = re.compile("^(?:ELLIOT: ).*$|(?:ELLIOT (.*): ).*$") #Pattern du fichier ep1.txt
    re_line_Elliot_two_points_Elliot = r"(?:ELLIOT: )|(?:ELLIOT (.*): )" #Retirer 'ELLIOT:'
    re_line_Robot_two_points = re.compile("^(?:MR. ROBOT: ).*$|(?:MR. ROBOT (.*): ).*$") #Pattern du fichier ep1.txt
    re_line_Robot_two_points_Robot = r"(?:MR. ROBOT: )|(?:MR. ROBOT (.*): )" #Retirer 'MR. ROBOT:'

    
    re_line_Elliot_break = re.compile("(?:ELLIOT\n).*$|(?:ELLIOT(.*)\n).*$") #Pattern des fichiers ep2.txt et ep3.txt
    re_line_Robot_break = re.compile("(?:MR ROBOT\n).*$|(?:MR ROBOT(.*)\n).*$") #Pattern des fichiers ep2.txt et ep3.txt


    for file in os.listdir(): #Chaque fichier

        if re_filename.match(file): #epN.txt
            with open(file, 'r') as f:
                lines = f.readlines()

                for i in range(0, len(lines)): #Chaque ligne

                    #Phrase 'ELLIOT: blabla'
                    if re_line_Elliot_two_points.match(lines[i]):
                        #On enlève 'ELLIOT:'
                        string = re.sub(re_line_Elliot_two_points_Elliot, '', lines[i])

                        #On récupère une liste de phrases séparées par ., ?, !, ???
                        sentences_in_string = split(string, ('.','?','!','???'))
                        for sentence in sentences_in_string:
                            #On ajoute ici une phrase à la liste de phrases. La phrase est une liste de mots.
                            sentences.append(clear(sentence))
                                

                    #Phrase 'MR. ROBOT: blabla'
                    elif re_line_Robot_two_points.match(lines[i]):
                        #On enlève 'MR. ROBOT:'
                        string = re.sub(re_line_Robot_two_points_Robot, '', lines[i])

                        #On récupère une liste de phrases séparées par ., ?, !, ???
                        sentences_in_string = split(string, ('.','?','!','???'))
                        for sentence in sentences_in_string:
                            #On ajoute ici une phrase à la liste de phrases. La phrase est une liste de mots.
                            sentences.append(clear(sentence))

                    #Phrase 'ELLIOT
                    #        blabla'
                    #ou
                    #       'MR. ROBOT
                    #        blabla'
                    # Dans ce cas on n'enlève rien, mais on récupère la deuxième ligne.
                    elif(re_line_Elliot_break.match(lines[i]) or re_line_Robot_break.match(lines[i])):

                        #On récupère une liste de phrases séparées par ., ?, !, ???
                        sentences_in_string = split(lines[i], ('.','?','!','???'))
                        for sentence in sentences_in_string:
                            #On ajoute ici une phrase à la liste de phrases. La phrase est une liste de mots.
                            sentences.append(clear(sentence))
    return sentences


def distance_append(nodes, node1, node2):
    """
    nodes = [[node1, node2, distance], [...]]
    Ajoute deux noeuds à la liste ou, s'ils y sont déjà, incrémente la valeur de leur distance.
    Futur : se renseigner sur '2.4 Generating Random Text with Bigrams' https://www.nltk.org/book/ch02.html
    """
    for n in nodes: #Pour chaque noeud
        if(n[0] == node1 and n[1] == node2): #Si l'arrête existe déjà
            n[2] += 1
            return
    nodes.append([node1, node2, 1])



def nodes_extract(sentences):
    """
    Retourne une liste de listes :
        nodes = [[node1, node2, distance], [...]]
    Ce sont des bigrams (https://www.wikiwand.com/fr/N-gramme)
    """
    nodes = []

    for sentence in sentences: #Pour chaque phrase
        sentence_list = sentence.tolist()
        for i in range(0, len(sentence_list)-1): #Pour chaque mot
            node = [sentence_list[i], sentence_list[i+1], 1]
            distance_append(nodes, sentence_list[i], sentence_list[i+1])
    return nodes
    


def graph(nodes):
    """
    Dessine un graphe et l'enregistre dans un fichier.
    Enregistre aussi un fichier gexf pour un usage dans Gephi.
    """
    G = nx.DiGraph()
    
    G.add_weighted_edges_from(nodes)

    options = {
      'node_color' : 'red',
      'node_size'  : 7,
      'edge_color' : 'tab:gray',
      'with_labels': False
    }

    plt.figure(figsize=(50,50))
    pos = nx.spring_layout(G,k=0.2, iterations=50) #50 : défaut
    nx.draw(G, pos, **options)
    plt.savefig("graphe.png")

    linefeed=chr(10)
    s = linefeed.join(nx.generate_gexf(G))
    with open("graphe.gexf", "w") as f:
        f.write(s)


"""
def sentence_generator():
    re_filename = re.compile("^\w{3}(?:.txt)$")
    for file in os.listdir(): #Pour chaque fichier
        if re_filename.match(file): # Si le fichier est en .txt
            with open(file, 'r') as f:
                robot=f.read() 
                keyword=robot.split()

                lists=[]
                for i in range(len(keyword)-1): # Pour chaque ligne
                    lists.append((keyword[i], keyword[i+1]))

                dictionnary={}
                for begin, end in lists:
                    if begin in dictionnary.keys():
                        dictionnary[begin].append(end)
                    else:
                        dictionnary[begin]=[end]

                first_word=np.random.choice(keyword)
                while first_word.islower():
                    first_word=np.random.choice(keyword)
                    chain=[first_word]
                    count=100
                    for i in range(count):
                        chain.append(np.random.choice(dictionnary[\
                            chain[-1]]))
                        sentences=' '.join(chain)
                    print(sentences)
                    
"""
                    
def sentence_generator():
    #nltk.download('punkt')
    re_filename = re.compile("^\w{3}(?:.txt)$")
    for file in os.listdir(): 
        if re_filename.match(file):
            with open(file, 'r') as f:
                robot=f.read() 
                keyword=word_tokenize(robot)
                #print(keyword)
                lists=[]
                for i in range(len(keyword)-1):
                    lists.append((keyword[i], keyword[i+1]))
                #print(lists)
                dictionnary={}
                for begin, end in lists:
                    if begin in dictionnary.keys():
                        dictionnary[begin].append(end)
                    else:
                        dictionnary[begin]=[end]
                #print(dictionnary)
                first_word=np.random.choice(keyword)
                while first_word.islower():
                    first_word=np.random.choice(keyword)
                    chain=[first_word]
                    count=100
                    for i in range(count):
                        chain.append(np.random.choice(dictionnary[\
                            chain[-1]]))
                        sentences=' '.join(chain)
                    print(sentences)


if __name__ == '__main__':
    sentences = extract_sentences()
    nodes = nodes_extract(sentences)
    graph(nodes)
    sentence_generator()
