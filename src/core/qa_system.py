import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
import logging
from difflib import get_close_matches

# Carrega variáveis de ambiente
dotenv_path = os.getenv('DOTENV_PATH', '.env')
load_dotenv(dotenv_path)

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StarWarsDynamicQA:
    """
    Sistema de QA dinâmico para Star Wars,
    com intent detection e formatação amigável
    """
    def __init__(self):
        # Config Neo4j
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
        self._setup_neo4j()

        # Map: palavra-chave → (relacionamento, label, propriedade)
        self.relation_map = {
            "naves": ("PILOTS", "Starship", "name"),
            "ship": ("PILOTS", "Starship", "name"),
            "citações": ("SAID", "Quote", "text"),
            "quotes": ("SAID", "Quote", "text"),
            "espécies": ("IS_SPECIES", "Species", "name"),
            "espécie": ("IS_SPECIES", "Species", "name"),
            "planeta": ("BORN_ON", "Planet", "name"),
            "filmes": ("APPEARS_IN", "Film", "title"),
            "filme": ("APPEARS_IN", "Film", "title"),
        }

    def _setup_neo4j(self):
        try:
            self.graph = Neo4jGraph(
                url=self.neo4j_uri,
                username=self.neo4j_user,
                password=self.neo4j_password
            )
            logger.info("Conectado ao Neo4j com sucesso")
        except Exception as e:
            logger.error(f"Falha ao conectar Neo4j: {e}")
            raise

    def _determine_intent(self, question: str, entity: str) -> str:
        ql = question.lower()
        if ql.startswith("quant") or "quantos" in ql or "quantas" in ql:
            return "count"
        if ql.startswith("quais") or ql.startswith("listar"):
            return "list"
        if entity:
            return "detail"
        return "list"

    def _build_cypher(self, intent: str, entity: str, relation) -> str:
        if intent == "count" and relation:
            rel, lbl, prop = relation
            return (
                f"MATCH (c:Character {{name: \"{entity}\"}})"
                f"-[:{rel}]->(x:{lbl}) RETURN count(x) AS count"
            )
        if intent == "list" and relation:
            rel, lbl, prop = relation
            return (
                f"MATCH (c:Character {{name: \"{entity}\"}})"
                f"-[:{rel}]->(x:{lbl}) RETURN x.{prop} AS value"
            )
        if intent == "detail":
            return (
                f"MATCH (c:Character {{name: \"{entity}\"}})\n"
                f"OPTIONAL MATCH (c)-[:IS_SPECIES]->(s:Species)\n"
                f"OPTIONAL MATCH (c)-[:BORN_ON]->(p:Planet)\n"
                f"OPTIONAL MATCH (c)-[:PILOTS]->(ship:Starship)\n"
                f"OPTIONAL MATCH (c)-[:SAID]->(q:Quote)\n"
                "RETURN c.name AS name, c.gender AS gender, c.birth_year AS birth_year, "
                "s.name AS species, p.name AS planet, collect(ship.name) AS ships, collect(q.text) AS quotes"
            )
        # Default list characters
        return "MATCH (c:Character) RETURN c.name AS value LIMIT 10"

    def _format_response(self, intent: str, data) -> str:
        if intent == "count":
            count = data[0].get("count", 0) if data else 0
            return f"Total: {count}"
        if intent == "list":
            values = [row.get("value") for row in data]
            clean = [v for v in values if v]
            return ", ".join(clean) if clean else "Nenhum encontrado"
        if intent == "detail":
            row = data[0] if data else {}
            parts = []
            parts.append(f"Nome: {row.get('name', 'Desconhecido')}")
            parts.append(f"Gênero: {row.get('gender', 'Desconhecido')}")
            parts.append(f"Ano de nascimento: {row.get('birth_year', 'Desconhecido')}")
            if row.get('species'):
                parts.append(f"Espécie: {row['species']}")
            if row.get('planet'):
                parts.append(f"Planeta natal: {row['planet']}")
            ships = row.get('ships', [])
            if ships:
                parts.append(f"Naves: {', '.join(ships)}")
            quotes = row.get('quotes', [])
            if quotes:
                parts.append(f"Citações: {', '.join(quotes)}")
            return "\n".join(parts)
        # Fallback generic
        return "\n".join([row.get("value", "") for row in data])

    def ask(self, question: str) -> str:
        # Extrair entidade simples (pode ser melhorado)
        entity = None
        sample_chars = ["Luke Skywalker", "Han Solo", "Darth Vader", "Leia Organa", "Yoda"]
        for name in sample_chars:
            if name.lower() in question.lower():
                entity = name
                break
        # Detectar relação
        relation = None
        for key, val in self.relation_map.items():
            if key in question.lower():
                relation = val
                break
        intent = self._determine_intent(question, entity or "")
        cypher = self._build_cypher(intent, entity or "", relation)
        try:
            data = self.graph.query(cypher)
            return self._format_response(intent, data)
        except Exception as e:
            logger.error(f"Erro na consulta: {e}")
            return f"Erro ao executar consulta: {e}" 