import numpy as np
from scipy import optimize
from scipy.stats import norm
from typing import List, Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class IRTEngine:
    """Complete IRT Engine with 1PL, 2PL, 3PL, and 4PL models"""
    
    def __init__(self, model: str = "3PL"):
        self.model = model
        self.valid_models = ["1PL", "2PL", "3PL", "4PL"]
        if model not in self.valid_models:
            raise ValueError(f"Model must be one of {self.valid_models}")
    
    def probability(self, theta: float, a: float = 1.0, b: float = 0.0, 
                   c: float = 0.0, d: float = 1.0) -> float:
        """Calculate probability of correct response"""
        if self.model == "1PL":  # Rasch model
            return 1 / (1 + np.exp(-(theta - b)))
        elif self.model == "2PL":
            return 1 / (1 + np.exp(-a * (theta - b)))
        elif self.model == "3PL":
            return c + (1 - c) / (1 + np.exp(-a * (theta - b)))
        elif self.model == "4PL":
            return c + (d - c) / (1 + np.exp(-a * (theta - b)))
        else:
            raise ValueError(f"Unknown model: {self.model}")
    
    def information(self, theta: float, a: float = 1.0, b: float = 0.0, 
                    c: float = 0.0, d: float = 1.0) -> float:
        """Calculate Fisher information at theta"""
        p = self.probability(theta, a, b, c, d)
        
        if self.model == "1PL":
            return p * (1 - p)
        elif self.model == "2PL":
            return a**2 * p * (1 - p)
        elif self.model == "3PL":
            q = 1 - p
            return (a**2 * q * (p - c)**2) / (p * (1 - c)**2) if p > 0 else 0
        elif self.model == "4PL":
            q = 1 - p
            numerator = a**2 * (d - c)**2 * q * p
            denominator = (c + (d - c) * p)**2
            return numerator / denominator if denominator > 0 else 0
    
    def likelihood(self, theta: float, responses: List[Dict]) -> float:
        """Calculate likelihood of response pattern"""
        likelihood = 1.0
        for resp in responses:
            p = self.probability(theta, resp['a'], resp['b'], resp.get('c', 0), resp.get('d', 1))
            if resp['correct']:
                likelihood *= p
            else:
                likelihood *= (1 - p)
        return likelihood
    
    def log_likelihood(self, theta: float, responses: List[Dict]) -> float:
        """Calculate log-likelihood (more numerically stable)"""
        ll = 0.0
        for resp in responses:
            p = self.probability(theta, resp['a'], resp['b'], resp.get('c', 0), resp.get('d', 1))
            if resp['correct']:
                ll += np.log(max(p, 1e-10))
            else:
                ll += np.log(max(1 - p, 1e-10))
        return ll
    
    def estimate_theta_mle(self, responses: List[Dict], 
                          initial_theta: float = 0.0) -> Tuple[float, float]:
        """Maximum Likelihood Estimation of theta"""
        if not responses:
            return 0.0, 1.0
        
        # Objective function (negative log-likelihood)
        def neg_log_likelihood(theta):
            return -self.log_likelihood(theta, responses)
        
        # Optimize
        result = optimize.minimize_scalar(
            neg_log_likelihood,
            bounds=(-4, 4),
            method='bounded'
        )
        
        theta_est = result.x
        
        # Calculate standard error using Fisher information
        total_info = sum(
            self.information(theta_est, r['a'], r['b'], r.get('c', 0), r.get('d', 1))
            for r in responses
        )
        se = 1 / np.sqrt(max(total_info, 0.1))
        
        return theta_est, se
    
    def estimate_theta_eap(self, responses: List[Dict], 
                          prior_mean: float = 0.0,
                          prior_sd: float = 1.0,
                          n_quadrature: int = 40) -> Tuple[float, float]:
        """Expected A Posteriori (Bayesian) estimation of theta"""
        if not responses:
            return prior_mean, prior_sd
        
        # Quadrature points and weights
        theta_points = np.linspace(-4, 4, n_quadrature)
        
        # Prior probabilities (normal distribution)
        prior_probs = norm.pdf(theta_points, prior_mean, prior_sd)
        prior_probs /= prior_probs.sum()
        
        # Likelihood at each quadrature point
        likelihoods = np.array([
            self.likelihood(theta, responses) for theta in theta_points
        ])
        
        # Posterior probabilities
        posterior = likelihoods * prior_probs
        posterior /= posterior.sum()
        
        # EAP estimate (expected value)
        theta_eap = np.sum(theta_points * posterior)
        
        # Posterior standard deviation
        variance = np.sum((theta_points - theta_eap)**2 * posterior)
        se_eap = np.sqrt(variance)
        
        return theta_eap, se_eap
    
    def estimate_theta_map(self, responses: List[Dict],
                          prior_mean: float = 0.0,
                          prior_sd: float = 1.0) -> Tuple[float, float]:
        """Maximum A Posteriori estimation of theta"""
        if not responses:
            return prior_mean, prior_sd
        
        # Objective function (negative log posterior)
        def neg_log_posterior(theta):
            log_prior = norm.logpdf(theta, prior_mean, prior_sd)
            log_likelihood = self.log_likelihood(theta, responses)
            return -(log_prior + log_likelihood)
        
        # Optimize
        result = optimize.minimize_scalar(
            neg_log_posterior,
            bounds=(-4, 4),
            method='bounded'
        )
        
        theta_map = result.x
        
        # Calculate standard error
        total_info = sum(
            self.information(theta_map, r['a'], r['b'], r.get('c', 0), r.get('d', 1))
            for r in responses
        )
        # Add prior information
        prior_info = 1 / (prior_sd**2)
        total_info += prior_info
        
        se = 1 / np.sqrt(max(total_info, 0.1))
        
        return theta_map, se
    
    def calibrate_items(self, response_matrix: np.ndarray,
                       method: str = "marginal_mle") -> Dict:
        """Calibrate item parameters from response data
        
        Args:
            response_matrix: N x M matrix (N examinees, M items)
            method: Calibration method
        
        Returns:
            Dictionary with item parameters
        """
        n_examinees, n_items = response_matrix.shape
        
        # Initialize parameters
        item_params = {
            'a': np.ones(n_items),
            'b': np.zeros(n_items),
            'c': np.ones(n_items) * 0.2 if self.model in ["3PL", "4PL"] else np.zeros(n_items),
            'd': np.ones(n_items) if self.model == "4PL" else np.ones(n_items)
        }
        
        # Simple calibration using item difficulty (p-values)
        for j in range(n_items):
            # Remove missing responses
            item_responses = response_matrix[:, j]
            valid_responses = item_responses[~np.isnan(item_responses)]
            
            if len(valid_responses) > 0:
                # P-value (proportion correct)
                p_value = np.mean(valid_responses)
                
                # Convert to difficulty parameter (b)
                # Using inverse normal approximation
                if 0.01 < p_value < 0.99:
                    item_params['b'][j] = -norm.ppf(p_value)
                else:
                    item_params['b'][j] = 0
                
                # Discrimination (point-biserial correlation)
                if len(valid_responses) > 1:
                    total_scores = np.nanmean(response_matrix, axis=1)
                    valid_total = total_scores[~np.isnan(item_responses)]
                    
                    if np.std(valid_total) > 0 and np.std(valid_responses) > 0:
                        correlation = np.corrcoef(valid_responses, valid_total)[0, 1]
                        item_params['a'][j] = max(0.1, min(3.0, 1.7 * correlation))
        
        return item_params
    
    def test_information_function(self, items: List[Dict], 
                                  theta_range: Tuple[float, float] = (-4, 4),
                                  n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate Test Information Function"""
        theta_points = np.linspace(theta_range[0], theta_range[1], n_points)
        tif = np.zeros(n_points)
        
        for i, theta in enumerate(theta_points):
            for item in items:
                tif[i] += self.information(
                    theta, 
                    item.get('a', 1.0),
                    item.get('b', 0.0),
                    item.get('c', 0.0),
                    item.get('d', 1.0)
                )
        
        return theta_points, tif
    
    def adaptive_select(self, theta: float, available_items: List[Dict],
                       method: str = "max_info",
                       exposure_control: Optional[Dict] = None) -> Optional[Dict]:
        """Select next item for adaptive testing
        
        Args:
            theta: Current ability estimate
            available_items: List of available items
            method: Selection method ('max_info', 'random', 'stratified')
            exposure_control: Exposure control parameters
        
        Returns:
            Selected item or None
        """
        if not available_items:
            return None
        
        if method == "random":
            return np.random.choice(available_items)
        
        # Calculate information for each item
        item_infos = []
        for item in available_items:
            info = self.information(
                theta,
                item.get('a', 1.0),
                item.get('b', 0.0),
                item.get('c', 0.0),
                item.get('d', 1.0)
            )
            
            # Apply exposure control if provided
            if exposure_control and item['id'] in exposure_control:
                k_value = exposure_control[item['id']].get('k', 1.0)
                info *= k_value
            
            item_infos.append((item, info))
        
        if method == "max_info":
            # Sort by information and select from top candidates
            item_infos.sort(key=lambda x: x[1], reverse=True)
            
            # Randomize among top 5 to avoid always selecting same item
            n_candidates = min(5, len(item_infos))
            candidates = item_infos[:n_candidates]
            
            if candidates:
                # Weighted random selection based on information
                weights = [info for _, info in candidates]
                weights = np.array(weights) / sum(weights)
                idx = np.random.choice(n_candidates, p=weights)
                return candidates[idx][0]
        
        elif method == "stratified":
            # Stratified selection based on difficulty
            target_b = theta  # Target difficulty near current ability
            
            # Calculate distance from target
            distances = []
            for item, info in item_infos:
                dist = abs(item.get('b', 0.0) - target_b)
                distances.append((item, info, dist))
            
            # Sort by distance and select from closest items
            distances.sort(key=lambda x: x[2])
            n_candidates = min(5, len(distances))
            
            if n_candidates > 0:
                return distances[np.random.choice(n_candidates)][0]
        
        return available_items[0] if available_items else None

class SympsonHetterControl:
    """Sympson-Hetter Exposure Control Algorithm"""
    
    def __init__(self, target_exposure: float = 0.2, alpha: float = 0.05):
        self.target_exposure = target_exposure
        self.alpha = alpha  # Learning rate
        self.k_values = {}  # Control parameters for each item
        self.exposure_counts = {}
        self.administration_counts = {}
    
    def initialize_items(self, item_ids: List[str]):
        """Initialize control parameters for items"""
        for item_id in item_ids:
            self.k_values[item_id] = 1.0  # Start with no control
            self.exposure_counts[item_id] = 0
            self.administration_counts[item_id] = 0
    
    def should_administer(self, item_id: str) -> bool:
        """Determine if item should be administered"""
        if item_id not in self.k_values:
            return True
        
        # Probabilistic administration based on k value
        return np.random.random() < self.k_values[item_id]
    
    def update_exposure(self, item_id: str, was_administered: bool):
        """Update exposure statistics"""
        if item_id not in self.exposure_counts:
            self.initialize_items([item_id])
        
        self.exposure_counts[item_id] += 1
        if was_administered:
            self.administration_counts[item_id] += 1
    
    def update_k_values(self):
        """Update control parameters based on exposure rates"""
        for item_id in self.k_values:
            if self.exposure_counts[item_id] > 0:
                # Current exposure rate
                current_rate = (self.administration_counts[item_id] / 
                              self.exposure_counts[item_id])
                
                # Update k value to move toward target
                if current_rate > self.target_exposure:
                    # Reduce k to decrease exposure
                    self.k_values[item_id] *= (1 - self.alpha)
                else:
                    # Increase k to increase exposure
                    self.k_values[item_id] = min(1.0, 
                        self.k_values[item_id] * (1 + self.alpha))
                
                # Ensure k stays in valid range
                self.k_values[item_id] = max(0.01, min(1.0, self.k_values[item_id]))
    
    def get_exposure_rates(self) -> Dict[str, float]:
        """Get current exposure rates for all items"""
        rates = {}
        for item_id in self.exposure_counts:
            if self.exposure_counts[item_id] > 0:
                rates[item_id] = (self.administration_counts[item_id] / 
                                 self.exposure_counts[item_id])
            else:
                rates[item_id] = 0.0
        return rates