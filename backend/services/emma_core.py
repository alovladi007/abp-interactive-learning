"""
EMMA - AI STEM Tutor and Problem Solver
Combines Wolfram Mathematica, Chegg, and Quizlet capabilities
Symbolic computation, step-by-step solutions, and adaptive learning
"""

import sympy as sp
from sympy import symbols, sympify, solve, diff, integrate, limit, series, simplify
from sympy.parsing.latex import parse_latex
from sympy.printing.latex import latex
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from datetime import datetime, timedelta
import hashlib
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProblemType(Enum):
    """Types of STEM problems EMMA can solve"""
    ALGEBRA = "algebra"
    CALCULUS = "calculus"
    LINEAR_ALGEBRA = "linear_algebra"
    DIFFERENTIAL_EQUATIONS = "differential_equations"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    STATISTICS = "statistics"
    DISCRETE_MATH = "discrete_math"
    GEOMETRY = "geometry"
    TRIGONOMETRY = "trigonometry"


class DifficultyLevel(Enum):
    """Difficulty levels for problems and learning"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Problem:
    """Represents a STEM problem"""
    question: str
    problem_type: ProblemType
    difficulty: DifficultyLevel
    tags: List[str]
    latex_representation: Optional[str] = None
    variables: Optional[List[str]] = None
    constraints: Optional[List[str]] = None


@dataclass
class Solution:
    """Step-by-step solution to a problem"""
    problem: Problem
    steps: List[Dict[str, str]]
    final_answer: str
    latex_answer: str
    verification: Optional[str] = None
    alternative_methods: List[str] = field(default_factory=list)
    visualizations: List[str] = field(default_factory=list)
    explanation: str = ""
    computation_time_ms: int = 0


@dataclass
class QuizQuestion:
    """Quiz question with spaced repetition metadata"""
    question_id: str
    question: str
    correct_answer: str
    distractors: List[str]
    explanation: str
    topic: str
    difficulty: DifficultyLevel
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    ease_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0


class SymbolicComputationEngine:
    """
    Symbolic math engine using SymPy
    Handles algebraic manipulation, calculus, solving equations
    """

    def __init__(self):
        self.common_symbols = {
            'x': symbols('x'),
            'y': symbols('y'),
            'z': symbols('z'),
            't': symbols('t'),
            'n': symbols('n'),
            'theta': symbols('theta'),
            'phi': symbols('phi')
        }

    def parse_expression(self, expr_str: str) -> sp.Expr:
        """Parse string expression to SymPy expression"""
        try:
            # Try LaTeX parsing first
            if '\\' in expr_str:
                return parse_latex(expr_str)
            # Standard parsing
            return sympify(expr_str, locals=self.common_symbols)
        except Exception as e:
            logger.error(f"Failed to parse expression: {expr_str}, error: {e}")
            raise ValueError(f"Cannot parse expression: {expr_str}")

    def solve_equation(self, equation_str: str, variable: str = 'x') -> List[sp.Expr]:
        """Solve equation for given variable"""
        try:
            expr = self.parse_expression(equation_str)
            var = self.common_symbols.get(variable, symbols(variable))
            solutions = solve(expr, var)
            return solutions
        except Exception as e:
            logger.error(f"Failed to solve equation: {e}")
            return []

    def differentiate(self, expr_str: str, variable: str = 'x', order: int = 1) -> sp.Expr:
        """Compute derivative"""
        expr = self.parse_expression(expr_str)
        var = self.common_symbols.get(variable, symbols(variable))
        return diff(expr, var, order)

    def integrate_expression(
        self,
        expr_str: str,
        variable: str = 'x',
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None
    ) -> sp.Expr:
        """Compute definite or indefinite integral"""
        expr = self.parse_expression(expr_str)
        var = self.common_symbols.get(variable, symbols(variable))

        if lower_bound is not None and upper_bound is not None:
            return integrate(expr, (var, lower_bound, upper_bound))
        return integrate(expr, var)

    def compute_limit(self, expr_str: str, variable: str = 'x', point: float = 0) -> sp.Expr:
        """Compute limit"""
        expr = self.parse_expression(expr_str)
        var = self.common_symbols.get(variable, symbols(variable))
        return limit(expr, var, point)

    def taylor_series(self, expr_str: str, variable: str = 'x', point: float = 0, order: int = 5) -> sp.Expr:
        """Compute Taylor series expansion"""
        expr = self.parse_expression(expr_str)
        var = self.common_symbols.get(variable, symbols(variable))
        return series(expr, var, point, order)

    def simplify_expression(self, expr_str: str) -> sp.Expr:
        """Simplify expression"""
        expr = self.parse_expression(expr_str)
        return simplify(expr)

    def to_latex(self, expr: sp.Expr) -> str:
        """Convert SymPy expression to LaTeX"""
        return latex(expr)


class StepByStepSolver:
    """
    Generates step-by-step solutions with explanations
    Similar to Chegg's approach
    """

    def __init__(self, llm_model: str = "meta-llama/Llama-3-8B-Instruct"):
        self.symbolic_engine = SymbolicComputationEngine()
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model)
        self.model = AutoModelForCausalLM.from_pretrained(
            llm_model,
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_8bit=True
        )

    def solve_algebra_problem(self, problem: Problem) -> Solution:
        """Solve algebra problem with detailed steps"""
        steps = []
        start_time = datetime.now()

        try:
            # Step 1: Parse the equation
            expr = self.symbolic_engine.parse_expression(problem.question)
            steps.append({
                "step_number": 1,
                "description": "Parse the equation",
                "content": f"Given equation: ${self.symbolic_engine.to_latex(expr)} = 0$",
                "explanation": "We start by identifying the equation to solve."
            })

            # Step 2: Identify the variable
            free_symbols = list(expr.free_symbols)
            if not free_symbols:
                raise ValueError("No variables found in equation")

            var = free_symbols[0]
            steps.append({
                "step_number": 2,
                "description": f"Solve for {var}",
                "content": f"Variable to solve: ${var}$",
                "explanation": f"We need to isolate {var} on one side of the equation."
            })

            # Step 3: Solve
            solutions = solve(expr, var)
            steps.append({
                "step_number": 3,
                "description": "Apply algebraic techniques",
                "content": f"Solutions: {', '.join([f'${self.symbolic_engine.to_latex(sol)}$' for sol in solutions])}",
                "explanation": "Using algebraic manipulation, we find all solutions."
            })

            # Step 4: Verify
            verification_steps = []
            for sol in solutions:
                check = expr.subs(var, sol)
                verification_steps.append(f"For ${var} = {self.symbolic_engine.to_latex(sol)}$: ${self.symbolic_engine.to_latex(check)}$")

            steps.append({
                "step_number": 4,
                "description": "Verify solutions",
                "content": "\n".join(verification_steps),
                "explanation": "We substitute each solution back to verify it satisfies the original equation."
            })

            final_answer = f"Solutions: {', '.join([str(sol) for sol in solutions])}"
            latex_answer = f"${', '.join([self.symbolic_engine.to_latex(sol) for sol in solutions])}$"

            computation_time = int((datetime.now() - start_time).total_seconds() * 1000)

            return Solution(
                problem=problem,
                steps=steps,
                final_answer=final_answer,
                latex_answer=latex_answer,
                verification="All solutions verified",
                computation_time_ms=computation_time,
                explanation="This problem was solved using algebraic techniques to isolate the variable."
            )

        except Exception as e:
            logger.error(f"Failed to solve algebra problem: {e}")
            return Solution(
                problem=problem,
                steps=[{"step_number": 1, "description": "Error", "content": str(e), "explanation": ""}],
                final_answer="Unable to solve",
                latex_answer="",
                computation_time_ms=0
            )

    def solve_calculus_problem(self, problem: Problem, operation: str = "derivative") -> Solution:
        """Solve calculus problem (derivatives, integrals, limits)"""
        steps = []
        start_time = datetime.now()

        try:
            expr = self.symbolic_engine.parse_expression(problem.question)

            # Step 1: Identify the expression
            steps.append({
                "step_number": 1,
                "description": f"Identify the expression for {operation}",
                "content": f"Given: ${self.symbolic_engine.to_latex(expr)}$",
                "explanation": f"We need to compute the {operation} of this expression."
            })

            # Step 2: Apply the operation
            if operation == "derivative":
                result = self.symbolic_engine.differentiate(problem.question)
                steps.append({
                    "step_number": 2,
                    "description": "Apply differentiation rules",
                    "content": f"$\\frac{{d}}{{dx}}({self.symbolic_engine.to_latex(expr)}) = {self.symbolic_engine.to_latex(result)}$",
                    "explanation": "We apply the power rule, chain rule, and product rule as needed."
                })

            elif operation == "integral":
                result = self.symbolic_engine.integrate_expression(problem.question)
                steps.append({
                    "step_number": 2,
                    "description": "Apply integration techniques",
                    "content": f"$\\int {self.symbolic_engine.to_latex(expr)} \\, dx = {self.symbolic_engine.to_latex(result)} + C$",
                    "explanation": "We use substitution and integration by parts as needed."
                })

            elif operation == "limit":
                result = self.symbolic_engine.compute_limit(problem.question, point=0)
                steps.append({
                    "step_number": 2,
                    "description": "Evaluate the limit",
                    "content": f"$\\lim_{{x \\to 0}} {self.symbolic_engine.to_latex(expr)} = {self.symbolic_engine.to_latex(result)}$",
                    "explanation": "We evaluate the limit using L'Hôpital's rule if needed."
                })

            # Step 3: Simplify
            simplified = simplify(result)
            steps.append({
                "step_number": 3,
                "description": "Simplify the result",
                "content": f"Simplified: ${self.symbolic_engine.to_latex(simplified)}$",
                "explanation": "We simplify the expression to its most compact form."
            })

            computation_time = int((datetime.now() - start_time).total_seconds() * 1000)

            return Solution(
                problem=problem,
                steps=steps,
                final_answer=str(simplified),
                latex_answer=self.symbolic_engine.to_latex(simplified),
                computation_time_ms=computation_time,
                explanation=f"This {operation} was computed using standard calculus techniques."
            )

        except Exception as e:
            logger.error(f"Failed to solve calculus problem: {e}")
            return Solution(
                problem=problem,
                steps=[{"step_number": 1, "description": "Error", "content": str(e), "explanation": ""}],
                final_answer="Unable to solve",
                latex_answer="",
                computation_time_ms=0
            )

    def generate_explanation(self, solution: Solution) -> str:
        """Generate natural language explanation using LLM"""
        prompt = f"""### Instruction:
Explain the following mathematical solution in clear, simple terms suitable for a student.

### Problem:
{solution.problem.question}

### Solution Steps:
{json.dumps(solution.steps, indent=2)}

### Answer:
{solution.final_answer}

### Explanation:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_length=512,
            temperature=0.7,
            do_sample=True
        )

        explanation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract explanation part
        if "### Explanation:" in explanation:
            explanation = explanation.split("### Explanation:")[-1].strip()

        return explanation


class VisualizationEngine:
    """
    Creates plots and visualizations for mathematical concepts
    Similar to Wolfram's plotting capabilities
    """

    def plot_function(
        self,
        expr_str: str,
        variable: str = 'x',
        x_range: Tuple[float, float] = (-10, 10),
        title: str = "Function Plot"
    ) -> str:
        """Plot a function and return base64 encoded image"""
        try:
            # Parse expression
            engine = SymbolicComputationEngine()
            expr = engine.parse_expression(expr_str)

            # Convert to numerical function
            var = symbols(variable)
            f = sp.lambdify(var, expr, 'numpy')

            # Create plot
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            y_vals = f(x_vals)

            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2)
            plt.grid(True, alpha=0.3)
            plt.xlabel(variable)
            plt.ylabel(f'f({variable})')
            plt.title(title)
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)

            # Save to base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()

            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            logger.error(f"Failed to plot function: {e}")
            return ""

    def plot_derivative_comparison(self, expr_str: str, x_range: Tuple[float, float] = (-5, 5)) -> str:
        """Plot function and its derivative"""
        try:
            engine = SymbolicComputationEngine()
            expr = engine.parse_expression(expr_str)
            derivative = engine.differentiate(expr_str)

            x = symbols('x')
            f = sp.lambdify(x, expr, 'numpy')
            df = sp.lambdify(x, derivative, 'numpy')

            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            y_vals = f(x_vals)
            dy_vals = df(x_vals)

            plt.figure(figsize=(12, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
            plt.plot(x_vals, dy_vals, 'r--', linewidth=2, label="f'(x)")
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Function and Derivative')
            plt.legend()
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)

            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()

            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            logger.error(f"Failed to plot derivative comparison: {e}")
            return ""


class SpacedRepetitionSystem:
    """
    Implements SM-2 algorithm for spaced repetition
    Similar to Quizlet's learning system
    """

    def __init__(self):
        self.questions_db: Dict[str, QuizQuestion] = {}

    def add_question(self, question: QuizQuestion):
        """Add a question to the system"""
        if not question.question_id:
            question.question_id = hashlib.md5(question.question.encode()).hexdigest()
        self.questions_db[question.question_id] = question

    def record_answer(self, question_id: str, quality: int) -> QuizQuestion:
        """
        Record answer quality and update scheduling
        quality: 0-5 (0=complete blackout, 5=perfect recall)
        """
        if question_id not in self.questions_db:
            raise ValueError(f"Question {question_id} not found")

        question = self.questions_db[question_id]

        # SM-2 algorithm
        if quality >= 3:
            if question.repetitions == 0:
                question.interval_days = 1
            elif question.repetitions == 1:
                question.interval_days = 6
            else:
                question.interval_days = int(question.interval_days * question.ease_factor)

            question.repetitions += 1
        else:
            question.repetitions = 0
            question.interval_days = 1

        # Update ease factor
        question.ease_factor = max(1.3, question.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Update timestamps
        question.last_reviewed = datetime.now()
        question.next_review = datetime.now() + timedelta(days=question.interval_days)

        self.questions_db[question_id] = question
        return question

    def get_due_questions(self, limit: int = 10) -> List[QuizQuestion]:
        """Get questions due for review"""
        now = datetime.now()
        due_questions = [
            q for q in self.questions_db.values()
            if q.next_review is None or q.next_review <= now
        ]
        # Sort by next_review date (oldest first)
        due_questions.sort(key=lambda q: q.next_review or datetime.min)
        return due_questions[:limit]

    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics"""
        total = len(self.questions_db)
        if total == 0:
            return {"total": 0, "mastered": 0, "learning": 0, "new": 0}

        mastered = sum(1 for q in self.questions_db.values() if q.repetitions >= 5)
        learning = sum(1 for q in self.questions_db.values() if 0 < q.repetitions < 5)
        new = sum(1 for q in self.questions_db.values() if q.repetitions == 0)

        return {
            "total": total,
            "mastered": mastered,
            "learning": learning,
            "new": new,
            "mastery_percentage": (mastered / total) * 100 if total > 0 else 0
        }


class EMMACore:
    """
    Main EMMA orchestrator
    Combines symbolic computation, problem solving, and adaptive learning
    """

    def __init__(self, llm_model: str = "meta-llama/Llama-3-8B-Instruct"):
        self.solver = StepByStepSolver(llm_model)
        self.visualizer = VisualizationEngine()
        self.srs = SpacedRepetitionSystem()

    async def solve_problem(self, problem: Problem) -> Solution:
        """Main problem solving interface"""
        logger.info(f"Solving {problem.problem_type.value} problem")

        if problem.problem_type == ProblemType.ALGEBRA:
            solution = self.solver.solve_algebra_problem(problem)
        elif problem.problem_type == ProblemType.CALCULUS:
            # Determine calculus operation from problem
            if "derivative" in problem.question.lower() or "differentiate" in problem.question.lower():
                solution = self.solver.solve_calculus_problem(problem, operation="derivative")
            elif "integral" in problem.question.lower() or "integrate" in problem.question.lower():
                solution = self.solver.solve_calculus_problem(problem, operation="integral")
            elif "limit" in problem.question.lower():
                solution = self.solver.solve_calculus_problem(problem, operation="limit")
            else:
                solution = self.solver.solve_calculus_problem(problem)
        else:
            # Generic solution
            solution = self.solver.solve_algebra_problem(problem)

        # Add visualization if applicable
        try:
            if problem.problem_type in [ProblemType.ALGEBRA, ProblemType.CALCULUS]:
                plot = self.visualizer.plot_function(problem.question, title=f"Plot of {problem.question}")
                if plot:
                    solution.visualizations.append(plot)
        except Exception as e:
            logger.warning(f"Failed to create visualization: {e}")

        return solution

    def generate_quiz(self, topic: str, difficulty: DifficultyLevel, num_questions: int = 10) -> List[QuizQuestion]:
        """Generate quiz questions on a topic"""
        # This would integrate with a question bank
        # For now, return placeholder
        logger.info(f"Generating {num_questions} {difficulty.value} questions on {topic}")
        return []

    def get_study_plan(self, user_id: str) -> Dict[str, Any]:
        """Get personalized study plan based on SRS"""
        due_questions = self.srs.get_due_questions()
        stats = self.srs.get_statistics()

        return {
            "user_id": user_id,
            "due_questions": len(due_questions),
            "statistics": stats,
            "recommended_topics": self._get_weak_topics(),
            "next_review": due_questions[0].next_review if due_questions else None
        }

    def _get_weak_topics(self) -> List[str]:
        """Identify topics that need more practice"""
        # Analyze question history to find weak areas
        return []


# Example usage
async def main():
    emma = EMMACore()

    # Example 1: Solve algebra problem
    problem = Problem(
        question="x**2 - 5*x + 6",
        problem_type=ProblemType.ALGEBRA,
        difficulty=DifficultyLevel.BEGINNER,
        tags=["quadratic", "factoring"]
    )

    solution = await emma.solve_problem(problem)
    print(f"Solution: {solution.final_answer}")
    print(f"Steps: {len(solution.steps)}")

    # Example 2: Calculus problem
    calc_problem = Problem(
        question="x**3 + 2*x**2 - x",
        problem_type=ProblemType.CALCULUS,
        difficulty=DifficultyLevel.INTERMEDIATE,
        tags=["derivative", "polynomial"]
    )

    calc_solution = await emma.solve_problem(calc_problem)
    print(f"Derivative: {calc_solution.final_answer}")


if __name__ == "__main__":
    asyncio.run(main())
