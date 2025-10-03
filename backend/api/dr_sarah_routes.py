"""
Dr. Sarah API Routes
Medical AI Assistant REST API
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import logging
import os
import shutil
from pathlib import Path

from services.dr_sarah_core import DrSarahCore
from services.medical_safety import MedicalSafetyValidator
from services.medical_data_integrator import MedicalDataIntegrator
from services.integration_jobs import jobs_manager, JobStatus
from config.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter()
dr_sarah = DrSarahCore()
safety_validator = MedicalSafetyValidator()


# Request/Response Models
class MedicalQuestion(BaseModel):
    question: str = Field(..., min_length=3, description="Medical question to analyze")
    include_triplets: bool = Field(True, description="Include knowledge triplets in response")
    include_entities: bool = Field(True, description="Include extracted medical entities")


class PatientCase(BaseModel):
    symptoms: List[str] = Field([], description="List of patient symptoms")
    medical_history: List[str] = Field([], description="Patient medical history")
    medications: List[str] = Field([], description="Current medications")
    age: Optional[int] = Field(None, ge=0, le=120, description="Patient age")
    gender: Optional[str] = Field(None, description="Patient gender")


class DrugInteractionCheck(BaseModel):
    drugs: List[str] = Field(..., min_items=2, description="List of drugs to check for interactions")


class ClinicalGuidelineSearch(BaseModel):
    condition: str = Field(..., min_length=2, description="Medical condition to search guidelines for")


class MedicalLiteratureSearch(BaseModel):
    query: str = Field(..., min_length=3, description="Search query")
    filters: Optional[Dict] = Field(None, description="Search filters")
    max_results: int = Field(20, ge=1, le=100, description="Maximum results to return")


# API Routes

@router.post("/medical-qa")
async def medical_question_answering(question: MedicalQuestion):
    """
    Answer medical questions using NER, knowledge graph, and clinical reasoning

    **Example Questions:**
    - "What are the drug interactions between warfarin and aspirin?"
    - "What is the first-line treatment for type 2 diabetes?"
    - "Which protein is associated with breast cancer?"
    """
    try:
        result = await dr_sarah.process_medical_query(question.question)

        # Filter response based on request
        if not question.include_triplets:
            result.pop('knowledge_triplets', None)

        if not question.include_entities:
            result.pop('medical_entities', None)

        return result

    except Exception as e:
        logger.error(f"Error processing medical question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/patient-case-analysis")
async def analyze_patient_case(case: PatientCase):
    """
    Analyze patient case and provide clinical insights

    **Features:**
    - Symptom analysis
    - Drug interaction checking
    - Differential diagnosis suggestions
    - Clinical knowledge integration
    """
    try:
        case_data = {
            'symptoms': case.symptoms,
            'medical_history': case.medical_history,
            'medications': case.medications,
            'age': case.age,
            'gender': case.gender
        }

        result = await dr_sarah.analyze_patient_case(case_data)
        return result

    except Exception as e:
        logger.error(f"Error analyzing patient case: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/drug-interactions")
async def check_drug_interactions(request: DrugInteractionCheck):
    """
    Check for drug-drug interactions

    **Returns:**
    - Interaction severity (minor, moderate, major, contraindicated)
    - Mechanism of interaction
    - Clinical management recommendations
    """
    try:
        interactions = dr_sarah.drug_checker.check_multiple(request.drugs)

        return {
            'drugs_checked': request.drugs,
            'interactions_found': len(interactions),
            'interactions': [
                {
                    'drug1': i.drug1,
                    'drug2': i.drug2,
                    'severity': i.severity,
                    'description': i.description,
                    'mechanism': i.mechanism,
                    'management': i.management
                } for i in interactions
            ],
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error checking drug interactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clinical-guidelines")
async def search_clinical_guidelines(request: ClinicalGuidelineSearch):
    """
    Search evidence-based clinical guidelines

    **Guidelines Include:**
    - Treatment recommendations
    - Evidence levels (A, B, C, D)
    - Contraindications
    - Source citations
    """
    try:
        # First try exact match
        recommendation = dr_sarah.clinical_support.get_recommendations(request.condition)

        if recommendation:
            return {
                'condition': recommendation.condition,
                'recommendations': recommendation.recommendations,
                'evidence_level': recommendation.evidence_level,
                'source': recommendation.source,
                'contraindications': recommendation.contraindications,
                'last_updated': '2024'
            }

        # If no exact match, search
        results = dr_sarah.clinical_support.search_guidelines(request.condition)

        if not results:
            return {
                'condition': request.condition,
                'message': 'No guidelines found for this condition',
                'suggestions': 'Try searching for related conditions or consult UpToDate/clinical practice guidelines'
            }

        return {
            'results': [
                {
                    'condition': r.condition,
                    'recommendations': r.recommendations,
                    'evidence_level': r.evidence_level,
                    'source': r.source
                } for r in results
            ]
        }

    except Exception as e:
        logger.error(f"Error searching clinical guidelines: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/medical-ner")
async def extract_medical_entities(text: str):
    """
    Extract medical entities from text using BioBERT-based NER

    **Entity Types:**
    - Diseases
    - Drugs
    - Symptoms
    - Genes
    - Proteins
    - Treatments
    - Medical tests
    """
    try:
        entities = dr_sarah.ner.extract_entities(text)

        # Group entities by type
        entities_by_type = {}
        for entity in entities:
            if entity.entity_type not in entities_by_type:
                entities_by_type[entity.entity_type] = []
            entities_by_type[entity.entity_type].append({
                'text': entity.text,
                'confidence': entity.confidence,
                'position': [entity.start, entity.end]
            })

        return {
            'text': text,
            'entities_by_type': entities_by_type,
            'total_entities': len(entities),
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error extracting medical entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/knowledge-graph")
async def query_knowledge_graph(entities: List[str]):
    """
    Query medical knowledge graph for relationships

    **Returns:**
    - Knowledge triplets (head, relation, tail)
    - Confidence scores
    - Source citations
    """
    try:
        # Convert strings to entity objects for processing
        from backend.services.dr_sarah_core import MedicalEntity

        entity_objects = [
            MedicalEntity(text=e, entity_type='unknown', start=0, end=len(e), confidence=1.0)
            for e in entities
        ]

        triplets = dr_sarah.knowledge_graph.find_triplets(entity_objects)

        return {
            'query_entities': entities,
            'triplets_found': len(triplets),
            'triplets': [
                {
                    'head': t.head,
                    'relation': t.relation,
                    'tail': t.tail,
                    'confidence': t.confidence,
                    'source': t.source
                } for t in triplets
            ],
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error querying knowledge graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kgarevion")
async def kgarevion_medical_qa(question: MedicalQuestion):
    """
    Process medical question using KGAREVION pipeline with safety validation

    **KGAREVION:** Knowledge Graph-Augmented Revision for Medical QA
    **Pipeline:** Generate → Review → Revise → Answer → Safety Check

    **Features:**
    - Entity extraction from medical text
    - Knowledge graph triplet generation
    - Triplet verification using medical KG
    - Iterative revision of false triplets
    - Confidence-scored answers
    - **Medical safety validation**
    - Emergency condition detection
    - Drug interaction checking
    - Risk level assessment
    """
    try:
        # Process through KGAREVION pipeline
        result = await dr_sarah.process_with_kgarevion(
            question_text=question.question,
            question_type="multiple_choice" if question.candidates else "open_ended",
            candidates=question.candidates
        )

        # Perform safety validation
        safety_result = safety_validator.validate_response(
            question=question.question,
            answer=result.get('answer', ''),
            confidence_score=result.get('confidence', 0.0)
        )

        # Add safety information to response
        result['safety'] = {
            'is_safe': safety_result.is_safe,
            'risk_level': safety_result.risk_level.value,
            'warnings': safety_result.warnings,
            'disclaimers': safety_result.required_disclaimers,
            'requires_human_review': safety_result.requires_human_review,
            'domain': safety_result.domain.value,
            'safety_explanation': safety_result.explanation
        }

        # Log high-risk responses
        if safety_result.risk_level.value in ['high', 'critical']:
            logger.warning(
                f"High-risk medical response generated: "
                f"Risk={safety_result.risk_level.value}, "
                f"Question='{question.question[:100]}...'"
            )

        return result

    except Exception as e:
        logger.error(f"KGAREVION processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get Dr. Sarah usage statistics for dashboard"""
    # In production, fetch from database
    return {
        'questions_answered': 247,
        'drugs_checked': 89,
        'cases_analyzed': 42,
        'literature_searches': 156
    }


@router.get("/medical-stats")
async def get_medical_stats():
    """Get Dr. Sarah system statistics"""
    return {
        'total_knowledge_triplets': len(dr_sarah.knowledge_graph.knowledge_base),
        'drug_interactions_database': len(dr_sarah.drug_checker.interactions),
        'clinical_guidelines': len(dr_sarah.clinical_support.guidelines),
        'supported_entity_types': list(dr_sarah.ner.entity_patterns.keys()),
        'version': '1.0.0',
        'kgarevion_enabled': True,
        'last_updated': '2024-10-02'
    }


@router.post("/literature-search")
async def search_medical_literature(search: MedicalLiteratureSearch):
    """
    Search medical literature (PubMed, clinical trials, etc.)

    **Note:** This is a placeholder. Implement with actual PubMed API integration.
    """
    try:
        # Extract medical entities from query
        entities = dr_sarah.ner.extract_entities(search.query)

        # Mock literature results
        mock_results = [
            {
                'title': f'Clinical study on {entities[0].text if entities else search.query}',
                'authors': ['Smith J.', 'Johnson A.', 'Williams K.'],
                'journal': 'New England Journal of Medicine',
                'year': 2024,
                'pmid': '12345678',
                'abstract': f'This study investigates {search.query}...',
                'relevance_score': 0.92
            }
        ]

        return {
            'query': search.query,
            'total_results': len(mock_results),
            'results': mock_results,
            'medical_entities_extracted': [e.text for e in entities],
            'message': 'This is a demo endpoint. Integrate with PubMed API for real results.'
        }

    except Exception as e:
        logger.error(f"Error searching medical literature: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def dr_sarah_info():
    """Dr. Sarah API information"""
    return {
        'name': 'Dr. Sarah - AI Medical Research Assistant',
        'version': '1.0.0',
        'description': 'Advanced medical AI with NER, knowledge graph, and clinical decision support',
        'capabilities': [
            'Medical Question Answering',
            'Drug Interaction Checking',
            'Clinical Guideline Search',
            'Patient Case Analysis',
            'Medical Entity Extraction',
            'Knowledge Graph Querying',
            'Medical Literature Search',
            'Medical Data Integration'
        ],
        'endpoints': {
            'POST /medical-qa': 'Answer medical questions',
            'POST /patient-case-analysis': 'Analyze patient cases',
            'POST /drug-interactions': 'Check drug interactions',
            'POST /clinical-guidelines': 'Search clinical guidelines',
            'POST /medical-ner': 'Extract medical entities',
            'POST /knowledge-graph': 'Query knowledge graph',
            'POST /literature-search': 'Search medical literature',
            'GET /medical-stats': 'Get system statistics',
            'POST /data-integration/start': 'Start data integration job',
            'POST /data-integration/upload': 'Upload and integrate medical data files',
            'GET /data-integration/status/{job_id}': 'Get integration job status',
            'GET /data-integration/history': 'List integration jobs',
            'GET /data-integration/preview': 'Preview file before integration'
        }
    }


# ==================== DATA INTEGRATION ENDPOINTS ====================

# Request/Response Models for Data Integration
class DataIntegrationRequest(BaseModel):
    directory_path: str = Field(..., description="Path to directory containing medical data files")
    file_filters: Optional[List[str]] = Field(None, description="File extensions to filter (e.g., ['.csv', '.json'])")
    batch_size: int = Field(1000, ge=1, le=10000, description="Batch size for processing")


class FilePreviewRequest(BaseModel):
    filepath: str = Field(..., description="Path to file to preview")
    num_rows: int = Field(10, ge=1, le=100, description="Number of rows to preview")


# Background task for data integration
async def run_integration_job(job_id: str, directory_path: str):
    """Background task to run data integration"""
    try:
        # Update job status to running
        jobs_manager.update_job(job_id, status=JobStatus.RUNNING, progress=0.0)

        # Create integrator
        integrator = MedicalDataIntegrator(
            neo4j_uri=settings.NEO4J_URI,
            neo4j_user=settings.NEO4J_USER,
            neo4j_password=settings.NEO4J_PASSWORD
        )

        # Progress callback
        async def update_progress(files_processed, files_total, current_file):
            progress = (files_processed / files_total * 100) if files_total > 0 else 0
            jobs_manager.update_job(
                job_id,
                progress=progress,
                current_file=current_file,
                files_processed=files_processed,
                files_total=files_total
            )

        # Run integration
        result = await integrator.integrate_from_directory(
            directory_path,
            progress_callback=update_progress
        )

        # Update job with results
        jobs_manager.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            progress=100.0,
            entities_added=result.get('total_entities', 0),
            relations_added=result.get('total_relations', 0),
            result=result
        )

        # Cleanup
        await integrator.close()

        logger.info(f"Integration job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Integration job {job_id} failed: {e}")
        jobs_manager.update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e)
        )


@router.post("/data-integration/start")
async def start_data_integration(
    request: DataIntegrationRequest,
    background_tasks: BackgroundTasks
):
    """
    Start medical data integration from a directory

    **Process:**
    1. Scans directory for supported medical data files
    2. Identifies file types (PrimeKG, UMLS, clinical data, etc.)
    3. Extracts entities and relations
    4. Integrates into Neo4j knowledge graph

    **Supported Formats:**
    - CSV, TSV, JSON, XML, Parquet
    - Compressed files (.gz, .zip)
    - Excel files (.xlsx)

    **Returns:**
    - Job ID for tracking progress
    """
    try:
        # Validate directory exists
        if not os.path.exists(request.directory_path):
            raise HTTPException(status_code=404, detail="Directory not found")

        # Create integration job
        job = jobs_manager.create_job(request.directory_path)

        # Start background task
        background_tasks.add_task(run_integration_job, job.job_id, request.directory_path)

        logger.info(f"Started integration job {job.job_id} for {request.directory_path}")

        return {
            "job_id": job.job_id,
            "status": job.status.value,
            "directory_path": request.directory_path,
            "started_at": job.started_at.isoformat(),
            "message": "Integration job started successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data-integration/upload")
async def upload_and_integrate(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload medical data file and trigger integration

    **Supported Files:**
    - Single CSV, JSON, XML, Parquet files
    - ZIP archives containing multiple files
    - Compressed files (.gz)

    **Returns:**
    - Job ID for tracking integration progress
    """
    try:
        # Create upload directory if it doesn't exist
        upload_dir = Path(settings.MEDICAL_DATA_UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded file
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Uploaded file saved to {file_path}")

        # If it's a zip file, extract it
        if file.filename.endswith('.zip'):
            extract_dir = upload_dir / file.filename.replace('.zip', '')
            extract_dir.mkdir(exist_ok=True)

            import zipfile
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            integration_path = str(extract_dir)
        else:
            integration_path = str(upload_dir)

        # Create integration job
        job = jobs_manager.create_job(integration_path)

        # Start background integration
        background_tasks.add_task(run_integration_job, job.job_id, integration_path)

        return {
            "job_id": job.job_id,
            "status": job.status.value,
            "filename": file.filename,
            "file_size": file.size if hasattr(file, 'size') else 0,
            "started_at": job.started_at.isoformat(),
            "message": "File uploaded and integration started"
        }

    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data-integration/status/{job_id}")
async def get_integration_status(job_id: str):
    """
    Get status of a data integration job

    **Returns:**
    - Job status (pending, running, completed, failed, cancelled)
    - Progress percentage (0-100)
    - Current file being processed
    - Files processed count
    - Entities and relations added
    - Error messages (if any)
    """
    job = jobs_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job.to_dict()


@router.get("/data-integration/history")
async def get_integration_history(
    limit: int = 50,
    status: Optional[str] = None
):
    """
    Get history of data integration jobs

    **Query Parameters:**
    - limit: Maximum number of jobs to return (default: 50)
    - status: Filter by status (pending, running, completed, failed, cancelled)

    **Returns:**
    - List of integration jobs with status and statistics
    """
    try:
        status_filter = JobStatus(status) if status else None
        jobs = jobs_manager.list_jobs(limit=limit, status_filter=status_filter)

        return {
            "total": len(jobs),
            "jobs": [job.to_dict() for job in jobs]
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status value")
    except Exception as e:
        logger.error(f"Error fetching job history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/data-integration/job/{job_id}")
async def cancel_integration_job(job_id: str):
    """
    Cancel a running integration job

    **Note:** This will stop the job but may not rollback already integrated data
    """
    success = jobs_manager.cancel_job(job_id)

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Job not found or not in running state"
        )

    return {
        "job_id": job_id,
        "message": "Job cancelled successfully"
    }


@router.post("/data-integration/preview")
async def preview_medical_file(request: FilePreviewRequest):
    """
    Preview file contents before integration

    **Returns:**
    - File metadata (type, source, format)
    - Sample rows
    - Detected columns
    - Estimated entity/relation counts
    """
    try:
        if not os.path.exists(request.filepath):
            raise HTTPException(status_code=404, detail="File not found")

        integrator = MedicalDataIntegrator(
            neo4j_uri=settings.NEO4J_URI,
            neo4j_user=settings.NEO4J_USER,
            neo4j_password=settings.NEO4J_PASSWORD
        )

        preview = await integrator.preview_file(request.filepath, request.num_rows)

        await integrator.close()

        return preview

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error previewing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data-integration/stats")
async def get_integration_stats():
    """
    Get overall data integration statistics

    **Returns:**
    - Total jobs run
    - Jobs by status
    - Total entities integrated
    - Total relations integrated
    """
    return jobs_manager.get_statistics()
