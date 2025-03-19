# 🚀 Configuração do Ambiente com Docker

## 📌 Requisitos
- **Docker**: [Download e Instalação](https://www.docker.com/get-started)
- **MongoDB Compass (GUI - Opcional)**: [Download](https://www.mongodb.com/try/download/compass)

---

## 🔧 Configuração Inicial

### 📄 Criar arquivo `.env` a partir do exemplo
```sh
cp .env.example .env
```

### 🌐 Criar Rede Docker
```sh
docker network create minha-network
```

---

## 🗄️ Banco de Dados - MongoDB
```sh
docker run --name mongodb --network minha-network -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

---

## 📨 Mensageria - RabbitMQ
```sh
docker run -d --hostname my-rabbit --network minha-network --name rabbitmq -p 8080:15672 -p 5672:5672 -p 25676:25676 rabbitmq:3-management
```

---

## 🌐 Backend - Flask

### 📦 Criar Imagem Docker Localmente
```sh
docker build -t middleware-local:latest .
```

### 🚀 Executar Container
```sh
docker run -d --name middleware-local --network minha-network -p 5001:5000 -v $(pwd)/src:/app/src middleware-local
```

### 🔄 Reiniciar Container (Build e Run)
```sh
docker stop middleware-local && docker rm middleware-local
```
```sh
docker build -t middleware-local:latest . && docker run -d --name middleware-local --network minha-network -p 5001:5000 -v $(pwd)/src:/app/src middleware-local
```

---

## ⚙️ Workers e Tarefas

### 🎯 Executar Workers (Supervisor gerencia automaticamente)
```sh
docker exec -it middleware-local python src/worker.py
```

### 📝 Criar Nova Tarefa
```sh
docker exec -it middleware-local python src/new_task.py
```

### 📊 Verificar Status dos Workers
```sh
docker exec -it middleware-local supervisorctl status
```

---

## 🛠️ Comandos Úteis

### 🛑 Parar Todos os Containers
```sh
docker stop $(docker ps -aq)
```

### 🧹 Limpeza Completa (Containers, Imagens, Volumes, Redes)
```sh
docker system prune -a --volumes -f
```

### 📤 Publicar Imagem no Docker Hub
```sh
docker build -t lucasg4x/sd-middleware:1.1 .
docker login -u <usuario>
docker push lucasg4x/sd-middleware:1.1
```

---

# 📚 Documentação da API

Esta API fornece acesso a informações sobre circuitos, sensores e atuadores. Abaixo estão descritas as rotas disponíveis, com exemplos de requisição e resposta.

## 🌍 Endpoints

### 1️⃣ Listar Todos os Circuitos
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

---

### 2️⃣ Listar Dispositivos de um Circuito
- **Rota:** `GET /circuits/{circuit_id}/devices`
- **Descrição:** Retorna todos os sensores e atuadores de um circuito.
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
      "valor": 34.05
    },
    {
      "circuito_id": 1,
      "id": 2,
      "timestamp": "2025-02-19T18:29:16.403370",
      "tipo": "Pressao",
      "valor": 39.27
    }
  ]
  ```

---

### 3️⃣ Obter o Último Valor de um Sensor
- **Rota:** `GET /circuits/{circuit_id}/sensor/{sensor_id}/last`
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
    "valor": 36.32
  }
  ```

---

### 4️⃣ Obter o Último Valor de um Atuador
- **Rota:** `GET /circuits/{circuit_id}/actuator/{actuator_id}/last`
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

---

### 5️⃣ Obter Valores de um Sensor em um Período Específico
- **Rota:** `GET /circuits/{circuit_id}/sensor/{sensor_id}/all?start_date={start_date}&end_date={end_date}`
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
      "valor": 36.32
    },
    {
      "circuito_id": 3,
      "id": 2,
      "timestamp": "2025-02-19T18:48:26.674557",
      "tipo": "Pressao",
      "valor": 31.26
    }
  ]
  ```

---

📌 **Caso nenhum dado seja encontrado:**
```json
{
  "message": "No data found",
  "start_date": "2025-01-01T00:00:00",
  "end_date": "2025-01-31T23:59:59"
}
```

