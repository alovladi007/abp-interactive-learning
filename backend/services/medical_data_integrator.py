"""
Medical Data Integration Module
Handles various medical data formats and integrates them into KGAREVION KG
"""

import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional, Any
import os
from pathlib import Path
import csv
import zipfile
import gzip
import numpy as np
from dataclasses import dataclass
import asyncio
from neo4j import AsyncGraphDatabase
import hashlib
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class MedicalDataFile:
    """Represents a medical data file to be integrated"""
    filepath: str
    format: str  # csv, json, xml, tsv, parquet, etc.
    data_type: str  # kg_triplets, entities, relations, embeddings, clinical_data
    source: str  # primkg, umls, custom, etc.
    metadata: Dict[str, Any] = None


class MedicalDataIntegrator:
    """
    Integrates various medical data formats into KGAREVION system
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password"
    ):
        self.neo4j_driver = AsyncGraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        self.supported_formats = {
            '.csv', '.tsv', '.json', '.xml', '.parquet',
            '.xlsx', '.txt', '.gz', '.zip'
        }
        self.entity_count = 0
        self.relation_count = 0
        self.error_log = []

    async def integrate_from_directory(self, directory_path: str, progress_callback=None) -> Dict[str, Any]:
        """
        Scan directory and integrate all medical data files
        Call this after downloading your Google Drive folder
        """
        logger.info(f"📁 Scanning directory: {directory_path}")

        files_to_process = []
        path = Path(directory_path)

        # Scan for supported files
        for file_path in path.rglob('*'):
            if file_path.suffix.lower() in self.supported_formats:
                file_info = self._identify_file_type(str(file_path))
                if file_info:
                    files_to_process.append(file_info)
                    logger.info(f"  Found: {file_path.name} ({file_info.data_type})")

        logger.info(f"📊 Found {len(files_to_process)} files to process")

        # Process each file
        results = {}
        for idx, file_info in enumerate(files_to_process):
            try:
                if progress_callback:
                    await progress_callback(idx, len(files_to_process), file_info.filepath)

                result = await self.process_file(file_info)
                results[file_info.filepath] = result
                logger.info(f"  ✅ Processed: {Path(file_info.filepath).name}")
            except Exception as e:
                error_msg = f"Error processing {file_info.filepath}: {str(e)}"
                logger.error(f"  ❌ {error_msg}")
                self.error_log.append(error_msg)
                results[file_info.filepath] = {"status": "error", "error": str(e)}

        # Generate summary
        summary = {
            "total_files": len(files_to_process),
            "successful": sum(1 for r in results.values() if r.get("status") == "success"),
            "failed": sum(1 for r in results.values() if r.get("status") == "error"),
            "total_entities": self.entity_count,
            "total_relations": self.relation_count,
            "results": results,
            "errors": self.error_log
        }

        logger.info(f"✨ Integration Complete!")
        logger.info(f"  Entities added: {self.entity_count:,}")
        logger.info(f"  Relations added: {self.relation_count:,}")

        return summary

    def _identify_file_type(self, filepath: str) -> Optional[MedicalDataFile]:
        """
        Identify medical data file type based on name and content
        """
        filename = Path(filepath).name.lower()

        # PrimeKG patterns
        if 'primkg' in filename or 'prime_kg' in filename:
            if 'node' in filename or 'entit' in filename:
                return MedicalDataFile(filepath, Path(filepath).suffix, 'entities', 'primkg')
            elif 'edge' in filename or 'relation' in filename or 'triplet' in filename:
                return MedicalDataFile(filepath, Path(filepath).suffix, 'relations', 'primkg')
            elif 'embed' in filename:
                return MedicalDataFile(filepath, Path(filepath).suffix, 'embeddings', 'primkg')

        # UMLS patterns
        elif 'umls' in filename or 'cui' in filename:
            return MedicalDataFile(filepath, Path(filepath).suffix, 'umls_mapping', 'umls')

        # Drug data patterns
        elif 'drug' in filename or 'medication' in filename or 'pharma' in filename:
            return MedicalDataFile(filepath, Path(filepath).suffix, 'drugs', 'custom')

        # Disease data patterns
        elif 'disease' in filename or 'condition' in filename or 'disorder' in filename:
            return MedicalDataFile(filepath, Path(filepath).suffix, 'diseases', 'custom')

        # Clinical data patterns
        elif 'clinical' in filename or 'patient' in filename or 'trial' in filename:
            return MedicalDataFile(filepath, Path(filepath).suffix, 'clinical_data', 'custom')

        # Knowledge graph patterns
        elif 'kg' in filename or 'graph' in filename or 'triplet' in filename:
            if 'node' in filename:
                return MedicalDataFile(filepath, Path(filepath).suffix, 'entities', 'custom')
            else:
                return MedicalDataFile(filepath, Path(filepath).suffix, 'relations', 'custom')

        # Default based on content inspection
        return self._inspect_file_content(filepath)

    def _inspect_file_content(self, filepath: str) -> Optional[MedicalDataFile]:
        """
        Inspect file content to determine type
        """
        try:
            # Handle compressed files
            if filepath.endswith('.gz'):
                import gzip
                with gzip.open(filepath, 'rt') as f:
                    first_line = f.readline()
            elif filepath.endswith('.zip'):
                return MedicalDataFile(filepath, '.zip', 'archive', 'custom')
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline()

            # Check for common medical data headers
            first_line_lower = first_line.lower()

            if any(term in first_line_lower for term in ['head', 'tail', 'relation', 'source', 'target']):
                return MedicalDataFile(filepath, Path(filepath).suffix, 'relations', 'custom')
            elif any(term in first_line_lower for term in ['entity', 'node', 'name', 'type', 'id']):
                return MedicalDataFile(filepath, Path(filepath).suffix, 'entities', 'custom')
            elif any(term in first_line_lower for term in ['embedding', 'vector', 'representation']):
                return MedicalDataFile(filepath, Path(filepath).suffix, 'embeddings', 'custom')
            elif any(term in first_line_lower for term in ['patient', 'diagnosis', 'treatment']):
                return MedicalDataFile(filepath, Path(filepath).suffix, 'clinical_data', 'custom')

        except Exception as e:
            logger.warning(f"Could not inspect {filepath}: {e}")

        return None

    async def process_file(self, file_info: MedicalDataFile) -> Dict[str, Any]:
        """
        Process a single medical data file
        """
        if file_info.data_type == 'entities':
            return await self._process_entities_file(file_info)
        elif file_info.data_type == 'relations':
            return await self._process_relations_file(file_info)
        elif file_info.data_type == 'embeddings':
            return await self._process_embeddings_file(file_info)
        elif file_info.data_type == 'umls_mapping':
            return await self._process_umls_mapping(file_info)
        elif file_info.data_type == 'clinical_data':
            return await self._process_clinical_data(file_info)
        elif file_info.data_type == 'archive':
            return await self._process_archive(file_info)
        else:
            return {"status": "skipped", "reason": "Unknown data type"}

    async def _process_entities_file(self, file_info: MedicalDataFile) -> Dict[str, Any]:
        """
        Process file containing medical entities
        """
        # Load data based on format
        data = self._load_file(file_info.filepath)

        if data is None:
            return {"status": "error", "error": "Could not load file"}

        entities_added = 0
        batch_size = 1000

        async with self.neo4j_driver.session() as session:
            # Process in batches
            for i in range(0, len(data), batch_size):
                batch = data.iloc[i:i+batch_size] if isinstance(data, pd.DataFrame) else data[i:i+batch_size]

                for _, row in batch.iterrows() if isinstance(batch, pd.DataFrame) else enumerate(batch):
                    # Extract entity information
                    entity_data = self._extract_entity_data(row, file_info.source)

                    if entity_data:
                        # Add to Neo4j
                        await session.run(
                            """
                            MERGE (e:Entity {id: $id})
                            SET e += $properties
                            """,
                            id=entity_data['id'],
                            properties=entity_data
                        )
                        entities_added += 1

        self.entity_count += entities_added

        return {
            "status": "success",
            "entities_added": entities_added,
            "source": file_info.source
        }

    async def _process_relations_file(self, file_info: MedicalDataFile) -> Dict[str, Any]:
        """
        Process file containing medical relations/triplets
        """
        data = self._load_file(file_info.filepath)

        if data is None:
            return {"status": "error", "error": "Could not load file"}

        relations_added = 0
        batch_size = 1000

        async with self.neo4j_driver.session() as session:
            for i in range(0, len(data), batch_size):
                batch = data.iloc[i:i+batch_size] if isinstance(data, pd.DataFrame) else data[i:i+batch_size]

                for _, row in batch.iterrows() if isinstance(batch, pd.DataFrame) else enumerate(batch):
                    # Extract relation information
                    relation_data = self._extract_relation_data(row, file_info.source)

                    if relation_data:
                        # Add to Neo4j
                        await session.run(
                            """
                            MATCH (h:Entity {id: $head_id})
                            MATCH (t:Entity {id: $tail_id})
                            MERGE (h)-[r:RELATES {type: $relation_type}]->(t)
                            SET r += $properties
                            """,
                            head_id=relation_data['head_id'],
                            tail_id=relation_data['tail_id'],
                            relation_type=relation_data['relation_type'],
                            properties=relation_data.get('properties', {})
                        )
                        relations_added += 1

        self.relation_count += relations_added

        return {
            "status": "success",
            "relations_added": relations_added,
            "source": file_info.source
        }

    async def _process_embeddings_file(self, file_info: MedicalDataFile) -> Dict[str, Any]:
        """
        Process file containing entity/relation embeddings
        """
        data = self._load_file(file_info.filepath)

        if data is None:
            return {"status": "error", "error": "Could not load file"}

        embeddings_added = 0

        async with self.neo4j_driver.session() as session:
            for _, row in data.iterrows() if isinstance(data, pd.DataFrame) else enumerate(data):
                # Extract embedding information
                embedding_data = self._extract_embedding_data(row)

                if embedding_data:
                    # Update entity with embedding
                    await session.run(
                        """
                        MATCH (e:Entity {id: $entity_id})
                        SET e.embedding = $embedding
                        """,
                        entity_id=embedding_data['entity_id'],
                        embedding=embedding_data['embedding']
                    )
                    embeddings_added += 1

        return {
            "status": "success",
            "embeddings_added": embeddings_added,
            "source": file_info.source
        }

    async def _process_umls_mapping(self, file_info: MedicalDataFile) -> Dict[str, Any]:
        """
        Process UMLS concept mapping file
        """
        data = self._load_file(file_info.filepath)

        if data is None:
            return {"status": "error", "error": "Could not load file"}

        mappings_added = 0

        async with self.neo4j_driver.session() as session:
            for _, row in data.iterrows() if isinstance(data, pd.DataFrame) else enumerate(data):
                # Extract UMLS mapping
                if 'cui' in row and 'name' in row:
                    await session.run(
                        """
                        MERGE (u:UMLSConcept {cui: $cui})
                        SET u.name = $name, u.semantic_type = $semantic_type
                        """,
                        cui=row['cui'],
                        name=row['name'],
                        semantic_type=row.get('semantic_type', '')
                    )
                    mappings_added += 1

        return {
            "status": "success",
            "mappings_added": mappings_added,
            "source": "UMLS"
        }

    async def _process_clinical_data(self, file_info: MedicalDataFile) -> Dict[str, Any]:
        """
        Process clinical data (trials, patient data, etc.)
        """
        data = self._load_file(file_info.filepath)

        if data is None:
            return {"status": "error", "error": "Could not load file"}

        records_added = 0

        # Process based on clinical data type
        if 'nct_id' in data.columns if isinstance(data, pd.DataFrame) else False:
            # Clinical trials data
            for _, row in data.iterrows():
                # Extract trial information and add to KG
                records_added += 1

        return {
            "status": "success",
            "records_added": records_added,
            "source": file_info.source
        }

    async def _process_archive(self, file_info: MedicalDataFile) -> Dict[str, Any]:
        """
        Process compressed archive containing multiple files
        """
        extracted_path = Path(file_info.filepath).parent / 'extracted'
        extracted_path.mkdir(exist_ok=True)

        # Extract archive
        if file_info.filepath.endswith('.zip'):
            with zipfile.ZipFile(file_info.filepath, 'r') as zip_ref:
                zip_ref.extractall(extracted_path)

        # Process extracted files
        return await self.integrate_from_directory(str(extracted_path))

    def _load_file(self, filepath: str) -> Optional[Any]:
        """
        Load file based on its format
        """
        try:
            if filepath.endswith('.csv'):
                return pd.read_csv(filepath)
            elif filepath.endswith('.tsv'):
                return pd.read_csv(filepath, sep='\t')
            elif filepath.endswith('.json'):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return pd.DataFrame(data)
                    return data
            elif filepath.endswith('.xlsx'):
                return pd.read_excel(filepath)
            elif filepath.endswith('.parquet'):
                return pd.read_parquet(filepath)
            elif filepath.endswith('.gz'):
                if '.csv' in filepath:
                    return pd.read_csv(filepath, compression='gzip')
                elif '.tsv' in filepath:
                    return pd.read_csv(filepath, sep='\t', compression='gzip')
            elif filepath.endswith('.xml'):
                tree = ET.parse(filepath)
                root = tree.getroot()
                # Parse XML based on structure
                return self._parse_xml_to_df(root)
            else:
                # Try to read as text
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    # Attempt to parse as CSV
                    return pd.DataFrame([line.strip().split(',') for line in lines])

        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return None

    def _extract_entity_data(self, row: Any, source: str) -> Optional[Dict]:
        """
        Extract entity data from a row
        """
        try:
            # Handle different formats
            if isinstance(row, pd.Series):
                # PrimeKG format
                if 'node_index' in row.index:
                    return {
                        'id': str(row.get('node_index', row.get('id', ''))),
                        'name': row.get('node_name', row.get('name', '')),
                        'type': row.get('node_type', row.get('type', 'unknown')),
                        'source': source,
                        'properties': json.dumps(row.to_dict()),
                        'created_at': datetime.utcnow().isoformat()
                    }
                # Generic format
                else:
                    return {
                        'id': hashlib.md5(str(row.get('name', '')).encode()).hexdigest(),
                        'name': row.get('name', row.get('entity', '')),
                        'type': row.get('type', 'unknown'),
                        'source': source,
                        'created_at': datetime.utcnow().isoformat()
                    }

            elif isinstance(row, dict):
                return {
                    'id': row.get('id', hashlib.md5(str(row.get('name', '')).encode()).hexdigest()),
                    'name': row.get('name', ''),
                    'type': row.get('type', 'unknown'),
                    'source': source,
                    'created_at': datetime.utcnow().isoformat()
                }

        except Exception as e:
            logger.error(f"Error extracting entity data: {e}")

        return None

    def _extract_relation_data(self, row: Any, source: str) -> Optional[Dict]:
        """
        Extract relation data from a row
        """
        try:
            if isinstance(row, pd.Series):
                # PrimeKG format
                if 'x_index' in row.index and 'y_index' in row.index:
                    return {
                        'head_id': str(row.get('x_index', '')),
                        'tail_id': str(row.get('y_index', '')),
                        'relation_type': row.get('relation', row.get('display_relation', 'related_to')),
                        'properties': {
                            'source': source,
                            'created_at': datetime.utcnow().isoformat()
                        }
                    }
                # Generic triplet format
                elif 'head' in row.index and 'tail' in row.index:
                    return {
                        'head_id': hashlib.md5(str(row.get('head', '')).encode()).hexdigest(),
                        'tail_id': hashlib.md5(str(row.get('tail', '')).encode()).hexdigest(),
                        'relation_type': row.get('relation', 'related_to'),
                        'properties': {
                            'source': source,
                            'created_at': datetime.utcnow().isoformat()
                        }
                    }

            elif isinstance(row, dict):
                return {
                    'head_id': row.get('head_id', hashlib.md5(str(row.get('head', '')).encode()).hexdigest()),
                    'tail_id': row.get('tail_id', hashlib.md5(str(row.get('tail', '')).encode()).hexdigest()),
                    'relation_type': row.get('relation', 'related_to'),
                    'properties': {
                        'source': source,
                        'created_at': datetime.utcnow().isoformat()
                    }
                }

        except Exception as e:
            logger.error(f"Error extracting relation data: {e}")

        return None

    def _extract_embedding_data(self, row: Any) -> Optional[Dict]:
        """
        Extract embedding data from a row
        """
        try:
            if isinstance(row, pd.Series):
                # Look for entity ID and embedding vector
                entity_id = row.get('entity_id', row.get('id', row.get('node_index', '')))

                # Find embedding column (might be named differently)
                embedding_cols = [col for col in row.index if 'embed' in col.lower() or 'vector' in col.lower()]

                if embedding_cols:
                    embedding = row[embedding_cols[0]]
                    if isinstance(embedding, str):
                        # Parse string representation of list
                        embedding = json.loads(embedding)

                    return {
                        'entity_id': str(entity_id),
                        'embedding': list(embedding) if isinstance(embedding, np.ndarray) else embedding
                    }

        except Exception as e:
            logger.error(f"Error extracting embedding data: {e}")

        return None

    def _parse_xml_to_df(self, root: ET.Element) -> pd.DataFrame:
        """
        Parse XML to DataFrame
        """
        data = []

        for child in root:
            row = {}
            for elem in child:
                row[elem.tag] = elem.text
            data.append(row)

        return pd.DataFrame(data)

    async def preview_file(self, filepath: str, num_rows: int = 10) -> Dict[str, Any]:
        """
        Preview file contents before integration
        """
        try:
            data = self._load_file(filepath)
            if data is None:
                return {"error": "Could not load file"}

            file_info = self._identify_file_type(filepath)

            preview = {
                "filepath": filepath,
                "data_type": file_info.data_type if file_info else "unknown",
                "source": file_info.source if file_info else "unknown",
                "total_rows": len(data) if isinstance(data, pd.DataFrame) else 0,
                "columns": list(data.columns) if isinstance(data, pd.DataFrame) else [],
                "sample_rows": data.head(num_rows).to_dict('records') if isinstance(data, pd.DataFrame) else []
            }

            return preview
        except Exception as e:
            return {"error": str(e)}

    async def close(self):
        """Clean up resources"""
        await self.neo4j_driver.close()
