import mysql.connector
import time
import datetime
import sys
import logging

# Configurar o logger para escrever em um arquivo de log
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Criar um manipulador para direcionar a saída para o console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # Definir o nível de severidade desejado para a saída no console

# Adicionar o manipulador ao logger raiz
logger = logging.getLogger()
logger.addHandler(console_handler)

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

def verificar_e_inserir_dados(connection, topic, minuto_inteiro, data):
    ultimo_minuto_registrado = obter_ultimo_minuto_registrado(connection, topic)

    if ultimo_minuto_registrado is None or ultimo_minuto_registrado < minuto_inteiro:
        cursor = connection.cursor()
        media = calcular_media_por_minuto(data['valores'])
        count = data['count']
        query = "INSERT INTO {} (avg, min, max, cnt, topic, unit, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(timeseries_table_name)
        values = (media, min(data['valores']), max(data['valores']), count, topic, data['unit'], minuto_inteiro)
        cursor.execute(query, values)
        cursor.close()
        connection.commit()
        #print(f"{hora} >>>>INSERIDO COM SUCESSO<<<<")
        logger.debug(">>>INSERT OK<<<")
    else:
        print(f"{hora} Já existem registros para o minuto {minuto_inteiro}. Dados não serão duplicados.")
        logger.debug(f"Já existem registros para o minuto {minuto_inteiro}. Dados não serão duplicados.")

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

if __name__ == "__main__":
    # Definir o intervalo de tempo para o loop (por exemplo, a cada minuto)
    intervalo_minuto = 60
    last_logged_minute = None  # Variável para controlar o último minuto registrado

    while True:
        try:
            ultimo_minuto = int(time.time()) - (int(time.time()) % intervalo_minuto)
            unixt = datetime.datetime.now()
            hora = unixt.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{hora} Iniciando Ciclo")
            logger.debug("Iniciando Ciclo")

            if ultimo_minuto != last_logged_minute:  # Verifique se há novos dados a serem processados
                dados_por_topico = ler_dados_do_banco(ultimo_minuto)
                connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
                for (topic, minuto_inteiro), data in dados_por_topico.items():
                    verificar_e_inserir_dados(connection, topic, minuto_inteiro, data)
                connection.close()
                last_logged_minute = ultimo_minuto

            time.sleep(intervalo_minuto)
        except Exception as e:
            # Em caso de erro, registre as informações no log
            error_message = f"Erro: {str(e)}"
            print(error_message)
            logger.error(error_message)
