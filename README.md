# grafanamqtt
MQTT dashboard project with grafana


## Requisitos: 
Ubuntu 22.04.2 LTS
Python3
pip3

###Instalando Grafana 

Baixar Repositorio
  wget -q -O - https://packages.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana.gpg > /dev/null

Adicionar a Lista APT
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

Atualize seu cache APT para atualizar suas listas de pacotes:

sudo apt update

Agora você pode prosseguir com a instalação:

sudo apt install grafana

Depois que o Grafana estiver instalado, use systemctl para iniciar o servidor Grafana:

sudo systemctl start grafana-server


### Instalando MariaDB

sudo apt update
sudo apt install mariadb-server


### Baixando o repositório

https://github.com/sm4l/grafanamqtt.git

Extraia repositorio na  pasta raiz, /home/seuusuario/

onde o caminho final deve ficar  /home/seuusuario/proj


execute o comando para instalar os repositórios necessários para os scripts de gravação.
pip3 install -r requirements.txt 


### Criando os serviços

Você deve criar os serviços para que os scripts fiquem rodando de forma constante para isso siga os passos

Vamos criar um serviço systemd chamado `timeseries.service` para executar o script `timeseries.py` localizado na pasta `/home/seuusuario/proj`. 

Aqui estão os passos para fazer isso:

1. Crie um arquivo de serviço systemd:

   Abra um terminal e execute o seguinte comando para criar um arquivo de serviço systemd:

   ```bash
   nano /etc/systemd/system/timeseries.service
   ```

2. Adicione o seguinte conteúdo ao arquivo `timeseries.service`:

   ```plaintext
   [Unit]
   Description=Serviço Timeseries

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /home/seuusuario/proj/timeseries.py
   WorkingDirectory=/home/seuusuario/proj
   Restart=on-failure
   RestartSec=30

   [Install]
   WantedBy=multi-user.target
   ```

   Certifique-se de substituir `/home/seuusuario/proj/timeseries.py` pelo caminho real para o seu script Python.

3. Salve o arquivo e saia do editor.

4. Atualize o systemd:

   Recarregue o systemd para que ele tome conhecimento do novo serviço:

   ```bash
   sudo systemctl daemon-reload
   ```

5. Inicie o serviço e defina-o para iniciar na inicialização:

   ```bash
   sudo systemctl start timeseries
   sudo systemctl enable timeseries
   ```

6. Verifique o status do serviço:

   ```bash
   sudo systemctl status timeseries
   ```

   Isso mostrará informações sobre o serviço, incluindo se ele está em execução ou não.

Agora, o seu script `timeseries.py` será executado continuamente como um serviço systemd e será iniciado automaticamente na inicialização do sistema. Certifique-se de ajustar as permissões do arquivo do seu script conforme necessário para garantir que o systemd possa executá-lo.

