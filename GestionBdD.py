import sqlite3

class GestionBdD:
    def __init__ (self):
        self.conn = sqlite3.connect('DBFormation.db')
        
    def insert_module(self, semestre, code, nom):
        cursor = self.conn.cursor()

        cursor.execute('''INSERT INTO Modules (semestre, code, nom)
                          VALUES (?, ?, ?)''', (semestre, code, nom))

        self.conn.commit()

    def insert_responsable(self, nom, prenom):
        cursor = self.conn.cursor()

        cursor.execute('''INSERT INTO Responsable (nom, prenom)
                          VALUES (?, ?)''', (nom, prenom))

        self.conn.commit()

    def insert_resp_mod(self, idMod, idResp):
        cursor = self.conn.cursor()

        cursor.execute('''INSERT INTO resp_mod (idMod, idResp)
                          VALUES (?, ?)''', (idMod, idResp))

        self.conn.commit()

    def insert_compt_acquis(self, idMod, Intitule, ComptAsso):
        cursor = self.conn.cursor()

        cursor.execute('''INSERT INTO Compt_Acquis (idMod, Intitule, ComptAsso)
                          VALUES (?, ?, ?)''', (idMod, Intitule, ComptAsso))

        self.conn.commit()

    def insert_Pre_Requis(self, idMod, idModPR):
        cursor = self.conn.cursor()

        cursor.execute('''INSERT INTO Pre_Requis (idMod, idModPR)
                          VALUES (?, ?)''', (idMod, idModPR))

        self.conn.commit()

    def get_responsable_id(self, nom, prenom):
        cursor = self.conn.cursor()

        query = "SELECT idResp FROM Responsable WHERE nom = ? AND prenom = ?"
        cursor.execute(query, (nom, prenom))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def get_list_codes(self):
        cursor = self.conn.cursor()

        query = "SELECT * FROM Modules WHERE 1"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def get_module_id(self, code):
        cursor = self.conn.cursor()

        query = "SELECT idMod FROM Modules WHERE code = ?"
        cursor.execute(query, (code,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0
