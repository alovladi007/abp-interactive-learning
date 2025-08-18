"""
IRT Adaptive Testing Engine
Implements 3-Parameter Logistic Model with Maximum Fisher Information selection
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from scipy import optimize
from scipy.stats import norm
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AdaptiveTestingEngine:
    """
    Implements IRT-based adaptive testing with 3PL model
    """
    
    def __init__(self, model_type: str = "3PL"):
        self.model_type = model_type
        self.D = 1.702  # Scaling constant for normal ogive approximation
        
    def probability_correct(self, theta: float, a: float, b: float, c: float = 0) -> float:
        """
        Calculate probability of correct response using 3PL model
        P(θ) = c + (1-c) / (1 + exp(-D*a*(θ-b)))
        
        Args:
            theta: Ability parameter
            a: Discrimination parameter
            b: Difficulty parameter
            c: Pseudo-guessing parameter
        """
        if self.model_type == "1PL":
            a = 1.0
            c = 0.0
        elif self.model_type == "2PL":
            c = 0.0
            
        exp_term = np.exp(-self.D * a * (theta - b))
        probability = c + (1 - c) / (1 + exp_term)
        return probability
    
    def fisher_information(self, theta: float, a: float, b: float, c: float = 0) -> float:
        """
        Calculate Fisher Information for an item
        I(θ) = D²a²[(P-c)²/(1-c)²] * [(1-P)/P]
        """
        P = self.probability_correct(theta, a, b, c)
        
        if P <= c or P >= 1.0:
            return 0.0
        
        numerator = (self.D ** 2) * (a ** 2) * ((P - c) ** 2)
        denominator = ((1 - c) ** 2) * P * (1 - P)
        
        information = numerator / denominator
        return information
    
    def estimate_ability_ml(self, responses: List[Dict], 
                           initial_theta: float = 0.0) -> Tuple[float, float]:
        """
        Maximum Likelihood estimation of ability
        
        Args:
            responses: List of response dictionaries with keys:
                       'a', 'b', 'c', 'response' (0 or 1)
            initial_theta: Starting point for optimization
        
        Returns:
            Tuple of (ability_estimate, standard_error)
        """
        if not responses:
            return initial_theta, 1.0
        
        def neg_log_likelihood(theta):
            ll = 0
            for resp in responses:
                p = self.probability_correct(theta, resp['a'], resp['b'], resp.get('c', 0))
                if resp['response'] == 1:
                    ll += np.log(max(p, 1e-10))
                else:
                    ll += np.log(max(1 - p, 1e-10))
            return -ll
        
        # Optimize
        result = optimize.minimize_scalar(
            neg_log_likelihood,
            bounds=(-4, 4),
            method='bounded'
        )
        
        theta_est = result.x
        
        # Calculate standard error using Fisher Information
        total_info = sum(
            self.fisher_information(theta_est, r['a'], r['b'], r.get('c', 0))
            for r in responses
        )
        
        se = 1.0 / np.sqrt(max(total_info, 0.01))
        
        return theta_est, se
    
    def estimate_ability_eap(self, responses: List[Dict], 
                            prior_mean: float = 0.0,
                            prior_sd: float = 1.0) -> Tuple[float, float]:
        """
        Expected A Posteriori (EAP) estimation of ability
        More robust than ML for small sample sizes
        """
        if not responses:
            return prior_mean, prior_sd
        
        # Quadrature points and weights for numerical integration
        n_quad = 40
        theta_points = np.linspace(-4, 4, n_quad)
        
        # Prior distribution (normal)
        prior = norm.pdf(theta_points, prior_mean, prior_sd)
        
        # Likelihood
        likelihood = np.ones(n_quad)
        for resp in responses:
            for i, theta in enumerate(theta_points):
                p = self.probability_correct(theta, resp['a'], resp['b'], resp.get('c', 0))
                if resp['response'] == 1:
                    likelihood[i] *= p
                else:
                    likelihood[i] *= (1 - p)
        
        # Posterior
        posterior = prior * likelihood
        posterior = posterior / np.sum(posterior)
        
        # EAP estimate
        theta_eap = np.sum(theta_points * posterior)
        
        # Posterior standard deviation
        variance = np.sum((theta_points - theta_eap) ** 2 * posterior)
        se = np.sqrt(variance)
        
        return theta_eap, se
    
    def select_next_item(self, available_items: List[Dict], 
                        theta: float,
                        administered_items: List[int] = None,
                        content_constraints: Dict = None) -> Optional[Dict]:
        """
        Select next item using Maximum Fisher Information criterion
        
        Args:
            available_items: List of item dictionaries
            theta: Current ability estimate
            administered_items: List of already administered item IDs
            content_constraints: Dictionary of content balancing requirements
        
        Returns:
            Selected item dictionary or None
        """
        if not available_items:
            return None
        
        administered_items = administered_items or []
        
        # Filter out already administered items
        candidates = [
            item for item in available_items 
            if item['id'] not in administered_items
        ]
        
        if not candidates:
            return None
        
        # Apply content constraints if specified
        if content_constraints:
            candidates = self._apply_content_constraints(
                candidates, administered_items, content_constraints
            )
        
        # Calculate information for each candidate
        item_info = []
        for item in candidates:
            info = self.fisher_information(
                theta, 
                item['discrimination'],
                item['difficulty'],
                item.get('guessing', 0)
            )
            
            # Apply exposure control factor
            exposure_factor = item.get('selection_probability', 1.0)
            adjusted_info = info * exposure_factor
            
            item_info.append((item, adjusted_info))
        
        # Sort by information (descending)
        item_info.sort(key=lambda x: x[1], reverse=True)
        
        # Randomize among top candidates to reduce item exposure
        n_top = min(5, len(item_info))
        top_items = item_info[:n_top]
        
        if top_items:
            # Weighted random selection based on information
            weights = [info for _, info in top_items]
            total_weight = sum(weights)
            
            if total_weight > 0:
                probabilities = [w / total_weight for w in weights]
                selected_idx = np.random.choice(n_top, p=probabilities)
                return top_items[selected_idx][0]
        
        return candidates[0] if candidates else None
    
    def _apply_content_constraints(self, candidates: List[Dict],
                                  administered_items: List[int],
                                  constraints: Dict) -> List[Dict]:
        """Apply content balancing constraints"""
        # This would implement content specification rules
        # For now, return all candidates
        return candidates
    
    def calculate_stopping_criterion(self, se: float, 
                                    n_items: int,
                                    se_threshold: float = 0.3,
                                    min_items: int = 10,
                                    max_items: int = 50) -> bool:
        """
        Determine if testing should stop
        
        Args:
            se: Current standard error of ability estimate
            n_items: Number of items administered
            se_threshold: Standard error threshold for stopping
            min_items: Minimum number of items required
            max_items: Maximum number of items allowed
        
        Returns:
            True if testing should stop
        """
        if n_items >= max_items:
            return True
        
        if n_items < min_items:
            return False
        
        return se <= se_threshold
    
    def simulate_cat(self, true_theta: float, 
                     item_pool: List[Dict],
                     max_items: int = 30) -> Dict:
        """
        Simulate a complete CAT session
        
        Args:
            true_theta: True ability level (for simulation)
            item_pool: Available item pool
            max_items: Maximum number of items
        
        Returns:
            Dictionary with simulation results
        """
        responses = []
        administered = []
        theta_history = [0.0]  # Start with prior mean
        se_history = [1.0]
        
        current_theta = 0.0
        current_se = 1.0
        
        for i in range(max_items):
            # Select next item
            next_item = self.select_next_item(
                item_pool, current_theta, administered
            )
            
            if not next_item:
                break
            
            # Simulate response
            p_correct = self.probability_correct(
                true_theta,
                next_item['discrimination'],
                next_item['difficulty'],
                next_item.get('guessing', 0)
            )
            
            response = 1 if np.random.random() < p_correct else 0
            
            # Record response
            responses.append({
                'a': next_item['discrimination'],
                'b': next_item['difficulty'],
                'c': next_item.get('guessing', 0),
                'response': response,
                'item_id': next_item['id']
            })
            
            administered.append(next_item['id'])
            
            # Update ability estimate
            current_theta, current_se = self.estimate_ability_eap(responses)
            theta_history.append(current_theta)
            se_history.append(current_se)
            
            # Check stopping criterion
            if self.calculate_stopping_criterion(current_se, len(responses)):
                break
        
        return {
            'final_theta': current_theta,
            'final_se': current_se,
            'n_items': len(responses),
            'responses': responses,
            'theta_history': theta_history,
            'se_history': se_history,
            'convergence': abs(current_theta - true_theta) < 0.5
        }
    
    def calculate_test_information(self, items: List[Dict], theta: float) -> float:
        """Calculate total test information at a given ability level"""
        total_info = sum(
            self.fisher_information(
                theta,
                item['discrimination'],
                item['difficulty'],
                item.get('guessing', 0)
            )
            for item in items
        )
        return total_info
    
    def get_ability_confidence_interval(self, theta: float, se: float, 
                                       confidence: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for ability estimate"""
        z_score = norm.ppf((1 + confidence) / 2)
        lower = theta - z_score * se
        upper = theta + z_score * se
        return (lower, upper)