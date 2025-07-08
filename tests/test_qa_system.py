#!/usr/bin/env python3
"""
Testes para o sistema de QA do Star Wars
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.qa_system import StarWarsDynamicQA
from src.config.settings import Settings

class TestStarWarsQA:
    """Testes para o sistema de QA"""
    
    @pytest.fixture
    def mock_neo4j(self):
        """Mock do Neo4j para testes"""
        with patch('core.qa_system.Neo4jGraph') as mock_graph:
            mock_instance = Mock()
            mock_graph.return_value = mock_instance
            yield mock_instance
    
    @pytest.fixture
    def qa_system(self, mock_neo4j):
        """Sistema QA com Neo4j mockado"""
        with patch.dict(os.environ, {
            'NEO4J_URI': 'bolt://localhost:7687',
            'NEO4J_USER': 'neo4j',
            'NEO4J_PASSWORD': 'password',
            'GOOGLE_API_KEY': 'test_key'
        }):
            return StarWarsDynamicQA()
    
    def test_init(self, qa_system):
        """Testa inicialização do sistema"""
        assert qa_system.neo4j_uri == 'bolt://localhost:7687'
        assert qa_system.neo4j_user == 'neo4j'
        assert qa_system.neo4j_password == 'password'
        assert 'naves' in qa_system.relation_map
    
    def test_determine_intent_count(self, qa_system):
        """Testa detecção de intent para contagem"""
        intent = qa_system._determine_intent("Quantas naves Han Solo pilota?", "Han Solo")
        assert intent == "count"
    
    def test_determine_intent_list(self, qa_system):
        """Testa detecção de intent para listagem"""
        intent = qa_system._determine_intent("Quais naves Han Solo pilota?", "Han Solo")
        assert intent == "list"
    
    def test_determine_intent_detail(self, qa_system):
        """Testa detecção de intent para detalhes"""
        intent = qa_system._determine_intent("Quem é Luke Skywalker?", "Luke Skywalker")
        assert intent == "detail"
    
    def test_build_cypher_count(self, qa_system):
        """Testa construção de Cypher para contagem"""
        relation = ("PILOTS", "Starship", "name")
        cypher = qa_system._build_cypher("count", "Han Solo", relation)
        assert "count(x) AS count" in cypher
        assert "Han Solo" in cypher
    
    def test_build_cypher_list(self, qa_system):
        """Testa construção de Cypher para listagem"""
        relation = ("PILOTS", "Starship", "name")
        cypher = qa_system._build_cypher("list", "Han Solo", relation)
        assert "x.name AS value" in cypher
        assert "Han Solo" in cypher
    
    def test_build_cypher_detail(self, qa_system):
        """Testa construção de Cypher para detalhes"""
        cypher = qa_system._build_cypher("detail", "Luke Skywalker", None)
        assert "OPTIONAL MATCH" in cypher
        assert "Luke Skywalker" in cypher
    
    def test_format_response_count(self, qa_system):
        """Testa formatação de resposta para contagem"""
        data = [{"count": 3}]
        response = qa_system._format_response("count", data)
        assert response == "Total: 3"
    
    def test_format_response_list(self, qa_system):
        """Testa formatação de resposta para listagem"""
        data = [{"value": "Millennium Falcon"}, {"value": "X-wing"}]
        response = qa_system._format_response("list", data)
        assert "Millennium Falcon" in response
        assert "X-wing" in response
    
    def test_format_response_detail(self, qa_system):
        """Testa formatação de resposta para detalhes"""
        data = [{
            "name": "Luke Skywalker",
            "gender": "male",
            "birth_year": "19BBY",
            "species": "Human",
            "planet": "Tatooine",
            "ships": ["X-wing"],
            "quotes": ["May the Force be with you"]
        }]
        response = qa_system._format_response("detail", data)
        assert "Luke Skywalker" in response
        assert "Human" in response
        assert "Tatooine" in response
    
    def test_ask_with_entity_detection(self, qa_system, mock_neo4j):
        """Testa detecção de entidade na pergunta"""
        mock_neo4j.query.return_value = [{"count": 2}]
        
        response = qa_system.ask("Quantas naves Han Solo pilota?")
        
        # Verifica se a query foi executada
        mock_neo4j.query.assert_called_once()
        call_args = mock_neo4j.query.call_args[0][0]
        assert "Han Solo" in call_args
    
    def test_ask_with_relation_detection(self, qa_system, mock_neo4j):
        """Testa detecção de relação na pergunta"""
        mock_neo4j.query.return_value = [{"value": "Millennium Falcon"}]
        
        response = qa_system.ask("Quais naves Han Solo pilota?")
        
        # Verifica se a query foi executada
        mock_neo4j.query.assert_called_once()
        call_args = mock_neo4j.query.call_args[0][0]
        assert "PILOTS" in call_args

class TestSettings:
    """Testes para configurações"""
    
    def test_settings_defaults(self):
        """Testa valores padrão das configurações"""
        assert Settings.NEO4J_URI == "bolt://localhost:7687"
        assert Settings.NEO4J_USER == "neo4j"
        assert Settings.APP_NAME == "Star Wars Knowledge Graph QA"
    
    def test_settings_validation_missing_vars(self):
        """Testa validação com variáveis faltantes"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                Settings.validate()
            assert "Variáveis de ambiente obrigatórias" in str(exc_info.value)
    
    def test_settings_validation_success(self):
        """Testa validação bem-sucedida"""
        with patch.dict(os.environ, {
            'NEO4J_URI': 'bolt://localhost:7687',
            'NEO4J_USER': 'neo4j',
            'NEO4J_PASSWORD': 'password',
            'GOOGLE_API_KEY': 'test_key'
        }):
            assert Settings.validate() is True

if __name__ == "__main__":
    pytest.main([__file__]) 