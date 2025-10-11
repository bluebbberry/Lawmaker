from typing import List, Dict, Any, Tuple, Optional
from src.query import Query
from src.game_result import GameResult

try:
    import janus_swi as janus

    JANUS_AVAILABLE = True
except ImportError:
    JANUS_AVAILABLE = False

class JanusPrologRunner:
    """Enhanced Prolog runner using janus_swi for better integration"""

    def __init__(self):
        self.janus_available = JANUS_AVAILABLE
        if self.janus_available:
            try:
                janus.query_once("writeln('Prolog available!')")
                self.prolog_available = True
            except Exception as e:
                print(f"Error initializing janus_swi: {e}")
                self.prolog_available = False
                self.janus_available = False
        else:
            self.prolog_available = False

    def run_queries(self, prolog_code: str, queries: List[Query]) -> Tuple[GameResult, Dict[str, Any]]:
        """Run Prolog queries using janus_swi"""
        if not self.prolog_available:
            return GameResult.PROLOG_ERROR, {
                "error": "Janus SWI-Prolog not available. Install with: pip install janus_swi"}

        try:
            janus.consult("temp_rules", prolog_code)
            results = {}
            all_correct = True

            for i, query in enumerate(queries):
                try:
                    actual_results = []
                    found_solutions = False

                    for solution in janus.query(query.query):
                        found_solutions = True
                        if solution:
                            if isinstance(solution, dict) and solution:
                                for var, value in solution.items():
                                    if value not in [True, False, 'True', 'False', None, 'None'] and str(value) not in [
                                        'True', 'False', 'None']:
                                        actual_results.append(str(value))
                            elif not isinstance(solution, dict):
                                if (solution not in [True, False, 'True', 'False', None, 'None'] and
                                        str(solution) not in ['True', 'False', 'None']):
                                    actual_results.append(str(solution))

                    if found_solutions and not actual_results:
                        if not query.expected or (len(query.expected) == 1 and query.expected[0] in ['true', True]):
                            actual_results.append("true")

                    if not found_solutions:
                        try:
                            result = janus.query_once(query.query)
                            if result is not None:
                                if isinstance(result, dict) and result:
                                    for var, value in result.items():
                                        if value not in [True, False, 'True', 'False', None, 'None']:
                                            actual_results.append(str(value))
                                elif result is True:
                                    if not any(c.isupper() for c in query.query):
                                        actual_results.append("true")
                        except:
                            pass

                    if not query.expected or query.expected == ['false']:
                        correct = len(actual_results) == 0
                    else:
                        expected_set = set(str(e) for e in query.expected)
                        actual_set = set(str(r) for r in actual_results)
                        correct = actual_set == expected_set

                    results[f"query_{i}"] = {
                        "query": query.query,
                        "expected": query.expected,
                        "actual": actual_results,
                        "correct": correct
                    }

                    if not correct:
                        all_correct = False

                except Exception as e:
                    results[f"query_{i}"] = {
                        "query": query.query,
                        "expected": query.expected,
                        "actual": [],
                        "error": str(e),
                        "correct": False
                    }
                    all_correct = False

            if all_correct:
                return GameResult.SUCCESS, results
            else:
                return GameResult.WRONG_RESULTS, results

        except Exception as e:
            return GameResult.PROLOG_ERROR, {"error": f"Prolog error: {str(e)}"}
