import logging
import sys
from src.core.qa_system import StarWarsDynamicQA
from src.config.settings import Settings

logging.basicConfig(
    level=getattr(logging, Settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Função principal da aplicação"""
    try:
        Settings.validate()
        logger.info("Configurações validadas com sucesso")
        
        qa_system = StarWarsDynamicQA()
        logger.info("Sistema QA inicializado com sucesso")
        
        # Exemplos de perguntas
        example_queries = [
            "Quantas naves Han Solo pilota?",
            "Listar citações de Darth Vader",
            "Quem é Luke Skywalker?",
            "Listar personagens"
        ]
        
        print("=== STAR WARS KNOWLEDGE GRAPH QA ===")
        print(f"Versão: {Settings.APP_VERSION}")
        print("=" * 50)
        
        for query in example_queries:
            print(f"\n🤖 Pergunta: {query}")
            try:
                answer = qa_system.ask(query)
                print(f"💡 Resposta: {answer}")
            except Exception as e:
                logger.error(f"Erro ao processar pergunta '{query}': {e}")
                print(f"❌ Erro: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Sistema funcionando corretamente!")
        
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        print(f"❌ Erro de configuração: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 