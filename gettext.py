import os
import re
import numpy as np


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
                            np.char.split( #Séparer les phrases en liste de mots.
                                np.replace(
                                    re.sub( #On enlève 'ELLIOT:' et '\n'
                                        r"\n", '', re.sub(
                                            re_line_Elliot_two_points_Elliot, '', lines[i])
                                    ), "\'", "'"
                                )
                            )
                        )
                    #MR. ROBOT: blabla
                    elif re_line_Robot_two_points.match(lines[i]):
                        sentences.append(
                            re.sub(
                                r"\n", '', re.sub(
                                    re_line_Robot_two_points_Robot, '', lines[i])
                            )
                        )
                    

                    #ELLIOT
                    #blabla
                    elif(re_line_Elliot_break.match(lines[i])):
                        sentences.append(
                            re.sub(r"\n", '', lines[i+1])
                        )
                        
                    #MR. ROBOT
                    #blabla
                    elif re_line_Robot_break.match(lines[i]):
                        sentences.append(
                            re.sub(r"\n", '', lines[i+1])
                        )
    return sentences


sentences = extract_sentences()
print(sentences)



"""
A faire :
Séparer les phrases qui se terminent par des . ? ! ???
Enlever les '-', '\'
Séparer le nettoyage en une fonction clean()

Créer les noeuds https://networkx.org/documentation/stable/tutorial.html ou bien https://pyvis.readthedocs.io/en/latest/tutorial.html
"""