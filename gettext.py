import os
import re

re_filename = re.compile("^\w{3}(?:.txt)$") #Noms de fichiers epN.txt
re_line_Elliot_two_points = re.compile("^(?:ELLIOT: ).*$|(?:ELLIOT (.*): ).*$") #Pattern du fichier ep1.txt
re_line_Elliot_two_points_Elliot = r"(?:ELLIOT: )|(?:ELLIOT (.*): )" #Retirer 'ELLIOT:'
re_line_Robot_two_points = re.compile("^(?:MR. ROBOT: ).*$|(?:MR. ROBOT (.*): ).*$") #Pattern du fichier ep1.txt
re_line_Robot_two_points_Robot = r"(?:MR. ROBOT: )|(?:MR. ROBOT (.*): )" #Retirer 'MR. ROBOT:'

 
re_line_Elliot_break = re.compile("(?:ELLIOT\n).*$|(?:ELLIOT(.*)\n).*$") #Pattern des fichiers ep2.txt et ep3.txt
re_line_Robot_break = re.compile("(?:MR ROBOT\n).*$|(?:MR ROBOT(.*)\n).*$") #Pattern des fichiers ep2.txt et ep3.txt


for file in os.listdir():
    if re_filename.match(file):
        with open(file, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):

                #ELLIOT: blabla
                if re_line_Elliot_two_points.match(lines[i]):
                    print(re.sub(re_line_Elliot_two_points_Elliot, '', lines[i]))
                #MR. ROBOT: blabla
                if re_line_Robot_two_points.match(lines[i]):
                    print(re.sub(re_line_Robot_two_points_Robot, '', lines[i]))
                

                #ELLIOT
                #blabla
                if(re_line_Elliot_break.match(lines[i])):
                    print(lines[i+1])
                #MR. ROBOT
                #blabla
                if re_line_Robot_break.match(lines[i]):
                    print(lines[i+1])
