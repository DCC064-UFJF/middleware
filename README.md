# Configuração do Ambiente
# 🚀 Setup do Ambiente com Docker

## 📌 Requisitos
- Instalar **Docker**: [Download e instalação](https://www.docker.com/get-started)

---

## Criar arquivo .env a partir do exemplo
```sh
cp .env.example .env
```


## Criar rede

```sh
docker network create minha-network
```
## 🗄️ Banco de Dados - MongoDB
```sh
docker run --name mongodb --network minha-network -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

### 🖥️ Ferramenta Gráfica para MongoDB

- **MongoDB Compass (GUI)**: [Download](https://www.mongodb.com/try/download/compass)

## 📨 Mensageria - RabbitMQ
```sh
docker run -d --hostname my-rabbit --network minha-network --name rabbit13 -p 8080:15672 -p 5672:5672 -p 25676:25676 rabbitmq:3-management
```

## 🌐 Backend - Flask

<!-- ### ✅ Usando Imagem Pronta (Docker Hub)
```sh
docker run -d --name middleware-prod --network  minha-network -p 5001:5000 lucasg4x/sd-middleware
``` -->

### 📦 Usando Dockerfile Local
```sh
docker build -t middleware-local:latest .
```
```sh
docker run -d --name middleware-local --network minha-network -p 5001:5000 -v $(pwd)/src:/app/src middleware-local
```

## ⚙️ Workers e Tarefas

### 🎯 Rodar Workers (Supervisor já faz isso automaticamente!)
```sh
docker exec -it middleware-local python src/worker.py
```

### 📝 Criar Nova Tarefa
```sh
docker exec -it middleware-local python src/new_task.py
```

### 🔄 Recriar Container Flask
```sh
docker stop middleware-local && docker rm middleware-local
```

```sh
docker build -t middleware-local:latest . && docker run -d --name middleware-local --network minha-network -p 5001:5000 -v $(pwd)/src:/app/src middleware-local
```


## 🛠️ Comandos Úteis

### 🛑 Parar Todos os Containers
```sh
docker stop $(docker ps -aq)
```

### 🧹 Limpeza Completa (Containers, Imagens, Volumes, Redes)
```sh
docker system prune -a --volumes -f
```



<!-- ## Criar ambiente virtual

```sh
python -m venv .venv
```

## Ativar ambiente virtual

### Windows
```sh
.venv\Scripts\activate
```

### Mac/Linux
```sh
source .venv/bin/activate
```

## Instalar as dependências do requirements.txt

```sh
pip install -r requirements.txt
```

## Subir os workers

```sh
python src/worker.py
python src/worker_actuator.py
```

## Criar novas tarefas

```sh
python src/new_task.py 
```-->



# Documentação da API 

Esta API fornece acesso a informações sobre circuitos, sensores e atuadores. Abaixo estão descritas as rotas disponíveis, com exemplos de requisição e resposta.

## Endpoints

### 1. Listar todos os circuitos
- **Rota:** `GET /circuits`
- **Descrição:** Retorna um array com os IDs dos circuitos existentes.
- **Exemplo de requisição:**
  ```http
  GET http://localhost:5001/circuits
  ```
- **Exemplo de resposta:**
  ```json
  ["1", "2", "3"]
  ```

### 2. Listar dispositivos de um circuito
- **Rota:** `GET /circuits/{circuit_id}/devices`
- **Descrição:** Retorna todos os dados de sensores e atuadores de um determinado circuito.
- **Exemplo de requisição:**
  ```http
  GET http://localhost:5001/circuits/1/devices
  ```
- **Exemplo de resposta:**
  ```json
  [
    {
    "circuito_id": 1,
    "id": 6,
    "timestamp": "2025-02-19T18:29:14.225767",
    "tipo": "Pressao",
    "valor": 34.0578674458435
  },
  {
    "circuito_id": 1,
    "id": 2,
    "timestamp": "2025-02-19T18:29:16.403370",
    "tipo": "Pressao",
    "valor": 39.275676128273176
  },
  ]
  ```

### 3. Obter o último valor de um sensor
- **Rota:** `GET /circuits/{circuit_id}/sensor/{sensor_id}/last`
- **Descrição:** Retorna o último valor registrado de um sensor de um circuito.
- **Exemplo de requisição:**
  ```http
  GET http://localhost:5001/circuits/3/sensor/2/last
  ```
- **Exemplo de resposta:**
  ```json
  {
  "circuito_id": 3,
  "id": 2,
  "timestamp": "2025-02-19T18:26:30.676066",
  "tipo": "Pressao",
  "valor": 36.32905832453196
    }
  ```

### 4. Obter o último valor de um atuador
- **Rota:** `GET /circuits/{circuit_id}/actuator/{actuator_id}/last`
- **Descrição:** Retorna o último valor registrado de um atuador de um circuito.
- **Exemplo de requisição:**
  ```http
  GET http://localhost:5001/circuits/1/actuator/4/last
  ```
- **Exemplo de resposta:**
  ```json
  {
  "circuito_id": 1,
  "id": 4,
  "timestamp": "2025-02-19T18:29:11.785804",
  "valor": 1
    }
  ```

### 5. Obter valores de um sensor em um período específico
- **Rota:** `GET /circuits/{circuit_id}/sensor/{sensor_id}/all?start_date={start_date}&end_date={end_date}`
- **Descrição:** Retorna todos os dados registrados de um sensor dentro de um período específico.
- **Parâmetros:**
  - `start_date` (string, obrigatório): Data e hora de início no formato ISO 8601 (ex: `2025-01-01T00:00:00`)
  - `end_date` (string, obrigatório): Data e hora de fim no formato ISO 8601 (ex: `2025-02-31T23:59:59`)
- **Exemplo de requisição:**
  ```http
  GET http://localhost:5001/circuits/3/sensor/2/all?start_date=2025-01-01T00:00:00&end_date=2025-02-31T23:59:59
  ```
- **Exemplo de resposta:**
  ```json
  [
    {
        "circuito_id": 3,
        "id": 2,
        "timestamp": "2025-02-19T18:26:30.676066",
        "tipo": "Pressao",
        "valor": 36.32905832453196
    },
    {
        "circuito_id": 3,
        "id": 2,
        "timestamp": "2025-02-19T18:48:26.674557",
        "tipo": "Pressao",
        "valor": 31.264318936627966
    }
    ]
  ```

- **Caso nenhum dado seja encontrado:**
  ```json
  {
    "end_date": "2025-01-31T23:59:59",
    "message": "No data found",
    "start_date": "2025-01-01T00:00:00"
    }
  ```


