# 🌟 Star Wars Knowledge Graph QA System

Sistema inteligente de perguntas e respostas sobre o universo Star Wars, construído com Neo4j, LangChain e Google Gemini.

## 🎬 Demonstração

<video src="./Demonstracao_star_wars-1751935682659.mp4"
       width="800"
       controls>
  Vídeo não suportado.
</video>

*Demonstração do sistema em funcionamento - Chat interativo respondendo perguntas sobre Star Wars*

## 🚀 Características

- **Knowledge Graph**: Dados estruturados em grafo usando Neo4j
- **QA Inteligente**: Sistema de perguntas e respostas em linguagem natural
- **Correção Automática**: Busca fuzzy para nomes de personagens
- **Docker**: Containerização completa com Docker Compose
- **Arquitetura Modular**: Código organizado e escalável

## 📁 Arquitetura do Projeto

```
star-wars/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── qa_system.py          # Sistema principal de QA
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py           # Configurações centralizadas
│   ├── utils/
│   │   ├── __init__.py
│   │   └── database.py           # Utilitários de banco
│   └── __init__.py
├── tests/                        # Testes unitários
├── docs/                         # Documentação
├── main.py                       # Ponto de entrada da aplicação
├── requirements.txt              # Dependências Python
├── Dockerfile                    # Container da aplicação
├── docker-compose.yml           # Orquestração Docker
├── setup.py                     # Script de instalação
└── README.md                    # Este arquivo
```

## 🛠️ Tecnologias

- **Python 3.11+**
- **Neo4j 5.15** - Banco de dados de grafos
- **LangChain** - Framework para LLMs
- **Google Gemini** - Modelo de linguagem
- **Docker & Docker Compose** - Containerização

## 🚀 Quick Start

### 1. Pré-requisitos

- Docker e Docker Compose instalados
- API Key do Google Gemini

### 2. Configuração

```bash
# Clone o repositório
git clone <repository-url>
cd star-wars

# Configure a API Key do Google
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env
```

### 3. Executar com Docker

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Executar importação de dados (opcional)
docker-compose --profile import up importer
```

### 4. Executar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas credenciais

# Executar aplicação
python main.py
```

### 5. Chat Interativo

#### Chat no Terminal
```bash
python chat.py
```

#### Chat Web (Interface Gráfica)
```bash
python web_chat.py
# Acesse: http://localhost:5000
```

## 📊 Dados Disponíveis

O sistema inclui dados sobre:

- **96 Personagens** (Luke Skywalker, Darth Vader, etc.)
- **13 Planetas** (Tatooine, Coruscant, etc.)
- **40 Espécies** (Human, Wookiee, etc.)
- **60 Naves** (Millennium Falcon, X-wing, etc.)
- **60 Armas** (Lightsaber, Blaster, etc.)
- **8 Organizações** (Jedi Order, Rebel Alliance, etc.)
- **99 Citações** famosas

## 💬 Exemplos de Perguntas

### Perguntas que o Sistema Responde

#### 👤 Sobre Personagens
```bash
"Quem é Luke Skywalker?"
"Fale sobre Han Solo"
"Informações sobre Darth Vader"
"Quem é o pai do Anakin?"
```

#### 📊 Contagem e Estatísticas
```bash
"Quantas naves Han Solo pilota?"
"Quantos personagens existem?"
"Quantas citações Darth Vader tem?"
```

#### 📋 Listagem
```bash
"Listar personagens"
"Quais naves existem?"
"Listar citações de Darth Vader"
"Quais personagens são da espécie Wookiee?"
```

#### 🌍 Relacionamentos
```bash
"Em que planeta Luke nasceu?"
"Qual a espécie de Chewbacca?"
"Quais filmes Luke aparece?"
"Quem pilota a Millennium Falcon?"
```

### Exemplo de Resposta
```
🤖 Sua pergunta: quem é han solo?
💡 Resposta: Nome: Han Solo
Gênero: Male
Espécie: Human
Planeta natal: Corellia
Naves: Millennium Falcon
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=starwars123

# Google Gemini
GOOGLE_API_KEY=sua_chave_aqui

# Logging
LOG_LEVEL=INFO
```

### Docker Compose

O `docker-compose.yml` inclui:

- **neo4j**: Banco de dados Neo4j com APOC
- **app**: Aplicação principal
- **importer**: Serviço para importar dados (perfil opcional)

## 🧪 Testes

```bash
# Executar testes
python -m pytest tests/

# Executar com cobertura
python -m pytest --cov=src tests/
```

## 📈 Monitoramento

### Neo4j Browser
- URL: http://localhost:7474
- Usuário: neo4j
- Senha: starwars123

### Logs
```bash
# Logs da aplicação
docker-compose logs app

# Logs do Neo4j
docker-compose logs neo4j
```

## 🎬 Demonstração do Sistema

### Vídeo de Demonstração
Assista ao vídeo demonstrativo para ver o sistema em ação:

[![Demonstração Star Wars QA](https://img.shields.io/badge/🎬-Ver_Demonstração-red?style=for-the-badge)](Demonstracao_star_wars-1751935682659.mp4)

### Screenshots do Sistema

#### Chat Terminal
```
🌟 STAR WARS KNOWLEDGE GRAPH CHAT 🌟
============================================================
💬 Faça perguntas sobre o universo Star Wars!

🤖 Sua pergunta: quem é han solo?
💡 Resposta: Nome: Han Solo
Gênero: Male
Espécie: Human
Planeta natal: Corellia
Naves: Millennium Falcon
```

#### Chat Web
- Interface gráfica moderna
- Chat visual com bolhas de mensagem
- Design responsivo
- Acessível via http://localhost:5000

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com Neo4j**
   ```bash
   # Verificar se o Neo4j está rodando
   docker-compose ps
   
   # Reiniciar serviços
   docker-compose restart
   ```

2. **Erro de API Key**
   ```bash
   # Verificar variável de ambiente
   echo $GOOGLE_API_KEY
   
   # Verificar arquivo .env
   cat .env
   ```

3. **Dados não carregados**
   ```bash
   # Executar importação
   docker-compose --profile import up importer
   ```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- [Neo4j](https://neo4j.com/) - Banco de dados de grafos
- [LangChain](https://langchain.com/) - Framework para LLMs
- [Google Gemini](https://ai.google.dev/) - Modelo de linguagem
- [Star Wars API](https://swapi.dev/) - Dados do universo Star Wars

---

**Que a Força esteja com você!** 🚀
