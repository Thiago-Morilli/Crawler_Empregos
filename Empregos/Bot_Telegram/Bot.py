import telebot 
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DataBase.Mysql_connection import Mysql_Connector

CHAVE_API = "7594338375:AAEfZMrMETc7_8Kehdh4gvBlWFmkDFE4VNY"

bot = telebot.TeleBot(CHAVE_API)


@bot.message_handler(func=lambda msg: True)
def user(mensagem):
    chat_id = mensagem.chat.id
    bot.send_message(chat_id, "Ola, Em qual cidade você quer buscar empregos?")
    bot.register_next_step_handler(mensagem, looking_for_jobs)

def looking_for_jobs(mensagem):
    cidade = mensagem.text.strip()

    conn = Mysql_Connector.Connection()
    cursor = conn[0]
    query = """SELECT title, company_name, type_work, salary, min_salary, max_salary, ref
    FROM Empregos 
    WHERE location = %s
    LIMIT 10"""
    cursor.execute(query, (cidade,))
    jobs = cursor.fetchall()
    
    if not jobs:
        bot.send_message(mensagem.chat.id, f"{cidade} não encontrada. Tente outra cidade!")
        bot.register_next_step_handler(mensagem, looking_for_jobs)  
        return
    
    resposta = f"Empregos em {cidade}:\n\n"

    for job in jobs:
        title, company, work_type, salary, min_salary, max_salary, ref = job
        resposta +=(
            f"Cargo: {title}\n"
            f"Empresa: {company}\n"
            f"Modelo: {work_type}\n"
            f"Salário: {salary}\n"
            f"Maximo Salario: {max_salary}\n"
            f"Minimo Salario: {min_salary}\n"
            f"Ref: {ref}\n"
            f"-----------------------------\n"
            )
        
    bot.send_message(mensagem.chat.id, resposta)
    

    cursor.close()
    conn[1].close()

bot.polling()

   