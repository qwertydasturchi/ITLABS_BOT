import sqlite3
class Database:
    
    
    
    def __init__(self):
        self.conn = sqlite3.connect('baza_bot.db')
        self.cur = self.conn.cursor()
    
    
    
    
    ####################################### users table uchun #######################################
    
    
    
    def create_table(self):
        self.cur.execute("""
                         create table if not exists  users(
                             telegram_id varchar(50),
                             username varchar(50)
                             )""")
    
    
    def insert_user(self, telegram_id: str, username: str):
        self.cur.execute("""
                         insert into users values ("{}", "{}")
                         """.format(telegram_id, username))
        self.conn.commit()
    
    
    def select_user(self, telegram_id):
        self.cur.execute("""
                         select * from users where telegram_id="{}" 
                         """.format(telegram_id))
        data = self.cur.fetchone()
        return data
    
    def select_users(self):
        self.cur.execute("""
                         select telegram_id from users 
                         """)
        data = self.cur.fetchall()
        return data
    
    
    
    
    ###############################  kurslar uchun  #######################################
    
    
    
    def create_table_kurs(self):
        self.cur.execute("""
                         create table if not exists  kurslar(
                             id INTEGER PRIMARY KEY   AUTOINCREMENT,
                             nomi varchar (50),
                             vaqti varchar(50),
                             davomiyligi varchar (50),
                             narxi varchar (50),
                             discription text,
                             photo text
                            )
                            """)
    
    
    def select_kurslar(self):
        self.cur.execute("""
                         select * from kurslar
                         """)
        data = self.cur.fetchall()
        return data
    
    
    
    def select_kurs(self, id: str):
        self.cur.execute("""
                         select * from kurslar where id="{}" 
                         """.format(id))
        data = self.cur.fetchone()
        return data
    
    
    def insert_kurs(self, nomi: str, vaqti: str, davomiyligi: str, narxi: str, discription: str, photo: str):
        self.cur.execute("""
                         insert into kurslar(nomi, vaqti, davomiyligi, narxi, discription, photo) values("{}","{}","{}","{}","{}","{}")
                         """.format(nomi, vaqti, davomiyligi, narxi, discription, photo))
        self.conn.commit()
    
    
    ##########################  filiallar uchun ###################
    
    
    
    def create_table_filial(self):
        self.cur.execute("""
                         create table if not exists filiallar(
                         t_r INTEGER PRIMARY KEY   AUTOINCREMENT,
                         nomi varchar(50),
                         location varchar(50)    
                         )
                         """)
    
    
    def select_filiallar(self):
        self.cur.execute("""
                         select * from filiallar
                         """)
        data = self.cur.fetchall()
        return data

    
    def select_filial(self, t_r: str):
        self.cur.execute("""
                         select * from filiallar where t_r="{}"
                         """.format(t_r))
        data = self.cur.fetchone()
        return data




####################  Admin uchun  #####################################


    def select_kurs_by_name(self, name: str):
        self.cur.execute("""
                         select * from kurslar where name="{}"
                         """.format(name))
        data = self.cur.fetchone()
        return data

    
    
    # def update_kurs_by_name(self, nomi: str, vaqti: str, davom: str, narx: str, disc: str, foto: str):
    #     self.cur.execute("""update users set nomi="{}", vaqti="{}", davom="{}", narxi="{}", disc="{}", foto="{}" where nomi="{}" """.format(nomi, vaqti, davom, narx, disc, foto, nomi))
    #     return self.conn.commit()


    # def update_kurs_name(self, new_name: str, name: str):
    #     self.cur.execute("""
    #                      update kurslar set nomi='{}' where nomi='{}'""".format(new_name, name))
    #     return self.conn.commit()


    # def update_kurs_vaqt(self, vaqt: str, name: str):
    #     self.cur.execute("""
    #                      update kurslar set vaqti='{}' where nomi='{}'
    #                      """.format(vaqt, name))
    #     return self.conn.commit()

    
    # def update_kurs_davom(self, davom: str, name: str):
    #     self.cur.execute("""
    #                      update kurslar set davomiyligi='{}' where nomi='{}'
    #                      """.format(davom, name))
    #     return self.conn.commit()



    # def update_kurs_narx(self, narx: str, name: str):
    #     self.cur.execute("""
    #                      update kurslar set narx='{}' where nomi='{}'
    #                      """.format(narx, name))
    #     return self.conn.commit()


    # def update_kurs_disc(self, disc: str, name: str):
    #     self.cur.execute("""
    #                      update kurslar set discriptoin='{}' where nomi='{}'
    #                      """.format(disc, name))
    #     return self.conn.commit()



    # def update_kurs_foto(self, foto: str, name: str):
    #     self.cur.execute("""
    #                      update kurslar set photo='{}' where nomi='{}'
    #                      """.format(foto, name))
    #     return self.conn.commit()


    def update_kurs_by_name(self,  old: str, new: str, name: str):
        self.cur.execute("""
                         update kurslar set '{}'='{}' where nomi='{}'
                         """.format(old, new, name))
        data =  self.conn.commit()
        return data
    
    def delete_kurs_by_name(self, name: str):
        self.cur.execute("""
                         delete from kurslar where nomi='{}'
                         """.format(name))
        data = self.conn.commit()
        return data





# db = Database()
# filial = db.select_filiallar()
# filial1= filial[0]
# filial2 = filial1[0]
# print(filial2)









# data = Database()

# info = data.select_filial(2)
# inf = info[2]
# belgi = inf.index(" ")
# latitude = inf[:belgi]
# longitude = inf[belgi+1: ]
# print(latitude, longitude)



 