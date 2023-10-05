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


###Baixando o repositório
Baixe o repositorio na  pasta raiz, /home/seuusuario/

onde o caminho final deve ficar  /home/seuusuario/
