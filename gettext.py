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


def distance_append(nodes, node1, node2):
    """
    nodes = [[node1, node2, distance], [...]]
    Ajoute deux noeuds à la liste ou, s'ils y sont déjà, incrémente la valeur de leur distance.
    """
    for n in nodes: #Pour chaque noeud
        if(n[0] == node1 and n[1] == node2): #Si l'arrête existe déjà
            n[2] += 1
            return
    nodes.append([node1, node2, 1])



def nodes_extract():
    """
    Retourne une liste de listes :
        nodes = [[node1, node2, distance], [...]]
    """
    nodes = []

    sentences = extract_sentences()
    for sentence in sentences: #Pour chaque phrase
        sentence_list = sentence.tolist()
        for i in range(0, len(sentence_list)-1): #Pour chaque mot
            node = [sentence_list[i], sentence_list[i+1], 1]
            distance_append(nodes, sentence_list[i], sentence_list[i+1])
    
    return nodes
    


def graph():
    G = nx.Graph()
    nodes = nodes_extract()

    #for n in nodes:
    #    G.add_edge(n[0], n[1])
    G.add_weighted_edges_from(nodes)
    print(len(nodes))
    print(len(G.edges))

    options = {
      'node_color' : 'red',
      'node_size'  : 7,
      'edge_color' : 'tab:gray',
      'with_labels': False
    }
    #nx.petersen_graph(G, with_labels = True,  pos=nx.spring_layout(G))
    plt.figure(figsize=(50,50))
    pos = nx.spring_layout(G,k=0.2, iterations=50) #50 : défaut
    nx.draw(G, pos, **options)
    plt.savefig("test.png")





if __name__ == '__main__':
    graph()

"""
A faire :
Séparer les phrases qui se terminent par des . ? ! ???
Créer les noeuds https://networkx.org/documentation/stable/tutorial.html ou bien https://pyvis.readthedocs.io/en/latest/tutorial.html
"""



"""
def graph(text):
    G=nx.Graph()
    # Separer les phrases avec ".","?","!","???""
    for w in sentences:
        sentence=text.split('.','?','!','???').clear()
        for i in words:
            try:
                G.nodes[i]['count']+=1
            except KeyError:
                G.add_node(i)
                G.nodes[i]['count']=1
            for j in words:
                if i==j or i in fin or j in fin:
                    continue
                if len(i)==0 or len(j)==0:
                    continue
                try:
                    G.edges[i,j]['count']+=1
                except KeyError:
                    G.add_edge(i,j, count=1)
    return G

# lire le texte et créer les noeuds à partir du texte
with open('aep1.txt') as f:
    text=f.read()
G=graph(text)

plt.figure()
nx.draw_networkx_edges(width=3, edge_color=blue, alpha=0.5, node_size=200) 
"""
# ne pas afficher les labels
# tuto delbot https://colab.research.google.com/drive/1ZR9H2PMFfgI6fvL8AONGD8H2LN_aUdiB?usp=sharing&pli=1#scrollTo=Wk5ZzO8Keynk

# outils de Paul https://tulip.labri.fr/TulipDrupal/ 
#              https://gephi.org/ qui place les sommets en fonction de leurs communautés.