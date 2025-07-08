@echo off
REM Script de inicialização do Star Wars QA System para Windows

echo 🌟 Iniciando Star Wars Knowledge Graph QA System...

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não está instalado. Por favor, instale o Docker primeiro.
    pause
    exit /b 1
)

REM Verificar se Docker Compose está instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro.
    pause
    exit /b 1
)

REM Verificar se arquivo .env existe
if not exist .env (
    echo ⚠️  Arquivo .env não encontrado. Criando a partir do exemplo...
    copy env.example .env
    echo 📝 Por favor, edite o arquivo .env com suas credenciais antes de continuar.
    echo    Especialmente a GOOGLE_API_KEY é obrigatória.
    pause
    exit /b 1
)

REM Verificar se GOOGLE_API_KEY está configurada
findstr "GOOGLE_API_KEY=sua_chave_api_do_google_aqui" .env >nul
if not errorlevel 1 (
    echo ❌ GOOGLE_API_KEY não configurada no .env
    echo    Por favor, edite o arquivo .env e configure sua API key do Google.
    pause
    exit /b 1
) else (
    echo ✅ Configurações encontradas no .env
)

echo 🚀 Iniciando serviços com Docker Compose...

REM Iniciar serviços
docker-compose up -d

echo ⏳ Aguardando Neo4j inicializar...
timeout /t 30 /nobreak >nul

echo 🔍 Verificando conexão com Neo4j...
curl -s http://localhost:7474 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Neo4j ainda não está respondendo. Aguardando mais 30 segundos...
    timeout /t 30 /nobreak >nul
)

echo 📊 Acesse o Neo4j Browser em: http://localhost:7474
echo    Usuário: neo4j
echo    Senha: starwars123

echo 🤖 Para executar o sistema QA:
echo    docker-compose logs -f app

echo 🎉 Sistema iniciado com sucesso!
pause 