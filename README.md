# Projeto de Extração de Compromissos

Este repositório contém os comandos essenciais para construir e interagir com a imagem Docker do projeto de extração de compromissos. O objetivo é facilitar a execução do script Python em um ambiente containerizado, garantindo consistência e portabilidade.

## Pré-requisitos Locais

Para que o aplicativo funcione corretamente, é **essencial** que você tenha um arquivo `.env` configurado na **máquina local** (no mesmo diretório onde você executa os comandos Docker). Este arquivo deve conter as variáveis de ambiente necessárias para o script Python.

## Comandos Docker Essenciais

A seguir, estão os comandos que você precisará para gerenciar a imagem e o container Docker deste projeto.

### 1. Construir a Imagem Docker

Este comando constrói a imagem Docker a partir do `Dockerfile` presente no diretório atual. A imagem será nomeada `get-compromissos-app`.

docker build -t get-compromissos-app .


### 2. Rodar o Script Python na Imagem Docker

Este comando cria e executa um novo container a partir da imagem `get-compromissos-app`, passando os argumentos necessários para o script Python.

docker run get-compromissos-app python get_compromissos.py {sigla} {data-inicio} {data-fim}


**Exemplo:**

docker run get-compromissos-app python get_compromissos.py MEC 28-07-2025 28-07-2025


### 3. Identificar o Nome do Container

Após executar o comando `docker run`, o Docker pode atribuir um nome aleatório ao container se você não especificar um. Use este comando para listar todos os containers (em execução ou parados) e encontrar o nome gerado.

docker ps -a


* **Identifique o nome do container na coluna "NAMES" (última coluna).** Por exemplo, você pode ver algo como `magical_cohen` ou `upbeat_kirch`.

### 4. Iniciar um Container Existente (se estiver parado)

Se o seu container estiver no estado "Exited" (parado), você precisará iniciá-lo antes de interagir com ele (por exemplo, para copiar arquivos). Lembre-se de usar o **nome real do container** (que você identificou no passo anterior), não o nome da imagem.

docker start 


**Exemplo (usando o nome hipotético que renomeamos anteriormente):**

docker start get-compromissos-app-container


### 5. Copiar a Pasta "temp" para a Máquina Local

A pasta `temp` dentro do container é onde os compromissos extraídos são salvos. Use este comando para copiar todo o conteúdo dessa pasta para o diretório atual da sua máquina local.

docker cp 


**Exemplo (usando o nome hipotético que renomeamos anteriormente):**

docker cp get-compromissos-app-container:/app/temp/ .# Extração do E-Agendas
Extração do E-Agendas ....
