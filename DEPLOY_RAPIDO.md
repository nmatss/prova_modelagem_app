# 🚀 Deploy Rápido - Docker

## Para usar em Docker EXISTENTE:

### Opção 1: Build e Run Manual
```bash
# Build
docker build -t prova_modelagem:latest .

# Run
docker run -d \
  --name prova_modelagem \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  -e SECRET_KEY="mude-esta-chave" \
  prova_modelagem:latest
```

### Opção 2: Adicionar ao docker-compose existente
```yaml
  prova_modelagem:
    build: ./prova_modelagem_app
    ports:
      - "5000:5000"
    volumes:
      - ./prova_modelagem_app/data:/app/data
      - ./prova_modelagem_app/uploads:/app/uploads
    environment:
      - SECRET_KEY=sua-chave-aqui
```

### Opção 3: Standalone (docker-compose próprio)
```bash
docker-compose up -d
```

## Acessar:
- URL: http://localhost:5000
- Usuário: admin
- Senha: admin123

## Documentação completa:
Ver DOCKER_DEPLOY.md
