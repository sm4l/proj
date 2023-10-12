import paho.mqtt.client as mqtt #pip install paho-mqtt
import json
import mysql.connector #pip install mysql-connector-python
import time
import datetime
import sys

sys.stdout = open('/home/proj/logreadings.log', 'a')
sys.stderr = sys.stdout

# Configurações do MQTT
broker_address = "aerisiot.com"
mqtt_topic = "+/update/sensor/+"

# Configurações do banco de dados MySQL
db_host = "localhost"  # Altere para o host do seu banco de dados MySQL
db_user = "seu_usuario_mysql"
db_password = "sua_senha_mysql"
db_name = "aeris"  # Nome do banco de dados
readings_table_name = "readings"  # Nome da tabela readings
timeseries_table_name = "timeseries"  # Nome da tabela timeseries

# Variáveis para armazenar os valores dos últimos dados de cada minuto
last_minute_values = []

# Função de callback para quando a conexão com o MQTT é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com sucesso.")
    client.subscribe(mqtt_topic)

# Função de callback para quando uma mensagem do MQTT é recebida
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic

        # Check if the topic contains both "update" and "sensor"
        if "update" in topic and "sensor" in topic:
            # Conectar ao banco de dados MySQL
            connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            cursor = connection.cursor()

            # Inserir os dados na tabela readings
            insert_query = "INSERT INTO {} (topic, value, unit, timestamp) VALUES (%s, %s, %s, %s)".format(readings_table_name)
            data = (topic, payload.get("value"), payload.get("unit"), payload.get("ts"))
            cursor.execute(insert_query, data)
            connection.commit()

            # Fechar a conexão com o banco de dados
            cursor.close()
            connection.close()
            # obetendo hora atual
            unixt = datetime.datetime.now()
            hora = unixt.strftime('%Y-%m-%d %H:%M:%S')
            #print(str(hora) + " readings.py INSERT OK.")
        else:
            print("Skipped inserting data from topic:", topic)
    except Exception as e:
        erro = e
        unixt = datetime.datetime.now()
        hora = unixt.strftime('%Y-%m-%d %H:%M:%S')
        print(str(hora) + " Erro readings:", e)

# Configurar o cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker MQTT
client.connect(broker_address, 1883, 60)

# Iniciar o loop para ficar escutando mensagens
client.loop_start()

while True:
    time.sleep(1)
