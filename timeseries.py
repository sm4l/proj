import mysql.connector
import time
import datetime

# Configurações do banco de dados MySQL
db_host = "localhost"  # Altere para o host do seu banco de dados MySQL
db_user = "seu_usuario_mysql"
db_password = "sua_senha_mysql"
db_name = "aeris"  # Nome do banco de dados
readings_table_name = "readings"  # Nome da tabela readings
timeseries_table_name = "timeseries"  # Nome da tabela timeseries

def calcular_media_por_minuto(valores_por_minuto):
    valores_validos = [v for v in valores_por_minuto if v is not None]
    return sum(valores_validos) / len(valores_validos) if valores_validos else None

def obter_ultimo_minuto_registrado(connection, topic):
    cursor = connection.cursor()
    query = "SELECT MAX(timestamp) FROM {} WHERE topic = %s".format(timeseries_table_name)
    cursor.execute(query, (topic,))
    ultimo_minuto = cursor.fetchone()[0]
    cursor.close()
    return ultimo_minuto

def ler_dados_do_banco(ultimo_minuto):
    # Estabelecer conexão com o banco de dados
    connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()

    # Consulta SQL para obter os dados da tabela readings referentes ao último minuto
    query = "SELECT topic, value, unit, timestamp FROM {} WHERE timestamp >= %s AND timestamp < %s AND timestamp IS NOT NULL AND value IS NOT NULL AND unit IS NOT NULL ORDER BY topic, timestamp".format(readings_table_name)
    cursor.execute(query, (ultimo_minuto, ultimo_minuto + 60))

    # Dicionário para armazenar as médias por minuto, unidades e contagem de leituras por minuto por tópico
    dados_por_topico = {}

    # Processar os resultados da consulta
    for topic, value, unit, timestamp in cursor.fetchall():
        # Arredondar para o minuto inteiro
        minuto_inteiro = timestamp - (timestamp % 60)

        key = (topic, minuto_inteiro)

        # Adicionar valor ao dicionário para cálculo posterior da média, unidade e contagem
        if key not in dados_por_topico:
            dados_por_topico[key] = {'valores': [value], 'unit': unit, 'count': 1}
        else:
            dados_por_topico[key]['valores'].append(value)
            dados_por_topico[key]['count'] += 1

    # Fechar a conexão com o banco de dados
    cursor.close()
    connection.close()

    return dados_por_topico

def escrever_dados_no_banco(dados_por_topico):
    # Estabelecer conexão com o banco de dados
    connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    
    for (topic, minuto_inteiro), data in dados_por_topico.items():
        ultimo_minuto_registrado = obter_ultimo_minuto_registrado(connection, topic)
        
        # Verificar se já existem registros para o último minuto
        if ultimo_minuto_registrado is not None and ultimo_minuto_registrado >= minuto_inteiro:
            #time.sleep(60)
            print(f"Já existem registros para o minuto {minuto_inteiro}. Dados não serão duplicados.")
            continue
        
        cursor = connection.cursor()

        media = calcular_media_por_minuto(data['valores'])
        count = data['count']

        # Consulta SQL para inserir os dados na tabela timeseries
        query = "INSERT INTO {} (avg, min, max, cnt, topic, unit, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(timeseries_table_name)
        values = (media, min(data['valores']), max(data['valores']), count, topic, data['unit'], minuto_inteiro)
        cursor.execute(query, values)

        cursor.close()

    # Confirmar as alterações no banco de dados
    connection.commit()

    # Fechar a conexão com o banco de dados
    connection.close()

if __name__ == "__main__":
    # Definir o intervalo de tempo para o loop (por exemplo, a cada minuto)
    intervalo_minuto = 60

    while True:
        # Obter o timestamp do último minuto
        ultimo_minuto = int(time.time()) - (int(time.time()) % intervalo_minuto)
        #obetendo hora atual
        unixt= datetime.datetime.now()
        hora=unixt.strftime('%Y-%m-%d %H:%M:%S')

        # Ler os dados da tabela readings relativos ao último minuto
        dados_por_topico = ler_dados_do_banco(ultimo_minuto)

        # Calcular as médias por minuto e escrever os dados na tabela timeseries
        escrever_dados_no_banco(dados_por_topico)

        print(str(hora)+" timeseries.py Calculo e Escrita OK .")

        # Esperar até o próximo ciclo (próximo minuto)
        time.sleep(intervalo_minuto)
