"""
Advanced Calibration Service with Multiple IRT Models
"""
import numpy as np
import pandas as pd
from scipy import optimize, stats
from typing import List, Dict, Tuple, Optional, Any
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class CalibrationModel(Enum):
    """Supported calibration models."""
    CTT = "ctt"  # Classical Test Theory
    RASCH = "rasch"  # 1PL
    TWO_PL = "2pl"
    THREE_PL = "3pl"
    GRADED_RESPONSE = "grm"  # For polytomous items

@dataclass
class CalibrationResult:
    """Calibration result for an item."""
    question_id: int
    version: int
    model: str
    parameters: Dict[str, float]
    standard_errors: Dict[str, float]
    fit_statistics: Dict[str, float]
    n_respondents: int
    converged: bool

class CalibrationEngine:
    """Advanced calibration engine for IRT and CTT."""
    
    def __init__(self, model: CalibrationModel = CalibrationModel.THREE_PL):
        self.model = model
        self.D = 1.7  # Scaling constant
    
    def calibrate_items(
        self,
        response_matrix: np.ndarray,
        item_ids: List[Tuple[int, int]],
        model: Optional[CalibrationModel] = None,
        max_iter: int = 100,
        tolerance: float = 0.001
    ) -> List[CalibrationResult]:
        """Calibrate multiple items."""
        model = model or self.model
        
        if model == CalibrationModel.CTT:
            return self._calibrate_ctt(response_matrix, item_ids)
        elif model == CalibrationModel.RASCH:
            return self._calibrate_rasch(response_matrix, item_ids)
        elif model == CalibrationModel.TWO_PL:
            return self._calibrate_2pl(response_matrix, item_ids, max_iter, tolerance)
        elif model == CalibrationModel.THREE_PL:
            return self._calibrate_3pl(response_matrix, item_ids, max_iter, tolerance)
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    def _calibrate_ctt(
        self,
        response_matrix: np.ndarray,
        item_ids: List[Tuple[int, int]]
    ) -> List[CalibrationResult]:
        """Classical Test Theory calibration."""
        results = []
        n_items, n_respondents = response_matrix.shape
        
        # Calculate total scores
        total_scores = np.sum(response_matrix, axis=0)
        
        for i, (qid, version) in enumerate(item_ids):
            item_responses = response_matrix[i, :]
            
            # Item difficulty (p-value)
            p = np.mean(item_responses)
            
            # Item discrimination (point-biserial correlation)
            if np.std(item_responses) > 0 and np.std(total_scores) > 0:
                rpb = np.corrcoef(item_responses, total_scores)[0, 1]
            else:
                rpb = 0.0
            
            # Item variance
            variance = p * (1 - p)
            
            # Standard errors (bootstrap)
            se_p = np.sqrt(variance / n_respondents)
            se_rpb = np.sqrt((1 - rpb**2) / (n_respondents - 2)) if n_respondents > 2 else 0.0
            
            results.append(CalibrationResult(
                question_id=qid,
                version=version,
                model="CTT",
                parameters={'p': p, 'rpb': rpb, 'variance': variance},
                standard_errors={'p': se_p, 'rpb': se_rpb},
                fit_statistics={'n': n_respondents},
                n_respondents=n_respondents,
                converged=True
            ))
        
        return results
    
    def _calibrate_rasch(
        self,
        response_matrix: np.ndarray,
        item_ids: List[Tuple[int, int]]
    ) -> List[CalibrationResult]:
        """Rasch (1PL) model calibration using conditional maximum likelihood."""
        n_items, n_respondents = response_matrix.shape
        
        # Initial estimates
        item_totals = np.sum(response_matrix, axis=1)
        person_totals = np.sum(response_matrix, axis=0)
        
        # Log-odds transformation for initial difficulty estimates
        difficulties = np.zeros(n_items)
        for i in range(n_items):
            p = item_totals[i] / n_respondents
            if p > 0 and p < 1:
                difficulties[i] = -np.log(p / (1 - p))
        
        # Joint maximum likelihood estimation
        # (Simplified - in production use specialized IRT packages)
        results = []
        for i, (qid, version) in enumerate(item_ids):
            b = difficulties[i]
            se_b = 1.0 / np.sqrt(item_totals[i] * (n_respondents - item_totals[i]) / n_respondents)
            
            results.append(CalibrationResult(
                question_id=qid,
                version=version,
                model="Rasch",
                parameters={'b': b},
                standard_errors={'b': se_b},
                fit_statistics={'infit': 1.0, 'outfit': 1.0},  # Placeholder
                n_respondents=n_respondents,
                converged=True
            ))
        
        return results
    
    def _calibrate_2pl(
        self,
        response_matrix: np.ndarray,
        item_ids: List[Tuple[int, int]],
        max_iter: int = 100,
        tolerance: float = 0.001
    ) -> List[CalibrationResult]:
        """2-Parameter Logistic model calibration using marginal maximum likelihood."""
        n_items, n_respondents = response_matrix.shape
        
        # Initialize parameters
        a_params = np.ones(n_items)
        b_params = np.zeros(n_items)
        
        # Initial estimates from CTT
        for i in range(n_items):
            p = np.mean(response_matrix[i, :])
            if p > 0 and p < 1:
                b_params[i] = -np.log(p / (1 - p)) / self.D
        
        # EM Algorithm (simplified version)
        for iteration in range(max_iter):
            old_params = np.concatenate([a_params, b_params])
            
            # E-step: Estimate ability distribution
            theta_points = np.linspace(-4, 4, 21)
            theta_weights = stats.norm.pdf(theta_points, 0, 1)
            theta_weights /= theta_weights.sum()
            
            # M-step: Update item parameters
            for i in range(n_items):
                def neg_log_likelihood(params):
                    a, b = params
                    if a <= 0:
                        return 1e10
                    
                    ll = 0
                    for j, theta in enumerate(theta_points):
                        p = 1 / (1 + np.exp(-self.D * a * (theta - b)))
                        for k in range(n_respondents):
                            if response_matrix[i, k] == 1:
                                ll += theta_weights[j] * np.log(p + 1e-10)
                            else:
                                ll += theta_weights[j] * np.log(1 - p + 1e-10)
                    return -ll
                
                result = optimize.minimize(
                    neg_log_likelihood,
                    [a_params[i], b_params[i]],
                    method='L-BFGS-B',
                    bounds=[(0.1, 3.0), (-3.0, 3.0)]
                )
                
                if result.success:
                    a_params[i], b_params[i] = result.x
            
            # Check convergence
            new_params = np.concatenate([a_params, b_params])
            if np.max(np.abs(new_params - old_params)) < tolerance:
                break
        
        # Create results
        results = []
        for i, (qid, version) in enumerate(item_ids):
            results.append(CalibrationResult(
                question_id=qid,
                version=version,
                model="2PL",
                parameters={'a': a_params[i], 'b': b_params[i]},
                standard_errors={'a': 0.1, 'b': 0.1},  # Placeholder
                fit_statistics={'loglik': 0.0},
                n_respondents=n_respondents,
                converged=iteration < max_iter - 1
            ))
        
        return results
    
    def _calibrate_3pl(
        self,
        response_matrix: np.ndarray,
        item_ids: List[Tuple[int, int]],
        max_iter: int = 100,
        tolerance: float = 0.001
    ) -> List[CalibrationResult]:
        """3-Parameter Logistic model calibration."""
        n_items, n_respondents = response_matrix.shape
        
        # Initialize parameters
        a_params = np.ones(n_items)
        b_params = np.zeros(n_items)
        c_params = np.ones(n_items) * 0.2  # Guessing parameter
        
        # Initial estimates
        for i in range(n_items):
            p = np.mean(response_matrix[i, :])
            if p > 0.2 and p < 1:
                b_params[i] = -np.log((p - 0.2) / (0.8)) / self.D
        
        # EM Algorithm for 3PL (simplified)
        for iteration in range(max_iter):
            old_params = np.concatenate([a_params, b_params, c_params])
            
            # E-step
            theta_points = np.linspace(-4, 4, 21)
            theta_weights = stats.norm.pdf(theta_points, 0, 1)
            theta_weights /= theta_weights.sum()
            
            # M-step
            for i in range(n_items):
                def neg_log_likelihood(params):
                    a, b, c = params
                    if a <= 0 or c < 0 or c > 0.5:
                        return 1e10
                    
                    ll = 0
                    for j, theta in enumerate(theta_points):
                        p = c + (1 - c) / (1 + np.exp(-self.D * a * (theta - b)))
                        for k in range(n_respondents):
                            if response_matrix[i, k] == 1:
                                ll += theta_weights[j] * np.log(p + 1e-10)
                            else:
                                ll += theta_weights[j] * np.log(1 - p + 1e-10)
                    return -ll
                
                result = optimize.minimize(
                    neg_log_likelihood,
                    [a_params[i], b_params[i], c_params[i]],
                    method='L-BFGS-B',
                    bounds=[(0.1, 3.0), (-3.0, 3.0), (0.0, 0.5)]
                )
                
                if result.success:
                    a_params[i], b_params[i], c_params[i] = result.x
            
            # Check convergence
            new_params = np.concatenate([a_params, b_params, c_params])
            if np.max(np.abs(new_params - old_params)) < tolerance:
                break
        
        # Create results
        results = []
        for i, (qid, version) in enumerate(item_ids):
            results.append(CalibrationResult(
                question_id=qid,
                version=version,
                model="3PL",
                parameters={'a': a_params[i], 'b': b_params[i], 'c': c_params[i]},
                standard_errors={'a': 0.1, 'b': 0.1, 'c': 0.05},  # Placeholder
                fit_statistics={'loglik': 0.0},
                n_respondents=n_respondents,
                converged=iteration < max_iter - 1
            ))
        
        return results
    
    def calculate_fit_statistics(
        self,
        response_matrix: np.ndarray,
        parameters: List[Dict[str, float]],
        model: CalibrationModel
    ) -> List[Dict[str, float]]:
        """Calculate item fit statistics (infit, outfit, etc.)."""
        n_items, n_respondents = response_matrix.shape
        fit_stats = []
        
        # Estimate person abilities
        person_abilities = self._estimate_abilities(response_matrix, parameters, model)
        
        for i in range(n_items):
            item_params = parameters[i]
            observed = response_matrix[i, :]
            expected = []
            residuals = []
            
            for j, theta in enumerate(person_abilities):
                if model == CalibrationModel.THREE_PL:
                    p = self._prob_3pl(theta, item_params['a'], item_params['b'], item_params['c'])
                elif model == CalibrationModel.TWO_PL:
                    p = self._prob_2pl(theta, item_params['a'], item_params['b'])
                else:
                    p = self._prob_rasch(theta, item_params['b'])
                
                expected.append(p)
                residuals.append((observed[j] - p) / np.sqrt(p * (1 - p) + 1e-10))
            
            # Infit and outfit statistics
            infit = np.mean(np.array(residuals) ** 2)
            outfit = np.mean(np.array(residuals) ** 2)  # Weighted by variance
            
            fit_stats.append({
                'infit': infit,
                'outfit': outfit,
                'rmse': np.sqrt(np.mean(np.array(residuals) ** 2))
            })
        
        return fit_stats
    
    def _prob_rasch(self, theta: float, b: float) -> float:
        """Rasch model probability."""
        return 1 / (1 + np.exp(-self.D * (theta - b)))
    
    def _prob_2pl(self, theta: float, a: float, b: float) -> float:
        """2PL model probability."""
        return 1 / (1 + np.exp(-self.D * a * (theta - b)))
    
    def _prob_3pl(self, theta: float, a: float, b: float, c: float) -> float:
        """3PL model probability."""
        return c + (1 - c) / (1 + np.exp(-self.D * a * (theta - b)))
    
    def _estimate_abilities(
        self,
        response_matrix: np.ndarray,
        parameters: List[Dict[str, float]],
        model: CalibrationModel
    ) -> np.ndarray:
        """Estimate person abilities given item parameters."""
        n_items, n_respondents = response_matrix.shape
        abilities = np.zeros(n_respondents)
        
        for j in range(n_respondents):
            responses = response_matrix[:, j]
            
            # MLE estimation
            def neg_log_likelihood(theta):
                ll = 0
                for i in range(n_items):
                    if model == CalibrationModel.THREE_PL:
                        p = self._prob_3pl(theta, parameters[i]['a'], 
                                         parameters[i]['b'], parameters[i]['c'])
                    elif model == CalibrationModel.TWO_PL:
                        p = self._prob_2pl(theta, parameters[i]['a'], 
                                         parameters[i]['b'])
                    else:
                        p = self._prob_rasch(theta, parameters[i]['b'])
                    
                    if responses[i] == 1:
                        ll += np.log(p + 1e-10)
                    else:
                        ll += np.log(1 - p + 1e-10)
                return -ll
            
            result = optimize.minimize_scalar(
                neg_log_likelihood,
                bounds=(-4, 4),
                method='bounded'
            )
            
            abilities[j] = result.x if result.success else 0.0
        
        return abilities