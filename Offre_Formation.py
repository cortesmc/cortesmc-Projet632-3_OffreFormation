from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import service
from difflib import SequenceMatcher
from time import sleep
from GestionBdD import *
import csv

class Offre_Formation:

    def __init__(self):
        self.list_responsables = []

        self.GestBdD = GestionBdD()
        PATH = "C:\Program Files (x86)\chromedrive.exe"
        options = webdriver.ChromeOptions() 
        #options.add_argument("--auto-open-devtools-for-tabs")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
        #options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.polytech.univ-smb.fr/intranet/accueil.html")
        sleep(2)
        gestionBD = GestionBdD ()

        btnCookies = self.driver.find_element(By.XPATH,("/html/body/div[4]/div[3]/button[1]"))
        btnCookies.click()

        self.login("utilisateur", "Mot de passe")
        
        self.getToModules()
        self.displayModules('idu')
        
        self.setModules(gestionBD)

        self.set_info_independant(gestionBD)

    def getToModules(self):
        navigator = self.driver.find_element(By.XPATH,('/html/body/div[3]/div/div/div/div[1]/ul/li[3]/ul/li[2]/a'))
        #navigator = self.driver.fing_element(By.XPATH,('/html/body/div[3]/div/div/div/div[1]/ul/li[3]/ul/li[2]/a'))
        self.driver.get(navigator.get_attribute('href'))
        
    def displayModules(self,specialite):
        navigator = self.driver.find_element(By.ID,(f'{specialite}_5'))
        navigator.click()

        navigator = self.driver.find_element(By.CLASS_NAME,('submit'))
        navigator.click()
    
    def setModules(self, gestionBD):
        listModules= self.driver.find_element(By.CLASS_NAME,('items'))
        cpt = 1

        semestre = self.driver.find_element(By.XPATH,('/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[2]/div[2]/ul/li[1]')).text
        while(True):
            try:
                semestreTmp = self.driver.find_element(By.XPATH,(f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{cpt}]/div[2]/ul/li[1]')).text

                if (semestreTmp.startswith('S')):
                    semestre = semestreTmp

                elem_code = self.driver.find_element(By.XPATH,(f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{cpt}]/div[2]/ul/li[3]')).text
                elem_intitule = self.driver.find_element(By.XPATH,(f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{cpt}]/div[2]/ul/li[4]/a')).text
                gestionBD.insert_module(semestre, elem_code, elem_intitule)
                cpt=cpt+1
            except :
                print('All the modules have been set into the data base.')
                break


    def set_info_independant(self, gestionBD):
        cpt = 1
        while True:
            try:
                elem_code = self.driver.find_element(By.XPATH,(f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{cpt}]/div[2]/ul/li[3]')).text
                navigator = self.driver.find_element(By.XPATH, (f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[{cpt}]/div[2]/ul/li[4]/a'))

                self.driver.get(navigator.get_attribute('href'))

                self.set_responsable(gestionBD, elem_code)

                self.set_Acquis_apprentissage(gestionBD,elem_code)

                self.set_Pre_Requis(gestionBD,elem_code)

                sleep(1)
                self.driver.back()
                cpt += 1
            except:
                break

    def set_responsable(self, gestionBD, code_module):
        elem_respo = self.driver.find_element(By.XPATH,('/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[3]/div[2]/div[2]'))
        list_noms = self.traitement_responsable(elem_respo.text)

        for list_names in list_noms:
            doesNotExists = True
            try:
                for elemexistant in self.list_responsables:
                    if elemexistant ==[]:
                        continue
                    if self.similar(list_names[0], elemexistant[0]) > 0.75 and self.similar(list_names[1], elemexistant[1]) > 0.75:
                        print(list_names ,' ya existe')
                        doesNotExists = False
                if doesNotExists :
                    gestionBD.insert_responsable(list_names[0], list_names[1])
                    self.list_responsables.append(list_names)
                    print('se agrego a ', list_names)
            except:
                continue

        self.set_resp_module(gestionBD, code_module, list_noms)

    def traitement_responsable(self,text):
        list_noms_final = []

        list_noms = []
        for ind, letter in enumerate(text):
            if letter == '@':
                tmp_letter = letter
                cpt = ind
                while tmp_letter != " ":
                    tmp_letter = text[cpt]
                    cpt -= 1
                    if cpt == 0:
                        break
                nom = text[cpt:ind]
                parts = nom.split(".")
                list_noms.append(parts)

        for elem_list in list_noms:
            new_elem = []
            for elem_name in elem_list:
                name = elem_name.replace(' ', '')
                name = name.replace(';', '')
                name = name.replace(',', '')
                new_elem.append(name)
            list_noms_final.append(new_elem)
        return list_noms_final

    def set_resp_module(self, gestionBD, code_module, list_respo):
        for elem_respo in list_respo:
            id_respo = 0
            for respo in self.list_responsables:
                if self.similar(elem_respo[0], respo[0]) > 0.75 and self.similar(elem_respo[1],respo[1]) > 0.75:
                    nom = respo[0]
                    prenom = respo[1]
                    id_respo = gestionBD.get_responsable_id(nom, prenom)
            gestionBD.insert_resp_mod(gestionBD.get_module_id(code_module), id_respo)

    def set_Acquis_apprentissage(self, gestionBD,  code_module):
        id_mod = gestionBD.get_module_id(code_module)
        cpt_intitule = 1
        while True:
            try:
                intitule = self.driver.find_element(By.XPATH,(f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[15]/div[1]/div[2]/div[{cpt_intitule}]/div[1]/div[1]/div[2]')).text

                cpt_comp = 1
                while True:
                    try:
                        comp_spe = self.driver.find_element(By.XPATH,(f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[15]/div[1]/div[2]/div[{cpt_intitule}]//div[4]/div[1]/div[2]/div[{cpt_comp}]/div/div[1]/div')).text
                        cpt_comp += 1
                        gestionBD.insert_compt_acquis(id_mod,intitule,comp_spe)
                    except:
                        break
                cpt_intitule += 1
            except :
                break

    def set_Pre_Requis(self, gestionBD,  code_module):
        try:
            list_codes = gestionBD.get_list_codes()
            id_mod = gestionBD.get_module_id(code_module)
            temp = self.driver.find_element(By.XPATH,(f'/html/body/div[2]/div/div/div/div[2]/div/div[5]/div[3]/div/div[2]/div[2]/div[10]/div[1]/div[2]/div/p')).text
            temp = temp.replace(' ', '')

            for elem in list_codes:
                if temp.__contains__(elem[2]):
                    id_modPR = gestionBD.get_module_id(elem[2])
                    gestionBD.insert_Pre_Requis(id_mod,id_modPR)


        except:
            print('error 175')
    def login(self,user,pw):
        input_user = self.driver.find_element(By.ID,("user"))
        input_password = self.driver.find_element(By.ID,("pass"))
        # Sending input text to search field
        input_user.send_keys(user)
        input_password.send_keys(pw)
        # Pressing enter to search input text
        input_user.send_keys(Keys.ENTER)
        sleep(3)

    def similar(self, a , b):
        return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
    
    Offre_Formation()