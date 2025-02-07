# Trabalho Final de Sistemas Distribuídos (DCC064) - 2024.3

# 🚀 Setup do Ambiente com Docker

## 📌 Requisitos
- Instalar **Docker**: [Download e instalação](https://www.docker.com/get-started)

---

## 🔹 Criar Rede Docker
```sh
docker network create minha-network
```

---

## 🗄️ Banco de Dados - MongoDB
```sh
docker run --name mongodb --network minha-network -p 27017:27017 -d mongodb/mongodb-community-server:latest
```
📌 **Documentação MongoDB**: [Instalação via Docker](https://www.mongodb.com/pt-br/docs/manual/tutorial/install-mongodb-community-with-docker/)

### 🖥️ Ferramenta Gráfica para MongoDB
- **MongoDB Compass (GUI)**: [Download](https://www.mongodb.com/try/download/compass)

---

## 📨 Mensageria - RabbitMQ
```sh
docker run -d --hostname my-rabbit --network minha-network --name rabbit13 -p 8080:15672 -p 5672:5672 -p 25676:25676 rabbitmq:3-management
```
📌 **Tutorial RabbitMQ com Docker**: [Acesse aqui](https://medium.com/xp-inc/rabbitmq-com-docker-conhecendo-o-admin-cc81f3f6ac3b)

---

## 🌐 Backend - Flask
📌 **Tutorial sobre Flask com Docker**: [Leia mais](https://akiradev.netlify.app/posts/flask-docker/)

### ✅ Usando Imagem Pronta (Docker Hub)
```sh
docker run -d --name middleware --network minha-network -p 5000:5000 -v $(pwd)/src:/app/src lucasg4x/sd-middleware
```

### 📦 Usando Dockerfile Local
```sh
docker build -t flask-docker:latest .
docker run -d --name middleware --network minha-network -p 5000:5000 -v $(pwd)/src:/app/src flask-docker
```

### 🌍 Acessar API
```
http://localhost:5000/sensor/
```

---

## ⚙️ Workers e Tarefas

### 🎯 Rodar Worker (Supervisor já faz isso automaticamente!)
```sh
docker exec -it middleware python src/worker.py
```

### 📝 Criar Nova Tarefa
```sh
docker exec -it middleware python src/new_task.py
```

### 🔄 Recriar Container Flask
```sh
docker stop middleware && docker rm middleware && docker build -t lucasg4x/sd-middleware . && docker run -d --name flask --network minha-network -p 5000:5000 -v $(pwd)/src:/app/src lucasg4x/sd-middleware
```

### 📊 Verificar Status dos Workers
```sh
supervisorctl status
```

---

## 🛠️ Comandos Úteis

### 🛑 Parar Todos os Containers
```sh
docker stop $(docker ps -aq)
```

### 🗑️ Remover Todos os Containers
```sh
docker rm $(docker ps -aq)
```

### 🖼️ Remover Todas as Imagens
```sh
docker rmi $(docker images -aq)
```

### 🔗 Remover Redes Não Utilizadas
```sh
docker network prune -f
```

### 💾 Remover Volumes Não Utilizados
```sh
docker volume prune -f
```

### 🧹 Limpeza Completa (Containers, Imagens, Volumes, Redes)
```sh
docker system prune -a --volumes -f
```

---

## 🚀 Agora seu ambiente está pronto! 🔥

