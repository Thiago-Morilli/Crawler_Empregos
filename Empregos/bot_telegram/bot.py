import telebot 
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DataBase.Mysql_connection import Mysql_Connector

CHAVE_API = "7594338375:AAEfZMrMETc7_8Kehdh4gvBlWFmkDFE4VNY"

bot = telebot.TeleBot(CHAVE_API)


@bot.message_handler(func=lambda msg: True)  
def responder(mensagem):
    city = mensagem.text.strip()  

    connector = Mysql_Connector.Connection()
    cursor = connector[0]
    db_connection = connector[1]
       
    query = """SELECT title, company_name, type_work, salary 
    FROM Empregos 
    WHERE location = %s"""
    cursor.execute(query, (city,))
    jobs = cursor.fetchall()

    if jobs:
        resposta = f"Todos empregos em {city}:\n\n"
        for job in jobs:
            title, company, work_type, salary = job
            resposta += (
                f"Cargo: {title}\n"
                f"Empresa: {company}\n"
                f"Modelo: {work_type}\n"
                f"Salário: {salary}\n"
                f"-----------------------------\n"
            )

    bot.reply_to(mensagem, resposta, parse_mode="Markdown")

    cursor.close()
    db_connection.close()

bot.polling()
