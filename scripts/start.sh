#!/bin/bash

# Script de inicialização do Star Wars QA System

echo "🌟 Iniciando Star Wars Knowledge Graph QA System..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado. Criando a partir do exemplo..."
    cp env.example .env
    echo "📝 Por favor, edite o arquivo .env com suas credenciais antes de continuar."
    echo "   Especialmente a GOOGLE_API_KEY é obrigatória."
    exit 1
fi

# Verificar se GOOGLE_API_KEY está configurada
if ! grep -q "GOOGLE_API_KEY=sua_chave_api_do_google_aqui" .env; then
    echo "✅ Configurações encontradas no .env"
else
    echo "❌ GOOGLE_API_KEY não configurada no .env"
    echo "   Por favor, edite o arquivo .env e configure sua API key do Google."
    exit 1
fi

echo "🚀 Iniciando serviços com Docker Compose..."

# Iniciar serviços
docker-compose up -d

echo "⏳ Aguardando Neo4j inicializar..."
sleep 30

# Verificar se Neo4j está respondendo
echo "🔍 Verificando conexão com Neo4j..."
if curl -s http://localhost:7474 > /dev/null; then
    echo "✅ Neo4j está respondendo"
else
    echo "⚠️  Neo4j ainda não está respondendo. Aguardando mais 30 segundos..."
    sleep 30
fi

echo "📊 Acesse o Neo4j Browser em: http://localhost:7474"
echo "   Usuário: neo4j"
echo "   Senha: starwars123"

echo "🤖 Para executar o sistema QA:"
echo "   docker-compose logs -f app"

echo "🎉 Sistema iniciado com sucesso!" 