"""
Medical Safety Layer and Clinical Validation System
Critical safety checks for medical AI responses

This implements comprehensive safety validation including:
- Emergency condition detection
- Drug interaction checking
- Protected population screening
- Clinical guideline validation
- Risk level assessment
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for medical responses"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class MedicalDomain(Enum):
    """Medical specialty domains"""
    GENERAL = "general"
    CARDIOLOGY = "cardiology"
    ONCOLOGY = "oncology"
    PSYCHIATRY = "psychiatry"
    EMERGENCY = "emergency"
    PEDIATRICS = "pediatrics"
    OBSTETRICS = "obstetrics"
    PHARMACOLOGY = "pharmacology"


@dataclass
class SafetyCheckResult:
    """Result of safety validation"""
    is_safe: bool
    risk_level: RiskLevel
    warnings: List[str]
    required_disclaimers: List[str]
    confidence_score: float
    requires_human_review: bool
    domain: MedicalDomain
    explanation: str
    timestamp: str


class MedicalSafetyValidator:
    """
    Comprehensive medical safety validation system

    Checks for:
    - Emergency medical situations
    - Drug interactions and contraindications
    - High-risk medications
    - Protected populations (pediatric, pregnant, elderly)
    - Dosage recommendations
    - Clinical guideline compliance
    """

    def __init__(self):
        # Initialize critical term databases
        self.emergency_terms = self._load_emergency_terms()
        self.contraindications = self._load_contraindications()
        self.high_risk_drugs = self._load_high_risk_drugs()
        self.protected_populations = ["pregnant", "pediatric", "elderly", "immunocompromised"]
        self.dosage_patterns = self._compile_dosage_patterns()

    def _load_emergency_terms(self) -> Set[str]:
        """Load terms indicating emergency medical situations"""
        return {
            # Cardiovascular emergencies
            "chest pain", "heart attack", "myocardial infarction", "cardiac arrest",
            "severe chest pressure", "crushing chest pain",

            # Respiratory emergencies
            "difficulty breathing", "shortness of breath", "dyspnea", "respiratory distress",
            "cannot breathe", "choking", "severe wheezing",

            # Neurological emergencies
            "stroke", "stroke symptoms", "facial drooping", "arm weakness", "speech difficulty",
            "unconscious", "unresponsive", "seizure", "convulsion", "paralysis",
            "severe headache", "worst headache", "sudden confusion", "vision loss",

            # Trauma & bleeding
            "severe bleeding", "uncontrolled bleeding", "hemorrhage", "severe trauma",
            "head injury", "loss of consciousness", "severe burn",

            # Other critical conditions
            "anaphylaxis", "allergic reaction", "difficulty swallowing", "throat swelling",
            "suicidal", "suicide attempt", "overdose", "poisoning",
            "severe pain", "acute abdomen", "severe vomiting", "severe diarrhea"
        }

    def _load_contraindications(self) -> Dict[str, List[str]]:
        """Load drug contraindication database"""
        return {
            # Anticoagulants
            "warfarin": ["aspirin", "nsaids", "ibuprofen", "naproxen", "active bleeding"],
            "heparin": ["active bleeding", "thrombocytopenia"],

            # Diabetes medications
            "metformin": ["kidney disease", "contrast dye", "iodine", "alcohol abuse", "liver disease"],
            "insulin": ["hypoglycemia"],

            # Cardiovascular
            "ace_inhibitors": ["pregnancy", "hyperkalemia", "bilateral renal stenosis", "angioedema"],
            "beta_blockers": ["asthma", "copd", "bradycardia", "heart block", "cardiogenic shock"],
            "calcium_channel_blockers": ["heart failure", "severe hypotension"],

            # Lipid-lowering
            "statins": ["pregnancy", "breastfeeding", "active liver disease", "rhabdomyolysis"],

            # Psychiatric
            "maoi": ["ssri", "snri", "tyramine_foods", "sympathomimetics", "meperidine"],
            "lithium": ["nsaids", "thiazides", "ace_inhibitors", "dehydration", "renal impairment"],

            # Pain management
            "nsaids": ["peptic ulcer", "kidney disease", "heart failure", "anticoagulants"],
            "opioids": ["respiratory depression", "sleep apnea", "alcohol"],

            # Antibiotics
            "fluoroquinolones": ["myasthenia gravis", "tendon problems", "pregnancy"],
        }

    def _load_high_risk_drugs(self) -> Set[str]:
        """Load ISMP high-alert medications list"""
        return {
            # Anticoagulants
            "warfarin", "heparin", "enoxaparin", "dabigatran", "rivaroxaban", "apixaban",

            # Diabetes agents
            "insulin", "regular insulin", "nph insulin", "insulin glargine", "insulin lispro",

            # Opioids
            "morphine", "fentanyl", "hydromorphone", "oxycodone", "hydrocodone", "methadone",

            # Sedatives
            "propofol", "midazolam", "lorazepam", "diazepam", "ketamine",

            # Chemotherapy
            "methotrexate", "cisplatin", "doxorubicin", "vincristine", "cyclophosphamide",

            # Cardiovascular
            "digoxin", "amiodarone", "lidocaine", "dopamine", "epinephrine", "norepinephrine",

            # Electrolytes
            "potassium chloride", "sodium chloride", "magnesium sulfate", "calcium gluconate",

            # Others
            "nitroprusside", "neuromuscular blockers", "thrombolytics", "immunosuppressants"
        }

    def _compile_dosage_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for dosage detection"""
        return [
            re.compile(r'\d+\s*(?:mg|mcg|g|ml|units?|iu)\b', re.IGNORECASE),
            re.compile(r'\d+\s*(?:times?|x)\s*(?:daily|per day|/day|a day)', re.IGNORECASE),
            re.compile(r'(?:take|administer|inject|give)\s+\d+', re.IGNORECASE),
            re.compile(r'\d+\s*(?:mg/kg|mcg/kg)', re.IGNORECASE),
        ]

    def validate_response(
        self,
        question: str,
        answer: str,
        patient_context: Optional[Dict] = None,
        confidence_score: float = 0.0
    ) -> SafetyCheckResult:
        """
        Comprehensive safety validation of medical response

        Args:
            question: User's medical question
            answer: AI-generated answer
            patient_context: Optional patient information
            confidence_score: Model's confidence in the answer

        Returns:
            SafetyCheckResult with safety assessment
        """
        warnings = []
        disclaimers = []
        risk_level = RiskLevel.LOW
        requires_review = False

        # Check for emergency situations
        emergency_check = self._check_emergency_conditions(question, answer)
        if emergency_check:
            warnings.append(emergency_check)
            disclaimers.append(
                "⚠️ EMERGENCY: This may be a medical emergency. "
                "Seek immediate medical attention or call emergency services (911)."
            )
            risk_level = RiskLevel.CRITICAL
            requires_review = True

        # Check for high-risk medications
        drug_check = self._check_drug_safety(answer, patient_context)
        if drug_check:
            warnings.extend(drug_check)
            if any("contraindication" in w.lower() for w in drug_check):
                risk_level = max(risk_level, RiskLevel.HIGH, key=lambda x: list(RiskLevel).index(x))
                requires_review = True

        # Check dosage recommendations
        dosage_check = self._check_dosage_safety(answer)
        if dosage_check:
            warnings.append(dosage_check)
            disclaimers.append(
                "⚕️ Dosage recommendations should always be verified by a healthcare provider."
            )
            risk_level = max(risk_level, RiskLevel.MODERATE, key=lambda x: list(RiskLevel).index(x))

        # Check for protected populations
        if patient_context:
            population_check = self._check_protected_populations(answer, patient_context)
            if population_check:
                warnings.extend(population_check)
                risk_level = max(risk_level, RiskLevel.MODERATE, key=lambda x: list(RiskLevel).index(x))

        # Check confidence threshold
        if confidence_score < 0.7:
            warnings.append(f"Low confidence response ({confidence_score:.2f})")
            requires_review = True

        # Determine medical domain
        domain = self._classify_medical_domain(question, answer)

        # Add standard disclaimers
        disclaimers.extend(self._get_standard_disclaimers(domain, risk_level))

        # Determine if response is safe to show
        is_safe = risk_level in [RiskLevel.LOW, RiskLevel.MODERATE] and not requires_review

        return SafetyCheckResult(
            is_safe=is_safe,
            risk_level=risk_level,
            warnings=warnings,
            required_disclaimers=disclaimers,
            confidence_score=confidence_score,
            requires_human_review=requires_review,
            domain=domain,
            explanation=self._generate_safety_explanation(warnings, risk_level),
            timestamp=datetime.utcnow().isoformat()
        )

    def _check_emergency_conditions(self, question: str, answer: str) -> Optional[str]:
        """Check for emergency medical conditions"""
        combined_text = f"{question} {answer}".lower()

        for term in self.emergency_terms:
            if term in combined_text:
                return f"Emergency condition detected: {term}"

        return None

    def _check_drug_safety(self, answer: str, patient_context: Optional[Dict]) -> List[str]:
        """Check for drug safety issues"""
        warnings = []
        answer_lower = answer.lower()

        # Check for high-risk drugs
        for drug in self.high_risk_drugs:
            if drug in answer_lower:
                warnings.append(f"High-risk medication mentioned: {drug.replace('_', ' ')}")

        # Check contraindications
        for drug, contraindications in self.contraindications.items():
            if drug in answer_lower:
                for contra in contraindications:
                    if contra in answer_lower:
                        warnings.append(
                            f"Potential contraindication: {drug.replace('_', ' ')} "
                            f"with {contra.replace('_', ' ')}"
                        )

        # Check patient-specific contraindications
        if patient_context and "medications" in patient_context:
            warnings.extend(self._check_drug_interactions(
                answer_lower,
                patient_context["medications"]
            ))

        return warnings

    def _check_drug_interactions(self, answer: str, current_medications: List[str]) -> List[str]:
        """Check for drug-drug interactions"""
        warnings = []

        # Simplified interaction checking
        critical_interactions = [
            (["warfarin", "coumadin"], ["aspirin", "nsaid", "ibuprofen", "naproxen"]),
            (["ssri", "prozac", "zoloft", "sertraline", "fluoxetine"], ["maoi", "tramadol"]),
            (["metformin"], ["contrast", "iodine"]),
            (["ace_inhibitor", "lisinopril", "enalapril"], ["potassium", "spironolactone"]),
        ]

        for drug_group1, drug_group2 in critical_interactions:
            if any(drug in answer for drug in drug_group1):
                for med in current_medications:
                    if any(contraindicated in med.lower() for contraindicated in drug_group2):
                        warnings.append(f"Potential drug interaction with current medication: {med}")

        return warnings

    def _check_dosage_safety(self, answer: str) -> Optional[str]:
        """Check if dosage recommendations are present"""
        for pattern in self.dosage_patterns:
            if pattern.search(answer):
                return "Dosage recommendation detected - requires professional verification"
        return None

    def _check_protected_populations(self, answer: str, patient_context: Dict) -> List[str]:
        """Check for special populations requiring extra caution"""
        warnings = []

        # Pediatric patients
        if "age" in patient_context:
            age = patient_context["age"]
            if age < 18:
                warnings.append("🧒 Pediatric patient - specialized dosing and monitoring required")
            elif age > 65:
                warnings.append("👴 Elderly patient - consider dose adjustments and drug interactions")

        # Pregnant patients
        if "pregnant" in patient_context and patient_context["pregnant"]:
            warnings.append("🤰 Pregnant patient - verify medication safety category")

        # Organ dysfunction
        if "conditions" in patient_context:
            conditions = [c.lower() for c in patient_context["conditions"]]
            if any(cond in conditions for cond in ["kidney disease", "renal failure", "ckd"]):
                warnings.append("⚕️ Kidney disease present - dose adjustment may be needed")
            if any(cond in conditions for cond in ["liver disease", "cirrhosis", "hepatitis"]):
                warnings.append("⚕️ Liver disease present - metabolism may be affected")

        return warnings

    def _classify_medical_domain(self, question: str, answer: str) -> MedicalDomain:
        """Classify the medical domain of the query"""
        combined = f"{question} {answer}".lower()

        domain_keywords = {
            MedicalDomain.CARDIOLOGY: ["heart", "cardiac", "arrhythmia", "blood pressure", "hypertension", "angina"],
            MedicalDomain.ONCOLOGY: ["cancer", "tumor", "chemotherapy", "oncology", "metastasis", "malignant"],
            MedicalDomain.PSYCHIATRY: ["depression", "anxiety", "mental", "psychiatric", "mood", "psychosis"],
            MedicalDomain.EMERGENCY: ["emergency", "acute", "urgent", "trauma", "critical", "911"],
            MedicalDomain.PEDIATRICS: ["child", "pediatric", "infant", "newborn", "adolescent"],
            MedicalDomain.OBSTETRICS: ["pregnancy", "pregnant", "fetal", "prenatal", "obstetric", "maternal"],
            MedicalDomain.PHARMACOLOGY: ["drug", "medication", "dose", "prescription", "pharmaceutical", "pharmacology"]
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in combined for keyword in keywords):
                return domain

        return MedicalDomain.GENERAL

    def _get_standard_disclaimers(self, domain: MedicalDomain, risk_level: RiskLevel) -> List[str]:
        """Get standard medical disclaimers based on context"""
        disclaimers = [
            "ℹ️ This information is for educational purposes only and not a substitute for professional medical advice.",
            "👨‍⚕️ Always consult with a qualified healthcare provider for medical decisions."
        ]

        if risk_level == RiskLevel.HIGH or risk_level == RiskLevel.CRITICAL:
            disclaimers.append(
                "⚠️ This response addresses potentially serious medical conditions. "
                "Immediate medical consultation is strongly recommended."
            )

        domain_disclaimers = {
            MedicalDomain.PHARMACOLOGY: "💊 Medication decisions should always be made in consultation with your healthcare provider or pharmacist.",
            MedicalDomain.PSYCHIATRY: "🧠 Mental health concerns should be evaluated by a qualified mental health professional.",
            MedicalDomain.PEDIATRICS: "👶 Pediatric medical care requires specialized expertise. Always consult a pediatrician.",
            MedicalDomain.OBSTETRICS: "🤰 Pregnancy-related medical care requires specialized obstetric expertise.",
            MedicalDomain.EMERGENCY: "🚨 Emergency medical situations require immediate professional medical attention.",
            MedicalDomain.ONCOLOGY: "🎗️ Cancer care requires multidisciplinary expertise and should be managed by oncology specialists."
        }

        if domain in domain_disclaimers:
            disclaimers.append(domain_disclaimers[domain])

        return disclaimers

    def _generate_safety_explanation(self, warnings: List[str], risk_level: RiskLevel) -> str:
        """Generate explanation for safety decision"""
        if not warnings:
            return "Response passed all safety checks."

        explanation = f"Risk level: {risk_level.value.upper()}. "

        if len(warnings) == 1:
            explanation += f"Issue identified: {warnings[0]}"
        else:
            explanation += f"Issues identified: {'; '.join(warnings[:3])}"
            if len(warnings) > 3:
                explanation += f" and {len(warnings)-3} more"

        return explanation


# Example usage
def demo_safety_validator():
    """Demonstrate medical safety validation"""
    logger.info("=" * 80)
    logger.info("Medical Safety Validator Demo")
    logger.info("=" * 80)

    validator = MedicalSafetyValidator()

    # Test cases
    test_cases = [
        {
            "question": "What should I do for a severe headache?",
            "answer": "For severe headaches, you can try over-the-counter pain relievers like ibuprofen.",
            "confidence": 0.85
        },
        {
            "question": "I have chest pain, what should I do?",
            "answer": "Chest pain can be serious. Please call 911 immediately.",
            "confidence": 0.95
        },
        {
            "question": "Can I take warfarin with aspirin?",
            "answer": "Warfarin and aspirin can interact, increasing bleeding risk.",
            "confidence": 0.90
        }
    ]

    for i, case in enumerate(test_cases, 1):
        logger.info(f"\nTest Case {i}:")
        logger.info(f"Q: {case['question']}")
        logger.info(f"A: {case['answer']}")

        result = validator.validate_response(
            question=case['question'],
            answer=case['answer'],
            confidence_score=case['confidence']
        )

        logger.info(f"\nSafety Result:")
        logger.info(f"  Is Safe: {result.is_safe}")
        logger.info(f"  Risk Level: {result.risk_level.value}")
        logger.info(f"  Domain: {result.domain.value}")
        logger.info(f"  Warnings: {len(result.warnings)}")
        for warning in result.warnings:
            logger.info(f"    - {warning}")
        logger.info(f"  Requires Review: {result.requires_human_review}")
        logger.info(f"  Explanation: {result.explanation}")

    logger.info("\n" + "=" * 80)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo_safety_validator()
