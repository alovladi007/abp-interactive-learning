"""
KGAREVION Core Pipeline Implementation
Medical QA System with Knowledge Graph Verification

Based on the paper: "KG-Agent: Empowering LLMs with Medical Knowledge Graph"
Implements Generate → Review → Revise → Answer pipeline
"""

import asyncio
import re
import logging
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


# Data Models
@dataclass
class MedicalTriplet:
    """Represents a medical knowledge triplet (head, relation, tail)"""
    head: str
    relation: str
    tail: str
    confidence: float = 1.0
    verified: bool = False
    source: str = "generated"


@dataclass
class Question:
    """Medical question structure"""
    text: str
    question_type: str  # "multiple_choice" or "open_ended"
    candidates: Optional[List[str]] = None
    medical_entities: Optional[List[str]] = None


class RelationType(Enum):
    """Medical relation types from PrimeKG"""
    PROTEIN_PROTEIN = "protein_protein"
    DRUG_PROTEIN = "drug_protein"
    DISEASE_PROTEIN = "disease_protein"
    DRUG_DRUG = "drug_drug"
    DRUG_DISEASE = "drug_disease"
    GENE_DISEASE = "gene_disease"
    INTERACTS_WITH = "interacts_with"
    ASSOCIATED_WITH = "associated_with"
    TREATS = "treats"
    CAUSES = "causes"
    CONTRAINDICATED = "contraindicated"
    SIDE_EFFECT = "side_effect"


class MedicalEntityExtractor:
    """Extract medical entities from text using pattern matching"""

    def __init__(self):
        # Common medical entity patterns
        self.protein_patterns = [
            r'\b[A-Z][A-Z0-9]{2,}\b',  # Protein names (e.g., HSPA8, DHDDS)
            r'\b(protein|enzyme|receptor)\s+\w+\b'
        ]

        self.disease_patterns = [
            r'\b\w+\s+(disease|syndrome|disorder)\b',
            r'\bRetinitis Pigmentosa\s*\d*\b',
            r'\b\w+itis\b',  # Inflammatory diseases
            r'\b\w+osis\b',  # Various conditions
            r'\b\w+oma\b',   # Tumors
        ]

        self.drug_patterns = [
            r'\b\w+mycin\b',  # Antibiotics
            r'\b\w+pril\b',   # ACE inhibitors
            r'\b\w+lol\b',    # Beta blockers
            r'\b\w+statin\b', # Statins
            r'\bwarfarin\b',
            r'\baspirin\b',
            r'\bmetformin\b',
        ]

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities categorized by type"""
        entities = {
            'proteins': [],
            'diseases': [],
            'drugs': [],
            'genes': []
        }

        # Extract proteins
        for pattern in self.protein_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['proteins'].extend(matches)

        # Extract diseases
        for pattern in self.disease_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['diseases'].extend(matches)

        # Extract drugs
        for pattern in self.drug_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['drugs'].extend(matches)

        # Remove duplicates and clean
        for key in entities:
            entities[key] = list(set([e.strip() for e in entities[key] if e.strip()]))

        return entities


class KnowledgeGraphSimulator:
    """Simulates knowledge graph with medical relationships"""

    def __init__(self):
        # Simplified KG - in production, use Neo4j
        self.triplets_db = [
            # Protein-Disease relationships
            MedicalTriplet("HSPA8", "interacts_with", "DHDDS", 0.95, True, "primekg"),
            MedicalTriplet("DHDDS", "associated_with", "Retinitis Pigmentosa 59", 0.92, True, "primekg"),
            MedicalTriplet("HSPA8", "associated_with", "Retinitis Pigmentosa 59", 0.88, True, "primekg"),

            # Drug interactions
            MedicalTriplet("warfarin", "interacts_with", "aspirin", 0.98, True, "drugbank"),
            MedicalTriplet("warfarin", "increases_risk_of", "bleeding", 0.95, True, "drugbank"),
            MedicalTriplet("aspirin", "increases_risk_of", "bleeding", 0.93, True, "drugbank"),

            # Diabetes relationships
            MedicalTriplet("metformin", "treats", "type 2 diabetes", 0.97, True, "primekg"),
            MedicalTriplet("diabetes", "causes", "hyperglycemia", 0.95, True, "primekg"),
            MedicalTriplet("diabetes", "treated_with", "metformin", 0.92, True, "primekg"),

            # Heart disease
            MedicalTriplet("hypertension", "causes", "heart disease", 0.90, True, "primekg"),
            MedicalTriplet("hypertension", "treated_with", "ACE inhibitors", 0.88, True, "primekg"),
        ]

    async def verify_triplet(self, triplet: MedicalTriplet) -> bool:
        """Check if triplet exists in knowledge graph"""
        for db_triplet in self.triplets_db:
            if (db_triplet.head.lower() == triplet.head.lower() and
                db_triplet.relation.lower() == triplet.relation.lower() and
                db_triplet.tail.lower() == triplet.tail.lower()):
                return True
        return False

    async def get_related_triplets(self, entity: str, max_results: int = 10) -> List[MedicalTriplet]:
        """Get triplets related to an entity"""
        related = []
        entity_lower = entity.lower()

        for triplet in self.triplets_db:
            if (entity_lower in triplet.head.lower() or
                entity_lower in triplet.tail.lower()):
                related.append(triplet)
                if len(related) >= max_results:
                    break

        return related


class GenerateAction:
    """Generate medical knowledge triplets from questions"""

    def __init__(self):
        self.entity_extractor = MedicalEntityExtractor()
        self.kg = KnowledgeGraphSimulator()

    async def generate_triplets(self, question: Question) -> List[MedicalTriplet]:
        """Generate relevant triplets for the question"""
        triplets = []

        # Extract entities
        entities = self.entity_extractor.extract_entities(question.text)

        # Store extracted entities in question
        all_entities = []
        for entity_type, entity_list in entities.items():
            all_entities.extend(entity_list)
        question.medical_entities = all_entities

        logger.info(f"Extracted entities: {entities}")

        if question.question_type == "multiple_choice" and question.candidates:
            # Choice-aware generation
            for candidate in question.candidates:
                candidate_triplets = await self._generate_for_candidate(question, candidate, entities)
                triplets.extend(candidate_triplets)
        else:
            # Non-choice-aware generation
            triplets = await self._generate_from_entities(entities)

        return triplets

    async def _generate_for_candidate(self, question: Question, candidate: str, entities: Dict[str, List[str]]) -> List[MedicalTriplet]:
        """Generate triplets for a specific answer candidate"""
        triplets = []

        # Extract entities from candidate
        candidate_entities = self.entity_extractor.extract_entities(candidate)

        # Generate relationships between question entities and candidate entities
        for q_type, q_entities in entities.items():
            for c_type, c_entities in candidate_entities.items():
                for q_entity in q_entities:
                    for c_entity in c_entities:
                        # Get related triplets from KG
                        related = await self.kg.get_related_triplets(c_entity)
                        triplets.extend(related)

        return triplets

    async def _generate_from_entities(self, entities: Dict[str, List[str]]) -> List[MedicalTriplet]:
        """Generate triplets from extracted entities"""
        triplets = []

        # Get related triplets for each entity
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                related = await self.kg.get_related_triplets(entity)
                triplets.extend(related)

        # Generate pairwise relationships
        all_entities = []
        for entity_list in entities.values():
            all_entities.extend(entity_list)

        for i, entity1 in enumerate(all_entities):
            for entity2 in all_entities[i+1:]:
                triplet = MedicalTriplet(
                    entity1,
                    "associated_with",
                    entity2,
                    confidence=0.7,
                    source="inferred"
                )
                triplets.append(triplet)

        return triplets


class ReviewAction:
    """Review and verify generated triplets using knowledge graph"""

    def __init__(self):
        self.kg = KnowledgeGraphSimulator()

    async def review_triplets(self, triplets: List[MedicalTriplet]) -> Tuple[List[MedicalTriplet], List[MedicalTriplet]]:
        """Separate triplets into verified and false sets"""
        verified_triplets = []
        false_triplets = []

        for triplet in triplets:
            is_valid = await self._verify_single_triplet(triplet)

            if is_valid:
                triplet.verified = True
                verified_triplets.append(triplet)
            else:
                false_triplets.append(triplet)

        logger.info(f"Review complete: {len(verified_triplets)} verified, {len(false_triplets)} false")

        return verified_triplets, false_triplets

    async def _verify_single_triplet(self, triplet: MedicalTriplet) -> bool:
        """Verify a single triplet"""
        # Check if triplet exists in KG
        exists = await self.kg.verify_triplet(triplet)

        if exists:
            return True

        # Apply soft constraint rules (from paper)
        # If entities are not in KG, keep the triplet (incomplete knowledge)
        if triplet.source == "generated":
            # Be lenient with generated triplets
            return triplet.confidence > 0.5

        return False


class ReviseAction:
    """Revise false triplets to correct them"""

    def __init__(self):
        self.kg = KnowledgeGraphSimulator()

    async def revise_triplets(self, false_triplets: List[MedicalTriplet], question: Question) -> List[MedicalTriplet]:
        """Revise false triplets"""
        revised_triplets = []

        for triplet in false_triplets:
            revised = await self._revise_single_triplet(triplet, question)
            if revised:
                revised_triplets.append(revised)

        return revised_triplets

    async def _revise_single_triplet(self, triplet: MedicalTriplet, question: Question) -> Optional[MedicalTriplet]:
        """Revise a single triplet by finding related correct triplets"""
        # Get related triplets from KG
        head_related = await self.kg.get_related_triplets(triplet.head)
        tail_related = await self.kg.get_related_triplets(triplet.tail)

        # Try to find a correct relationship
        for related in head_related:
            if related.tail.lower() == triplet.tail.lower():
                return MedicalTriplet(
                    triplet.head,
                    related.relation,
                    triplet.tail,
                    confidence=0.8,
                    source="revised"
                )

        # If no revision found, return with lower confidence
        triplet.confidence = 0.3
        triplet.source = "revised_uncertain"
        return triplet


class AnswerAction:
    """Generate final answer from verified triplets"""

    def generate_answer(self, question: Question, verified_triplets: List[MedicalTriplet]) -> Dict[str, Any]:
        """Generate final answer based on verified triplets"""

        if not verified_triplets:
            return {
                "answer": "I don't have enough verified knowledge to answer this question confidently.",
                "confidence": 0.0,
                "explanation": "No verified triplets found in knowledge graph."
            }

        # Calculate overall confidence
        avg_confidence = sum(t.confidence for t in verified_triplets) / len(verified_triplets)

        if question.question_type == "multiple_choice" and question.candidates:
            # For MC questions, select best candidate based on triplet support
            candidate_scores = {}

            for candidate in question.candidates:
                score = 0
                for triplet in verified_triplets:
                    if candidate.lower() in triplet.head.lower() or candidate.lower() in triplet.tail.lower():
                        score += triplet.confidence
                candidate_scores[candidate] = score

            if candidate_scores:
                best_candidate = max(candidate_scores, key=candidate_scores.get)
                best_score = candidate_scores[best_candidate]

                # Generate explanation
                relevant_triplets = [
                    t for t in verified_triplets
                    if best_candidate.lower() in t.head.lower() or best_candidate.lower() in t.tail.lower()
                ]

                explanation = f"Based on {len(relevant_triplets)} verified knowledge triplets:\n"
                for t in relevant_triplets[:3]:  # Top 3 triplets
                    explanation += f"• {t.head} {t.relation} {t.tail}\n"

                return {
                    "answer": best_candidate,
                    "confidence": min(best_score / len(question.candidates), 1.0),
                    "explanation": explanation
                }

        # For open-ended questions, generate textual answer
        answer_parts = []
        for triplet in verified_triplets[:5]:  # Use top 5 triplets
            answer_parts.append(f"{triplet.head} {triplet.relation.replace('_', ' ')} {triplet.tail}")

        answer = "Based on the medical knowledge graph: " + ". ".join(answer_parts) + "."

        return {
            "answer": answer,
            "confidence": avg_confidence,
            "explanation": f"Answer generated from {len(verified_triplets)} verified triplets."
        }


class KGARevionPipeline:
    """Main KGAREVION pipeline orchestrator"""

    def __init__(self):
        self.generate_action = GenerateAction()
        self.review_action = ReviewAction()
        self.revise_action = ReviseAction()
        self.answer_action = AnswerAction()

        self.max_revise_rounds = 3

    async def process_question(self, question: Question) -> Dict[str, Any]:
        """Process a medical question through the full KGAREVION pipeline"""

        start_time = datetime.now()

        logger.info(f"Processing question: {question.text[:100]}...")

        try:
            # Step 1: Generate triplets
            generated_triplets = await self.generate_action.generate_triplets(question)
            logger.info(f"Generated {len(generated_triplets)} triplets")

            # Step 2: Review triplets
            verified_triplets, false_triplets = await self.review_action.review_triplets(generated_triplets)
            logger.info(f"Review: {len(verified_triplets)} verified, {len(false_triplets)} false")

            # Step 3: Revise false triplets (iteratively)
            for round_num in range(self.max_revise_rounds):
                if not false_triplets:
                    break

                logger.info(f"Revise round {round_num + 1}")
                revised_triplets = await self.revise_action.revise_triplets(false_triplets, question)

                # Re-review revised triplets
                newly_verified, still_false = await self.review_action.review_triplets(revised_triplets)
                verified_triplets.extend(newly_verified)
                false_triplets = still_false

            # Step 4: Generate answer
            answer_result = self.answer_action.generate_answer(question, verified_triplets)

            processing_time = (datetime.now() - start_time).total_seconds() * 1000

            result = {
                "question": question.text,
                "answer": answer_result["answer"],
                "confidence": answer_result["confidence"],
                "explanation": answer_result.get("explanation", ""),
                "verified_triplets": [
                    {
                        "head": t.head,
                        "relation": t.relation,
                        "tail": t.tail,
                        "confidence": t.confidence,
                        "source": t.source
                    }
                    for t in verified_triplets
                ],
                "medical_entities": question.medical_entities or [],
                "processing_stats": {
                    "total_triplets_generated": len(generated_triplets),
                    "triplets_verified": len(verified_triplets),
                    "triplets_revised": len(generated_triplets) - len(verified_triplets) - len(false_triplets),
                    "processing_time_ms": int(processing_time)
                }
            }

            return result

        except Exception as e:
            logger.error(f"Error in KGAREVION pipeline: {e}", exc_info=True)
            return {
                "question": question.text,
                "answer": "An error occurred while processing your question.",
                "confidence": 0.0,
                "error": str(e),
                "verified_triplets": [],
                "medical_entities": []
            }

    async def close(self):
        """Clean up resources"""
        pass


# Example usage
async def main():
    """Test the KGAREVION pipeline"""
    pipeline = KGARevionPipeline()

    # Test multiple choice question
    question1 = Question(
        text="Which protein is associated with Retinitis Pigmentosa 59?",
        question_type="multiple_choice",
        candidates=["HSPA4", "HSPA8", "HSPA1B", "HSPA1A"]
    )

    result1 = await pipeline.process_question(question1)
    print("=== Multiple Choice Question ===")
    print(f"Question: {result1['question']}")
    print(f"Answer: {result1['answer']}")
    print(f"Confidence: {result1['confidence']:.2f}")
    print(f"Verified Triplets: {len(result1['verified_triplets'])}")
    print()

    # Test open-ended question
    question2 = Question(
        text="What are the drug interactions between warfarin and aspirin?",
        question_type="open_ended"
    )

    result2 = await pipeline.process_question(question2)
    print("=== Open-Ended Question ===")
    print(f"Question: {result2['question']}")
    print(f"Answer: {result2['answer']}")
    print(f"Confidence: {result2['confidence']:.2f}")
    print()

    await pipeline.close()


if __name__ == "__main__":
    asyncio.run(main())
