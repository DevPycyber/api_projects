from tkinter import *
from PIL import Image, ImageTk
import meteofrance_api
import tkinter.messagebox as message
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image

old_cold = 'blue'
old_norm = 'yellow'
old_moy = 'orange'
old_red = 'red'
color_froide = 'blue'
color_normale = 'yellow'
color_moyenne = 'orange'
color_chaud = 'red'

modif_couleur = False
modify_froid = False
modify_normal = False
modify_moy = False
modify_chaud = False

class MeteoApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("meteo")
        self.top_window_dim = (940, 500)
        self.geometry("{}x{}".format(self.top_window_dim[0], self.top_window_dim[1]))
        self.resizable(width=False, height=False)
        
        self.temperature = None
        self.wind_speed = None
        self.global_weather = None 

        #define element
        self.carte = Map(self)
        self.espace = User_space(self)
       
        
    def quit_app(self):
       message_return = message.askyesno('quit application', 'Voulez-vous vraiment quitter le logiciel ?')
       if message_return:
            self.destroy()

    def run_app(self):
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.mainloop()
        


class Map(Frame):
    def __init__(self, parent):
        self.frame_map_dim = (470, 500)
        Frame.__init__(self, master=parent, width=self.frame_map_dim[0], height=self.frame_map_dim[1])
        self.client = meteofrance_api.MeteoFranceClient()
        self.path = './carte_regions.jpg'
        self.can_map = Canvas(self, width=self.frame_map_dim[0], height=self.frame_map_dim[1])

        self.image = ImageTk.PhotoImage(Image.open(self.path))
        self.can_map.create_image(0, 0, image=self.image, anchor='nw')
        

        #zones de dessin régions
        self.zone_nord_pas_calais = self.can_map.create_polygon(238, 9, 270, 3, 330, 60, 305, 120, 243, 100, 234, 44, fill=self.color_temp_region(self.moyenne_temp_region(4, 'Calais', 'Arras', 'Amiens', 'Laon', 'Beauvais'))) #ok
        self.normandie = self.can_map.create_polygon(120, 67, 170, 95, 230, 50, 240, 75, 245, 100, 210, 150, 120, 120, fill=self.color_temp_region(self.moyenne_temp_region(6, 'Rouen', 'Caen', 'Le Havre', 'Cherbourg', 'Flers', 'Evreux')))
        self.Bretagne = self.can_map.create_polygon(10, 120, 50, 115, 75, 100, 95, 120, 130, 122, 145, 127, 135, 170, 90, 185, 10, 150, fill=self.color_temp_region(self.moyenne_temp_region(5, 'Brest', 'Saint-Malo', 'Quimper', 'Guingamp', 'Carhaix-Plouguer')))
        self.pays_loire = self.can_map.create_polygon(150, 130, 210, 150, 210, 170, 178, 210, 150, 220, 154, 248, 118, 250, 90, 190, fill=self.color_temp_region(self.moyenne_temp_region(4, 'Chartres', 'Bourges', 'Tours', 'Orleans')))
        self.nouvelle_aquitaine = self.can_map.create_polygon(118, 250, 155, 250, 150, 215, 190, 200, 220, 250, 270, 270, 250, 320, 240, 320, 210 , 355, 180, 370, 160, 430, 110, 410, 125, 288, fill=self.color_temp_region(self.moyenne_temp_region(5, 'La Rochelle', 'Bordeaux', 'Bayonne', 'Limoges', 'Poitiers')))
        self.occitanie = self.can_map.create_polygon(160, 430, 180, 370, 210, 355, 240, 320, 285, 320, 350, 360, 340, 400, 295, 420, 295, 460, fill=self.color_temp_region(self.moyenne_temp_region(5, 'Perpignan', 'Montpellier', 'Tarbes', 'Figeac', 'Toulouse')))
        self.provence = self.can_map.create_polygon(340, 400, 420, 420,470, 360, 410, 310, 350, 360, fill=self.color_temp_region(self.moyenne_temp_region(7, 'Nice', 'Marseille' ,'Briancon', 'Arles', 'Avignon', 'Gap', 'Manosque')))
        self.auvergne = self.can_map.create_polygon(220, 245, 280, 225, 430, 240, 440, 300, 412, 310, 350, 360, 253, 320, fill=self.color_temp_region(self.moyenne_temp_region(4, 'Lyon', 'Clermont-Ferrand', 'Valence', 'Grenoble')))
        self.centre_val_loire = self.can_map.create_polygon(215, 250, 290, 220, 289, 158, 245, 136, 233, 127, 235, 115, 210, 148, 190, 200, fill=self.color_temp_region(self.moyenne_temp_region(6, 'Nantes', 'Angers', 'Le Mans', 'Laval', 'Saint-Nazaire', 'Luçon')))
        self.ile_france = self.can_map.create_polygon(233, 120, 245, 100, 305, 120, 305 ,145, 290, 160, 233, 130, fill=self.color_temp_region(self.moyenne_temp_region(4, 'Paris', 'Etampes', 'Mantes-la-Jolie', 'Provins')))
        self.Bourgogne = self.can_map.create_polygon(305, 145, 370, 180,  390, 155, 450, 180, 430, 240, 288, 226, 291, 160, fill=self.color_temp_region(self.moyenne_temp_region(4, 'Besançon' ,'Dijon', 'Belfort', 'Auxerre', 'Macon', 'Nevers')))
        self.grand_est = self.can_map.create_polygon(330, 60, 360, 72, 468, 105, 450, 180, 369, 179, 305 ,145, 305, 120, fill=self.color_temp_region(self.moyenne_temp_region(4, 'Strasbourg', 'Reims', 'Nancy', 'Troyes', 'Mulhouse', 'Metz')))
        self.list_zone_region = [self.zone_nord_pas_calais, self.normandie, self.Bretagne, self.pays_loire, self.nouvelle_aquitaine, self.occitanie, self.provence, self.auvergne, self.centre_val_loire, self.ile_france, self.Bourgogne, self.grand_est]
        self.size_gde_metropole = 11
        self.size_mineur = 8
        self.list_lab=[]
        #Zones de textes métropoles
        self.Lab_Lille = Label(self.can_map, text="Lille", font=('Century Gothic', self.size_gde_metropole), padx=0, pady=0)
        self.Lab_Rouen = Label(self.can_map, text="Rouen", font=('Century Gothic', self.size_gde_metropole))            
        self.Lab_Metz = Label(self.can_map, text="Metz", font=('Century Gothic', self.size_mineur))    
        self.Lab_Strasbourg = Label(self.can_map, text="Strasbourg", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Paris = Label(self.can_map, text="Paris", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Tours = Label(self.can_map, text="Tours", font=('Century Gothic', self.size_mineur))      
        self.Lab_Rennes = Label(self.can_map, text="Rennes", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Brest = Label(self.can_map, text="Brest", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Nantes = Label(self.can_map, text="Nantes", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Orleans = Label(self.can_map, text="Orleans", font=('Century Gothic', self.size_mineur))    
        self.Lab_Nancy = Label(self.can_map, text="Nancy", font=('Century Gothic', self.size_mineur))    
        self.Lab_Bordeaux = Label(self.can_map, text="Bordeaux", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Toulouse = Label(self.can_map, text="Toulouse", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Montpellier = Label(self.can_map, text="Montpellier", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Marseille = Label(self.can_map, text="Marseille", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Toulon = Label(self.can_map, text="Toulon", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Dijon = Label(self.can_map, text="Dijon", font=('Century Gothic', self.size_mineur))    
        self.Lab_Saint_Etienne= Label(self.can_map, text="Saint_Etienne", font=('Century Gothic', self.size_mineur))    
        self.Lab_Grenoble = Label(self.can_map, text="Grenoble", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Nice= Label(self.can_map, text="Nice", font=('Century Gothic', self.size_gde_metropole))    
        self.Lab_Clermont_Ferrand = Label(self.can_map, text="Clermont \n Ferrand", font=('Century Gothic', self.size_mineur))    
        self.Lab_Lyon = Label(self.can_map, text="Lyon", font=('Century Gothic', self.size_gde_metropole))
        self.list_lab.extend([self.Lab_Lille, self.Lab_Rouen, self.Lab_Paris, self.Lab_Brest, self.Lab_Rennes, self.Lab_Nantes, self.Lab_Strasbourg, self.Lab_Bordeaux, self.Lab_Lyon, self.Lab_Grenoble, self.Lab_Toulouse, self.Lab_Montpellier, self.Lab_Marseille, self.Lab_Nice, self.Lab_Dijon, self.Lab_Clermont_Ferrand, self.Lab_Saint_Etienne, self.Lab_Tours, self.Lab_Metz, self.Lab_Nancy, self.Lab_Orleans, self.Lab_Toulon])
        self.liste_metropole = ['Lille', 'Rouen', 'Paris', 'Brest', 'Rennes', 'Nantes', 'Strasbourg', 'Bordeaux', 'Lyon', 'Grenoble', 'Toulouse', 'Montpellier', 'Marseille', 'Nice', 'Dijon', 'Clermont-Ferrand', 'St-Etienne', 'Tours', 'Metz', 'Nancy', 'Orleans', 'Toulon']

        self.Lab_Lille.place(x=280, y=10)
        self.Lab_Rouen.place(x=180, y=67)
        self.Lab_Paris.place(x=250, y=110)
        self.Lab_Brest.place(x=30, y=125)
        self.Lab_Rennes.place(x=100, y=130)
        self.Lab_Nantes.place(x=90, y=190)
        self.Lab_Strasbourg.place(x=380, y=105)
        self.Lab_Bordeaux.place(x=125, y=290)
        self.Lab_Toulouse.place(x=125, y=370)
        self.Lab_Montpellier.place(x=230, y=400)
        self.Lab_Marseille.place(x=280, y=365)
        self.Lab_Toulon.place(x=380, y=400)
        self.Lab_Nice.place(x=400, y=350)
        self.Lab_Grenoble.place(x=350, y=310)
        self.Lab_Clermont_Ferrand.place(x=220, y=210)
        self.Lab_Saint_Etienne.place(x=270, y=270)
        self.Lab_Lyon.place(x=370, y=240)
        self.Lab_Dijon.place(x=330, y=180)
        self.Lab_Tours.place(x=150, y=180)
        self.Lab_Metz.place(x=340, y=85)
        self.Lab_Nancy.place(x=350, y=140)
        self.Lab_Orleans.place(x=210, y=170)
        # tester pour tenter de raccourcir == échouer jusqu'à présent
        self.Lab_Lille.bind('<Button-1>', lambda x: self.get_infos_metropole('Lille', True))
        self.Lab_Rouen.bind('<Button-1>', lambda x : self.get_infos_metropole('Rouen', True))
        self.Lab_Metz.bind('<Button-1>', lambda x :self.get_infos_metropole('Metz', True))
        self.Lab_Strasbourg.bind('<Button-1>', lambda x : self.get_infos_metropole('Strasbourg', True))
        self.Lab_Paris.bind('<Button-1>', lambda x : self.get_infos_metropole('Paris', True))
        self.Lab_Tours.bind('<Button-1>', lambda x : self.get_infos_metropole('Tours', True))
        self.Lab_Orleans.bind('<Button-1>', lambda x :self.get_infos_metropole('Orléans', True))
        self.Lab_Rennes.bind('<Button-1>', lambda x :self.get_infos_metropole('Rennes', True))
        self.Lab_Brest.bind('<Button-1>', lambda x :self.get_infos_metropole('Brest', True))
        self.Lab_Nantes.bind('<Button-1>', lambda x :self.get_infos_metropole('Nantes', True))
        self.Lab_Nancy.bind('<Button-1>', lambda x :self.get_infos_metropole('Nancy', True)) 
        self.Lab_Bordeaux.bind('<Button-1>', lambda x :self.get_infos_metropole('Bordeaux', True)) 
        self.Lab_Toulouse.bind('<Button-1>', lambda x :self.get_infos_metropole('Toulouse', True))
        self.Lab_Montpellier.bind('<Button-1>', lambda x :self.get_infos_metropole('Montpellier', True))
        self.Lab_Marseille.bind('<Button-1>', lambda x :self.get_infos_metropole('Marseille', True))
        self.Lab_Toulon.bind('<Button-1>', lambda x :self.get_infos_metropole('Toulon', True))
        self.Lab_Dijon.bind('<Button-1>', lambda x :self.get_infos_metropole('Dijon', True))
        self.Lab_Saint_Etienne.bind('<Button-1>', lambda x :self.get_infos_metropole('Saint-Etienne', True))
        self.Lab_Grenoble.bind('<Button-1>', lambda x :self.get_infos_metropole('Grenoble', True))
        self.Lab_Nice.bind('<Button-1>', lambda x :self.get_infos_metropole('Nice', True))
        self.Lab_Clermont_Ferrand.bind('<Button-1>', lambda x :self.get_infos_metropole('Clermont-Ferrand', True))
        self.Lab_Lyon.bind('<Button-1>', lambda x :self.get_infos_metropole('Lyon', True))
        self.affiche_intemperies()
        self.can_map.pack()
        self.pack(side=RIGHT)
        


    def print_infos_metropole(self, nom):
        self.infos = Tk()
        self.infos.title('infos pour {}'.format(nom))
        self.infos.geometry('250x100')
        self.infos.resizable(width=True, height=False)
        self.lab_temp = Label(self.infos, text="temperature : {}°".format(self.infos_metropole['temperature']))
        self.lab_wind_speed = Label(self.infos, text="vitesse du vent : {} km/h".format(self.infos_metropole['vitesse du vent']))
        self.lab_weather_desc = Label(self.infos, text="description général : {}".format(self.infos_metropole['description generale']))
        self.lab_temp.grid(row=0, column=0)
        self.lab_weather_desc.grid(row=1, column=0)
        self.lab_wind_speed.grid(row=2, column=0)
        self.infos.mainloop()

    def color_temp_region(self, moyenne):
        if moyenne <= 10:
            return color_froide
        elif moyenne > 10 and moyenne < 24:
            return  color_normale
        elif moyenne >= 24 and moyenne < 33:
            return color_moyenne
        elif moyenne > 33:
            return color_chaud 
        
    def calc_moy_desc(self, *villes_desc):
        dict_eve = {}
        dict_eve['nuage'] = 0
        dict_eve['pluie'] = 0
        dict_eve['pluie__'] = 0
        dict_eve['__pluie'] = 0
        dict_eve['soleil'] = 0
        dict_eve['Orages'] = 0
        dict_eve['eclaircies'] = 0
        dict_eve['couvert'] = 0
        dict_eve['RAS'] = False
        for desc in villes_desc:
            if desc=="Ensolleilé": dict_eve['soleil'] +=1
            elif desc == "Pluie faible": dict_eve['pluie__'] +=1
            elif desc == "Pluie forte": dict_eve['__pluie'] +=1
            elif desc == "Pluie": dict_eve['pluie'] +=1
            elif desc == "Nuageux": dict_eve['nuage'] +=1
            elif desc=="Couvert": dict_eve['couvert'] +=1
            elif desc == 'Orages': dict_eve['Orages'] +=1
            elif desc == 'Eclaircies' : dict_eve['eclaircies'] +=1
            elif desc=='null': dict_eve['RAS'] == True

        maxi = 0
        for v in dict_eve.values():
            if v > maxi:
                maxi = v
        for k in dict_eve.keys():
            if dict_eve[k] == maxi:
                if dict_eve['RAS'] == False:
                    return k
                else: return None

    def affiche_intemperies(self):
        self.dict_regions_intemperies = {}
        self.item_Nord = self.calc_moy_desc('Calais', 'Arras', 'Amiens', 'Laon', 'Beauvais')
        self.itemp_IDF = self.calc_moy_desc('Paris', 'Etampes', 'Mantes-la-Jolie', 'Provins')
        self.itemp_Normandie = self.calc_moy_desc('Rouen', 'Caen', 'Le Havre', 'Cherbourg', 'Flers', 'Evreux')
        self.itemp_Bretagne = self.calc_moy_desc('Brest', 'Saint-Malo', 'Quimper', 'Guingamp', 'Carhaix-Plouguer')
        self.itemp_Pays = self.calc_moy_desc('Chartres', 'Bourges', 'Tours', 'Orleans')
        self.itemp_Centre = self.calc_moy_desc('Nantes', 'Angers', 'Le Mans', 'Laval', 'Sant-Nazaire', 'Luçon')
        self.itemp_Auvergne = self.calc_moy_desc('Lyon', 'Clermont-Ferrand', 'Valence', 'Grenoble')
        self.itemp_Occitanie = self.calc_moy_desc('Perpignant', 'Montpellier', 'Tarbes', 'Figeac', 'Toulouse')
        self.intemp_Provence = self.calc_moy_desc('Nice', 'Marseille', 'Brançon', 'Arles', 'Avignon', 'Gap', 'Manosque')
        self.intemp_Bourgogne = self.calc_moy_desc('Besançon', 'Dijon', 'Belfort', 'Auxerre', 'Nevers', 'Macon')
        self.intemp_est = self.calc_moy_desc('Strasbourg', 'Reims', 'Nancy', 'Troyes', 'Mulhouse', 'Metz')
        self.intemp_NA = self.calc_moy_desc('La Rochelle', 'Bordeaux', 'Bayonne', 'Limoges', 'Poitiers')
        self.list_intemperies = [self.item_Nord, self.itemp_IDF, self.itemp_Normandie, self.intemp_Bourgogne, self.itemp_Occitanie, self.itemp_Centre, self.intemp_NA, self.intemp_est, self.intemp_Provence, self.itemp_Auvergne, self.itemp_Pays, self.itemp_Bretagne]
        self.list_regions = ['Nord', 'IDF', 'Normandie', 'Bourgogne', 'Occitanie', 'Centre', 'Nouvelle Aquitaine', 'Grand Est', 'Provence', 'Auvergne', 'Pays', 'Bretagne']
        self.dict_regions_intemperies = {
            'Nord' : [270, 30],
            'IDF' : [275, 110],
            'Normandie' : [130, 67],
            'Bourgogne' : [10, 120],
            'Occitanie' : [150, 130],
            'Centre' : [215, 250],
            'Nouvelle Aquitaine' : [220, 245],
            'Grand Est' : [
                160, 430],
            'Provence' : [340, 400],
            'Auvergne' : [305, 145],
            'Pays' : [330, 60],
            'Bretagne' : [118, 250]
        }
        self.image_orage = ImageTk.PhotoImage(Image.open('./icones/orages.jpg'))
        self.image_soleil = ImageTk.PhotoImage(Image.open('./icones/soleil.png'))
        self.image_nuage = ImageTk.PhotoImage(Image.open('./icones/nuages_soleil.jpg'))
        self.image_forte_pluie = ImageTk.PhotoImage(Image.open('./icones/forte_pluie.png'))
        self.eclaircies = ImageTk.PhotoImage(Image.open('./icones/eclaircies.png'))

        for i in range(len(self.list_regions)):
            if self.list_intemperies[i] != None:
                if self.list_regions[i] == "couvert" or self.list_intemperies[i] == "nuage":
                    self.can_map.create_image(self.dict_regions_intemperies[self.list_regions[i]][0],self.dict_regions_intemperies[self.list_regions[i]][1], image=self.image_nuage, anchor = "nw")
                elif self.list_regions[i] == "soleil":
                    self.can_map.create_image(self.dict_regions_intemperies[self.list_regions[i]][0], self.dict_regions_intemperies[self.list_regions[i]][1],image=self.image_soleil, anchor='nw')
                elif self.list_regions[i] == "Orages":
                    self.can_map.create_image(self.dict_regions_intemperies[self.list_regions[i]][0], self.dict_regions_intemperies[self.list_regions[i]][1],image=self.image_orage, anchor='nw')
                elif self.list_regions[i] == "__pluie":
                    self.can_map.create_image(self.dict_regions_intemperies[self.list_regions[i]][0], self.dict_regions_intemperies[self.list_regions[i]][1],image=self.image_forte_pluie, anchor='nw')
                elif self.list_regions[i] == "eclaircies":
                    self.can_map.create_image(self.dict_regions_intemperies[self.list_regions[i]][0], self.dict_regions_intemperies[self.list_regions[i]][1],image=self.eclaircies, anchor='nw')

    def moyenne_temp_region(self, nb_villes, *villes_name): 
        temp_sum = 0
        for arg in villes_name:
            temp_sum += self.get_infos_metropole(arg, False)['temperature']
        return temp_sum / nb_villes
        

    def get_infos_metropole(self,nom, print_info):
        self.place_metropole = self.client.search_places(nom)
        self.current_temp_metropole = self.client.get_observation_for_place(self.place_metropole[0])
        self.infos_metropole = {}
        self.infos_metropole['temperature'] = self.current_temp_metropole.temperature
        self.infos_metropole['vitesse du vent'] = self.current_temp_metropole.wind_speed
        self.infos_metropole['description generale'] = self.current_temp_metropole.weather_description
        if print_info:
            self.print_infos_metropole(nom)
        else:
            return self.infos_metropole


class User_space(Frame):
    def __init__(self, parent):
        self.frame_user_dim = (470, 500)
        Frame.__init__(self, parent, width=self.frame_user_dim[0], height=self.frame_user_dim[1])
        self.space_temperature = Frame(self, width=200, height=150)
        self.space_perturbations = Frame(self, width=200, height=100)

        #espace temperatures
        self.temp_froide = Temperature_legende(self.space_temperature, color_froide, '- de 10°')
        self.temp_moyenne = Temperature_legende(self.space_temperature, color_moyenne, '>15 et <28°')
        self.temp_chaude = Temperature_legende(self.space_temperature, color_chaud, '>28°')
        self.temp_froide.grid(row=0, column=0)
        self.temp_moyenne.grid(row=1, column=0)
        self.temp_chaude.grid(row=2, column=0)

        #espace perturbation


        self.space_perturbations.place(x=100, y=250)
        self.space_temperature.place(x=310, y=350)
        self.pack()        
            
class Temperature_legende(Frame):
    def __init__(self, parent, couleur, text):
        Frame.__init__(self, parent, width=100, height=20)
        self.legende_color = couleur
        self.legende_texte = text
        self.can_legende = Canvas(self, width=30, height=20) # à gauche
        self.rect = self.can_legende.create_rectangle(0, 0, 30, 20, fill=self.legende_color)
        self.lab_legend = Label(self, text=self.legende_texte, font=('Arial', 10))

        self.can_legende.bind('<Button-1>', self.manage_color)
        self.can_legende.pack(side=LEFT)
        self.lab_legend.pack(side=RIGHT)

    def manage_color(self, e):
        global color_froide, color_moyenne, color_normale, color_chaud, modify_chaud, modify_froid, modify_moy, modify_normal
        global old_norm, old_cold, old_moy, old_red
        if self.legende_color == color_froide:
            old_cold = color_froide
            color_froide = askcolor()[1]
            self.legende_color = color_froide
            self.can_legende.itemconfig(self.rect, fill=self.legende_color)
            modify_froid = True
            
        if self.legende_color == color_moyenne:
            old_moy = color_moyenne
            color_moyenne = askcolor()[1]
            self.legende_color = color_moyenne
            self.can_legende.itemconfig(self.rect, fill=self.legende_color)
            modify_moy = True

        if self.legende_color == color_normale:
            old_norm = color_normale
            color_normale = askcolor()[1]
            self.legende_color = color_normale
            self.can_legende.itemconfig(self.rect, fill=self.legende_color)
            modify_normal = True

        if self.legende_color == color_chaud:
            old_red = color_chaud
            color_chaud = askcolor()[1]
            self.legende_color = color_chaud
            self.can_legende.itemconfig(self.rect, fill=self.legende_color)
            modify_chaud = True


if __name__ == '__main__': 
    app = MeteoApp()
                        
    app.run_app()
    
    while 1:
        if modif_couleur:
            if modify_normal or modify_chaud  or modify_froid or modify_moy:
                if modify_froid:
                    for reg in app.carte.list_zone_region:
                        if app.carte.can_map.itemcget(reg, 'fill') == old_cold:
                            app.carte.can_map.itemconfig(reg, fill=color_froide)
                            modify_froid = False
                            modif_couleur = False
                elif modify_normal:
                    print("normal")
                    for reg in app.carte.list_zone_region:
                        if app.carte.can_map.itemcget(reg, 'fill') == old_norm:
                            app.carte.can_map.itemconfig(reg, fill=color_normale)
                            modify_normal = False
                            modif_couleur = False
                    
                elif modify_moy:
                    print("moyenne")
                    for reg in app.carte.list_zone_region:        
                        if app.carte.can_map.itemcget(reg, 'fill') == old_moy:
                            app.carte.can_map.itemconfig(reg, fill=color_moyenne)
                            modify_moy = False
                            modif_couleur = False
                    
                elif modify_chaud:
                    for reg in app.carte.list_zone_region:        
                        if app.carte.can_map.itemcget(reg, 'fill') == old_red:
                            app.carte.can_map.itemconfig(reg, fill=color_chaud)
                            modify_chaud = False
                            modif_couleur = False
