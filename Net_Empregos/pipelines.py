from Net_Empregos_Database.MySql_Connection import Mysql_Connector
from Net_Empregos.items import NetEmpregosItem


class NetEmpregosPipeline:
    def process_item(self, item, spider):
        #print(item)

        connector = Mysql_Connector.Connection()
        cursor = connector[0]
        db_connection = connector[1]
        

        cursor.execute(
           """CREATE TABLE IF NOT EXISTS Empregos(
            Name VARCHAR(200),
            Description LONGTEXT,
            Organization VARCHAR(100),
            Location VARCHAR(100),
            Ref LONGTEXT
            );"""
        )

        db_connection.commit()      

        insert_query = """
                    INSERT INTO  Empregos(Name, Description, Organization, Location, Ref)
                    VALUES (%s, %s, %s, %s, %s)"""
        

        cursor.execute(insert_query, (
            item["Name"],
            item["Organization"],
            item["Location"],
            item["Ref"],
            item["Description"]
        ))

        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()
