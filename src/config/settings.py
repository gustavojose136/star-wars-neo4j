import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
dotenv_path = os.getenv('DOTENV_PATH', '.env')
load_dotenv(dotenv_path)

class Settings:
    """Configurações centralizadas do sistema"""
    
    # Neo4j
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "star_wars.db")
    
    # App
    APP_NAME = "Star Wars Knowledge Graph QA"
    APP_VERSION = "1.0.0"
    
    @classmethod
    def validate(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        required_vars = [
            "NEO4J_URI",
            "NEO4J_USER", 
            "NEO4J_PASSWORD",
            "GOOGLE_API_KEY"
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(cls, var):
                missing.append(var)
        
        if missing:
            raise ValueError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing)}")
        
        return True 