"""
Dr. Sarah API Routes
Medical AI Assistant REST API
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import logging

from services.dr_sarah_core import DrSarahCore
from services.medical_safety import MedicalSafetyValidator

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
            'Medical Literature Search'
        ],
        'endpoints': {
            'POST /medical-qa': 'Answer medical questions',
            'POST /patient-case-analysis': 'Analyze patient cases',
            'POST /drug-interactions': 'Check drug interactions',
            'POST /clinical-guidelines': 'Search clinical guidelines',
            'POST /medical-ner': 'Extract medical entities',
            'POST /knowledge-graph': 'Query knowledge graph',
            'POST /literature-search': 'Search medical literature',
            'GET /medical-stats': 'Get system statistics'
        }
    }
