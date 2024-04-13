"""
Nom du fichier: bot.py
Auteur: Étienne-Théodore PRIN
Date: 2024-02-02

Description:
Ce module définie la classe bot qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

Classe:
    - bot : classe qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

Dépendances:
    - math
    - time
    - matrice_def (définition de matrice constante et de dictionnaire utilisé pour effectuer les choix )
"""

from use_fonction.configuration.matrice_def import matrice_choix_def_response,dict_trad,elixir_price,dictionnaire_translation,card_dictionnary
import time
import math
import random
import numpy as np
import random

# S_0 : 0 Sol / 1 Air 
# S_1 : 0 Sol / 1 Air / 2 Building
# S_2 : x Portee
# S_3 : x point de vie
# S_4 : x Dps 
# S_5 : x cout en mana


S = {"archer": [1,1,5,304,107,118,3],"chevalier" : [0,0,0,1607,153,3],"gargouilles" : [1,1,0,690,321,3],"gargouille" : [1,1,0,209,107,1],"geant" : [0,2,0,4091,154,5],"mousquetaire" : [0,1,6,720,218,4],"miniPK" : [0,0,0,1361,410,4],"boulefeu" : [0,0,0,0,0,0],"fleches" : [0,0,0,0,0,0]}

class bot():
    
    """
    classe qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

    Méthodes:
        public:
        get_action(state) : renvoie l'action préconisé par le bot
            sous la forme [] si aucune action est prise ou
            [index_de_la_carte_à_poser(int),position_ou_placer([x(int),y(int)])]
        private:

    """
    def __init__(self):
        """
        Créer un objet qui a pour but de choisir l'action à effectuer en fonction de l'état de la partie clash royal.

        Args:
            None
            
        Returns:
            None
        """
        self.A = {}  # Variable d'instance A
        self.E = {}  # Variable d'instance E
    
    def get_action(self, state):
        """
        Renvoie l'action préconisé par le bot

        Args:
            state : l'état du jeu à l'instant t
            [True,[0,"elixir",5],4*[1,[pos_x,pos_y],"alive/destoyed tower",[h,w]],
             4*[0,"carte",carte.str],x*[1,[pos],"nom_objet",[w,h]]] si en partie 
            ou [False] si dans les menus

        Returns:
            action : sous la forme [] si aucune action est prise ou
                [index_de_la_carte_à_poser(int),position_ou_placer([x(int),y(int)])] si une carte doit être joué
        """
        n = 2
        d_minimale_pour_associer = 200
        
        def tank_adc(cartes_jouables):
            ratio_tank = 0 
            i_tank = 0
            ratio_adc = 0
            i_adc = 0
            if len(cartes_jouables)==0:
                return [-1,-1]
            for c in cartes_jouables : 
                dps_c = c[1][4]
                pts_c = c[1][3]
                r_tank_c = pts_c/dps_c
                r_adc_c = dps_c/pts_c
                
                if r_tank_c > ratio_tank : 
                    ratio_tank = r_tank_c
                    i_tank = c[0]
                
                if r_adc_c > ratio_adc :
                    ratio_adc = r_adc_c
                    i_adc = c[0]
                
            return [i_tank,i_adc]
        
        def poser(i,position):
            if i < 0 :
                print("rien poser c i <0 ")
                return []
            [x_gauche,y_tour] = position
            non = state[6 + i][-1].split('.')[0]
            if non in self.A : 
                self.A[non].append([[x_gauche,y_tour],n,1])
                return [i,[x_gauche,y_tour]]
            else : 
                self.A[non] = [[[x_gauche,y_tour],n,1]]
                return [i,[x_gauche,y_tour]]
        
        def position_relative(v, largeur = 480, hauteur = 800):
            [coord_x, coord_y] = v
            tiers_y = hauteur // 3
        
            if coord_y < tiers_y:
                position_verticale = 0  # partie haute
            elif coord_y < 2 * tiers_y:
                position_verticale = 1  # partie moyenne
            else:
                position_verticale = 2  # partie basse
        
            milieu_x = largeur // 2
        
            if coord_x < milieu_x:
                position_horizontale = 0  # partie gauche
            else :
                position_horizontale = 1  # partie droite
        
            return position_verticale, position_horizontale
        def distance(vecteur1, vecteur2):
            """
            Calcule la distance euclidienne entre deux vecteurs.
            
            Args:
                vecteur1 (list): Les composantes du premier vecteur.
                vecteur2 (list): Les composantes du deuxième vecteur.
            
            Returns:
                float: La distance euclidienne entre les deux vecteurs.
            """
            if len(vecteur1) != len(vecteur2):
                raise ValueError("Les vecteurs doivent avoir la même longueur")
            
            somme_carres_differences = sum((x - y) ** 2 for x, y in zip(vecteur1, vecteur2))
            return math.sqrt(somme_carres_differences)
        dps_tour = 136
        lim_nana_proaction = 5
        if state[0]:
            if state[1][2]>=0:
                C1 = state[6]
                C2 = state[7]
                C3 = state[8]
                C4 = state[9]
                
                if str(C1[-1]) != "0" : 
                    nom_c1 = C1[-1].split('.')[0]
                    info_c1 = S[nom_c1]
                    print("nom_c1 : " + str(nom_c1))
                else : 
                    info_c1 = None
                
                if str(C2[-1]) != "0" :
                    nom_c2 = C2[-1].split('.')[0]
                    info_c2 = S[nom_c2]
                    print("nom_c2 : " + str(nom_c2))
                else : 
                    info_c2 = None
                
                if str(C3[-1]) != "0" :
                    nom_c3 = C3[-1].split('.')[0]
                    info_c3 = S[nom_c3]
                    print("nom_c3 : " + str(nom_c3))
                else : 
                    info_c3 = None
                
                if str(C4[-1]) != "0" :
                    nom_c4 = C4[-1].split('.')[0]
                    info_c4 = S[nom_c4]
                else : 
                    info_c4 = None
                
                x = len(state) - 10
                
                for j in range(x):
                    nouveau = state[j+10]
                    nom = nouveau[2]
                    if not(nom in self.A) :
                        if nom in self.E :
                            P = self.E[nom]
                            gerer = False
                            for p in P :
                                if p[-1]==0 : 
                                    gerer = True
                                    p[0] = nouveau[1]
                                    break
                            if not(gerer) : 
                                P.append([nouveau[1],n,1])
                            self.E[nom] = P
                        
                        else : 
                            self.E[nom] = []  # Initialise la liste associée à nom si elle n'existe pas déjà
                            self.E[nom].append([nouveau[1],n,1])
                    
                    if nom in self.A :
                        if not(nom in self.E) : 
                            P = self.A[nom]
                            vecteur1 = nouveau[1]
                            d = math.inf
                            nin = -1
                            for i in range(len(P)): 
                                if P[i][-1] != 0 :
                                    vecteur2 = P[i][0]
                                    d_actuel = distance(vecteur1 , vecteur2)
                                    if d_actuel < d :
                                        d = d_actuel
                                        nin = i
                            # 30 pix/s d'un géant.
                            if d > d_minimale_pour_associer : 
                                self.E[nom] = [[vecteur1,n,1]]
                            else : 
                                P[nin] = [vecteur1,n,1]
                                self.E[nom] = P
                        else :
                            P_a = self.A[nom]
                            P_e = self.E[nom]
                            vecteur1 = nouveau[1]
                            d = math.inf
                            nin = -1
                            it_is_e = False
                            for i in range(len(P_a)): 
                                if P_a[i][-1] != 0 :
                                    vecteur2 = P_a[i][0]
                                    d_actuel = distance(vecteur1 , vecteur2)
                                    if d_actuel < d :
                                        d = d_actuel
                                        nin = i
                            for j in range(len(P_e)): 
                                if P_e[j][-1] != 0 :
                                    vecteur2 = P_e[j][0]
                                    d_actuel = distance(vecteur1 , vecteur2)
                                    if d_actuel < d :
                                        d = d_actuel
                                        nin = j
                                        it_is_e = True
                            
                            if d > d_minimale_pour_associer :
                                P =  self.E[nom]
                                P.append([vecteur1,n,1])
                                self.E[nom] = P
                            else : 
                                if it_is_e : 
                                    P_e[nin] = [vecteur1,n,1]
                                    self.E[nom] = P_e
                                else :
                                    P_a[nin] = [vecteur1,n,1]
                                    self.A[nom] = P_a
                    
                nana = state[1][-1]
                L_a_pop = []
                if len(self.A.items()) != 0 :
                    # Boucle for pour parcourir les paires clé-valeur
                    for cle, valeur in self.A.items():
                        for v in valeur : 
                            if v[-1] == 0 :
                                v[-2] -= 1 
                                if v[-2] < 0 :
                                    valeur.remove(v)
                                    if len(valeur) == 0 :
                                        L_a_pop.append(cle)
                                else : 
                                    v[-1] = 0
                            else : 
                                v[-1] = 0
                                
                print("L_a_pop : " + str(L_a_pop))
                for cle in L_a_pop : 
                    self.A.pop(cle)
                L_e_pop = []

                if len(self.E.items()) != 0 :    
                    for cle, valeur in self.E.items():
                        for v in valeur :
                            if v[-1] == 0 :
                                v[-2] -= 1 
                                if v[-2] < 0 :
                                    valeur.remove(v)
                                    if len(valeur) == 0 : 
                                        L_e_pop.append(cle)
                                else : 
                                    v[-1] = 0
                            else : 
                                v[-1] = 0
                            
                                    
                print("L_e_pop : " + str(L_e_pop))
                for cle in L_e_pop : 
                    self.E.pop(cle)
                
                # terrain [lignes][colonne][j] j = 0 => Nbre de créature j=1 => DPS creatures j=2 => Points de vie créatures
                terrain_a = [ [[0,0],[0,0]] for i in range(3)]
                L_t_a = [[0,0] for i in range(3)]
                for cle, valeur in self.A.items():
                    for v in valeur : 
                        postion_t = position_relative(v[0])
                        [b,c] = terrain_a[postion_t[0]][postion_t[1]]
                        a = L_t_a[postion_t[0]][postion_t[1]]
                        a += 1 
                        b += S[cle][4]
                        c += S[cle][3]
                        terrain_a[postion_t[0]][postion_t[1]] = [b,c]
                        L_t_a[postion_t[0]][postion_t[1]] = a
                
                terrain_e = [ [[0,0],[0,0]] for i in range(3)]
                L_t_e = [[0,0] for i in range(3)]
                for cle, valeur in self.E.items():
                    if cle =="info-message" or cle == "clock": 
                        break
                    for v in valeur : 
                        postion_t = position_relative(v[0])
                        [b,c] = terrain_e[postion_t[0]][postion_t[1]]
                        a = L_t_e[postion_t[0]][postion_t[1]]
                        a += 1 
                        b += S[cle][4]
                        c += S[cle][3]
                        terrain_e[postion_t[0]][postion_t[1]] = [b,c]
                        L_t_e[postion_t[0]][postion_t[1]] = a
                cartes_jouables = []
                if nana > 2 : 
                    if info_c1 is not None and info_c1[-1] < nana and nom_c1 != "fleches" and nom_c1 != "boulefeu":
                        cartes_jouables.append([0, info_c1])
                    if info_c2 is not None and info_c2[-1] < nana and nom_c2 != "fleches" and nom_c2 != "boulefeu":
                        cartes_jouables.append([1, info_c2])
                    if info_c3 is not None and info_c3[-1] < nana and nom_c3 != "fleches" and nom_c3 != "boulefeu":
                        cartes_jouables.append([2, info_c3])
                    if info_c4 is not None and info_c4[-1] < nana and nom_c4 != "fleches" and nom_c4 != "boulefeu":
                        cartes_jouables.append([3, info_c4])
                
                np_terrain_e = np.array(terrain_e)
                np_terrain_a = np.array(terrain_a)
                
                [[Dps_g_e , Pts_de_vie_g_e],[Dps_d_e, Pts_de_vie_d_e]] = np.sum(np_terrain_e,axis = 0)
                [[Dps_g_a , Pts_de_vie_g_a],[Dps_d_a, Pts_de_vie_d_a]] = np.sum(np_terrain_a,axis = 0)
                
                # # Affichage des résultats
                # print(f"Pour l'équipe ennemie:")
                # print(f"Dps global: {Dps_g_e}, Points de vie global: {Pts_de_vie_g_e}")
                # print(f"Dps défensif: {Dps_d_e}, Points de vie défensif: {Pts_de_vie_d_e}\n")
                
                # print(f"Pour l'équipe alliée:")
                # print(f"Dps global: {Dps_g_a}, Points de vie global: {Pts_de_vie_g_a}")
                # print(f"Dps défensif: {Dps_d_a}, Points de vie défensif: {Pts_de_vie_d_a}")
                
                
                # print(self.A)
                # print(self.E)
                
                def_g_a = Pts_de_vie_g_e / Dps_g_a if Dps_g_a != 0 else Pts_de_vie_g_e/dps_tour
                def_d_a = Pts_de_vie_d_e / Dps_d_a if Dps_d_a != 0 else Pts_de_vie_d_e/dps_tour
                def_g_e = Pts_de_vie_g_a / Dps_g_e if Dps_g_e != 0 else Pts_de_vie_g_a/dps_tour
                def_d_e = Pts_de_vie_d_a / Dps_d_e if Dps_d_e != 0 else Pts_de_vie_d_a/dps_tour

                diff_g = def_g_a - def_g_e
                diff_d = def_d_a - def_d_e
                
                print("def_g_a : " + str(def_g_a))
                print("def_g_e : " + str(def_g_e))
                print("def_d_e : " + str(def_d_e))
                print("def_d_e : " + str(def_d_e))
                
                print("np_terrain_e : " + str(np_terrain_e))
                print("np_terrain_a : " + str(np_terrain_a))
                
                dps_l_g_e = [ligne[0][0] for ligne in np_terrain_e]
                dps_l_g_a = [ligne[0][0] for ligne in np_terrain_a]
                dps_l_d_e = [ligne[1][0] for ligne in np_terrain_e]
                dps_l_d_a = [ligne[1][0] for ligne in np_terrain_a]
                
                tank_l_g_e = [ligne[0][1] for ligne in np_terrain_e]
                tank_l_g_a = [ligne[0][1] for ligne in np_terrain_a]
                tank_l_d_e = [ligne[1][1] for ligne in np_terrain_e]
                tank_l_d_a = [ligne[1][1] for ligne in np_terrain_a]
                
                i_tank,i_adc = tank_adc(cartes_jouables)
                y_nilieu = 350
                x_gauche = 90
                x_droit = 340
                # x_gauche = x_droit
                y_tour = 400
                y_fin = 600
                
                # Stratégie 1 : 
                
                # play_g_fast = False
                # play_d_fast = False
                # play_g = False
                # play_d = False    
                
                # if diff_g > 0 : 
                #     if diff_d > 0 :
                #         if diff_g > diff_d and diff_g > 2: 
                #             play_g_fast = True
                        
                #         elif diff_d > diff_g and diff_d > 2: 
                #             play_d_fast = True
                        
                #         elif diff_g > diff_d : 
                #             play_g = True
                        
                #         elif diff_d > diff_g : 
                #             play_d = True
                #     else : 
                #         play_g = True
                # else : 
                #     if diff_d > 0 :
                #         play_d = True
                
                # print("play_g_fast : " + str(play_g_fast))
                # print("play_d_fast : " + str(play_d_fast))
                # print("play_g : " + str(play_g))
                # print("play_d : " + str(play_d))
                
                # print("diff_g : " + str(diff_g))
                # print("diff_d : " + str(diff_d))
                
                # if play_g_fast : 
                #     indice_max_dps = dps_l_g_e.index(max(dps_l_g_e))
                #     print("play_g_fast : " + str(indice_max_dps))
                #     if indice_max_dps == 2 : 
                #         return poser(i_tank,[x_gauche,y_nilieu])
                #     elif indice_max_dps == 1 :
                #         return poser(i_adc,[x_gauche,y_tour])
                #     else : 
                #         indice_max_tank = tank_l_g_e.index(max(tank_l_g_e))
                #         if indice_max_tank == 0 :
                #             return poser(i_adc,[x_gauche,y_nilieu])
                #         else :
                #             return poser(i_adc,[x_gauche,y_tour])
                # elif play_d_fast : 
                #     indice_max_dps = dps_l_d_e.index(max(dps_l_d_e))
                #     print("play_d_fast : " + str(indice_max_dps))
                #     if indice_max_dps == 2 : 
                #         return poser(i_tank,[x_droit,y_nilieu])
                #     elif indice_max_dps == 1 :
                #         return poser(i_adc,[x_droit,y_tour])
                #     else : 
                #         indice_max_tank = tank_l_d_e.index(max(tank_l_d_e))
                #         if indice_max_tank == 0 :
                #             return poser(i_tank,[x_droit,y_nilieu])
                #         else :
                #             return poser(i_adc,[x_droit,y_tour])
                # elif play_g : 
                #     indice_max_dps = dps_l_g_e.index(max(dps_l_g_e))
                #     print("play_g : " + str(indice_max_dps))
                #     if nana >= 4 and indice_max_dps == 2 :
                #         return poser(i_tank,[x_gauche,y_nilieu])
                #     elif nana >= 4 and indice_max_dps == 1 : 
                #         return poser(i_adc,[x_gauche,y_tour])
                #     else :
                #         if nana <= 4 :
                #             return []
                #         indice_max_tank = tank_l_g_e.index(max(tank_l_g_e))
                #         if indice_max_tank == 0 :
                #             return poser(i_tank,[x_gauche,y_nilieu])
                #         else :
                #             return poser(i_adc,[x_gauche,y_tour])
                # elif play_d : 
                #     indice_max_dps = dps_l_g_e.index(max(dps_l_g_e))
                #     print("play_d : " + str(indice_max_dps))
                #     if nana >= 7 and indice_max_dps == 2 : 
                #         return poser(i_tank,[x_gauche,y_nilieu])
                #     elif nana >= 7 and indice_max_dps == 1 :
                #         return poser(i_adc,[x_gauche,y_tour])
                #     else :
                #         if nana <= 7 :
                #             return []
                #         indice_max_tank = tank_l_g_e.index(max(tank_l_g_e))
                #         if indice_max_tank == 0 :
                #             return poser(i_tank,[x_gauche,y_nilieu])
                #         else :
                #             return poser(i_adc,[x_gauche,y_tour])
                # elif nana >= 8:
                #     resultat = random.randint(0, 1)
                #     if resultat : 
                #         return poser(i_tank,[x_gauche,y_fin])
                #     else : 
                #         return poser(i_tank,[x_droit,y_fin])
                # elif Pts_de_vie_g_a > Dps_g_a*5 :
                #     return poser(i_adc,[x_gauche,y_tour])
                # elif Dps_g_a > Pts_de_vie_g_a/5 :
                #     return poser(i_tank,[x_gauche,y_nilieu])
                # elif Pts_de_vie_d_a > Dps_d_a*5 :
                #     return poser(i_adc,[x_droit,y_tour])
                # elif Dps_d_a > Pts_de_vie_d_a/5 :
                #     return poser(i_tank,[x_droit,y_nilieu])
                # else : 
                #     return []
                
                ## Fin de stratégie 1
                
                
                ## Startégie 2 : 
                
                defence_gauche_huge = False
                defence_droite_huge = False
                
                attaque_gauche_huge = False
                attaque_droite_huge = False
                
                defence_gauche = False
                defence_droite = False
                
                attaque_gauche = False
                attaque_droite = False
                
                t_huge = 10
                
                if diff_g > 0 : 
                    defence_gauche = True
                    if diff_g > t_huge and Dps_g_e != 0 : 
                        defence_gauche_huge = True
                else : 
                    attaque_gauche = True
                    if np.abs(diff_g) > t_huge and Dps_g_e != 0 : 
                        attaque_gauche_huge = True
                
                if diff_d > 0 :
                    defence_droite =True
                    if diff_d > t_huge and Dps_d_e != 0 : 
                        defence_droite_huge = True
                else : 
                    attaque_droite = True
                    if np.abs(diff_d) > t_huge and Dps_d_e != 0 : 
                        attaque_droite_huge = True
                
                print("diff_g : " + str(diff_g))
                print("diff_d : " + str(diff_d) + "\n")
                
                print("defence_gauche_huge : " + str(defence_gauche_huge))
                print("defence_droite_huge : " + str(defence_droite_huge))
                print("attaque_gauche_huge : " + str(attaque_gauche_huge))
                print("attaque_droite_huge : " + str(attaque_droite_huge))
                
                print("defence_gauche : " + str(defence_gauche))
                print("defence_droite : " + str(defence_droite))
                print("attaque_gauche : " + str(attaque_gauche))
                print("attaque_droite : " + str(attaque_droite))
                
                if defence_gauche_huge and diff_g > diff_d  : 
                    indice_max_dps = dps_l_g_e.index(max(dps_l_g_e))
                    print("defence_gauche_huge : " + str(indice_max_dps))
                    if indice_max_dps == 2 : 
                        return poser(i_tank,[x_gauche,y_nilieu])
                    elif indice_max_dps == 1 :
                        return poser(i_adc,[x_gauche,y_tour])
                    else : 
                        indice_max_tank = tank_l_g_e.index(max(tank_l_g_e))
                        if indice_max_tank == 0 :
                            return poser(i_adc,[x_gauche,y_nilieu])
                        else :
                            return poser(i_adc,[x_gauche,y_tour])
                elif defence_droite_huge : 
                    indice_max_dps = dps_l_d_e.index(max(dps_l_d_e))
                    print("play_d_fast : " + str(indice_max_dps))
                    if indice_max_dps == 2 : 
                        return poser(i_tank,[x_droit,y_nilieu])
                    elif indice_max_dps == 1 :
                        return poser(i_adc,[x_droit,y_tour])
                    else : 
                        indice_max_tank = tank_l_d_e.index(max(tank_l_d_e))
                        if indice_max_tank == 0 :
                            return poser(i_tank,[x_droit,y_nilieu])
                        else :
                            return poser(i_adc,[x_droit,y_tour])
                elif defence_gauche and diff_g > diff_d : 
                    indice_max_dps = dps_l_g_e.index(max(dps_l_g_e))
                    print("play_g : " + str(indice_max_dps))
                    if nana >= lim_nana_proaction and indice_max_dps == 2 :
                        return poser(i_tank,[x_gauche,y_nilieu])
                    elif nana >= lim_nana_proaction and indice_max_dps == 1 : 
                        return poser(i_adc,[x_gauche,y_tour])
                    else :
                        if nana <= lim_nana_proaction :
                            return []
                        indice_max_tank = tank_l_g_e.index(max(tank_l_g_e))
                        if indice_max_tank == 0 :
                            return poser(i_tank,[x_gauche,y_nilieu])
                        else :
                            return poser(i_adc,[x_gauche,y_tour])
                elif defence_droite : 
                    indice_max_dps = dps_l_d_e.index(max(dps_l_d_e))
                    print("play_d : " + str(indice_max_dps))
                    if nana >= lim_nana_proaction and indice_max_dps == 2 : 
                        return poser(i_tank,[x_droit,y_nilieu])
                    elif nana >= lim_nana_proaction and indice_max_dps == 1 :
                        return poser(i_adc,[x_droit,y_tour])
                    else :
                        if nana <= lim_nana_proaction :
                            return []
                        indice_max_tank = tank_l_g_e.index(max(tank_l_g_e))
                        if indice_max_tank == 0 :
                            return poser(i_tank,[x_droit,y_nilieu])
                        else :
                            return poser(i_adc,[x_droit,y_tour])
                
                print("defence_gauche_huge : " + str(defence_gauche_huge))
                print("defence_droite_huge : " + str(defence_droite_huge))
                print("attaque_gauche_huge : " + str(attaque_gauche_huge))
                print("attaque_droite_huge : " + str(attaque_droite_huge))
                
                print("defence_gauche : " + str(defence_gauche))
                print("defence_droite : " + str(defence_droite))
                print("attaque_gauche : " + str(attaque_gauche))
                print("attaque_droite : " + str(attaque_droite))
                
                ## Attaque : 
                if attaque_gauche_huge and diff_g > diff_d : 
                    indice_max_dps = dps_l_g_a.index(max(dps_l_g_a))
                    print("attaque_gauche_huge : " + str(indice_max_dps))
                    if nana >= lim_nana_proaction and indice_max_dps == 2 :
                        return poser(i_adc,[x_gauche,y_tour])
                    elif nana >= lim_nana_proaction and indice_max_dps == 1 : 
                        return poser(i_adc,[x_gauche,y_nilieu])
                    else :
                        if nana <= lim_nana_proaction :
                            return []
                        indice_max_tank = tank_l_g_a.index(max(tank_l_g_a))
                        if indice_max_tank == 0 :
                            return poser(i_adc,[x_gauche,y_tour])
                        else :
                            return []
                elif attaque_droite_huge  : 
                    indice_max_dps = dps_l_d_a.index(max(dps_l_d_a))
                    print("attaque_droite_huge : " + str(indice_max_dps))
                    print("attaque_gauche_huge : " + str(indice_max_dps))
                    if nana >= lim_nana_proaction and indice_max_dps == 2 :
                        return poser(i_adc,[x_droit,y_tour])
                    elif nana >= lim_nana_proaction and indice_max_dps == 1 : 
                        return poser(i_adc,[x_droit,y_nilieu])
                    else :
                        if nana <= lim_nana_proaction :
                            return []
                        indice_max_tank = tank_l_d_a.index(max(tank_l_d_a))
                        if indice_max_tank == 0 :
                            return poser(i_adc,[x_droit,y_tour])
                        else :
                            return []
                elif attaque_gauche and diff_g > diff_d : 
                    indice_max_dps = dps_l_g_a.index(max(dps_l_g_a))
                    print("defence_gauche_huge : " + str(indice_max_dps))
                    if indice_max_dps == 0 : 
                        return poser(i_tank,[x_gauche,y_nilieu])
                    elif indice_max_dps == 1 :
                        indice_max_tank = tank_l_g_a.index(max(tank_l_g_a))
                        if indice_max_tank == 2 :
                            return poser(i_adc,[x_gauche,y_nilieu])
                        else :
                            return []
                    else : 
                        return []
                elif attaque_droite : 
                    indice_max_dps = dps_l_d_a.index(max(dps_l_d_a))
                    print("attaque_droite : " + str(indice_max_dps))
                    if indice_max_dps == 0 : 
                        return poser(i_tank,[x_droit,y_nilieu])
                    elif indice_max_dps == 1 :
                        indice_max_tank = tank_l_g_a.index(max(tank_l_g_a))
                        if indice_max_tank == 2 :
                            return poser(i_adc,[x_droit,y_nilieu])
                        else :
                            return []
                    else : 
                        return []
                else : 
                    return []
                
                ## Fin de stratégie 2
                
                
                
        return []
