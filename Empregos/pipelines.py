
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
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100), 
            company_name VARCHAR (100),
            location Varchar(60),
            salary VARCHAR(20),
            description LONGTEXT,
            type_work VARCHAR (50),
            min_salary VARCHAR(20),
            max_salary VARCHAR (20),
            ref LONGTEXT
            );''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Empregos(title, company_name, location, salary, description, type_work, min_salary, max_salary, ref)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""" 
        
        cursor.execute(insert_query, [
                item.get("title"),
                item.get("company_name"),
                item.get("location"),
                item.get("salary"),
                item.get("description"),
                item.get("type_work"),       
                item.get("min_salary"),
                item.get("max_salary"),
                item.get("ref"),
            ])
        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()
