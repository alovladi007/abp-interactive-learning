"""
Enhanced Sympson-Hetter Iterative Calibration
"""
import numpy as np
import psycopg2
from typing import Dict, List, Tuple, Optional, Any
import json
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ExposureControlParams:
    """Parameters for Sympson-Hetter exposure control."""
    tau: float = 0.2  # Target exposure rate
    n_simulees: int = 1000  # Number of simulated examinees
    test_length: int = 30  # Test length
    iterations: int = 10  # Number of iterations
    alpha: float = 0.8  # Learning rate
    theta_dist: str = "normal(0,1)"  # Ability distribution
    floor: float = 0.01  # Minimum exposure probability
    ceiling: float = 1.0  # Maximum exposure probability
    topic_tau: Optional[Dict[str, float]] = None  # Topic-specific targets
    topic_weights: Optional[Dict[str, float]] = None  # Topic weights

class SympsonHetterCalibrator:
    """Enhanced Sympson-Hetter exposure control calibrator."""
    
    def __init__(self, params: ExposureControlParams):
        self.params = params
        self.D = 1.7
    
    def calibrate(
        self,
        pool: List[Dict[str, Any]],
        seed: Optional[int] = None
    ) -> Tuple[Dict[Tuple[int, int], float], List[Dict], List[Dict]]:
        """
        Run iterative Sympson-Hetter calibration.
        
        Returns:
            - k_map: Dictionary of (question_id, version) -> sh_p values
            - exposure_history: List of exposure statistics per iteration
            - convergence_history: List of convergence metrics
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Initialize k values
        k_map = {
            (item["question_id"], item["version"]): item.get("sh_p", 1.0)
            for item in pool
        }
        
        exposure_history = []
        convergence_history = []
        
        # Compute topic-specific targets
        topic_tau = self._compute_topic_tau()
        
        for iteration in range(self.params.iterations):
            logger.info(f"Iteration {iteration + 1}/{self.params.iterations}")
            
            # Update pool with current k values
            for item in pool:
                key = (item["question_id"], item["version"])
                item["sh_p"] = k_map[key]
            
            # Simulate test administrations
            exposures = self._simulate_administrations(pool)
            
            # Calculate exposure rates
            rates = {
                key: count / self.params.n_simulees
                for key, count in exposures.items()
            }
            
            # Update k values
            new_k_map = self._update_k_values(
                pool, k_map, rates, topic_tau
            )
            
            # Calculate statistics
            stats = self._calculate_statistics(rates, topic_tau, pool)
            exposure_history.append(stats)
            
            # Check convergence
            convergence = self._check_convergence(k_map, new_k_map, rates)
            convergence_history.append(convergence)
            
            k_map = new_k_map
            
            # Early stopping if converged
            if convergence["converged"]:
                logger.info(f"Converged at iteration {iteration + 1}")
                break
        
        return k_map, exposure_history, convergence_history
    
    def _compute_topic_tau(self) -> Dict[str, float]:
        """Compute topic-specific exposure targets."""
        if self.params.topic_tau:
            return self.params.topic_tau
        
        if self.params.topic_weights:
            total_weight = sum(self.params.topic_weights.values())
            return {
                topic: self.params.tau * (weight / total_weight)
                for topic, weight in self.params.topic_weights.items()
            }
        
        return {}
    
    def _simulate_administrations(
        self,
        pool: List[Dict[str, Any]]
    ) -> Dict[Tuple[int, int], int]:
        """Simulate test administrations for exposure calculation."""
        exposures = {
            (item["question_id"], item["version"]): 0
            for item in pool
        }
        
        for _ in range(self.params.n_simulees):
            # Sample ability
            theta = self._sample_theta()
            
            # Administer test
            administered = set()
            
            for _ in range(min(self.params.test_length, len(pool))):
                # Get available items
                available = [
                    item for item in pool
                    if (item["question_id"], item["version"]) not in administered
                ]
                
                if not available:
                    break
                
                # Select item using Sympson-Hetter
                selected = self._select_item_sh(available, theta)
                
                if selected:
                    key = (selected["question_id"], selected["version"])
                    administered.add(key)
                    exposures[key] += 1
        
        return exposures
    
    def _sample_theta(self) -> float:
        """Sample ability from specified distribution."""
        dist = self.params.theta_dist
        
        if dist.startswith("normal"):
            # Parse normal(mean, std)
            params = dist.replace("normal", "").strip("()")
            if params:
                mean, std = map(float, params.split(","))
            else:
                mean, std = 0.0, 1.0
            return np.random.normal(mean, std)
        
        elif dist.startswith("uniform"):
            # Parse uniform(min, max)
            params = dist.replace("uniform", "").strip("()")
            if params:
                min_val, max_val = map(float, params.split(","))
            else:
                min_val, max_val = -3.0, 3.0
            return np.random.uniform(min_val, max_val)
        
        else:
            return 0.0
    
    def _select_item_sh(
        self,
        available: List[Dict[str, Any]],
        theta: float
    ) -> Optional[Dict[str, Any]]:
        """Select item using Sympson-Hetter method."""
        # Calculate information for each item
        scored = []
        for item in available:
            info = self._fisher_info_3pl(
                theta,
                item.get("a", 1.0),
                item.get("b", 0.0),
                item.get("c", 0.2)
            )
            scored.append((info, item))
        
        # Sort by information (descending)
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # Probabilistic selection
        for _, item in scored:
            sh_p = item.get("sh_p", 1.0)
            if np.random.random() <= sh_p:
                return item
        
        # Fallback to highest information
        return scored[0][1] if scored else None
    
    def _fisher_info_3pl(
        self,
        theta: float,
        a: float,
        b: float,
        c: float
    ) -> float:
        """Calculate Fisher information for 3PL model."""
        p = c + (1 - c) / (1 + np.exp(-self.D * a * (theta - b)))
        q = 1 - p
        
        if p <= 0 or q <= 0 or (1 - c) <= 0:
            return 0.0
        
        return (self.D ** 2) * (a ** 2) * (q / p) * ((p - c) / (1 - c)) ** 2
    
    def _update_k_values(
        self,
        pool: List[Dict[str, Any]],
        k_map: Dict[Tuple[int, int], float],
        rates: Dict[Tuple[int, int], float],
        topic_tau: Dict[str, float]
    ) -> Dict[Tuple[int, int], float]:
        """Update k values based on exposure rates."""
        new_k_map = {}
        
        for item in pool:
            key = (item["question_id"], item["version"])
            current_k = k_map[key]
            actual_rate = rates.get(key, 0.0)
            
            # Get target rate (topic-specific or global)
            if topic_tau and item.get("topic_id"):
                target_rate = topic_tau.get(str(item["topic_id"]), self.params.tau)
            else:
                target_rate = self.params.tau
            
            # Update k value
            if actual_rate <= 0.0:
                # Item not exposed, increase k slightly
                new_k = min(self.params.ceiling, current_k * 1.1)
            else:
                # Adjust based on ratio
                ratio = target_rate / actual_rate
                new_k = current_k * (ratio ** self.params.alpha)
                new_k = max(self.params.floor, min(self.params.ceiling, new_k))
            
            new_k_map[key] = new_k
        
        return new_k_map
    
    def _calculate_statistics(
        self,
        rates: Dict[Tuple[int, int], float],
        topic_tau: Dict[str, float],
        pool: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate exposure statistics."""
        rate_values = list(rates.values())
        
        # Overall statistics
        stats = {
            "iteration": len(rate_values),
            "mean_exposure": np.mean(rate_values) if rate_values else 0.0,
            "max_exposure": np.max(rate_values) if rate_values else 0.0,
            "min_exposure": np.min(rate_values) if rate_values else 0.0,
            "std_exposure": np.std(rate_values) if rate_values else 0.0,
        }
        
        # Calculate overexposure
        if topic_tau:
            overexposures = []
            for item in pool:
                key = (item["question_id"], item["version"])
                actual = rates.get(key, 0.0)
                target = topic_tau.get(str(item.get("topic_id")), self.params.tau)
                overexposures.append(max(0, actual - target))
            stats["max_overexposure"] = np.max(overexposures) if overexposures else 0.0
        else:
            overexposures = [
                max(0, rate - self.params.tau)
                for rate in rate_values
            ]
            stats["max_overexposure"] = np.max(overexposures) if overexposures else 0.0
        
        return stats
    
    def _check_convergence(
        self,
        old_k: Dict[Tuple[int, int], float],
        new_k: Dict[Tuple[int, int], float],
        rates: Dict[Tuple[int, int], float]
    ) -> Dict[str, Any]:
        """Check convergence criteria."""
        # Calculate k value changes
        k_changes = [
            abs(new_k[key] - old_k[key])
            for key in old_k.keys()
        ]
        
        # Calculate rate deviations from target
        rate_deviations = [
            abs(rate - self.params.tau)
            for rate in rates.values()
        ]
        
        # Convergence criteria
        max_k_change = np.max(k_changes) if k_changes else 0.0
        mean_k_change = np.mean(k_changes) if k_changes else 0.0
        max_rate_deviation = np.max(rate_deviations) if rate_deviations else 0.0
        
        converged = (
            max_k_change < 0.01 and
            max_rate_deviation < 0.05
        )
        
        return {
            "converged": converged,
            "max_k_change": max_k_change,
            "mean_k_change": mean_k_change,
            "max_rate_deviation": max_rate_deviation,
            "mean_rate_deviation": np.mean(rate_deviations) if rate_deviations else 0.0
        }

def load_pool_from_db(conn: psycopg2.extensions.connection, exam_code: str) -> List[Dict[str, Any]]:
    """Load item pool from database."""
    sql = """
        SELECT 
            qv.question_id,
            qv.version,
            qv.topic_id,
            COALESCE(ic.a, 1.0) as a,
            COALESCE(ic.b, 0.0) as b,
            COALESCE(ic.c, 0.2) as c,
            COALESCE(iec.sh_p, 1.0) as sh_p
        FROM question_publications qp
        JOIN question_versions qv 
            ON qv.question_id = qp.question_id 
            AND qv.version = qp.live_version
        LEFT JOIN item_calibration ic 
            ON ic.question_id = qv.question_id 
            AND ic.version = qv.version 
            AND ic.model = '3PL'
        LEFT JOIN item_exposure_control iec 
            ON iec.question_id = qv.question_id 
            AND iec.version = qv.version
        WHERE qp.exam_code = %s 
            AND qv.state = 'published'
    """
    
    with conn.cursor(psycopg2.extras.DictCursor) as cur:
        cur.execute(sql, (exam_code,))
        rows = cur.fetchall()
    
    return [
        {
            "question_id": int(row["question_id"]),
            "version": int(row["version"]),
            "topic_id": row["topic_id"],
            "a": float(row["a"]),
            "b": float(row["b"]),
            "c": float(row["c"]),
            "sh_p": float(row["sh_p"])
        }
        for row in rows
    ]

def save_k_values_to_db(
    conn: psycopg2.extensions.connection,
    k_map: Dict[Tuple[int, int], float]
) -> int:
    """Save calibrated k values to database."""
    with conn.cursor() as cur:
        cur.execute("SET search_path TO public")
        
        for (qid, ver), k_value in k_map.items():
            cur.execute(
                """
                INSERT INTO item_exposure_control (question_id, version, sh_p)
                VALUES (%s, %s, %s)
                ON CONFLICT (question_id, version)
                DO UPDATE SET 
                    sh_p = EXCLUDED.sh_p,
                    updated_at = now()
                """,
                (qid, ver, float(k_value))
            )
    
    conn.commit()
    return len(k_map)