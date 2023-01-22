from flask import Flask,request
import requests
import time
app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'TOKEN_FACEBOOK'

API = "https://graph.facebook.com/v13.0/me/messages?access_token="+PAGE_ACCESS_TOKEN

@app.route("/", methods=['GET'])
def fbverify():
    if request.args.get("hub.mode") == "subscribe" and requests.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")== "anystring":
            return "Verification token missmatch", 403
        return requests.args['hub.challenge'], 200
    return "Hello world", 200

CRUMBLE = 85
nb_crumble = 0
CRAQUELES = 160
nb_craqueles = 0


TIMER = 1800
CODES_VIP = ["4Lp","g4z","pp8","rS7","Ds4","aTT","z8L","Qr9","Cr7","Kb9","f5t"]

VIP_ALERTE = []

def time_to_horo(t):
    delta = int(time.time()-t)
    minutes = delta // 60
    secondes = delta % 60
    if minutes == 0:
        return str(secondes) + "s"
    return str(minutes) + "m" + str(secondes) + "s"

#context

def request_text(sender_id,text):
    return {
                    "recipient": {
                        "id": sender_id
                    },
                    "message": {
                        "text": text
                    }
                }

def request_test(sender_id,text):
    return [request_text(sender_id,text),request_text(sender_id,text)]

def request_quick(sender_id,text,choices):
    quicks = []
    for choice in choices:
        quicks.append({
                            "content_type": "text",
                            "title": choice,
                            "payload": "<POSTBACK_PAYLOAD>"
                        })
    return {
                "recipient": {
                    "id": sender_id
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": text,
                    "quick_replies": quicks
                }
            }

def help(sender_id):
    request_body =  request_text(sender_id,"Veuillez contacter Noé LOISIL en cas de problème\nBonne journée !")
    return requests.post(API, json=request_body).json()


def default(sender_id):
    request_body =  request_text(sender_id,"Désolé je ne comprends pas")
    return requests.post(API, json=request_body).json()

def liste_vip(sender_id):
    text = "Liste des vips:\n"
    for vip in VIPS:
        text += str(vip)+"\n"
    request_body =  request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def newvip(sender_id):
    request_body = request_text(sender_id,"Vous êtes maintenant vip !")
    return requests.post(API, json=request_body).json()

# admin
def login(sender_id,id):
    request_body =  request_text(sender_id,str(id) + " veuillez rentrer le mot de passe administrateur")
    return requests.post(API, json=request_body).json()

def admin_incorrect(sender_id):
    request_body =  request_text(sender_id,"Mot de passe incorrect, veuillez retaper login pour retenter")
    return requests.post(API, json=request_body).json()

def enrengistrement_administrateur(sender_id):
    request_body =  request_quick(sender_id,"Vous êtes maintenant enrengistré en tant qu'administrateur, veuillez selectionner votre rôle",["Cuisinier","Livreur","Support","Noé"])
    return requests.post(API, json=request_body).json()

def admin_leave(sender_id):
    request_body = request_text(sender_id,"Vous êtes totalement deconnecté, à bientôt")
    return requests.post(API, json=request_body).json()

def admin_interaction(sender_id,username):
    request_body = request_text(sender_id,"Interactions avec " + username + " reintialisés")
    return requests.post(API, json=request_body).json()

def admin_role_incorrect(sender_id):
    request_body =  request_quick(sender_id,"Veuillez selectionner votre rôle",["Cuisinier","Livreur","Support","Noé"])
    return requests.post(API, json=request_body).json()


#noé

def admin_role_noe(sender_id):
    request_body = request_quick(sender_id,"Vous êtes sur ?",["Oui","Annuler"])
    return requests.post(API, json=request_body).json()

def admin_noe_erreur(sender_id):
    request_body = request_text(sender_id,"Nope")
    return requests.post(API, json=request_body).json()

def admin_noe_accueil(sender_id):
    request_body = request_text(sender_id,"Salut Noé")
    return requests.post(API, json=request_body).json()

def admin_noe_incorrect(sender_id):
    request_body = request_quick(sender_id,"Es-tu Noé ?",["Oui","Annuler"])
    return requests.post(API, json=request_body).json()

def admin_noe_dump_error(sender_id):
    text = ""
    if len(errors) == 0:
        text = "Pas d'erreurs"
    else:
        text = str(len(errors)) + " erreurs:\n"
        for err in errors:
            text += err + "\n"
        errors = []
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_noe_dump_data(sender_id,id):
    if id in id_to_sender:
        s_id = id_to_sender[id]
        user = users[s_id]
        text = "Utilisateur " + str(id) +"\n"
        text += "sender_id = " + str(s_id) + "\n"
        text += "derniere commandes: " + str(time.time()-user[USER_LASTCOMMAND]) + "\n"
        text += "contexte: " + user[USER_CONTEXT] + "\n"
        text += "Crumble: " + user[USER_CRUMBLE] + "\n"
        text += "Craqueles: " + user[USER_CRAQUELES] + "\n"
        text += "prenom: " + user[USER_PRENOM] + "\n"
        text += "batiment: " + user[USER_BATIMENT] + "\n"
        text += "chambre: " + user[USER_CHAMBRE] + "\n"
        text += "infos supps: " + user[USER_INFOS_SUPP] + "\n"
        request_body = request_text(sender_id,text)
        return requests.post(API, json=request_body).json()
    text = "Erreur, vous n'existez pas"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_noe_dump_cuisinier(sender_id,id):
    if id in id_to_sender:
        s_id = id_to_sender[id]
        user = cuisiniers[s_id]
        text = "Cuisinier " + str(id) +"\n"
        text += "sender_id = " + str(s_id) + "\n"
        text += "cuisine: " + user[1] + "\n"
        request_body = request_text(sender_id,text)
        return requests.post(API, json=request_body).json()
    text = "Erreur, vous n'existez pas"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_noe_activites(sender_id):
    text = "Liste des connectés au réseau :\n"
    text += str(len(users)) + " users:\n"
    for user in users.values():
        text += "id: " + str(user[USER_ID]) + " | " + str(id_to_sender[user[USER_ID]]) + "\n"
    text += str(len(livreurs)) + " livreurs:\n"
    for livreur in livreurs.values():
        text += "id: " + str(livreur[0]) + " | " + str(id_to_sender[livreur[0]]) + "\n"

    text += str(len(cuisiniers)) + " cuisiniers:\n"
    for cuisinier in cuisiniers.values():
        text += "id: " + str(cuisinier[0]) + " | " + str(id_to_sender[cuisinier[0]]) + "\n"

    text += str(len(livreurs)) + " supports:\n"
    for supp in supports.values():
        text += "id: " + str(supp[0]) + " | " + str(id_to_sender[supp[0]]) + "\n"

    text += str(len(noe)) + " noés:\n"
    for nono in noe.values():
        text += "id: " + str(nono) + " | " + str(id_to_sender[nono]) + "\n"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_noe_isvip(sender_id,id):
    text = ""
    if id_to_sender[id] in VIPS:
        text = "l'utilisateur " + str(id) + " est un vip"
    else:
        text = "l'utilisateur " + str(id) + " n'est pas un vip"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_noe_addvip(sender_id,id):
    text = "l'utilisateur " + str(id) + " est maintenant un vip"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_noe_listvip(sender_id):
    text = str(len(VIPS)) + " vips:\n"
    for vip in VIPS:
        text += str(vip) + "\n"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_noe_dump_commandes(sender_id):
    return admin_cuisinier_commandes(sender_id)

def admin_noe_dump_user(sender_id,id):
    return admin_noe_dump_data(sender_id,id)

def admin_noe_reset(sender_id):
    request_body = request_text(sender_id,"Base de donnée reintialisé")
    return requests.post(API, json=request_body).json()

#livreurs

def admin_role_livreur(sender_id):
    request_body = request_quick(sender_id,"Welcome to UbeLantAs",["Continuer","Annuler"])
    return requests.post(API, json=request_body).json()

def admin_accueil_livreur(sender_id):
    request_body = request_text(sender_id,"A partir de maintenant, vous pouvez prendre des commandes. Tapez \"x\" pour prendre x commandes. Pour être averti de l'arrivée d'une nouvelle commande, tapez \"suivant\". Pour prendre juste une nouvelle commande tapez \"1\".\n")
    return requests.post(API, json=request_body).json()

def admin_role_livreur_incorrect(sender_id):
    request_body = request_quick(sender_id,"Veux tu continuer ?",["Continuer","Annuler"])
    return requests.post(API, json=request_body).json()

def admin_livreur_commande_zero(sender_id):
    request_body = request_text(sender_id,"Il n'y a aucune commande à prendre actuellement, pour être averti de l'arrivé d'une commande, tapez \"suivant\"")
    return requests.post(API, json=request_body).json()

def admin_livreur_commande_erreur(sender_id):
    request_body = request_text(sender_id,"Mauvaise entrée")
    return requests.post(API, json=request_body).json()

def admin_livreur_commande_one(sender_id,infos):
    text = "Une livraison vous a été attribué :\n"
    text += "Crumble: " + infos[3] + "\n"
    text += "Craqueles: " + infos[5] + "\n"
    text += "Prénom: " + infos[0] + "\n"
    text += "Batiment: " + infos[1] + "\n"
    text += "Chambre: " + infos[2] + "\n"
    if infos[8] != "":
        text += "Infos supp: " + infos[8] + "\n"
    text += "Il y a " + time_to_horo(infos[7]) + "\n"
    if infos[4] in VIP_ALERTE:
        text += "C'est un VIP !\n"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_livreur_x(sender_id,infos):
    text = str(len(infos)) + " livraisons vous ont été attribués :\n"
    request_body = request_text(sender_id,text)
    requests.post(API, json=request_body).json()
    index = 0
    for info in infos:
        index += 1
        text = ""
        text += "Livraison " + str(index) + ":\n"
        text += " Crumble: " + info[3] + "\n"
        text += " Craqueles: " + info[5] + "\n"
        text += " Prénom: " + info[0] + "\n"
        text += " Batiment: " + info[1] + "\n"
        text += " Chambre: " + info[2] + "\n"
        if info[8] != "":
            text += "Infos supp: " + info[8] + "\n"
        text += "Il y a " + time_to_horo(info[7]) + "\n"
        if info[4] in VIP_ALERTE:
            text += "C'est un VIP !\n\n"
        request_body = request_text(sender_id,text)
        requests.post(API, json=request_body).json()
    return "Ca marche pas", 200

def admin_livreur_notification(sender_id):
    request_body = request_text(sender_id,"Une nouvelle livraison est disponible !\nLes notifications sont maintenant désactivés pour vous")
    return requests.post(API, json=request_body).json()

def admin_livreur_activer_notification(sender_id):
    request_body = request_text(sender_id,"Vous recevrez une notification quand une nouvelle livraison sera disponible")
    return requests.post(API, json=request_body).json()

def admin_livreur_desactiver_notification(sender_id):
    request_body = request_text(sender_id,"Vous ne recevrez pas de notification quand une nouvelle livraison sera disponible")
    return requests.post(API, json=request_body).json()

def admin_livreur_erreur(sender_id):
    request_body = request_text(sender_id,"Moi pas comprendre")
    return requests.post(API, json=request_body).json()

#cuisinier

def admin_role_cuisinier(sender_id):
    request_body = request_quick(sender_id,"Cool, Veux tu continuer ?",["Continuer","Annuler"])
    return requests.post(API, json=request_body).json()

def admin_accueil_cuisinier(sender_id):
    request_body =  request_text(sender_id,"Bienvenue, à partir de maintenant vous recevrez les commandes vous concernant\nTaper help pour les commandes")
    return requests.post(API, json=request_body).json()

def admin_role_cuisinier_incorrect(sender_id):
    request_body = request_quick(sender_id,"Veux tu continuer ?",["Continuer","Annuler"])
    return requests.post(API, json=request_body).json()

def admin_cuisinier_help(sender_id):
    request_body =  request_text(sender_id,"Pour des informations à propos du rôle cuisinier, appeller Noé")
    return requests.post(API, json=request_body).json()

def admin_cuisinier_erreur(sender_id):
    request_body =  request_text(sender_id,"Une erreur a eu lieu, veuillez contacter Noé")
    return requests.post(API, json=request_body).json()

def admin_cuisinier_notification(sender_id,infos):
    text = "Une commande vous a été attribué :\n"
    text += "Crumble: " + infos[3] + "\n"
    text += "Craqueles: " + infos[5] + "\n"
    text += "Prénom: " + infos[0] + "\n"
    text += "Id: " + str(sender_to_id[infos[4]]) + "\n"
    text += "Batiment: " + infos[1] + "\n"
    text += "Chambre: " + infos[2] + "\n"
    if infos[8] != "":
            text += "Infos supp: " + infos[8] + "\n"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()


# support

def admin_accueil_support(sender_id):
    request_body = request_text(sender_id,"A partir de maintenant, vous allez être notifié en cas de problème")
    return requests.post(API, json=request_body).json()
    
def admin_support_notification(sender_id,username):
    request_body = request_text(sender_id,"Besoin d'un support, " + str(username) + " a besoin d'aide")
    return requests.post(API, json=request_body).json()

def admin_support_idle(sender_id):
    request_body = request_text(sender_id,"Pas d'interaction bot pour le support")
    return requests.post(API, json=request_body).json()

def admin_reset_succefull(sender_id,username):
    request_body = request_text(sender_id,"Les données de " + username + "ont été effacés")
    return requests.post(API, json=request_body).json()

def admin_reset_failure(sender_id,username):
    request_body = request_text(sender_id,username + "n'est pas un utilisateur")
    return requests.post(API, json=request_body).json()

# UI

def support_technique(sender_id):
    request_body = request_quick(sender_id,"Voulez vous contacter un support ?",["Oui","Non"])
    return requests.post(API, json=request_body).json()

def support_technique_repeat(sender_id):
    request_body = request_quick(sender_id,"Voulez vous contacter un support ?",["Oui","Non"])
    return requests.post(API, json=request_body).json()

def contact_technique(sender_id):
    request_body = request_text(sender_id,"Quelqu'un va venir vous contacter, veuillez attendre quelques instants\nLes interactions avec le bot ont été désactivés")
    return requests.post(API, json=request_body).json()

def bienvenue(sender_id,id):
    request_body = request_quick(sender_id,"Bienvenue dans les allos de Koh LantAs " + str(id) + " !\nNous proposons un service de livraison de nourriture gratuite !\nNous servons du crumble et des craquelés !\nVoulez vous commander ?",["Oui","Non","Annuler"])
    return requests.post(API, json=request_body).json()

def au_revoir(sender_id):
    request_body = {
        "recipient": {
            "id" : sender_id
        },
        "message": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": "https://i.kym-cdn.com/photos/images/masonry/001/305/803/48d.png",
                            "is_reusable": True
                        }
                    }
                }
    }
    return requests.post(API, json=request_body).json()

def bienvenue_repeat(sender_id):
    request_body = request_quick(sender_id,"Désolé je n'ai pas bien compris votre réponse, pour répondre, veuillez cliquer si l'une des options ci dessous", ["Oui","Non","Annuler"])
    return requests.post(API, json=request_body).json()

def crumble(sender_id):
    if nb_craqueles >= CRAQUELES:
        request_body = request_quick(sender_id,"Voulez-vous du crumble ?",["Oui"] + ["Annuler"])
        return requests.post(API, json=request_body).json()
    request_body = request_quick(sender_id,"Voulez-vous du crumble ?",CHOIX_CRUMBLE + ["Annuler"])
    return requests.post(API, json=request_body).json()

def crumble_aide(sender_id):
    return support_technique(sender_id)

def crumble_repeat(sender_id):
    if nb_craqueles >= CRAQUELES:
        request_body = request_quick(sender_id,"Désolé je n'ai pas bien compris votre réponse, pour repondre, veuillez cliquer si l'une des options ci dessous, Voulez-vous du crumble ?",["Oui"] + ["Aide"])
        return requests.post(API, json=request_body).json()
    request_body = request_quick(sender_id,"Désolé je n'ai pas bien compris votre réponse, pour repondre, veuillez cliquer si l'une des options ci dessous, Voulez-vous du crumble ?",CHOIX_CRUMBLE + ["Aide"])
    return requests.post(API, json=request_body).json()

def croque_fruits_rouges(sender_id):
    text = ""
    if nb_crumble >= CRUMBLE and nb_craqueles >= CRAQUELES:
        text = "Voulez vous un croque fruits rouges ?"
        request_body = request_quick(sender_id,text,["Oui"] + ["Annuler"])
        return requests.post(API, json=request_body).json()
    if users[sender_id][USER_CRUMBLE] == "Oui":
        if users[sender_id][USER_CRAQUELES] == "Oui":
            text = "Vous avez choisis un croque nut et un croque framboise, voulez vous aussi un croque fruits rouges ?"
        else:
            text = "Vous avez choisis un croque nut, voulez vous aussi un croque fruits rouges ?"
    else:
        if users[sender_id][USER_CRAQUELES] == "Oui":
            text = "Vous avez choisis un croque framboise, voulez vous aussi un croque fruits rouges ?"
        else:
            text = "Vous n'avez pas choisis de croques pour l'instant, voulez vous aussi un croque fruits rouges ?"
            request_body = request_quick(sender_id,text,["Oui"] + ["Changer la commande","Annuler"])
            return requests.post(API, json=request_body).json()
    request_body = request_quick(sender_id,text,CHOIX_FRUITS_ROUGES + ["Changer la commande","Annuler"])
    return requests.post(API, json=request_body).json()

def croque_fruits_rouges_aide(sender_id):
    return support_technique(sender_id)

def croque_fruits_rouges_repeat(sender_id):
    if nb_crumble >= CRUMBLE and nb_craqueles >= CRAQUELES:
        request_body = request_quick(sender_id,"Je n'ai pas compris. Vous pouvez choisir un croque fruits rouges si vous désirez.",CHOIX_FRUITS_ROUGES + ["Annuler"])
        return requests.post(API, json=request_body).json()
    request_body = request_quick(sender_id,"Je n'ai pas compris. Vous pouvez choisir un croque fruits rouges si vous désirez.",CHOIX_FRUITS_ROUGES + ["Changer la commande","Annuler"])
    return requests.post(API, json=request_body).json()


def prenom(sender_id):
    request_body = request_text(sender_id,"Pour la livraison, nous avons besoin de quelques informations\nEn premier, quel est votre prénom ?")
    return requests.post(API, json=request_body).json()

def prenom_incorrect(sender_id):
    request_body = request_text(sender_id,"Je n'ai pas compris votre prénom, pouvez vous réessayer ?")
    return requests.post(API, json=request_body).json()

def prenom_aide(sender_id):
    return support_technique(sender_id)

def batiment(sender_id):
    request_body = request_quick(sender_id,"Nous avons aussi besoin de votre batiment pour la livraison, c'est lequel ?",BATIMENTS)#+["Aide"])
    return requests.post(API, json=request_body).json()

def batiment_incorrect(sender_id):
    request_body = request_quick(sender_id,"Je n'ai pas compris votre bâtiment, c'est lequel ?",BATIMENTS)
    return requests.post(API, json=request_body).json()

def batiment_aide(sender_id):
    return support_technique(sender_id)

def chambre(sender_id):
    if users[sender_id][USER_BATIMENT] == "Autre" or users[sender_id][USER_BATIMENT] == "Arpej":
        request_body = request_text(sender_id,"Où es tu ?")
        return requests.post(API, json=request_body).json()
    request_body = request_text(sender_id,"Maintenant j'ai besoin du numéro de ta chambre, quelle est ta chambre ?\n (0 pour la cuisine)")
    return requests.post(API, json=request_body).json()

def chambre_incorrect(sender_id):
    if users[sender_id][USER_BATIMENT] == "Autre" or users[sender_id][USER_BATIMENT] == "Arpej":
        request_body = request_text(sender_id,"Je n'ai pas compris, où es tu ?")
        return requests.post(API, json=request_body).json()
    request_body = request_text(sender_id,"Je n'ai pas compris ta chambre, peux tu répéter le numéro de ta chambre  ?\n (0 pour la cuisine)")
    return requests.post(API, json=request_body).json()

def chambre_aide(sender_id):
    return support_technique(sender_id)

def commande_prise(sender_id):
    request_body = request_text(sender_id,"Votre commande a été prise en compte, elle arrivera bientôt, vous pouvez connaître votre position dans la liste d'attente en parlant au bot\nBonne soirée !")
    return requests.post(API, json=request_body).json()

def cuisine_en_cours(sender_id,position):
    request_body = request_quick(sender_id,"Votre commande est en cours de préparation, vous êtes en position " + str(position) + " dans la liste d'attente",["Aide"])
    return requests.post(API, json=request_body).json()

def cuisine_aide(sender_id):
    return support_technique(sender_id)

def livraison_en_cours(sender_id):
    request_body = request_quick(sender_id,"Votre commande est en cours de livraison, elle arrivera bientôt",["Annuler"])
    return requests.post(API, json=request_body).json()

def timeout(sender_id):
    request_body = request_quick(sender_id,"Vous avez déjà commandé recemment, veuillez réessayer plus tard",["Aide"])
    return requests.post(API, json=request_body).json()
# data commandes


def admin_stop(sender_id):
    request_body = request_text(sender_id,"Le système a arrêter de prendre les commandes")
    return requests.post(API, json=request_body).json()

def admin_hard_stop(sender_id):
    request_body = request_text(sender_id,"Le système a arrêter de prendre les commandes et annulé celles en cours")
    return requests.post(API, json=request_body).json()

def admin_already_stopped(sender_id):
    request_body = request_text(sender_id,"Le système a déjà arrêté de prendre les commandes")
    return requests.post(API, json=request_body).json()

def admin_remove_item(sender_id,item):
    request_body = request_text(sender_id,"Le système a enlevé " + item + " de son menu, les utilisateurs en train de lancer une commande avec cet item ont été retournés au menu principal")
    return requests.post(API, json=request_body).json()

def admin_remove_item_erreur(sender_id,item):
    request_body = request_text(sender_id,"L'item " + item + " n'existe pas")
    return requests.post(API, json=request_body).json()

def admin_add_item(sender_id,item,group):
    request_body = request_text(sender_id,"L'item " + item + " a été ajouté dans " + group)
    return requests.post(API, json=request_body).json()

def commande_annule(sender_id):
    request_body = request_text(sender_id,"Désolé, le système vient d'arrêter de prendre des commandes, veuillez essayer plus tard")
    return requests.post(API, json=request_body).json()

def system_ferme(sender_id):
    request_body = request_text(sender_id,"Désolé, on n'a plus de stocks, bonne soirée !")
    return requests.post(API, json=request_body).json()

def rupture_stock(sender_id,item):
    request_body = request_text(sender_id,"Désolé, l'item " + item + " vient d'entrer en rupture de stock")
    return requests.post(API, json=request_body).json()

def craqueles(sender_id):
    if nb_crumble < CRUMBLE:
        if users[sender_id][USER_CRUMBLE] == "Non":
            request_body = request_quick(sender_id,"Vous n'avez pas choisi de crumble, voulez-vous un craquelé ?",["Oui"] + ["Annuler"])
            return requests.post(API, json=request_body).json()
        request_body = request_quick(sender_id,"Vous avez choisi du crumble, Voulez-vous aussi un craquelé ?",CHOIX_CRAQUELES + ["Annuler"])
        return requests.post(API, json=request_body).json()
    else:
        request_body = request_quick(sender_id,"Voulez-vous un craquelé ?",["Oui"] + ["Annuler"])
        return requests.post(API, json=request_body).json()

def craqueles_repeat(sender_id):
    if users[sender_id][USER_CRUMBLE] == "Non":
        request_body = request_quick(sender_id,"Je n'ai pas bien compris, voulez vous un craquelé ?",["Oui"] + ["Annuler"])
        return requests.post(API, json=request_body).json()
    request_body = request_quick(sender_id,"Je n'ai pas bien compris, voulez vous un craquelé ?",CHOIX_CRAQUELES + ["Annuler"])
    return requests.post(API, json=request_body).json()

def custom(sender_id,text):
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def craqueles_aide(sender_id):
    return support_technique(sender_id)

def admin_cuisinier_commandes(sender_id):
    text = "Il y a actuellement " + str(len(commandes)) + " commandes en cours\n"
    request_body = request_text(sender_id,text)
    requests.post(API, json=request_body).json()
    text = ""
    for i in range(len(commandes)):
        commande = commandes[i]
        text += commande[0] + " ; " + commande[1] + " ; " + commande[2] + " ; " + commande[3] + " ; " + commande[5] + " ; " + commande[6] + " ; " + time_to_horo(commande[7]) + " ; " + commande[8] + "\n"
        if i%20 == 19 and i != len(commandes)-1: 
            request_body = request_text(sender_id,text)
            requests.post(API, json=request_body).json()
            text = ""
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_cuisinier_nbcommandes(sender_id):
    text = "Il y a actuellement " + str(len(commandes)) + " commandes en cours\n"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_cuisinier_passedcommandes(sender_id):
    text = "Il y a eu " + str(len(passed_commandes)) + " commandes passées\n"
    request_body = request_text(sender_id,text)
    requests.post(API, json=request_body).json()
    text = ""
    for i in range(len(passed_commandes)):
        commande = passed_commandes[i]
        text += commande[0] + " ; " + commande[1] + " ; " + commande[2] + " ; " + commande[3] + " ; " + commande[5] + " ; " + commande[6] + " ; " + time_to_horo(commande[7]) + " ; " + commande[8] + "\n"
        if i%20 == 19 and i != len(passed_commandes)-1: 
            request_body = request_text(sender_id,text)
            requests.post(API, json=request_body).json()
            text = ""
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_cuisinier_nbpassedcommandes(sender_id):
    text = "Il y a eu " + str(len(passed_commandes)) + " commandes passées\n"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()


def connexion_vip(sender_id,id):
    request_body =  request_text(sender_id,str(id) + " veuillez rentrer votre mot de passe vip")
    return requests.post(API, json=request_body).json()

def start(sender_id):
    request_body =  request_text(sender_id,"Le système est en cours de marche")
    return requests.post(API, json=request_body).json()


def informations_supplementaires(sender_id):
    request_body =  request_quick(sender_id,"Voulez vous rentrer des informations supplémentaires ?\n(Appuyez sur Non pour confirmer la commande)",["Oui","Non","Annuler"])
    return requests.post(API, json=request_body).json()

def informations_supplementaires_repeat(sender_id):
    request_body =  request_quick(sender_id,"Je n'ai pas bien compris, voulez vous rentrer des informations supplémentaires ?\n(Appuyez sur Non pour confirmer la commande)",["Oui","Non","Annuler"])
    return requests.post(API, json=request_body).json()

def informations_supplementaires_aide(sender_id):
    return support_technique()

def enter_info_supp(sender_id):
    request_body =  request_text(sender_id,"Veuillez rentrer vos informations supplémentaires")
    return requests.post(API, json=request_body).json()

def enter_info_supp_repeat(sender_id):
    request_body =  request_text(sender_id,"Je n'ai pas bien compris, veuillez rentrer vos informations supplémentaires")
    return requests.post(API, json=request_body).json()

def enter_info_aide(sender_id):
    return support_technique()

# keys : sender_id
senders = dict()
'''
Structure :
int : id
'''

users = dict()
'''
Structure :
array :
0 -> sender_id
1 -> int : id
2 -> int : lastCommand
3 -> string : context
4 -> string : choix_crumble
5 -> string : choix_dessert # artefact
6 -> string : prenom
7 -> string : batiment
8 -> string : chambre
9 -> string : choix_craqueles
10 -> infos supp : string
'''

supports = dict()
'''
Structure :
0 -> int : id
'''

livreurs = dict()
'''
Structure :
array :
0 -> int : id
1 -> bool : notification
2 -> string : zone
'''

cuisiniers = dict()
'''
Structure :
array:
0 -> int : id
1 -> string : cuisine
'''

noe  = dict()
'''
Structure :
0 -> int : id
'''
VIPS = []

CHOIX_CRUMBLE = ["Oui","Non"]
CHOIX_FRUITS_ROUGES = ["Oui","Non"]
CHOIX_CRAQUELES = ["Oui","Non"]

LOGIN = "login"
MOT_DE_PASSE = "motdepasse"

BATIMENTS = ["I1","I2","I3","I5","I6","I7","I8","I9","I10","I11","I12","Arpej","Autre"]
id_allocator = 0
errors = []

commandes = []
passed_commandes = []
id_to_sender = dict()
sender_to_id = dict()

USER_ID = 1
USER_LASTCOMMAND = 2
USER_CONTEXT = 3
USER_CRUMBLE = 4
USER_CRAQUELES = 5
USER_PRENOM = 6
USER_BATIMENT = 7
USER_CHAMBRE = 8
USER_FRUITS_ROUGE = 9
USER_INFOS_SUPP = 10

def addvip(sender_id,id):
    if not id in id_to_sender:
        return default(sender_id)
    s_id = id_to_sender[id]
    VIPS.append(s_id)
    for i in range(len(commandes)):
        if commandes[i][4] == s_id:
            commandes.insert(0,commandes.pop(i))
            break
    newvip(s_id)
    return admin_noe_addvip(sender_id,id)

def add_myvip(sender_id):
    VIPS.append(sender_id)
    for i in range(len(commandes)):
        if commandes[i][4] == sender_id:
            commandes.insert(0,commandes.pop(i))
            break
    return newvip(sender_id)

def erreur_vip(sender_id):
    request_body =  request_text(sender_id,"Mot de passe incorrect, veuillez retaper vip pour retenter")
    return requests.post(API, json=request_body).json()

def admin_cuisinier_status(sender_id):
    text = "Nombre de commandes de crumble faites: " + str(nb_crumble) + " / " + str(CRUMBLE) + "\n"
    text += "Nombre de commandes de craquelés faites: " + str(nb_craqueles) + " / " + str(CRAQUELES) + "\n"
    request_body = request_text(sender_id,text)
    return requests.post(API, json=request_body).json()

def admin_cuisinier_crumble(sender_id):
    request_body = request_text(sender_id,"Le nombre de crumble maximal est maintenant de " + str(CRUMBLE))
    return requests.post(API, json=request_body).json()

def admin_cuisinier_craqueles(sender_id):
    request_body = request_text(sender_id,"Le nombre de craquelé maximal est maintenant de " + str(CRAQUELES))
    return requests.post(API, json=request_body).json()
    
CONTEXT_COMMAND = ["crumble","prenom","batiment","chambre","craqueles"]
CONTEXT_COMMAND_POST_FRITE = ["prenom","batiment","chambre","craqueles"]
CONTEXT_COMMAND_POST_DESSERT = ["prenom","batiment","chambre"]
STOP = False
VIP_MODE = False

def register_command(sender_id):
    global senders,users,supports,livreurs,cuisiniers,noe,CHOIX_CRUMBLE,CHOIX_FRUITS_ROUGES,LOGIN,MOT_DE_PASSE,BATIMENTS,id_allocator
    global errors,USER_ID,USER_LASTCOMMAND,USER_CONTEXT,USER_CRUMBLE,USER_CRAQUELES,USER_PRENOM,USER_BATIMENT,USER_CHAMBRE
    global sender_to_id,id_to_sender,STOP,CHOIX_CRAQUELES,commandes,passed_commandes,nb_crumble,nb_craqueles
    global CRUMBLE,CRAQUELES
    users[sender_id][USER_LASTCOMMAND] = time.time()
    if users[sender_id][USER_CRUMBLE] == "Oui" : nb_crumble += 1
    if users[sender_id][USER_CRAQUELES] == "Oui" : nb_craqueles += 1
    if nb_crumble >= CRUMBLE and nb_craqueles >= CRAQUELES:
        STOP = True
    info = [users[sender_id][USER_PRENOM],
            users[sender_id][USER_BATIMENT],
            users[sender_id][USER_CHAMBRE],
            users[sender_id][USER_CRUMBLE],
            sender_id,
            users[sender_id][USER_CRAQUELES],
            users[sender_id][USER_FRUITS_ROUGE],
            time.time(),
            users[sender_id][USER_INFOS_SUPP]]
    if sender_id in VIPS:
        commandes.insert(0,info)
    else:
        commandes.append(info)
    
    for target in cuisiniers.values():
        admin_cuisinier_notification(id_to_sender[target[0]],info)
    for target in livreurs.values():
        if target[1]:
            target[1] = False
            admin_livreur_notification(id_to_sender[target[0]])
    return commande_prise(sender_id)

def definetimer(sender_id):
    request_body = request_text(sender_id,"Le timer est maintenant de " + str(TIMER))
    return requests.post(API, json=request_body).json()

@app.route("/", methods=['POST'])
def fbwebhook():
    global senders,users,supports,livreurs,cuisiniers,noe,CHOIX_CRUMBLE,CHOIX_FRUITS_ROUGES,LOGIN,MOT_DE_PASSE,BATIMENTS,id_allocator
    global errors,USER_ID,USER_LASTCOMMAND,USER_CONTEXT,USER_CRUMBLE,USER_CRAQUELES,USER_PRENOM,USER_BATIMENT,USER_CHAMBRE
    global sender_to_id,id_to_sender,STOP,CHOIX_CRAQUELES,commandes,passed_commandes,nb_crumble,nb_craqueles
    global CRUMBLE,CRAQUELES,TIMER
    data = request.get_json()

    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    
    #return custom(sender_id,"Nous ne livrons pas pour le moment. Pour être au courant des distributions, rendez vous sur notre page insta bds_koh_lantas")
    if not 'text' in message:
        message['text'] = " "
    text = message['text']

    if VIP_MODE:
        if sender_id in senders:
            return "Ca marche pas", 200
        else:
            senders[sender_id] = 0
            VIPS.append(sender_id)
            return newvip(sender_id)
    
    if text == "whoami":
        if sender_id in users:
            return admin_noe_dump_data(sender_id,users[sender_id][USER_ID])
        elif sender_id in cuisiniers:
            return admin_noe_dump_cuisinier(sender_id,cuisiniers[sender_id][0])
        else:
            return help(sender_id)
    if text == "vip":
        if sender_id in users:
            users[sender_id][USER_CONTEXT] = "role_vip"
            return connexion_vip(sender_id,users[sender_id][USER_ID])
    
    
    if sender_id in users and text == "login":
        users[sender_id][USER_CONTEXT] = "login"
        return login(sender_id,users[sender_id][USER_ID])
    
    if sender_id in senders: # si est dans la base de donnée
        if sender_id in users: # ceux qui passent les commandes
            context = users[sender_id][USER_CONTEXT]
            if context == "login":
                if text == MOT_DE_PASSE:
                    users[sender_id][USER_CONTEXT] = "role_admin"
                    return enrengistrement_administrateur(sender_id)
                else:
                    users[sender_id][USER_CONTEXT] = "bienvenue"
                    return admin_incorrect(sender_id)
            elif context == "role_admin":
                if text == "Cuisinier":
                    users[sender_id][USER_CONTEXT] = "role_cuisinier"
                    return admin_role_cuisinier(sender_id)
                elif text == "Livreur":
                    users[sender_id][USER_CONTEXT] = "role_livreur"
                    return admin_role_livreur(sender_id)
                elif text == "Support":
                    supports[sender_id] = users[sender_id][USER_ID]
                    del users[sender_id]
                    return admin_accueil_support(sender_id)
                elif text == "Noé":
                    users[sender_id][USER_CONTEXT] = "role_noe"
                    return admin_role_noe(sender_id)
                else:
                    return admin_role_incorrect(sender_id)
            elif context == "role_cuisinier":
                if text == "Continuer":
                    cuisiniers[sender_id] = [users[sender_id][USER_ID]]
                    del users[sender_id]
                    return admin_accueil_cuisinier(sender_id)
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "role_admin"
                    return admin_incorrect(sender_id)
                else:
                    return admin_role_cuisinier_incorrect(sender_id)
            elif context == "role_livreur":
                if text == "Continuer":
                    livreurs[sender_id] = [users[sender_id][USER_ID],False]
                    del users[sender_id]
                    return admin_accueil_livreur(sender_id)
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "role_admin"
                    return admin_incorrect(sender_id)
                else:
                    return admin_role_livreur_incorrect(sender_id)
            elif context == "role_noe":
                if text == "Oui":
                    noe[sender_id] = users[sender_id][USER_ID]
                    del users[sender_id]
                    return admin_noe_accueil(sender_id)
                elif text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "role_admin"
                    return admin_incorrect(sender_id)
                else:
                    return admin_noe_incorrect(sender_id)
            elif context == "role_vip":
                if text in CODES_VIP:
                    CODES_VIP.remove(text)
                    if text in CODES_VIP:
                        VIP_ALERTE.append(sender_id)
                        CODES_VIP.remove(text)
                    users[sender_id][USER_CONTEXT] = "standard"
                    return add_myvip(sender_id)
                users[sender_id][USER_CONTEXT] = "standard"
                return erreur_vip(sender_id)
            elif context == "bienvenue":
                if text == "Oui":
                    if STOP:
                        return system_ferme(sender_id)
                    if nb_crumble < CRUMBLE:
                        users[sender_id][USER_CONTEXT] = "crumble"
                        return crumble(sender_id)
                    else:
                        users[sender_id][USER_CRUMBLE] = "Non"
                        users[sender_id][USER_CONTEXT] = "craqueles"
                        return craqueles(sender_id)
                elif text == "Non":
                    users[sender_id][USER_CONTEXT] = "standard"
                    return au_revoir(sender_id)
                elif text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return support_technique(sender_id)
                else:
                    return bienvenue_repeat(sender_id)
            elif context == "support_technique":
                if text == "Oui":
                    for supp in supports.values():
                        admin_support_notification(id_to_sender[supp],sender_to_id[sender_id])
                    users[sender_id][USER_CONTEXT] = "en attente de contact"
                    return contact_technique(sender_id)
                elif text == "Non":
                    if time.time() - users[sender_id][USER_LASTCOMMAND] > TIMER or users[sender_id][USER_LASTCOMMAND] == -1:
                        users[sender_id][USER_CONTEXT] = "bienvenue"
                        return bienvenue(sender_id,users[sender_id][USER_ID])
                    users[sender_id][USER_CONTEXT] = "standard"
                    return timeout(sender_id)
                else:
                    return support_technique_repeat(sender_id)
            elif context == "en attente de contact":
                return "Ca marche pas", 200
            elif context == "crumble":
                for ITEM_CRUMBLE in CHOIX_CRUMBLE:
                    if text == ITEM_CRUMBLE:
                        users[sender_id][USER_CRUMBLE] = ITEM_CRUMBLE
                        if nb_craqueles < CRAQUELES:
                            users[sender_id][USER_CONTEXT] = "craqueles"
                            return craqueles(sender_id)
                        else:
                            users[sender_id][USER_CRAQUELES] = "Non"
                            users[sender_id][USER_CONTEXT] = "prenom"
                            return prenom(sender_id)
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return crumble_aide(sender_id)
                else:
                    return crumble_repeat(sender_id)
            elif context == "dessert": # artefact
                for ITEM_CRAQUELES in CHOIX_FRUITS_ROUGES:
                    if text == ITEM_CRAQUELES:
                        users[sender_id][USER_CONTEXT] = "prenom"
                        users[sender_id][USER_FRUITS_ROUGE] = ITEM_CRAQUELES
                        return prenom(sender_id)
                if text == "Changer la commande":
                    if nb_crumble < CRUMBLE:
                        users[sender_id][USER_CONTEXT] = "crumble"
                        return crumble(sender_id)
                    else:
                        users[sender_id][USER_CRUMBLE] = "Non"
                        users[sender_id][USER_CONTEXT] = "craqueles"
                        return craqueles(sender_id)
                elif text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return croque_fruits_rouges_aide(sender_id)
                else:
                    return croque_fruits_rouges_repeat(sender_id)
            elif context == "craqueles":
                for ITEM_CRAQUELES in CHOIX_CRAQUELES:
                    if text == ITEM_CRAQUELES:
                        users[sender_id][USER_CRAQUELES] = text
                        users[sender_id][USER_CONTEXT] = "prenom"
                        return prenom(sender_id)
                        
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return craqueles_aide(sender_id)
                else:
                    return craqueles_repeat(sender_id)
            elif context == "prenom":
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return prenom_aide(sender_id)
                normalized_text = str(text).strip().lower()
                if len(normalized_text) > 1:
                    users[sender_id][USER_PRENOM] = normalized_text
                    users[sender_id][USER_CONTEXT] = "batiment"
                    return batiment(sender_id)
                else:
                    return prenom_incorrect(sender_id)
            elif context == "batiment":
                if text == "Annuler":
                        return batiment_aide(sender_id)
                for bat in BATIMENTS:
                    if text == bat:
                        users[sender_id][USER_BATIMENT] = text
                        users[sender_id][USER_CONTEXT] = "chambre"
                        return chambre(sender_id)
                return batiment_incorrect(sender_id)
            elif context == "chambre":
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return chambre_aide(sender_id)
                if text.isdigit() or users[sender_id][USER_BATIMENT] == "Autre" or users[sender_id][USER_BATIMENT] == "Arpej":
                    users[sender_id][USER_CHAMBRE] = text
                    users[sender_id][USER_CONTEXT] = "infos"
                    return informations_supplementaires(sender_id)
                else:
                    return chambre_incorrect(sender_id)
            elif context == "infos":
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return informations_supplementaires_aide(sender_id)
                elif text == "Oui":
                    users[sender_id][USER_CONTEXT] = "enter_info"
                    return enter_info_supp(sender_id)
                elif text == "Non":
                    users[sender_id][USER_INFOS_SUPP] = ""
                    users[sender_id][USER_CONTEXT] = "cuisine"
                    return register_command(sender_id)
            elif context == "enter_info":
                if text == "Annuler":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return enter_info_aide
                else:
                    users[sender_id][USER_CONTEXT] = "cuisine"
                    users[sender_id][USER_INFOS_SUPP] = text.replace('\n',' ')
                    return register_command(sender_id)
                    
                
            elif context == "cuisine":
                if text == "Aide":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return cuisine_aide(sender_id)
                position = 0
                for i in range(len(commandes)):
                    if commandes[i][4] == sender_id:
                        position = i
                position += 1
                return cuisine_en_cours(sender_id,position)
            elif context == "standard":
                if text == LOGIN:
                    users[sender_id][USER_CONTEXT] = "login"
                    return login(sender_id,sender_to_id[sender_id])
                if text == "Annuler" or text == "Aide":
                    users[sender_id][USER_CONTEXT] = "support_technique"
                    return support_technique(sender_id)
                if time.time() - users[sender_id][USER_LASTCOMMAND] > TIMER or users[sender_id][USER_LASTCOMMAND] == -1:
                    users[sender_id][USER_CONTEXT] = "bienvenue"
                    return bienvenue(sender_id,users[sender_id][USER_ID])
                else:
                    return timeout(sender_id)
            else:
                errors.append("erreur de context :" + context)
                return "Ca marche pas", 200
        elif sender_id in supports:
            if text == "deconnexion":
                del supports[sender_id]
                del senders[sender_id]
                return admin_leave(sender_id)
            if text[:len("reset ")] == "reset ":
                if text[len("reset "):].isdigit():
                    id = int(text[len("reset "):])
                    if id in id_to_sender and id_to_sender[id] in users:
                        users[id_to_sender[id]][USER_CONTEXT] = "standard"
                        return admin_reset_succefull(sender_id,str(id))
                    else:
                        return admin_reset_failure(sender_id,str(id))
                return admin_reset_failure(sender_id,text)
            return admin_support_idle(sender_id)
        elif sender_id in livreurs:
            if text == "deconnexion":
                del livreurs[sender_id]
                del senders[sender_id]
                return admin_leave(sender_id)
            elif text[:len("isvip ")] == "isvip ":
                if text[len("isvip "):].isdigit():
                    id = int(text[len("isvip "):])
                    return admin_noe_isvip(sender_id,id)
                return default(sender_id)
            elif text[:len("addvip ")] == "addvip ":
                if text[len("addvip "):].isdigit():
                    id = int(text[len("addvip "):])
                    return addvip(sender_id,id)
                return default(sender_id)
            if text.isdigit() or text == "k":
                nb = 0
                if text == "k":
                    nb = 1
                else:
                    nb = int(text)
                if nb <= 0:
                    return admin_livreur_commande_erreur(sender_id)
                elif nb == 1:
                    if len(commandes) == 0:
                        return admin_livreur_commande_zero(sender_id)
                    info = commandes.pop(0)
                    passed_commandes.append(info)
                    if info[4] in users:
                        users[info[4]][USER_CONTEXT] = "standard"
                    livraison_en_cours(info[4])
                    return admin_livreur_commande_one(sender_id,info)
                else:
                    if len(commandes) == 0:
                        return admin_livreur_commande_zero(sender_id)
                    infos = []
                    nb = min(len(commandes),nb)
                    for i in range(nb):
                        info = commandes.pop(0)
                        infos.append(info)
                        passed_commandes.append(info)
                        if info[4] in users:
                            users[infos[-1][4]][USER_CONTEXT] = "standard"
                        livraison_en_cours(infos[-1][4])
                    return admin_livreur_x(sender_id,infos)
            elif text == "suivant":
                if livreurs[sender_id][1] == False:
                    livreurs[sender_id][1] = True
                    return admin_livreur_activer_notification(sender_id)
                else:
                    livreurs[sender_id][1] = False
                    return admin_livreur_desactiver_notification(sender_id)
            
            for bat in BATIMENTS:
                if text[:len(bat + " ")] == bat + " ":
                    if text[len(bat + " "):].isdigit():
                        nb = int(text[len(bat + " "):])
                        coms_bat = []
                        for commande in commandes:
                            if commande[1] == bat:
                                coms_bat.append(commande)
                        
                        if nb <= 0:
                            return admin_livreur_commande_erreur(sender_id)
                        elif nb == 1:
                            if len(coms_bat) == 0:
                                return admin_livreur_commande_zero(sender_id)
                            info = coms_bat.pop(0)
                            commandes.remove(info)
                            passed_commandes.append(info)
                            if info[4] in users:
                                users[info[4]][USER_CONTEXT] = "standard"
                            livraison_en_cours(info[4])
                            return admin_livreur_commande_one(sender_id,info)
                        else:
                            if len(coms_bat) == 0:
                                return admin_livreur_commande_zero(sender_id)
                            infos = []
                            nb = min(len(coms_bat),nb)
                            for i in range(nb):
                                info = coms_bat.pop(0)
                                commandes.remove(info)
                                infos.append(info)
                                passed_commandes.append(info)
                                if info[4] in users:
                                    users[infos[-1][4]][USER_CONTEXT] = "standard"
                                livraison_en_cours(infos[-1][4])
                            return admin_livreur_x(sender_id,infos)
                        
                    else:
                        return admin_livreur_commande_erreur(sender_id)
            if text == "commandes":
                return admin_cuisinier_commandes(sender_id)
            elif text == "status":
                return admin_cuisinier_status(sender_id)
            elif text == "nbcommandes":
                return admin_cuisinier_nbcommandes(sender_id)

            return admin_livreur_erreur(sender_id)
            return "Ca marche pas", 200
        elif sender_id in cuisiniers:
            if text == "deconnexion":
                del cuisiniers[sender_id]
                del senders[sender_id]
                return admin_leave(sender_id)
            elif text == "help":
                return admin_cuisinier_help(sender_id)
            elif text[:len("isvip ")] == "isvip ":
                if text[len("isvip "):].isdigit():
                    id = int(text[len("isvip "):])
                    return admin_noe_isvip(sender_id,id)
                return default(sender_id)
            elif text[:len("addvip ")] == "addvip ":
                if text[len("addvip "):].isdigit():
                    id = int(text[len("addvip "):])
                    return addvip(sender_id,id)
                return default(sender_id)
            elif text == "stop":
                if STOP:
                    return admin_already_stopped(sender_id)
                else:
                    STOP = True
                    return admin_stop(sender_id)
            elif text == "hard stop":
                for user in users:
                    if user[USER_CONTEXT] in CONTEXT_COMMAND:
                        user[USER_CONTEXT] = "standard"
                        commande_annule(id_to_sender[user[USER_ID]])
                    return admin_hard_stop(sender_id)
                if STOP:
                    return admin_already_stopped(sender_id)
                else:
                    STOP = True
                    return admin_hard_stop(sender_id)
            elif text == "start":
                STOP = False
                return start(sender_id)
            elif text[:len("remove ")] == "remove ":
                texts = text.split(" ")
                if len(texts) < 2:
                    return admin_cuisinier_erreur(sender_id)
                item = ""
                for i in range(1,len(texts)):
                    item += texts[i] + " "
                item = item.removesuffix(" ")
                if item in CHOIX_CRUMBLE:
                    CHOIX_CRUMBLE.remove(item)
                    for user in users:
                        if user[USER_CONTEXT] in CONTEXT_COMMAND_POST_FRITE:
                            if user[USER_CRUMBLE] == item:
                                rupture_stock(id_to_sender[user[USER_ID]],item)
                                user[USER_CONTEXT] = "standard"
                    return admin_remove_item(sender_id,item)
                if item in CHOIX_FRUITS_ROUGES:
                    CHOIX_FRUITS_ROUGES.remove(item)
                    for user in users:
                        if user[USER_CONTEXT] in CONTEXT_COMMAND_POST_DESSERT:
                            if user[USER_CRAQUELES] == item:
                                rupture_stock(id_to_sender[user[USER_ID]],item)
                                user[USER_CONTEXT] = "standard"
                    return admin_remove_item(sender_id,item)
                if item in CHOIX_CRAQUELES:
                    CHOIX_CRAQUELES.remove(item)
                    return admin_remove_item(sender_id,item)
            
            elif text[:len("add ")] == "add ":
                texts = text.split(" ")
                if len(texts) < 3:
                    return admin_cuisinier_erreur(sender_id)
                item = ""
                group = texts[1]
                for i in range(2,len(texts)):
                    item += texts[i] + " "
                item = item.removesuffix(" ")
                if group == "crumble":
                    CHOIX_CRUMBLE.append(item)
                    return admin_add_item(sender_id,item,group)
                elif group == "craqueles":
                    CHOIX_CRAQUELES.append(item)
                    return admin_add_item(sender_id,item,group)
            elif text == "commandes":
                return admin_cuisinier_commandes(sender_id)
            elif text == "status":
                return admin_cuisinier_status(sender_id)
            elif text == "nbcommandes":
                return admin_cuisinier_nbcommandes(sender_id)
            elif text == "nbpassedcommandes":
                return admin_cuisinier_nbpassedcommandes(sender_id)
            elif text == "passedcommandes":
                return admin_cuisinier_passedcommandes(sender_id)
            elif text[:len("setcrumble ")] == "setcrumble ":
                if text[len("setcrumble "):].isdigit():
                    nb = int(text[len("setcrumble "):])
                    CRUMBLE = nb
                    return admin_cuisinier_crumble(sender_id)
                return default(sender_id)
            elif text[:len("setcraqueles ")] == "setcraqueles ":
                if text[len("setcraqueles "):].isdigit():
                    nb = int(text[len("setcraqueles "):])
                    CRAQUELES = nb
                    return admin_cuisinier_craqueles(sender_id)
                return default(sender_id)
            elif text[:len("timer ")] == "timer ":
                if text[len("timer "):].isdigit():
                    nb = int(text[len("timer "):])
                    TIMER = nb
                    return definetimer(sender_id)
                return default(sender_id)
            
            
            return admin_cuisinier_erreur(sender_id)
            return "Ca marche pas", 200
        elif sender_id in noe:
            if text == "deconnexion":
                del noe[sender_id]
                del senders[sender_id]
                return admin_leave(sender_id)
            elif text == "dump error":
                return admin_noe_erreur(sender_id)
            elif text == "dump actives":
                return admin_noe_activites(sender_id)
            elif text[:len("isvip ")] == "isvip ":
                if text[len("isvip "):].isdigit():
                    id = int(text[len("isvip "):])
                    return admin_noe_isvip(sender_id,id)
                return default(sender_id)
            elif text == "listvip":
                return admin_noe_listvip(sender_id)
            elif text[:len("addvip ")] == "addvip ":
                if text[len("addvip "):].isdigit():
                    id = int(text[len("addvip "):])
                    return addvip(sender_id,id)
                return default(sender_id)
            elif text == "dump commandes":
                return admin_noe_dump_commandes(sender_id)
            elif text[:len("dump user ")] == "dump user ":
                if text[len("dump user "):].isdigit():
                    id = int(text[len("dump user "):])
                    return admin_noe_dump_user(sender_id,id)
                return default(sender_id)
            elif text == "sudo reset":
                senders = dict()
                users = dict()
                supports = dict()
                livreurs = dict()
                cuisiniers = dict()
                noe  = dict()
                commandes = []
                passed_commandes = []
                id_to_sender = dict()
                sender_to_id = dict()
                return admin_noe_reset(sender_id)
            elif text[:len("reset ")] == "reset ":
                if text[len("reset "):].isdigit():
                    id = int(text[len("reset "):])
                    if id in id_to_sender and id_to_sender[id] in users:
                        users[id_to_sender[id]][USER_CONTEXT] = "standard"
                        return admin_reset_succefull(sender_id,str(id))
                    else:
                        return admin_reset_failure(sender_id,str(id))
                return admin_reset_failure(sender_id,text)
            else:
                return default(sender_id)
            return "Ca marche pas", 200
        else:
            return help(sender_id)
            return "Ca marche pas", 200
    else: #sinon
        if text == "test" or True:
            id = id_allocator
            senders[sender_id] = id
            sender_to_id[sender_id] = id
            id_to_sender[id] = sender_id
            id_allocator += 1
            users[sender_id] = [sender_id,id,-1,"bienvenue","NULL","NULL","NULL","NULL","NULL","NULL",""]
            if text == "vip":
                users[sender_id][USER_CONTEXT] = "role_vip"
                return connexion_vip(sender_id,users[sender_id][USER_ID])
            if text == LOGIN:
                users[sender_id][USER_CONTEXT] = "login"
                return login(sender_id,id)
            else:
                if STOP:
                    return system_ferme(sender_id)
                return bienvenue(sender_id,id)
        else:
            return custom(sender_id,"Nous ne livrons pas pour le moment. Pour être au courant des distributions, rendez vous sur notre page insta bds_koh_lantas")
    return "Ca marche pas", 200