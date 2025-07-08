import sqlite3
import logging
from typing import List, Dict, Any
from src.config.settings import Settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de banco de dados SQLite"""
    
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or Settings.SQLITE_DB_PATH
    
    def get_connection(self):
        """Retorna conexão com o banco"""
        return sqlite3.connect(self.db_path)
    
    def get_tables(self) -> List[str]:
        """Retorna lista de tabelas no banco"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [row[0] for row in cursor.fetchall()]
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Retorna informações sobre uma tabela"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            return [
                {
                    "name": col[1],
                    "type": col[2],
                    "not_null": bool(col[3]),
                    "default": col[4],
                    "primary_key": bool(col[5])
                }
                for col in columns
            ]
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retorna dados de exemplo de uma tabela"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_table_count(self, table_name: str) -> int:
        """Retorna número de registros em uma tabela"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            return cursor.fetchone()[0]
    
    def get_database_summary(self) -> Dict[str, Any]:
        """Retorna resumo do banco de dados"""
        tables = self.get_tables()
        summary = {
            "tables": {},
            "total_tables": len(tables)
        }
        
        for table in tables:
            summary["tables"][table] = {
                "count": self.get_table_count(table),
                "columns": self.get_table_info(table)
            }
        
        return summary 