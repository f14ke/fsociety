f**k society.


## Installation
**Etape  1  :**  
Installer  un  IDE.  Voici  les  lignes  de  commandes  pour  installer  VisualStudio Code sur linux :
* 1.  Mettez a jour les packages et installez les dépendances
 $ sudo   apt   update
 $ sudo   apt   install   software−properties−common apt−transport−https wget
* 2.  Importez la clé Microsoft GPG
$ wget−q https://packages.microsoft.com/keys/microsoft.asc−O− sudo apt−key add−
*3. Activez le référentiel Visual Studio Code
$  sudo add−apt−repository  ”deb[ a r c h=amd64 ] https://packages.microsoft.com/repos/vscode stable main”
*4.  Installez Visual Studio Code
$ sudo   apt   update 
$ sudo   apt   install   code
**Etape 2 :** Installer python et pip
sudo apt−get update
sudo   apt−get   install python3.8  python3−pip
Etape 3 : Clonez le dépôt git. Utilisez cette option si vous avez configurer l’accès SSH à GitHub
git  clone   git@github.com:f14ke/fsociety.git 
Ou celle-là, sinon
git clone  https://github.com/f14ke/fsociety.git
Etape 4 : Mettez-vous dans le repertoire du projet, créez un environnement virtuelle
cd fsociety python3−m venv  env. env/bin/activate
Etape 5 : Installez les librairies nécessaires 
~fsociety$  pip  install  requierements.txt
~fsociety$  pip  install nltk
