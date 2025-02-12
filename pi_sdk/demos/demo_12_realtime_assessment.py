"""Real-time assessment strategies demo for the PI API."""

import json
import logging
from typing import Any, Dict, List

from pi_sdk.client import PIClient
from pi_sdk.models import Contract, Dimension

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize PI client
client = PIClient()


def generate_assessment_contract() -> Dict[str, Any]:
    """Generate a contract for testing real-time assessment strategies.
    
    1. Create contract with assessment dimensions - v1
    2. Include timing and feedback elements - v1
    3. Add progression tracking - v1
    """
    contract_data = {
        "name": "Real-time Math Assessment",
        "description": "Evaluate effectiveness of real-time assessment strategies in mathematical explanations."
    }
    
    try:
        response = client.generate_contract(contract_data)
        logger.info("Contract generated successfully")
        return response
    except Exception as e:
        logger.error(f"Error generating contract: {e}")
        raise


def generate_assessment_dimensions(contract_id: str) -> List[Dimension]:
    """Generate dimensions for real-time assessment.
    
    1. Create assessment-specific dimensions - v1
    2. Include timing metrics - v1
    3. Add feedback quality measures - v1
    """
    dimension_data = {
        "assessment_types": [
            "Immediate Feedback",
            "Progress Tracking",
            "Concept Checking",
            "Error Analysis"
        ],
        "contract_id": contract_id
    }
    
    try:
        response = client.generate_dimensions(dimension_data)
        logger.info("Dimensions generated successfully")
        return response
    except Exception as e:
        logger.error(f"Error generating dimensions: {e}")
        raise


def test_assessment_strategies(contract_id: str, dimensions: List[Dimension]) -> Dict[str, Any]:
    """Test different real-time assessment strategies.
    
    1. Test immediate feedback - v1
    2. Test progress tracking - v1
    3. Test concept checking - v1
    4. Test error analysis - v1
    """
    test_cases = [
        {
            "strategy": "Immediate Feedback",
            "problem": "Solve x² + 5x + 6 = 0",
            "response": (
                "Let's solve this step by step:\n"
                "1. This is a quadratic equation in standard form ax² + bx + c = 0\n"
                "2. We can solve it by factoring\n"
                "3. x² + 5x + 6 = (x + 2)(x + 3)\n"
                "4. Set each factor to zero:\n"
                "   x + 2 = 0 or x + 3 = 0\n"
                "5. Solve:\n"
                "   x = -2 or x = -3\n\n"
                "Is this correct? Let's verify:\n"
                "- Plug in x = -2: (-2)² + 5(-2) + 6 = 4 - 10 + 6 = 0 [CHECK]\n"
                "- Plug in x = -3: (-3)² + 5(-3) + 6 = 9 - 15 + 6 = 0 [CHECK]"
            )
        },
        {
            "strategy": "Progress Tracking",
            "problem": "Find the derivative of f(x) = x³ - 2x² + 4x - 1",
            "response": (
                "Progress Check 1: Identify the function type\n"
                "[CHECK] This is a polynomial function of degree 3\n\n"
                "Progress Check 2: Apply power rule\n"
                "[CHECK] For x³: derivative is 3x²\n"
                "[CHECK] For -2x²: derivative is -4x\n"
                "[CHECK] For 4x: derivative is 4\n"
                "[CHECK] For -1: derivative is 0\n\n"
                "Progress Check 3: Combine terms\n"
                "[CHECK] f'(x) = 3x² - 4x + 4\n\n"
                "Final Answer: f'(x) = 3x² - 4x + 4"
            )
        }
    ]
    
    try:
        results = []
        for test_case in test_cases:
            score = client.score_response(contract_id, test_case["response"], dimensions)
            results.append({
                "strategy": test_case["strategy"],
                "problem": test_case["problem"],
                "scores": score
            })
        
        logger.info("Assessment strategies tested successfully")
        return {"results": results}
    except Exception as e:
        logger.error(f"Error testing assessment strategies: {e}")
        raise


def save_results(results: Dict[str, Any]) -> None:
    """Save test results to file.
    
    1. Format results - v1
    2. Save to JSON - v1
    3. Log completion - v1
    """
    try:
        with open("demo_results/demo_12_results.json", "w") as f:
            json.dump(results, f, indent=2)
        logger.info("Results saved successfully")
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise


def main():
    """Run the real-time assessment demo.
    
    1. Generate contract - v1
    2. Create dimensions - v1
    3. Test strategies - v1
    4. Save results - v1
    """
    try:
        # Generate contract
        contract = generate_assessment_contract()
        
        # Generate dimensions
        dimensions = generate_assessment_dimensions(contract["id"])
        
        # Test assessment strategies
        results = test_assessment_strategies(contract["id"], dimensions)
        
        # Save results
        save_results(results)
        
        logger.info("Demo completed successfully")
    except Exception as e:
        logger.error(f"Error running demo: {e}")
        raise


if __name__ == "__main__":
    main()
""" 