import sqlite3
import pandas as pd
import os
from neo4j import GraphDatabase
from typing import Dict, List
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StarWarsNeo4jImporter:
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str, sqlite_db: str):
        """
        Inicializa o importador
        
        Args:
            neo4j_uri: URI do Neo4j (ex: bolt://localhost:7687)
            neo4j_user: Usuário do Neo4j
            neo4j_password: Senha do Neo4j
            sqlite_db: Caminho para o banco SQLite
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.sqlite_db = sqlite_db
        
    def close(self):
        """Fecha a conexão com o Neo4j"""
        self.driver.close()
        
    def clear_database(self):
        """Limpa todos os dados do Neo4j"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Banco de dados Neo4j limpo")
    
    def create_constraints(self):
        """Cria constraints únicos para evitar duplicatas"""
        constraints = [
            "CREATE CONSTRAINT character_id IF NOT EXISTS FOR (c:Character) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT species_id IF NOT EXISTS FOR (s:Species) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT planet_id IF NOT EXISTS FOR (p:Planet) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT starship_id IF NOT EXISTS FOR (s:Starship) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT weapon_id IF NOT EXISTS FOR (w:Weapon) REQUIRE w.id IS UNIQUE",
            "CREATE CONSTRAINT organization_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE",
            "CREATE CONSTRAINT film_id IF NOT EXISTS FOR (f:Film) REQUIRE f.id IS UNIQUE",
            "CREATE CONSTRAINT vehicle_id IF NOT EXISTS FOR (v:Vehicle) REQUIRE v.id IS UNIQUE",
            "CREATE CONSTRAINT city_id IF NOT EXISTS FOR (c:City) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT droid_id IF NOT EXISTS FOR (d:Droid) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT quote_id IF NOT EXISTS FOR (q:Quote) REQUIRE q.id IS UNIQUE",
            "CREATE CONSTRAINT battle_id IF NOT EXISTS FOR (b:Battle) REQUIRE b.id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    # Usar exec() para evitar problemas de tipo
                    session.run(constraint)  # type: ignore
                except Exception as e:
                    logger.warning(f"Constraint já existe ou erro: {e}")
    
    def import_species(self):
        """Importa espécies"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM species", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (s:Species {
                        id: $id,
                        name: $name,
                        classification: $classification,
                        designation: $designation,
                        average_height: $average_height,
                        skin_colors: $skin_colors,
                        hair_colors: $hair_colors,
                        eye_colors: $eye_colors,
                        average_lifespan: $average_lifespan,
                        language: $language,
                        homeworld: $homeworld
                    })
                """, dict(row))
        
        logger.info(f"Importadas {len(df)} espécies")
    
    def import_planets(self):
        """Importa planetas"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM planets", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (p:Planet {
                        id: $id,
                        name: $name,
                        diameter: $diameter,
                        rotation_period: $rotation_period,
                        orbital_period: $orbital_period,
                        gravity: $gravity,
                        population: $population,
                        climate: $climate,
                        terrain: $terrain,
                        surface_water: $surface_water,
                        residents: $residents,
                        films: $films
                    })
                """, dict(row))
        
        logger.info(f"Importados {len(df)} planetas")
    
    def import_characters(self):
        """Importa personagens"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM characters", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                # Criar personagem
                session.run("""
                    CREATE (c:Character {
                        id: $id,
                        name: $name,
                        gender: $gender,
                        height: $height,
                        weight: $weight,
                        hair_color: $hair_color,
                        eye_color: $eye_color,
                        skin_color: $skin_color,
                        year_born: $year_born,
                        year_died: $year_died,
                        description: $description
                    })
                """, dict(row))
                
                # Relacionar com espécie
                species_value = row.get('species')
                if species_value is not None and pd.notna(species_value) and str(species_value) != 'nan':
                    session.run("""
                        MATCH (c:Character {id: $char_id})
                        MATCH (s:Species {name: $species_name})
                        CREATE (c)-[:IS_SPECIES]->(s)
                    """, char_id=row['id'], species_name=str(species_value))
                
                # Relacionar com planeta natal
                homeworld_value = row.get('homeworld')
                if homeworld_value is not None and pd.notna(homeworld_value) and str(homeworld_value) != 'nan':
                    session.run("""
                        MATCH (c:Character {id: $char_id})
                        MATCH (p:Planet {name: $planet_name})
                        CREATE (c)-[:BORN_ON]->(p)
                    """, char_id=row['id'], planet_name=str(homeworld_value))
        
        logger.info(f"Importados {len(df)} personagens")
    
    def import_starships(self):
        """Importa naves espaciais"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM starships", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (s:Starship {
                        id: $id,
                        name: $name,
                        model: $model,
                        manufacturer: $manufacturer,
                        cost_in_credits: $cost_in_credits,
                        length: $length,
                        max_atmosphering_speed: $max_atmosphering_speed,
                        crew: $crew,
                        passengers: $passengers,
                        cargo_capacity: $cargo_capacity,
                        consumables: $consumables,
                        hyperdrive_rating: $hyperdrive_rating,
                        MGLT: $MGLT,
                        starship_class: $starship_class,
                        pilots: $pilots,
                        films: $films
                    })
                """, dict(row))
        
        logger.info(f"Importadas {len(df)} naves espaciais")
    
    def import_weapons(self):
        """Importa armas"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM weapons", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (w:Weapon {
                        id: $id,
                        name: $name,
                        model: $model,
                        manufacturer: $manufacturer,
                        cost_in_credits: $cost_in_credits,
                        length: $length,
                        type: $type,
                        description: $description,
                        films: $films
                    })
                """, dict(row))
        
        logger.info(f"Importadas {len(df)} armas")
    
    def import_organizations(self):
        """Importa organizações"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM organizations", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (o:Organization {
                        id: $id,
                        name: $name,
                        founded: $founded,
                        dissolved: $dissolved,
                        leader: $leader,
                        members: $members,
                        affiliation: $affiliation,
                        description: $description,
                        films: $films
                    })
                """, dict(row))
        
        logger.info(f"Importadas {len(df)} organizações")
    
    def import_films(self):
        """Importa filmes"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM films", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (f:Film {
                        id: $id,
                        title: $title,
                        release_date: $release_date,
                        director: $director,
                        producer: $producer,
                        opening_crawl: $opening_crawl
                    })
                """, dict(row))
        
        logger.info(f"Importados {len(df)} filmes")
    
    def import_quotes(self):
        """Importa citações"""
        conn = sqlite3.connect(self.sqlite_db)
        df = pd.read_sql_query("SELECT * FROM quotes", conn)
        conn.close()
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    CREATE (q:Quote {
                        id: $id,
                        quote: $quote,
                        source: $source
                    })
                """, dict(row))
                
                # Relacionar com personagem
                char_name_value = row.get('character_name')
                if char_name_value is not None and pd.notna(char_name_value) and str(char_name_value) != 'nan':
                    session.run("""
                        MATCH (q:Quote {id: $quote_id})
                        MATCH (c:Character {name: $char_name})
                        CREATE (c)-[:SAID]->(q)
                    """, quote_id=row['id'], char_name=str(char_name_value))
        
        logger.info(f"Importadas {len(df)} citações")
    
    def create_relationships(self):
        """Cria relacionamentos entre entidades"""
        with self.driver.session() as session:
            # Relacionar personagens com naves (baseado no campo pilots)
            session.run("""
                MATCH (c:Character), (s:Starship)
                WHERE s.pilots CONTAINS c.name
                CREATE (c)-[:PILOTS]->(s)
            """)
            
            # Relacionar personagens com filmes (baseado no campo films)
            session.run("""
                MATCH (c:Character), (f:Film)
                WHERE f.title IN split(c.films, ', ')
                CREATE (c)-[:APPEARS_IN]->(f)
            """)
            
            # Relacionar naves com filmes
            session.run("""
                MATCH (s:Starship), (f:Film)
                WHERE f.title IN split(s.films, ', ')
                CREATE (s)-[:APPEARS_IN]->(f)
            """)
            
            # Relacionar armas com filmes
            session.run("""
                MATCH (w:Weapon), (f:Film)
                WHERE f.title IN split(w.films, ', ')
                CREATE (w)-[:APPEARS_IN]->(f)
            """)
            
            # Relacionar organizações com filmes
            session.run("""
                MATCH (o:Organization), (f:Film)
                WHERE f.title IN split(o.films, ', ')
                CREATE (o)-[:APPEARS_IN]->(f)
            """)
        
        logger.info("Relacionamentos criados")
    
    def import_all(self):
        """Executa toda a importação"""
        logger.info("Iniciando importação para Neo4j...")
        
        # Limpar banco e criar constraints
        self.clear_database()
        self.create_constraints()
        
        # Importar dados
        self.import_species()
        self.import_planets()
        self.import_characters()
        self.import_starships()
        self.import_weapons()
        self.import_organizations()
        self.import_films()
        self.import_quotes()
        
        # Criar relacionamentos
        self.create_relationships()
        
        logger.info("Importação concluída!")

if __name__ == "__main__":
    # Carregar configurações do arquivo .env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Configurações do arquivo .env
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    SQLITE_DB = "star_wars.db"
    
    print(f"Conectando ao Neo4j: {NEO4J_URI}")
    print(f"Usuário: {NEO4J_USER}")
    
    importer = StarWarsNeo4jImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, SQLITE_DB)
    
    try:
        importer.import_all()
    finally:
        importer.close() 