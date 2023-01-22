# KohLantAsBot
Bot for KohLantAs

Bot créé pour la liste BDS 2023 KohLantAs, utilisant systemctl et flask

Installation:

Créer un compte développeur facebook, créer une app messenger, créer un token.
Mettre le bot sur serveur avec systemctl, update le token, et faire le webhook
(le bot doit être on pour que cela marche).
Demander à facebook l'autorisation pour que le bot puisse envoyer des messages (cela peut prendre 2-3 jours)
Mettre le bot en live.

En cas de difficultés demander à Jules Decaestecker ou Noé Loisil.

Remarques:

-Il n'y a pas de base de données, donc le bot se reset à chaque fois.

-J'ai un peu rush le bot, donc tout est dans un seul fichier, c'est donc pas trop lisible

-Il y a des artefacts des anciens cahiers des charges comme une troisième commande nommé dessert.

-Il y a un peu de restructuration à faire, notamment pour stocker les dialogues

-Il n'y a pas de commentaires, pour avoir de l'aide envoyez moi un message

-Le système n'utilise que l'id facebook pour identifier les gens, récupérer aussi le nom facebook peut-être pratique
notamment pour le support

Attention:
Par défaut systemctl m'a créé 3 workers, pensez à n'en mettre qu'un si vous souhaitez un bot cohérent
