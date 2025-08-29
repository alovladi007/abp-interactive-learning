"""
Neo4j Knowledge Graph adapter
"""
from neo4j import GraphDatabase
from typing import List, Dict

class KGClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def upsert_fact(self, subj: str, rel: str, obj: str):
        cypher = """
        MERGE (a:Entity {name:$subj})
        MERGE (b:Entity {name:$obj})
        MERGE (a)-[r:REL {type:$rel}]->(b)
        RETURN a,b,r
        """
        with self.driver.session() as s:
            s.run(cypher, subj=subj, rel=rel, obj=obj)
    
    def query(self, name: str) -> List[Dict]:
        cypher = "MATCH (n:Entity {name:$name})-[r:REL]->(m) RETURN n,m,r LIMIT 20"
        with self.driver.session() as s:
            res = s.run(cypher, name=name)
            return [dict(r) for r in res]
