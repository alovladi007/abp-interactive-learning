"""
Seed Neo4j with demo knowledge graph
"""
import os
from services.kg.neo4j_adapter import KGClient

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4jpassword")

kg = KGClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# Add demo facts
facts = [
    ("Ohm's law", "relates", "Voltage"),
    ("Ohm's law", "relates", "Current"),
    ("Ohm's law", "involves", "Resistance"),
    ("Gauss's law", "relates", "Electric flux"),
    ("Projectile motion", "involves", "Gravity"),
    ("Projectile motion", "requires", "Initial velocity"),
]

for subj, rel, obj in facts:
    kg.upsert_fact(subj, rel, obj)
    print(f"✅ Added: {subj} -{rel}-> {obj}")

print("Neo4j seeded with demo entities.")
