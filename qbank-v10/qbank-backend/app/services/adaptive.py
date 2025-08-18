"""
Enhanced Adaptive Testing Engine with IRT
"""
import math
import random
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# IRT Constants
D = 1.7  # Scaling constant for logistic IRT models

class SelectionStrategy(Enum):
    """Item selection strategies for adaptive testing."""
    MAXIMUM_INFORMATION = "max_info"
    SYMPSON_HETTER = "sympson_hetter"
    RANDOM = "random"
    STRATIFIED = "stratified"
    CONTENT_BALANCED = "content_balanced"
    EXPOSURE_CONTROLLED = "exposure_controlled"

@dataclass
class ItemParameters:
    """IRT item parameters."""
    question_id: int
    version: int
    a: float = 1.0  # Discrimination
    b: float = 0.0  # Difficulty
    c: float = 0.0  # Guessing (for 3PL)
    sh_p: float = 1.0  # Sympson-Hetter probability
    topic_id: Optional[int] = None
    exposure_count: int = 0
    metadata: Dict[str, Any] = None

@dataclass
class AbilityEstimate:
    """User ability estimate."""
    theta: float = 0.0
    se: float = 1.0  # Standard error
    n_items: int = 0
    history: List[Tuple[int, bool]] = None  # (item_id, correct)

class IRTEngine:
    """Item Response Theory engine for adaptive testing."""
    
    @staticmethod
    def logistic(x: float) -> float:
        """Logistic function."""
        try:
            return 1.0 / (1.0 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0
    
    @staticmethod
    def prob_2pl(theta: float, a: float, b: float) -> float:
        """2-Parameter Logistic model probability."""
        return IRTEngine.logistic(D * a * (theta - b))
    
    @staticmethod
    def prob_3pl(theta: float, a: float, b: float, c: float) -> float:
        """3-Parameter Logistic model probability."""
        return c + (1.0 - c) * IRTEngine.logistic(D * a * (theta - b))
    
    @staticmethod
    def fisher_info_2pl(theta: float, a: float, b: float) -> float:
        """Fisher information for 2PL model."""
        p = IRTEngine.prob_2pl(theta, a, b)
        q = 1.0 - p
        if p <= 0 or q <= 0:
            return 0.0
        return (D ** 2) * (a ** 2) * p * q
    
    @staticmethod
    def fisher_info_3pl(theta: float, a: float, b: float, c: float) -> float:
        """Fisher information for 3PL model."""
        p = IRTEngine.prob_3pl(theta, a, b, c)
        q = 1.0 - p
        if p <= 0 or q <= 0 or (1.0 - c) <= 0:
            return 0.0
        return (D ** 2) * (a ** 2) * (q / p) * ((p - c) / (1.0 - c)) ** 2
    
    @staticmethod
    def likelihood_2pl(
        responses: List[Tuple[ItemParameters, bool]], 
        theta: float
    ) -> float:
        """Likelihood of responses given theta (2PL)."""
        likelihood = 1.0
        for item, correct in responses:
            p = IRTEngine.prob_2pl(theta, item.a, item.b)
            likelihood *= p if correct else (1.0 - p)
        return likelihood
    
    @staticmethod
    def likelihood_3pl(
        responses: List[Tuple[ItemParameters, bool]], 
        theta: float
    ) -> float:
        """Likelihood of responses given theta (3PL)."""
        likelihood = 1.0
        for item, correct in responses:
            p = IRTEngine.prob_3pl(theta, item.a, item.b, item.c)
            likelihood *= p if correct else (1.0 - p)
        return likelihood
    
    @staticmethod
    def mle_theta(
        responses: List[Tuple[ItemParameters, bool]], 
        model: str = "3PL",
        initial_theta: float = 0.0,
        max_iter: int = 50,
        tolerance: float = 0.001
    ) -> Tuple[float, float]:
        """Maximum Likelihood Estimation of theta."""
        if not responses:
            return initial_theta, 1.0
        
        theta = initial_theta
        for _ in range(max_iter):
            # Calculate first and second derivatives
            d1, d2 = 0.0, 0.0
            
            for item, correct in responses:
                if model == "3PL":
                    p = IRTEngine.prob_3pl(theta, item.a, item.b, item.c)
                    w = (p - item.c) / (1.0 - item.c)
                else:
                    p = IRTEngine.prob_2pl(theta, item.a, item.b)
                    w = p
                
                q = 1.0 - p
                if p > 0 and q > 0:
                    d1 += D * item.a * (correct - p) * w / p
                    d2 -= (D ** 2) * (item.a ** 2) * w * q
            
            if abs(d2) < 0.0001:
                break
            
            # Newton-Raphson update
            delta = d1 / d2
            theta = theta - delta
            
            # Bound theta to reasonable range
            theta = max(-4.0, min(4.0, theta))
            
            if abs(delta) < tolerance:
                break
        
        # Calculate standard error
        info = sum(
            IRTEngine.fisher_info_3pl(theta, item.a, item.b, item.c)
            if model == "3PL" else
            IRTEngine.fisher_info_2pl(theta, item.a, item.b)
            for item, _ in responses
        )
        
        se = 1.0 / math.sqrt(info) if info > 0 else 1.0
        
        return theta, se
    
    @staticmethod
    def eap_theta(
        responses: List[Tuple[ItemParameters, bool]], 
        model: str = "3PL",
        prior_mean: float = 0.0,
        prior_sd: float = 1.0,
        n_quadrature: int = 61
    ) -> Tuple[float, float]:
        """Expected A Posteriori estimation of theta."""
        if not responses:
            return prior_mean, prior_sd
        
        # Quadrature points
        theta_points = np.linspace(-4, 4, n_quadrature)
        
        # Prior (normal distribution)
        prior = np.exp(-0.5 * ((theta_points - prior_mean) / prior_sd) ** 2)
        prior /= prior.sum()
        
        # Likelihood at each quadrature point
        likelihood = np.ones(n_quadrature)
        for i, theta in enumerate(theta_points):
            for item, correct in responses:
                if model == "3PL":
                    p = IRTEngine.prob_3pl(theta, item.a, item.b, item.c)
                else:
                    p = IRTEngine.prob_2pl(theta, item.a, item.b)
                likelihood[i] *= p if correct else (1.0 - p)
        
        # Posterior
        posterior = likelihood * prior
        posterior /= posterior.sum()
        
        # EAP estimate
        eap = np.sum(theta_points * posterior)
        
        # Standard error
        var = np.sum((theta_points - eap) ** 2 * posterior)
        se = math.sqrt(var)
        
        return float(eap), float(se)

class AdaptiveSelector:
    """Advanced adaptive item selection with multiple strategies."""
    
    def __init__(
        self, 
        strategy: SelectionStrategy = SelectionStrategy.SYMPSON_HETTER,
        exposure_control: bool = True,
        content_balancing: bool = True
    ):
        self.strategy = strategy
        self.exposure_control = exposure_control
        self.content_balancing = content_balancing
        self.irt_engine = IRTEngine()
    
    def select_next_item(
        self,
        candidates: List[ItemParameters],
        ability: AbilityEstimate,
        administered: List[int],
        constraints: Optional[Dict[str, Any]] = None
    ) -> Optional[ItemParameters]:
        """Select next item based on strategy and constraints."""
        
        # Filter out already administered items
        available = [
            item for item in candidates 
            if item.question_id not in administered
        ]
        
        if not available:
            return None
        
        # Apply content constraints if specified
        if constraints and self.content_balancing:
            available = self._apply_content_constraints(available, constraints)
        
        # Select based on strategy
        if self.strategy == SelectionStrategy.MAXIMUM_INFORMATION:
            return self._select_max_information(available, ability.theta)
        elif self.strategy == SelectionStrategy.SYMPSON_HETTER:
            return self._select_sympson_hetter(available, ability.theta)
        elif self.strategy == SelectionStrategy.STRATIFIED:
            return self._select_stratified(available, ability.theta)
        elif self.strategy == SelectionStrategy.CONTENT_BALANCED:
            return self._select_content_balanced(available, ability.theta, constraints)
        elif self.strategy == SelectionStrategy.EXPOSURE_CONTROLLED:
            return self._select_exposure_controlled(available, ability.theta)
        else:
            return random.choice(available)
    
    def _select_max_information(
        self, 
        items: List[ItemParameters], 
        theta: float
    ) -> ItemParameters:
        """Select item with maximum Fisher information at current theta."""
        best_item = None
        max_info = -1
        
        for item in items:
            info = self.irt_engine.fisher_info_3pl(theta, item.a, item.b, item.c)
            if info > max_info:
                max_info = info
                best_item = item
        
        return best_item or items[0]
    
    def _select_sympson_hetter(
        self, 
        items: List[ItemParameters], 
        theta: float
    ) -> ItemParameters:
        """Sympson-Hetter method with probabilistic exposure control."""
        # Calculate information for all items
        scored = []
        for item in items:
            info = self.irt_engine.fisher_info_3pl(theta, item.a, item.b, item.c)
            scored.append((info, item))
        
        # Sort by information (descending)
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Probabilistic selection based on sh_p
        for _, item in scored:
            if random.random() <= max(0.0, min(1.0, item.sh_p)):
                return item
        
        # Fallback to highest information item
        return scored[0][1] if scored else items[0]
    
    def _select_stratified(
        self, 
        items: List[ItemParameters], 
        theta: float
    ) -> ItemParameters:
        """Stratified selection based on difficulty levels."""
        # Stratify items by difficulty
        strata = {
            'easy': [],
            'medium': [],
            'hard': []
        }
        
        for item in items:
            if item.b < -0.5:
                strata['easy'].append(item)
            elif item.b < 0.5:
                strata['medium'].append(item)
            else:
                strata['hard'].append(item)
        
        # Select stratum based on current ability
        if theta < -0.5:
            stratum = strata['easy'] or strata['medium'] or strata['hard']
        elif theta < 0.5:
            stratum = strata['medium'] or strata['easy'] or strata['hard']
        else:
            stratum = strata['hard'] or strata['medium'] or strata['easy']
        
        # Select best item from stratum
        if stratum:
            return self._select_max_information(stratum, theta)
        
        return items[0]
    
    def _select_content_balanced(
        self, 
        items: List[ItemParameters], 
        theta: float,
        constraints: Optional[Dict[str, Any]]
    ) -> ItemParameters:
        """Content-balanced selection considering blueprint coverage."""
        if not constraints or 'topic_targets' not in constraints:
            return self._select_max_information(items, theta)
        
        topic_targets = constraints['topic_targets']
        topic_counts = constraints.get('topic_counts', {})
        
        # Calculate coverage gaps
        gaps = {}
        for topic_id, target in topic_targets.items():
            current = topic_counts.get(topic_id, 0)
            gaps[topic_id] = max(0, target - current)
        
        # Prioritize items from underrepresented topics
        priority_items = [
            item for item in items
            if item.topic_id and gaps.get(item.topic_id, 0) > 0
        ]
        
        if priority_items:
            return self._select_max_information(priority_items, theta)
        
        return self._select_max_information(items, theta)
    
    def _select_exposure_controlled(
        self, 
        items: List[ItemParameters], 
        theta: float
    ) -> ItemParameters:
        """Selection with exposure control using progressive method."""
        # Calculate information for all items
        scored = []
        for item in items:
            info = self.irt_engine.fisher_info_3pl(theta, item.a, item.b, item.c)
            # Adjust by exposure rate
            exposure_factor = 1.0 / (1.0 + item.exposure_count / 100.0)
            adjusted_info = info * exposure_factor
            scored.append((adjusted_info, item))
        
        # Sort by adjusted information
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Select with some randomization
        n_consider = min(5, len(scored))
        weights = [1.0 / (i + 1) for i in range(n_consider)]
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        selected_idx = np.random.choice(n_consider, p=weights)
        return scored[selected_idx][1]
    
    def _apply_content_constraints(
        self, 
        items: List[ItemParameters],
        constraints: Dict[str, Any]
    ) -> List[ItemParameters]:
        """Apply content constraints to item pool."""
        filtered = items
        
        # Topic constraints
        if 'required_topics' in constraints:
            required = set(constraints['required_topics'])
            filtered = [
                item for item in filtered
                if item.topic_id in required
            ]
        
        # Difficulty constraints
        if 'min_difficulty' in constraints:
            min_b = constraints['min_difficulty']
            filtered = [item for item in filtered if item.b >= min_b]
        
        if 'max_difficulty' in constraints:
            max_b = constraints['max_difficulty']
            filtered = [item for item in filtered if item.b <= max_b]
        
        return filtered if filtered else items