import sqlite3

# Connect to database
conn = sqlite3.connect('DBFormation.db')



cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Modules
                  (idMod INTEGER PRIMARY KEY,
                   semestre TEXT NOT NULL,
                   code TEXT NOT NULL,
                   nom TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Responsable
                  (idResp INTEGER PRIMARY KEY,
                   nom TEXT NOT NULL,
                   prenom TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS resp_mod
                  (idMod INTEGER NOT NULL,
                   idResp INTEGER NOT NULL,
                   FOREIGN KEY (idMod) REFERENCES Modules(idMod),
                   FOREIGN KEY (idResp) REFERENCES Responsable(idResp),
                   PRIMARY KEY (idMod, idResp))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Compt_Acquis
                  (idCA INTEGER PRIMARY KEY,
                   idMod INTEGER NOT NULL,
                   Intitule TEXT NOT NULL,
                   ComptAsso TEXT NOT NULL,
                   FOREIGN KEY (idMod) REFERENCES Modules(idMod))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Pre_Requis
                  (idPR INTEGER PRIMARY KEY,
                   idMod INTEGER NOT NULL,
                   idModPR INTEGER NOT NULL,
                   FOREIGN KEY (idModPR) REFERENCES Modules(idMod),
                   FOREIGN KEY (idMod) REFERENCES Modules(idMod))''')

conn.commit()

    