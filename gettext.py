import os
import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


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

                    #ELLIOT: blabla
                    if re_line_Elliot_two_points.match(lines[i]):
                        sentences.append(
                            clear(#On enlève 'ELLIOT:'
                                re.sub(
                                    re_line_Elliot_two_points_Elliot, '', lines[i])
                            )
                        )
                    #MR. ROBOT: blabla
                    elif re_line_Robot_two_points.match(lines[i]):
                        sentences.append(
                            clear(
                                re.sub(
                                    re_line_Robot_two_points_Robot, '', lines[i])
                            )
                        )
                    

                    #ELLIOT
                    #blabla
                    elif(re_line_Elliot_break.match(lines[i])):
                        sentences.append(
                            clear(lines[i+1])
                        )
                        
                    #MR. ROBOT
                    #blabla
                    elif re_line_Robot_break.match(lines[i]):
                        sentences.append(
                            clear(lines[i+1])
                        )
    return sentences


def nodes():
    """

    Retourne une liste de dictionnaires :
        {'noeud1': 'fuck', 'noeud2': 'society', 'count': '50'}
    """
    nodes = pd.DataFrame(columns=['noeud1', 'noeud2', 'count'])

    sentences = extract_sentences()
    for sentence in sentences: #Pour chaque phrase
        sentence_list = sentence.tolist()
        for i in range(0, len(sentence_list)-1): #Pour chaqe mot
            data = [sentence_list[i], sentence_list[i+1], 1]
            df = pd.Series(data, index=['noeud1', 'noeud2', 'count'])
            nodes = nodes.append(df, ignore_index=True)
    """
    print(nodes.isin(
        pd.Series(['hello', 'friend.'], index=['noeud1', 'noeud2'])
    ))
    """
    print(nodes.columns)
    #! je ne comprends pas comment vérifier si un subset existe. Il me faut spécifier les columns
    #! dans lesquelles recehrcher. Il faut incrémenter si le lien existe déjà. 
    #! puis il faudra prévenir networkx que ça existe.

"""
def graph():
    G = nx.Graph()
    

        G.add_nodes_from(sentence_list)
        
            

    #nx.petersen_graph(G, with_labels = True,  pos=nx.spring_layout(G)) 
    plt.savefig("test.png")


graph()"""


if __name__ == '__main__':
    nodes()

"""
A faire :
Séparer les phrases qui se terminent par des . ? ! ???

Créer les noeuds https://networkx.org/documentation/stable/tutorial.html ou bien https://pyvis.readthedocs.io/en/latest/tutorial.html
"""