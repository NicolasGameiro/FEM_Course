# FEM_Course

## Présentation du contenu

Ce dépot Git contient des cours sur la méthode des éléments finis (Finite Element Method en anglais d'où le FEM dans les noms de fichiers) avec des applications directes en code python.

Les applications sont sur des cas mécaniques notamments des structures en treillis et des poutres. L'objectif est de pouvoir modéliser une caténaire tout en initiant à la modélisation par la méthode des élèments finis.

## Structure dui git

L'arboresence du git est la suivante : 
- Le dossier "config" contient des fichiers .json qui permettront à l'avenir d'enregistrer des paramètres de simulation.
- Le dossier "gui" qui contient la version application des modèles éléments finis : pour l'instant, ce sont juste des tests du package "pyQt5" sur un notebook jupyter.
- Le dossier "Images" contient les images qui sont présentes dans les notebooks jupyter
- Le dossier "mesh" contient des fichiers de maillage qui peuvent être appelé par les notebooks : il contient actuellement des fichiers au format gmsh qui peuvent etre lus par une fonction et un fichier .txt qui peut être lu par une fonction aussi (le format de ce fichier n'est pas standard !)
- Le dossier "Notebooks" contient les script des différentes modélisation éléments finis : 
    * Barre_simple.ipynb : correspond à un script pour évaluer les frequences propres de la poutre
    * Modele_Barre_1D.ipynb : correspond à une modélisation élément fini 1D avec uniquement des efforts axiaux de type traction/compression
    * Modele_Barre_2D.ipynb : contient le modèle barre dans un espace 2D (attention les éléments sont toujours 1D)
    * Modele_Barre_3D.ipynb : contient le modèle barre dans un espace 2D (attention les éléments sont toujours 1D)
    * Modele_Euler_Bernoulli_2D.ipynb : correspond à une modélisation élément fini 1D avec uniquement les efforts tranchants (perpendiculaire à l'axe de la poutre) et de flexion (les moments) (attention les éléments sont toujours 1D)
    * Modele_Poutre_Catenaire.ipynb : contient une tentative de modélisation de caténaire pour des poutres basées sur le modèle Euler bernoulli
- Le dossier "Ressources" contient des fichiers python qui contient des fonctions d'autres projets personnels ou trouvés sur interne dnt je me suis inspiré pour construire mes notebooks
- Le dossier "src" contient des fonctions utilisées par les notebooks qui sont appelées par les lignes de commande "%run __chemin du fichier__"
- Le dossier "Test" contient des cas particuliers d'applications des scripts elements finis : On peut trouver par exemple un cas d'application sur une charpente.

## Avancement 

- [x] Feuille de calcul FEM 1D
  * [x] Modèle barre (uniquement efforts axiaux)
  * [x] Modèle poutre Euler Bernoulli (uniquement efforts tranchants et de flexions)
  * [x] Modèle poutre complet (efforts axiaux, tranchants et de flexions)
  * [x] Extension en 3D
- [ ] Feuille de calcul FEM 2D (en cours)
- [ ] Feuille de calcul FEM 3D (Pas sur que je le fasse)

## Sources 

Je me suis grandement basé sur les cours de Clayton Pettit sur Youtube qui applique la méthode des éléments finis à la mécanique : 
- <https://www.youtube.com/watch?v=IzUfWuh8B8Q> : Cours sur modéle Euler Bernoulli pour element 1D
- <https://www.youtube.com/watch?v=rl8QPPNrWSY> : Cours sur Solid Element
- <https://www.youtube.com/watch?v=WO158Hb9YZM> : Cours sur element triangulaire 2D
- <https://www.youtube.com/watch?v=paC9iEUZ2vY> : Cours sur element rectangulaire 2D
- <https://www.youtube.com/watch?v=gJzqCaOEqsA> : Cours sur element isoparametric et integration de gauss
- <https://www.youtube.com/watch?v=IHXtS66uok0> : Cours prise en compte des contraintes et contacts

### Sources pour modélisation éléments finis 1D

* [1]: <https://www.youtube.com/watch?v=1Wv-S6OCsPY> Je me suis grandement inspiré des excellentes vidéos de Mike Foster sur Youtube
* [2]: <https://www.yyy> Vidéo modélisation poutre de Euler Bernoulli
* [3]: <https://www.youtube.com/watch?v=eReuOiF_96k> Vidéo modélisation poutre de Timoshenko
* [x]: <> yyy

### Sources pour modélisation éléments finis 2D

* [1]: <https://www.youtube.com/watch?v=kIiVQirjvyo> Vidéo modélisation FEM 2D - Mesh 2D
* [2]: <https://www.youtube.com/watch?v=Ey2C_6eYyc4> Vidéo modélisation FEM 2D - Stiffness
* [3]: <https://www.youtube.com/watch?v=5wNrMYjPDjc> Vidéo modélisation FEM 2D - Calcul
* [4]: <https://www.youtube.com/watch?v=yVue3U0FFKQ> Vidéo modélisation FEM 2D - Post
* [5]: <https://www.youtube.com/watch?v=TusCNRUfDPw> Vidéo modélisation plaque flechissante
