"""
Seed pgvector from demo corpus
"""
import os
import glob
from services.retriever.pgvector_store import PgVectorStore

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/emma")
store = PgVectorStore(DATABASE_URL)

# Add demo content
demo_content = {
    "ohms_law.md": """# Ohm's Law
V = I × R where V is voltage, I is current, and R is resistance.
Applications: Circuit analysis, power calculations.""",
    "projectile_motion.md": """# Projectile Motion
Range = (v₀² × sin(2θ)) / g
Maximum height = (v₀² × sin²(θ)) / (2g)""",
    "gauss_law.md": """# Gauss's Law
Electric flux through closed surface equals enclosed charge divided by ε₀."""
}

for filename, content in demo_content.items():
    store.upsert_from_text(uri=filename, text_content=content)
    print(f"✅ Seeded {filename}")

print("pgvector seeded from demo corpus.")
