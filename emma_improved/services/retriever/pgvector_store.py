"""
pgvector store with simple embedding
"""
import math
import re
import hashlib
import json
from typing import List, Dict
from sqlalchemy import create_engine, text

# Simple 128-d embedding using hashed bag-of-words
DIM = 128

def embed(text: str) -> list:
    """Create simple embedding from text."""
    vec = [0.0] * DIM
    tokens = [t for t in re.split(r"\W+", text.lower()) if t]
    for t in tokens:
        h = int(hashlib.sha256(t.encode("utf-8")).hexdigest(), 16)
        idx = h % DIM
        vec[idx] += 1.0
    # L2 normalize
    norm = math.sqrt(sum(v*v for v in vec)) or 1.0
    return [v/norm for v in vec]

DDL = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    uri TEXT,
    kind TEXT,
    sha256 TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    source_id INT REFERENCES sources(id),
    text TEXT,
    meta JSON,
    embedding vector(%(dim)s)
);
CREATE INDEX IF NOT EXISTS chunks_embedding_idx 
    ON chunks USING ivfflat (embedding vector_cosine_ops);
"""

class PgVectorStore:
    def __init__(self, url: str):
        self.engine = create_engine(url, pool_pre_ping=True)
        with self.engine.begin() as conn:
            conn.execute(text(DDL), {"dim": DIM})
    
    def upsert_from_text(self, uri: str, text_content: str, kind: str = "file") -> int:
        sha = hashlib.sha256(text_content.encode("utf-8")).hexdigest()
        lines = text_content.splitlines()
        
        with self.engine.begin() as conn:
            # Ensure source exists
            res = conn.execute(
                text("SELECT id FROM sources WHERE sha256=:sha"),
                {"sha": sha}
            ).fetchone()
            
            if res:
                source_id = res[0]
            else:
                res = conn.execute(
                    text("INSERT INTO sources (uri,kind,sha256) VALUES (:u,:k,:s) RETURNING id"),
                    {"u": uri, "k": kind, "s": sha}
                )
                source_id = res.fetchone()[0]
            
            # Delete old chunks
            conn.execute(text("DELETE FROM chunks WHERE source_id=:sid"), {"sid": source_id})
            
            # Create chunks (~20 lines each)
            chunk, start = [], 1
            for i, line in enumerate(lines, start=1):
                chunk.append(line)
                if len(chunk) >= 20 or i == len(lines):
                    text_chunk = "\n".join(chunk).strip()
                    if text_chunk:
                        emb = embed(text_chunk)
                        conn.execute(
                            text("INSERT INTO chunks (source_id,text,meta,embedding) VALUES (:sid,:t,:m,:e)"),
                            {
                                "sid": source_id,
                                "t": text_chunk,
                                "m": json.dumps({"range": f"L{start}-L{i}"}),
                                "e": emb
                            }
                        )
                    chunk, start = [], i+1
        return 1
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        q_emb = embed(query)
        with self.engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT s.uri, s.sha256, c.text, c.meta, 
                       1 - (c.embedding <=> :q::vector) AS score
                FROM chunks c
                JOIN sources s ON s.id = c.source_id
                ORDER BY c.embedding <=> :q::vector
                LIMIT :k
            """), {"q": q_emb, "k": top_k}).fetchall()
        
        out = []
        for uri, sha, text_chunk, meta, score in rows:
            snip = text_chunk.splitlines()[:3]
            out.append({
                "file": uri,
                "sha": (sha or "")[:12],
                "score": float(score),
                "highlight": f"{uri}: {' '.join(snip)}"
            })
        return out
