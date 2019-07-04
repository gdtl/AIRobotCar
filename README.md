# AIRobotCar
Autonomous car race


Voici le fruit de notre projet AI Robot Car, qui se propose de construire à moindre coût une voiture autonome sur un circuit dessiné au sol, en utilisant les réseaux de neurones.
Ce projet s'inscrit dans une perspective de participation aux courses IronCar http://www.ironcar.org/.

Il utilise des ressources en open source développées par Vincent Houlbrèque https://github.com/vinzeebreak/ironcar et en particulier son simulateur de route https://github.com/vinzeebreak/road_simulator mais n'utilise pas la même connectique RaspberryPi-Moteurs (réduction du coût) ce qui nécessite un changement du code.

Toutes nos interfaces ont été codées en Python, ce qui est suffisant pour un traitement relativement lent (mais fonctionnel) des processus.


# HARDWARE

# What is the Raspberry Pi ?
Une Raspberry Pi est un micro-ordinateur à très bas coût développée par la fondation éponyme. Nous vous conseillons pour vous familiariser avec son fonctionnement de suivre les tutoriels écrits par Adafruit (https://learn.adafruit.com/series/learn-raspberry-pi). L'OS utilisé est Raspbian. Il s'agit d'une distribution de Linux. Quelques manipulations seront à effectuer à partir de la console de Raspbian (version de Debian pour la Rapsberry Pi), nous vous conseillons donc de vous familiariser avec le langage de la console. Ubuntu étant la distribution de Linux la plus connue et avec la communauté la plus active, il est fort heureux qu'elle repose sur Debian. Vous pourrez normalement résoudre l'intégralité de vos problèmes Linux en suivant les tutoriels Ubuntu. Evidemment, contrairement à un PC classique, une raspi n'est pas dotée d'un écran. Elle ne possède d'ailleurs initialement même pas d'OS. Il vous faudra burn, ie. imprimer Raspbian sur une carte SD (dont la taille dépend des caractéristiques de la Raspi). Je vous renvoie au paragraphe "initialisation de la Rapsberry Pi" dans la partie "Software" pour plus de détails. Si vous avez déjà un écran de PC, un clavier et une souris, grand bien vous en fasse, vous pouvez travailler directement une fois la carte SD insérée dans la Pi, et votre Pi branchée sur secteur ou sur une baterie portable, car ce n'est ni plus ni moins qu'un petit PC. Mais si vous n'avez pas tout ça, pas besoin d'acheter ce matériel, nous vous renvoyons vers le paragraphe "connexion à la Pi" dans la partie "Software".

# Raspberry Pi 3, 2 ou Zero ?
En fonction des coûts et des performances, on choisit de réaliser la voiture avec l'un de ces trois modèles de Raspi, de la plus performante à la moins performante.
La Raspberry Pi 2 n'est pas équipée de carte wifi, il faudra donc penser à acquérir un dongle wifi de ce type par exemple : https://www.amazon.com/gp/product/B003MTTJOY/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B003MTTJOY&linkCode=as2&tag=rapihq-20&linkId=7QAXDGG72H4EWYFB
ou utiliser directement une Raspberry Pi 3, aussi puissante qu'une 2, avec quasiment les mêmes caractéristiques techniques.

# Moteurs/Plateforme/Roues
Voilà l'équipement utilisé : https://www.amazon.fr/Yao-Chassis-Encoder-Battery-Arduino/dp/B07QLX4F6M/ref=sr_1_26?mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=robot+car+chassis+kit&qid=1562238775&s=gateway&sr=8-26 (ou tout modèle similaire en tapant "robot car kit" sur Amazon). Pour un budget très restreint, c'est très efficace, les moteurs sont suffisamment puissants pour que la voiture roule suffisamment vite à plein régime. Nous ne saurions que recommander de rajouter plus de piles pour alimenter les roues que celles prévues dans le package. En effet, l'utilisation du L293DNE (voir paragraphe suivant), impose une réduction de la tension aux bornes des roues par rapport à celle fournie par les piles. Autrement dit, les roues tournent beaucoup moins vite quand on rajoute le L293DNE. Nous avons réalisé notre test sur de la moquette, car c'est très facile à trouver (du moins ça l'était pour nous à CentraleSupélec), c'est peu cher, c'est transportable, et c'est suffisamment uniforme pour créer un circuit test convaincant. Il s'avère néanmoins que la moquette n'est pas une surface lisse, et que les roues vont vite accrocher dessus à cause de la perte de puissance. Il ne faut donc pas hésiter à rajouter des piles en série. Pour ceux dont les cours d'électrocinétique remontent à quelque temps, il s'agit dont de rajouter un boitié de piles en reliant le moins de ce boitier au plus d'une pile déjà présente, et le plus au moins, selon le schéma présent ici : https://www.myshop-solaire.com/guide-de-montage-des-batteries-en-serie-parallele-_r_80_a_20.html

# Contrôle des moteurs: GPIO, L293DNE et alimentation
Pour contrôler les moteurs à partir de la Rapsberry Pi, on utilise les sorties GPIO de la carte. Les tutoriels Adafruit sont largement suffisants pour en comprendre le fonctionnement, et il n'est pas nécessaire de tout connaître.
Le circuit intégré L293DNE produit par Texas Instruments (qu'on peut trouver ici https://fr.farnell.com/texas-instruments/l293dne/driver-peripheral-double-36v/dp/1470423) est un drive double pont-H. Le détail technique de ce composant électronique n'est pas important, nul besoin d'être un expert en micro-électronique. Ce qu'il faut savoir, c'est que le L293DNE est nécessaire si l'on souhaite produire un signal PWM (Pulse Width modulation) pour contrôler les moteurs. Il s'agit d'un mode de délivrance de tension qui consiste à envoyer périodiquement pendant une certaine durée un signal de tension non nul et fixe. Plus la durée du signal est grande, plus la puissance délivrée aux moteurs est élevée. Par exemple, si sur une période, le signal est non nul (5V en sortie de la Raspberry Pi) pendant 20% (respectivement 50%) du temps, la puissance délivrée aux moteurs sera 20% (respectivement 50%) de la puissance totale).
Pour plus de détails sur le montage du circuit autour du L293DNE qui en est la pièce principale, nous vons conseillons de suivre ce tutoriel : https://learn.adafruit.com/series/learn-raspberry-pi qui est probablement ce que nous avons trouvé de plus pédagogique et complet sur le sujet.

# Caméra
Pour piloter la voiture, le programme autonomous_race.py (celui qui permet à la voiture de se déplacer de manière autonome le long d'un circuit) a recours a la prise d'images de caméra, qu'il traite en temps réel grâce au module Python picamera (et c'est tout ce dont vous avez besoin). Nous vous conseillons d'utiliser une caméra fish-eye (grand angle) compatible Raspberry Pi telle que celle-ci https://www.amazon.fr/SainSmart-Module-175-Degree-Panoramic-Raspberry/dp/B01LH77Q74/ref=sr_1_3?mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=SainSmart+Wide+Angle+Raspberry+Pi+camera&qid=1562233671&s=gateway&sr=8-3 
Nous avons aussi testé notre programme avec une plus petite caméra, donc moins cher, mais l'angle latéral étant trop faible, la précision diminue énormément, puisqu'à chaque fois que la voiture s'éloigne un tant soit peu de la ligne du circuit, elle la perd complètement et ne peut se remettre sur le chemin.
Voilà un rapide tutoriel pour installer la caméra sur sa Rapsberry Pi : https://www.pihomeserver.fr/2014/01/09/raspberry-pi-home-server-installer-facilement-la-camera-raspberry-pi/
Et voilà un tutoriel pour se familiariser rapidement avec l'utilisation du module picamera : https://projects.raspberrypi.org/en/projects/getting-started-with-picamera

# Batterie portable
Il faut une batterie portable pour alimenter la Raspberry Pi que vous puissiez fixer sur le chassis. Essayez d'abord avec un très petit et léger modèle à très bas coût de ce type : https://www.amazon.fr/ningbao771-Multicolor-Optional-Portable-Powerbank/dp/B07MGB55TM/ref=sr_1_1?mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=small+power+bank&qid=1562239327&s=gateway&sr=8-1 et si ce n'est pas assez puissant, optez pour ce type de batterie portable peu chère et très légère https://www.amazon.fr/Xnuoyo-Portable-10000mAh-Chargeur-Batterie/dp/B07JFQBX5Z/ref=sr_1_51_sspa?mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=small+power+bank&qid=1562239327&s=gateway&smid=A2O4HM2RPZOZ14&sr=8-51-spons&psc=1

# Coût total
Farnell est un très bon fournisseur de composants électroniques, mais vous pourrez aussi trouver tout ce dont vous avez besoin chez Amazon
Résumons un peu tout le hardware dont vous aurez besoin et les coûts associés : 
- Raspberry Pi 2/3 ~ 30€
- Kit robot car (2 moteurs DC, chassis, roues, boîtier batterie) ~ 9€
- Boitier batterie supplémentaire, piles ~ 1€
- Circuit intégré L293DNE ~ 8€
- kit Breadboard et jumper cables (pour réaliser le circuit électronique)  ~ 5€
- Camera fish-eye ~ 25€
- Batterie portable ~ 1€<20€
Total ~ 80€

# SOFTWARE

# Initialisation de la Raspberry Pi
Il s'agit d'abord de brun Raspbian sur une carte SD. Cela peut se faire directement sur un PC, préférablement équipé de Linux (déjà parce que c'est simplement mieux que Windows, point) parce que ce sera beaucoup plus simple pour configurer le programme de Raspbian consacré à la connexion wifi de la raspi, pour pouvoir la contrôler à partir de votre PC. Le contrôle se faisant, là encore, beaucoup plus facilement à partir d'un PC sous Linux. Voici un guide d'installation de Raspbian sur la carte SD : https://www.raspberrypi.org/downloads/raspbian/ couplé avec https://www.raspberrypi.org/documentation/installation/installing-images/README.md

# Connexion à la Pi: Wifi/SSH
Pour contrôler la Rapsberry Pi depuis votre ordinateur préférablement sous Linux, vous pouvez utiliser un protocole de connexion SSH qui vous permet d'accéder à la console de la Pi. Voici un tutoriel très complet sur le sujet : https://raspbian-france.fr/controlez-raspberry-pi-ssh-ordinateur/
Une fois ceci fait, si vous préférez avoir accès à l'interface graphique de la Rapsberry Pi depuis votre ordinateur, vous pouvez utiliser le logiciel VNC sur linux, dont un tutoriel très complet est proposé par Adafruit : https://learn.adafruit.com/adafruit-raspberry-pi-lesson-7-remote-control-with-vnc
Si vous disposez d'un réseau wifi personnel fourni par une box, c'est très simple. Mais si vous souhaitez pouvoir utiliser votre voiture n'importe où, il vous faut pouvoir lancer le programme depuis un PC portable, ou même depuis votre téléphone si besoin. Dans les deux cas, il vous faut un réseau internet auquel puisse se connecter à la fois votre PC et votre Raspberry Pi. Quoi de mieux qu'un partage de connexion depuis votre smartphone ? Voilà un tutoriel qui vous permettra de configurer votre Raspi pour qu'elle se connecte directement à votre smartphone dès l'allumage, et pour éventuellement la contrôler depuis votre smartphone : https://alcalyn.github.io/raspberry-connectee-telephone/

# Installation des modules
Pour faire fonctionner les programmes Python du projet, vous aurez besoin d'installer différents modules sur votre raspi : 
- picamera
- time
- os
- numpy
- tqdm
- scipy
- Rpi.GPIO
- shutil
- tensorflow
- keras
Les deux modules/bibliothèques qui peuvent poser problème sont tensorflow et keras. En effet, il faut que leurs versions respectives soient compatibles. Techniquement, si vous installez les dernières versions de chacun des modules, vous ne devriez pas avoir de problème. Pour cela, nous vous conseillons de suivre le tutoriel de Vincent sur son GitHub.

# Essais de conduite de la voiture depuis une interface python
Pour tester les branchements des moteurs aux Batterie/L293/RaspberryPi, nous avons décidé de créer un code pour conduire la voiture. Cela permet aussi de calibrer la direction et la vitesse qui peuvent comporter une partie imprévisible, surtout avec du matériel bas de gamme. Nous avons utilisé un fichier python, et le module GPIO qui contrôle le courant en sortie des pins du GPIO sur la RaspberryPi (la double rangée de pins sur la Pi). On implémente la classe Motor pour définir les 2 moteurs dans le code et les pins qui leurs correspondent en sortie du GPIO. Puis on lance la fonction race(), de préférence depuis la console ssh sur l'ordinateur pour un temps de traitement plus faible. La vitesse se contrôle avec les touches 0 à 5 (0 arrêt, 5 vitesse maximale), la direction se fait grâce aux touches q/d pour gauche/droite, z/s pour devant/derrière, en appuyant à chaque fois sur entrée pour rentrer la commande, le programme attend une entrée avec la fonction input().
Le code est le suivant:


# Création du modèle, choix des paramètres
Le modèle contient plusieurs parties: Le simulateur de route, créé par Vincent Houlbrèque (cf introduction) crée des images virtuelles de route en simulant le sol et les lignes de la route avec différents effets permettant de se rapprocher d'images réelles de la course; le réseau de neurones qui prend ce dataset en entrée et crée un modèle pouvant prédire la direction associée à une image de route (direction que la voiture devrait prendre si elle se trouvait devant l'image de route prise en compte). 
A propos du simulateur de route: Plusieurs couches (layers) peuvent être ajoutées à l'instance roadsimulator de la classe Simulator(). La couche DrawLines dessine des lignes (on peut changer une partie des arguments (couleur, etc...), et en modifiant la classe DrawLines, on peut choisir si on veut dessiner seulement la ligne centrale, ou les lignes extérieures, si on veut des lignes en plus servant de "bruit", etc...).
La couche Perspective permet d'aplatir l'image initiale pour donner un effet de perspective pour ressembler à l'image réelle prise depuis une caméra censée être proche du sol. 
La couche Crop s'applique après la couche Perspective pour reprendre l'image aplatie et la recadrer en remplissant un rectangle entier, sans bandes noires sur le côté dûes à "Perspective". Attention aux dimensions des images transformées, qui doivent être les bonnes pour le traitement par le réseau de neurone ensuite. 
En exécutant le code, on peut créer le dataset avec l'instance roadsimulator à qui on a ajouté les layers.
En ce qui concerne le modèle: C'est un réseau de neurones créé avec keras fonctionnant sur TensorFlow, avec une partie dense et une partie convolutionnelle. Il est largement inspiré de celui de Vincent Houlbrèque préconisé sur le Readme de son Git RoadSimulator. Le modèle est assez simple, il fonctionne déjà très bien sur des images de route simple (avec une seule ligne noire devant la voiture), avec une accuracy de 95%. Pour les images de route plus compliquées (plusieurs couleurs, plusieurs lignes, ajout de lignes de bruitage...) le réseau ne donne pas une très bonne accuracy, il faut le modifier ou essayer un grand nombre d'epochs (>20), ou un grand nombre d'images (>2000), ce qui prend du temps en exécution.
Les codes pour le simulateur de route sont dans le dossier road_simulator-master. Le dossier ground_pics permet de donner au modèle des images du sol sur lequel a lieu la course pour créer des images plus fidèles à la réalité. 
Le code TEST Simulator.py permet de créer un modèle du type .h5, il faudra importer cette bibliothèque sur la Pi. Le modèle est déplacé sur la Pi et chargé dans le code utilisé pour la course (avec la bibliothèque Keras) pour prédire directement la direction en utilisant l'image prise par la caméra, avec model.predict().

# Lancement de la course
Le code pour le lancement de la course est le code automatic_run.py. 
Avec la bibliothèque keras on charge le modèle pour les prédictions. La bibliothèque PiCamera installée sur la Pi permet de récupérer les photos. On a décidé d'utiliser Python pour récupérer environ deux images par seconde (en photo et pas en stream continu), ce qui est suffisant pour une voiture lente mais très peu pour une voiture rapide. L'utilisation du module OpenCV pour récupérer les photos est conseillée (nous n'avons pas réussi à télécharger le module), pour éviter Python qui est très lent pour ce genre d'opérations système. On choisit d'appeler la fonction principale avec un nombre maximal d'images prises pour que la voiture s'arrête à un moment, et on spécifie ses vitesses en ligne droite et en virage (toujours entre 0 et 5). Pour chaque image prise par la caméra, (stockée dans Current_Pic (ne pas oublier de créer ce répertoire)), on stocke en plus cette image avec les autres dans le dossier Pictures, on prédit la direction grâce au modèle chargé, et on transforme cette direction (le résultat de la prédiction du réseau est une direction discrétisée en 5 valeurs: extrême gauche, gauche, tout droit, droite, extrême droite) en une commande de vitesse pour les roues. Puis on efface l'image de Current_Pic et on recommence, tant qu'on a pris moins d'images que le maximum fixé.
Le code de lancement de la course autonome:

# CONCLUSION
Nous avons tenté de résumer notre travail pour permettre de créer facilement une voiture autonome et surtout avoir l'occasion d'expérimenter Hardware et Software ce qui procure une bonne initiation à l'électronique, Linux, les protocoles de connexion, les réseaux de neurones, etc...
Les éléments d'amélioration sont: Eviter l'utilisation de Python pour récupérer les photos de la caméra (s'inspirer du code de Vincent H); Modifier le réseau pour obtenir une bonne accuracy sur des routes plus complexes.

Pour plus d'informations, toute question, contactez baptiste MOREAU-PERNET sur ce Github.

