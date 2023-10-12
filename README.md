# GRAFANA
#### Lucas Augusto Mendes Silva
#### email: lucasmendess96@outlook.com

## Requisitos: 

- Ubuntu 22.04.2 LTS;
- Quad-Core 4GB (8GB recomendado)

- Python3
- pip3

### Instalando Grafana 

Instale os pacotes de pré- requisito

```bash
sudo apt-get install -y apt-transport-https software-properties-common wget
```
Importar a GPG key:

```bash
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/graf
```

Adicionar a Lista APT
   ```bash
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```
Baixar gpgkey
   ```bash
  wget -q -O - https://packages.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana.gpg > /dev/null
```


Atualize seu cache APT para atualizar suas listas de pacotes:
   ```bash
sudo apt update
   ```
Agora você pode prosseguir com a instalação:
   ```bash
sudo apt install grafana
```
Depois que o Grafana estiver instalado, use systemctl para iniciar o servidor Grafana:
   ```bash

sudo systemctl start grafana-server
```

### Instalando MariaDB
   ```bash
sudo apt update
sudo apt install mariadb-server
   ```
### CRIANDO O BANCO DE DADOS
Abra um terminal e acesse o MariaDB como root:

```bash
sudo mysql -u root -p
```
Em seguida, crie um usuário que pode se conectar de qualquer host:

   ```bash
CREATE USER 'seu_usuario_mysql'@'%' IDENTIFIED BY 'sua_senha_mysql';
   ```

Conceda permissões ao usuário para o banco de dados "aeris":
   ```bash
GRANT ALL PRIVILEGES ON aeris.* TO 'seu_usuario_mysql'@'%';
   ```

Certifique-se de que o usuário tenha permissões para acessar o banco de dados "aeris":

Atualize as permissões do MariaDB:
```bash
FLUSH PRIVILEGES;
```
Saia do MariaDB:
```bash
EXIT;
```
Reinicie o serviço MariaDB:
```bash
sudo service mariadb restart
```


### CRIANDO O BANCO DE DADOS
Passo 1: Entre no mysql
```bash 
sudo mysql
```
Passo 2: Crie o Banco de Dados "aeris"
No MariaDB, execute o seguinte comando para criar o banco de dados "aeris":

```bash
CREATE DATABASE aeris;
```
Passo 3: Use o Banco de Dados "aeris"
Execute o seguinte comando para usar o banco de dados "aeris":

```bash
USE aeris;
```
Passo 4: Crie a Tabela "timeseries"
Execute o seguinte comando para criar a tabela "timeseries":

```bash
CREATE TABLE timeseries (
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(128) NOT NULL,
    avg FLOAT,
    min FLOAT,
    max FLOAT,
    cnt INT(11),
    unit VARCHAR(32),
    timestamp INT(11)
);
```
Passo 5: Crie a Tabela "readings"
Execute o seguinte comando para criar a tabela "readings":

```bash
CREATE TABLE readings (
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(128) NOT NULL,
    value FLOAT,
    unit VARCHAR(32),
    timestamp INT(11)
);
```
Agora você criou o banco de dados "aeris" com as tabelas "timeseries" e "readings" prontas para serem usadas em seu projeto.

### Baixando o repositório
   ```bash
git clone https://github.com/sm4l/proj.git
   ```
Extraia repositorio na  pasta raiz, /home/seuusuario/

onde o caminho final deve ficar  /home/seuusuario/proj


execute o comando para instalar os repositórios necessários para os scripts de gravação.
   ```bash
pip3 install -r requirements.txt 
   ```

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
   User=SEUUSUARIO
   Group=SEUGRUPO
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


# REPETIR O MESMO PROCESSO PARA READINGS.PY

## CRIANDO OS SERVIÇOS 

Para criar um serviço que execute os programas timeseries.py e readings.py sempre que o sistema é iniciado e os reinicie em caso de falha, você pode usar o systemd, um sistema de inicialização comum em sistemas Linux modernos. Aqui estão os passos para criar um serviço systemd para cada um dos seus programas:

Crie os serviços systemd:

bash
sudo nano /etc/systemd/system/timeseries.service

b. No arquivo de serviço, adicione o seguinte conteúdo (substitua /caminho/para/timeseries.py pelo caminho absoluto para o arquivo timeseries.py):

```bash
[Unit]
Description=Timeseries Program
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/proj/timeseries.py
WorkingDirectory=/home/proj
Restart=always
User=seu_usuario
Group=seu_grupo

[Install]
WantedBy=multi-user.target

```
Também, substitua seu_usuario e seu_grupo pelo seu nome de usuário e grupo.
c. Salve o arquivo e saia do editor.

d. Crie um arquivo de serviço semelhante para o readings.py:

```bash
sudo nano /etc/systemd/system/readings.service
```
```bash
Copy code
[Unit]
Description=Readings Program
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/proj/readings.py
WorkingDirectory=/home/proj
Restart=always
User=seu_usuario
Group=seu_grupo

[Install]
WantedBy=multi-user.target
```
Recarregue o systemd:

```bash

sudo systemctl daemon-reload
```
Inicie e habilite os serviços:

```bash
sudo systemctl start timeseries
sudo systemctl enable timeseries
sudo systemctl start readings
sudo systemctl enable readings
```

Verifique o status dos serviços:
Você pode verificar o status dos serviços a qualquer momento com os comandos:

```
bash
sudo systemctl status timeseries
sudo systemctl status readings
```

Os serviços devem ser iniciados e configurados para reiniciar automaticamente em caso de falha. Certifique-se de que o caminho para os arquivos Python esteja correto e que o usuário e grupo sejam definidos corretamente nos arquivos de serviço.



