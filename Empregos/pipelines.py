from itemadapter import ItemAdapter
from Empregos.DataBase.Mysql_connection import Mysql_Connector

class EmpregosPipeline:
    def process_item(self, item, spider):
        
         
        self.save_mysql(item)

    def save_mysql(self, item):
        connector = Mysql_Connector.Connection()
        cursor = connector[0]
        db_connection = connector[1]

        cursor.execute(
           '''CREATE TABLE IF NOT EXISTS Empregos(
            title VARCHAR(100), 
            company_name VARCHAR (100),
            location Varchar(60),
            salary VARCHAR(20),
            description LONGTEXT
            );''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Empregos(title, company_name, location, salary, description)
                        VALUES (%s, %s, %s, %s, %s)""" 
        
        cursor.execute(insert_query, (
            item["title"],
            item["company_name"],
            item["location"],
            item["salary"],
            item["description"]
        ))

        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()
