#!/usr/bin/env python3
"""
Chat interativo para o sistema Star Wars Knowledge Graph QA
"""

import os
import sys
from dotenv import load_dotenv

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.qa_system import StarWarsDynamicQA
from src.config.settings import Settings

def print_banner():
    """Imprime o banner do chat"""
    print("=" * 60)
    print("🌟 STAR WARS KNOWLEDGE GRAPH CHAT 🌟")
    print("=" * 60)
    print("💬 Faça perguntas sobre o universo Star Wars!")
    print("📝 Exemplos de perguntas:")
    print("   • Quem é Luke Skywalker?")
    print("   • Quantas naves Han Solo pilota?")
    print("   • Listar citações de Darth Vader")
    print("   • Em que planeta Luke nasceu?")
    print("   • Quais personagens são da espécie Wookiee?")
    print("   • Listar personagens")
    print("=" * 60)
    print("💡 Digite 'sair' para encerrar")
    print("💡 Digite 'ajuda' para ver exemplos")
    print("=" * 60)

def print_help():
    """Mostra exemplos de perguntas"""
    print("\n🎯 EXEMPLOS DE PERGUNTAS:")
    print("-" * 40)
    print("📊 CONTAGEM:")
    print("   • Quantas naves Han Solo pilota?")
    print("   • Quantos personagens existem?")
    print("   • Quantas citações Darth Vader tem?")
    print()
    print("📋 LISTAGEM:")
    print("   • Quais naves Han Solo pilota?")
    print("   • Listar citações de Darth Vader")
    print("   • Quais personagens são da espécie Wookiee?")
    print("   • Listar personagens")
    print()
    print("👤 DETALHES:")
    print("   • Quem é Luke Skywalker?")
    print("   • Fale sobre Han Solo")
    print("   • Informações sobre Darth Vader")
    print()
    print("🌍 RELACIONAMENTOS:")
    print("   • Em que planeta Luke nasceu?")
    print("   • Qual a espécie de Chewbacca?")
    print("   • Quais filmes Luke aparece?")
    print("-" * 40)

def main():
    """Função principal do chat"""
    try:
        # Carregar configurações
        load_dotenv()
        
        # Validar configurações
        Settings.validate()
        print("✅ Configurações validadas com sucesso")
        
        # Inicializar sistema QA
        qa_system = StarWarsDynamicQA()
        print("✅ Sistema QA inicializado com sucesso")
        
        # Mostrar banner
        print_banner()
        
        # Loop principal do chat
        while True:
            try:
                # Obter pergunta do usuário
                pergunta = input("\n🤖 Sua pergunta: ").strip()
                
                # Verificar comandos especiais
                if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                    print("\n👋 Até logo! Que a Força esteja com você!")
                    break
                
                if pergunta.lower() in ['ajuda', 'help', 'h']:
                    print_help()
                    continue
                
                if not pergunta:
                    print("❌ Por favor, digite uma pergunta.")
                    continue
                
                # Processar pergunta
                print("🔄 Processando...")
                resposta = qa_system.ask(pergunta)
                
                # Mostrar resposta
                print(f"💡 Resposta: {resposta}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrompido. Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro ao processar pergunta: {e}")
                print("💡 Tente reformular sua pergunta.")
    
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        print("💡 Verifique o arquivo .env")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 