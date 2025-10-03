"""
MARIA - Machine Learning Augmented Research and Intelligent Analysis
Complete Medical AI System with KGAREVION, NER, Knowledge Graph, and Clinical Decision Support
Implements the KGAREVION pipeline: Generate → Review → Revise → Answer
"""

import os
import re
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass
import asyncio

# Import KGAREVION pipeline
from services.kgarevion import KGARevionPipeline, Question as KGQuestion

logger = logging.getLogger(__name__)


@dataclass
class MedicalEntity:
    """Medical entity extracted from text"""
    text: str
    entity_type: str  # disease, drug, symptom, gene, protein, treatment
    start: int
    end: int
    confidence: float


@dataclass
class KnowledgeTriplet:
    """Medical knowledge graph triplet"""
    head: str
    relation: str
    tail: str
    confidence: float
    source: str


@dataclass
class DrugInteraction:
    """Drug-drug interaction information"""
    drug1: str
    drug2: str
    severity: str  # minor, moderate, major, contraindicated
    description: str
    mechanism: str
    management: str


@dataclass
class ClinicalRecommendation:
    """Clinical decision support recommendation"""
    condition: str
    recommendations: List[str]
    evidence_level: str  # A, B, C, D
    source: str
    contraindications: List[str]


class MedicalNER:
    """Medical Named Entity Recognition using BioBERT patterns"""

    def __init__(self):
        self.entity_patterns = {
            'disease': [
                r'\b(diabetes|hypertension|cancer|alzheimer|parkinson|asthma|copd|pneumonia|tuberculosis|hepatitis|cirrhosis|stroke|myocardial infarction|heart failure|arrhythmia|sepsis|meningitis|encephalitis|epilepsy|schizophrenia|depression|anxiety)\b',
                r'\b[A-Z][a-z]+\s+(disease|syndrome|disorder|infection)\b',
            ],
            'drug': [
                r'\b(metformin|insulin|aspirin|warfarin|heparin|amoxicillin|ciprofloxacin|azithromycin|lisinopril|atorvastatin|simvastatin|omeprazole|metoprolol|amlodipine|levothyroxine|albuterol|prednisone|gabapentin|sertraline|fluoxetine)\b',
                r'\b[A-Z][a-z]+(?:mab|nib|pril|sartan|statin|olol|pine|cillin|mycin|oxacin|tidine|zole)\b',
            ],
            'symptom': [
                r'\b(fever|cough|pain|nausea|vomiting|diarrhea|headache|dizziness|fatigue|weakness|dyspnea|chest pain|palpitations|edema|rash|pruritus|jaundice|hematuria|hemoptysis|syncope)\b',
            ],
            'gene': [
                r'\b([A-Z]{2,}[0-9]+|[A-Z][a-z]{2}[A-Z][0-9]+)\b',  # Gene symbols
            ],
            'protein': [
                r'\b(hemoglobin|albumin|globulin|fibrinogen|troponin|creatinine|bilirubin|amylase|lipase|CRP|ESR)\b',
            ],
            'treatment': [
                r'\b(surgery|chemotherapy|radiotherapy|immunotherapy|dialysis|transplantation|resection|bypass|angioplasty|stenting)\b',
            ],
            'test': [
                r'\b(MRI|CT scan|X-ray|ultrasound|ECG|EEG|blood test|urinalysis|biopsy|endoscopy|colonoscopy)\b',
            ]
        }

    def extract_entities(self, text: str) -> List[MedicalEntity]:
        """Extract medical entities from text"""
        entities = []
        text_lower = text.lower()

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                    entities.append(MedicalEntity(
                        text=match.group(),
                        entity_type=entity_type,
                        start=match.start(),
                        end=match.end(),
                        confidence=0.85
                    ))

        # Remove duplicates and overlapping entities
        entities = self._remove_overlapping(entities)
        return entities

    def _remove_overlapping(self, entities: List[MedicalEntity]) -> List[MedicalEntity]:
        """Remove overlapping entities, keeping higher confidence ones"""
        if not entities:
            return []

        # Sort by start position
        sorted_entities = sorted(entities, key=lambda e: (e.start, -e.confidence))

        filtered = []
        last_end = -1

        for entity in sorted_entities:
            if entity.start >= last_end:
                filtered.append(entity)
                last_end = entity.end

        return filtered


class MedicalKnowledgeGraph:
    """Medical knowledge graph for relationship extraction and reasoning"""

    def __init__(self):
        # Predefined medical knowledge triplets
        self.knowledge_base = [
            KnowledgeTriplet("diabetes", "CAUSES", "hyperglycemia", 0.95, "medical_literature"),
            KnowledgeTriplet("diabetes", "TREATED_WITH", "metformin", 0.92, "clinical_guidelines"),
            KnowledgeTriplet("diabetes", "RISK_FACTOR_FOR", "cardiovascular disease", 0.90, "clinical_studies"),
            KnowledgeTriplet("hypertension", "TREATED_WITH", "lisinopril", 0.91, "clinical_guidelines"),
            KnowledgeTriplet("hypertension", "RISK_FACTOR_FOR", "stroke", 0.88, "clinical_studies"),
            KnowledgeTriplet("aspirin", "PREVENTS", "myocardial infarction", 0.85, "clinical_trials"),
            KnowledgeTriplet("warfarin", "INTERACTS_WITH", "aspirin", 0.93, "drug_database"),
            KnowledgeTriplet("metformin", "SIDE_EFFECT", "lactic acidosis", 0.75, "adverse_events"),
            KnowledgeTriplet("statins", "REDUCE", "cholesterol", 0.94, "clinical_guidelines"),
            KnowledgeTriplet("ACE inhibitors", "CONTRAINDICATED_IN", "pregnancy", 0.96, "clinical_guidelines"),
            # Add more triplets for comprehensive coverage
            KnowledgeTriplet("BRCA1", "ASSOCIATED_WITH", "breast cancer", 0.93, "genetic_studies"),
            KnowledgeTriplet("TP53", "TUMOR_SUPPRESSOR", "multiple cancers", 0.94, "genetic_database"),
            KnowledgeTriplet("insulin", "REGULATES", "blood glucose", 0.97, "physiology"),
            KnowledgeTriplet("beta blockers", "TREAT", "arrhythmia", 0.89, "cardiology"),
        ]

        # Create index for fast lookup
        self.entity_index = {}
        for triplet in self.knowledge_base:
            if triplet.head not in self.entity_index:
                self.entity_index[triplet.head] = []
            self.entity_index[triplet.head].append(triplet)

    def find_triplets(self, entities: List[MedicalEntity]) -> List[KnowledgeTriplet]:
        """Find knowledge triplets related to extracted entities"""
        triplets = []
        entity_texts = {e.text.lower() for e in entities}

        for entity_text in entity_texts:
            if entity_text in self.entity_index:
                triplets.extend(self.entity_index[entity_text])

        return triplets[:10]  # Return top 10 triplets

    def infer_relationships(self, entity1: str, entity2: str) -> Optional[KnowledgeTriplet]:
        """Infer relationship between two entities"""
        # Check direct relationships
        if entity1 in self.entity_index:
            for triplet in self.entity_index[entity1]:
                if triplet.tail.lower() == entity2.lower():
                    return triplet

        return None


class DrugInteractionChecker:
    """Drug-drug interaction checker"""

    def __init__(self):
        self.interactions = {
            ('warfarin', 'aspirin'): DrugInteraction(
                drug1='warfarin',
                drug2='aspirin',
                severity='major',
                description='Increased risk of bleeding due to additive anticoagulant effects',
                mechanism='Both drugs inhibit coagulation - warfarin via vitamin K antagonism and aspirin via platelet inhibition',
                management='Monitor INR closely. Consider alternative antiplatelet agent or reduce warfarin dose'
            ),
            ('metformin', 'contrast dye'): DrugInteraction(
                drug1='metformin',
                drug2='contrast dye',
                severity='moderate',
                description='Risk of lactic acidosis due to contrast-induced nephropathy',
                mechanism='Contrast dye can cause acute kidney injury, leading to metformin accumulation',
                management='Hold metformin 48 hours before and after contrast administration'
            ),
            ('lisinopril', 'spironolactone'): DrugInteraction(
                drug1='lisinopril',
                drug2='spironolactone',
                severity='moderate',
                description='Risk of hyperkalemia',
                mechanism='Both drugs increase serum potassium levels',
                management='Monitor serum potassium. Consider potassium restriction'
            ),
            ('simvastatin', 'clarithromycin'): DrugInteraction(
                drug1='simvastatin',
                drug2='clarithromycin',
                severity='major',
                description='Increased risk of rhabdomyolysis',
                mechanism='Clarithromycin inhibits CYP3A4, increasing simvastatin levels',
                management='Avoid combination. Use alternative antibiotic or statin'
            ),
        }

    def check_interaction(self, drug1: str, drug2: str) -> Optional[DrugInteraction]:
        """Check for drug-drug interaction"""
        drug1_lower = drug1.lower()
        drug2_lower = drug2.lower()

        # Check both orders
        interaction = (
            self.interactions.get((drug1_lower, drug2_lower)) or
            self.interactions.get((drug2_lower, drug1_lower))
        )

        return interaction

    def check_multiple(self, drugs: List[str]) -> List[DrugInteraction]:
        """Check interactions among multiple drugs"""
        interactions = []

        for i, drug1 in enumerate(drugs):
            for drug2 in drugs[i+1:]:
                interaction = self.check_interaction(drug1, drug2)
                if interaction:
                    interactions.append(interaction)

        return interactions


class ClinicalDecisionSupport:
    """Clinical decision support system"""

    def __init__(self):
        self.guidelines = {
            'diabetes': ClinicalRecommendation(
                condition='Type 2 Diabetes Mellitus',
                recommendations=[
                    'First-line: Metformin 500-2000mg daily',
                    'Lifestyle modifications: diet, exercise, weight loss',
                    'HbA1c target: <7% for most patients',
                    'Consider GLP-1 agonist or SGLT2 inhibitor if cardiovascular disease',
                    'Screen for complications: retinopathy, nephropathy, neuropathy'
                ],
                evidence_level='A',
                source='ADA 2024 Guidelines',
                contraindications=[
                    'Metformin: eGFR <30 ml/min, severe hepatic impairment',
                    'SGLT2 inhibitors: history of DKA'
                ]
            ),
            'hypertension': ClinicalRecommendation(
                condition='Essential Hypertension',
                recommendations=[
                    'BP target: <130/80 mmHg for most patients',
                    'First-line: ACE inhibitor, ARB, CCB, or thiazide diuretic',
                    'Lifestyle: sodium restriction, weight loss, exercise',
                    'Combination therapy if BP >20/10 above target',
                    'Monitor renal function and electrolytes'
                ],
                evidence_level='A',
                source='ACC/AHA 2023 Guidelines',
                contraindications=[
                    'ACE inhibitors: pregnancy, bilateral renal artery stenosis',
                    'Beta blockers: severe bradycardia, heart block'
                ]
            ),
            'heart failure': ClinicalRecommendation(
                condition='Heart Failure with Reduced Ejection Fraction',
                recommendations=[
                    'Quadruple therapy: ACE-i/ARB/ARNI + beta blocker + MRA + SGLT2i',
                    'Diuretics for volume overload',
                    'Monitor daily weights, symptoms',
                    'Cardiac rehabilitation',
                    'Consider ICD if EF ≤35% despite optimal medical therapy'
                ],
                evidence_level='A',
                source='ESC 2023 Guidelines',
                contraindications=[
                    'ARNI: history of angioedema with ACE inhibitor',
                    'MRA: severe renal impairment, hyperkalemia'
                ]
            ),
        }

    def get_recommendations(self, condition: str) -> Optional[ClinicalRecommendation]:
        """Get clinical recommendations for a condition"""
        return self.guidelines.get(condition.lower())

    def search_guidelines(self, query: str) -> List[ClinicalRecommendation]:
        """Search clinical guidelines"""
        results = []
        query_lower = query.lower()

        for condition, guideline in self.guidelines.items():
            if (query_lower in condition.lower() or
                query_lower in guideline.condition.lower() or
                any(query_lower in rec.lower() for rec in guideline.recommendations)):
                results.append(guideline)

        return results


class MARIACore:
    """Main MARIA - Machine Learning Augmented Research and Intelligent Analysis"""

    def __init__(self):
        self.ner = MedicalNER()
        self.knowledge_graph = MedicalKnowledgeGraph()
        self.drug_checker = DrugInteractionChecker()
        self.clinical_support = ClinicalDecisionSupport()

    async def process_medical_query(self, question: str) -> Dict:
        """Process medical question with full pipeline"""
        start_time = datetime.now()

        # Extract medical entities
        entities = self.ner.extract_entities(question)

        # Find knowledge triplets
        triplets = self.knowledge_graph.find_triplets(entities)

        # Check for drug interactions
        drug_entities = [e.text for e in entities if e.entity_type == 'drug']
        drug_interactions = []
        if len(drug_entities) >= 2:
            drug_interactions = self.drug_checker.check_multiple(drug_entities)

        # Generate answer based on question type
        answer = await self._generate_answer(question, entities, triplets, drug_interactions)

        # Calculate confidence
        confidence = self._calculate_confidence(entities, triplets)

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return {
            'answer': answer,
            'medical_entities': [
                {
                    'text': e.text,
                    'type': e.entity_type,
                    'confidence': e.confidence
                } for e in entities
            ],
            'knowledge_triplets': [
                {
                    'head': t.head,
                    'relation': t.relation,
                    'tail': t.tail,
                    'confidence': t.confidence,
                    'source': t.source
                } for t in triplets
            ],
            'drug_interactions': [
                {
                    'drug1': di.drug1,
                    'drug2': di.drug2,
                    'severity': di.severity,
                    'description': di.description,
                    'mechanism': di.mechanism,
                    'management': di.management
                } for di in drug_interactions
            ],
            'confidence_score': confidence,
            'processing_time_ms': round(processing_time, 2),
            'timestamp': datetime.now().isoformat()
        }

    async def _generate_answer(
        self,
        question: str,
        entities: List[MedicalEntity],
        triplets: List[KnowledgeTriplet],
        drug_interactions: List[DrugInteraction]
    ) -> str:
        """Generate medical answer"""

        # Check if question is about drug interactions
        if len(drug_interactions) > 0:
            answer_parts = ["I found the following drug interactions:\n"]
            for interaction in drug_interactions:
                answer_parts.append(
                    f"\n**{interaction.drug1.title()} + {interaction.drug2.title()}** "
                    f"(Severity: {interaction.severity.upper()})\n"
                    f"- {interaction.description}\n"
                    f"- Mechanism: {interaction.mechanism}\n"
                    f"- Management: {interaction.management}"
                )
            return "\n".join(answer_parts)

        # Check if question is about a specific condition
        disease_entities = [e for e in entities if e.entity_type == 'disease']
        if disease_entities:
            condition = disease_entities[0].text
            recommendation = self.clinical_support.get_recommendations(condition)

            if recommendation:
                answer_parts = [
                    f"**Clinical Recommendations for {recommendation.condition}:**\n",
                    "\n**Treatment Recommendations:**"
                ]
                for i, rec in enumerate(recommendation.recommendations, 1):
                    answer_parts.append(f"{i}. {rec}")

                answer_parts.append(f"\n**Evidence Level:** {recommendation.evidence_level}")
                answer_parts.append(f"**Source:** {recommendation.source}")

                if recommendation.contraindications:
                    answer_parts.append("\n**Contraindications:**")
                    for contra in recommendation.contraindications:
                        answer_parts.append(f"- {contra}")

                return "\n".join(answer_parts)

        # Use knowledge triplets to generate answer
        if triplets:
            answer_parts = ["Based on medical knowledge:\n"]
            for triplet in triplets[:5]:
                relation_text = triplet.relation.replace('_', ' ').lower()
                answer_parts.append(
                    f"- {triplet.head.title()} {relation_text} {triplet.tail} "
                    f"(confidence: {triplet.confidence:.0%}, source: {triplet.source})"
                )
            return "\n".join(answer_parts)

        # Fallback response
        if entities:
            entity_list = ", ".join([e.text for e in entities[:5]])
            return (
                f"I identified the following medical concepts: {entity_list}. "
                "While I don't have specific information to fully answer your question, "
                "I recommend consulting current medical literature or clinical guidelines "
                "for the most accurate and up-to-date information."
            )

        return (
            "I couldn't extract specific medical entities from your question. "
            "Please rephrase your question with specific medical terms, conditions, "
            "drugs, or symptoms you'd like to know about."
        )

    def _calculate_confidence(
        self,
        entities: List[MedicalEntity],
        triplets: List[KnowledgeTriplet]
    ) -> float:
        """Calculate answer confidence"""
        if not entities:
            return 0.2

        entity_conf = sum(e.confidence for e in entities) / len(entities)

        if triplets:
            triplet_conf = sum(t.confidence for t in triplets) / len(triplets)
            return (entity_conf + triplet_conf) / 2

        return entity_conf * 0.7  # Reduce if no triplets found

    async def analyze_patient_case(self, case_data: Dict) -> Dict:
        """Analyze patient case and provide clinical insights"""
        symptoms = case_data.get('symptoms', [])
        medical_history = case_data.get('medical_history', [])
        medications = case_data.get('medications', [])

        # Extract entities from all inputs
        all_text = ' '.join(symptoms + medical_history + medications)
        entities = self.ner.extract_entities(all_text)

        # Check drug interactions
        drug_interactions = self.drug_checker.check_multiple(medications)

        # Find related knowledge
        triplets = self.knowledge_graph.find_triplets(entities)

        # Generate differential diagnosis suggestions
        disease_entities = [e for e in entities if e.entity_type == 'disease']
        symptom_entities = [e for e in entities if e.entity_type == 'symptom']

        return {
            'identified_conditions': [e.text for e in disease_entities],
            'symptoms_analyzed': [e.text for e in symptom_entities],
            'drug_interactions': [
                {
                    'drugs': f"{di.drug1} + {di.drug2}",
                    'severity': di.severity,
                    'description': di.description
                } for di in drug_interactions
            ],
            'clinical_knowledge': [
                {
                    'relationship': f"{t.head} {t.relation.replace('_', ' ').lower()} {t.tail}",
                    'confidence': t.confidence
                } for t in triplets[:5]
            ],
            'recommendations': 'Please consult with the patient\'s healthcare provider for personalized medical advice.'
        }

    async def process_with_kgarevion(self, question_text: str, question_type: str = "open_ended", candidates: Optional[List[str]] = None) -> Dict:
        """
        Process medical question using KGAREVION pipeline
        Implements: Generate → Review → Revise → Answer
        """
        try:
            # Initialize KGAREVION pipeline
            pipeline = KGARevionPipeline()

            # Create question object
            question = KGQuestion(
                text=question_text,
                question_type=question_type,
                candidates=candidates
            )

            # Process through KGAREVION pipeline
            result = await pipeline.process_question(question)

            # Clean up
            await pipeline.close()

            return result

        except Exception as e:
            logger.error(f"KGAREVION processing error: {e}", exc_info=True)
            return {
                "question": question_text,
                "answer": "I encountered an error processing your question with the knowledge graph.",
                "confidence": 0.0,
                "error": str(e),
                "verified_triplets": [],
                "medical_entities": []
            }
