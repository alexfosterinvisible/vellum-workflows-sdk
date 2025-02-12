"""Test file to debug Vellum typing issues."""
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import vellum.types as vt
from vellum.client import Vellum

# Simple type aliases
VellumInput = Dict[str, str]
VellumOutput = Dict[str, Any]


@dataclass
class TestPromptInfo:
    """Test class for prompt info."""
    name: str
    input_variables: List[str]
    description: Optional[str] = None


def create_vellum_input(name: str, value: str) -> vt.PromptRequestInput:
    """Create a Vellum input object safely."""
    return {"name": name, "value": value}  # type: ignore


def test_vellum_types() -> None:
    """Test function to verify Vellum type handling."""
    print("🔍 Testing Vellum type handling...")

    # Create test data
    test_prompt = TestPromptInfo(
        name="test_prompt",
        input_variables=["input1", "input2"],
        description="Test prompt"
    )

    # Test input handling
    inputs: VellumInput = {
        "input1": "test value 1",
        "input2": "test value 2"
    }

    # Convert to Vellum format
    vellum_inputs = [
        create_vellum_input(name, value)
        for name, value in inputs.items()
    ]

    print("\n✅ Successfully created Vellum inputs:")
    for input_obj in vellum_inputs:
        print(f"  - {input_obj['name']}: {input_obj['value']}")

    # Test with actual Vellum client
    api_key = os.getenv("VELLUM_API_KEY")
    if api_key:
        print("\n🔌 Testing Vellum client connection...")
        client = Vellum(api_key=api_key)

        try:
            # List deployments
            response = client.deployments.list()
            print("\n✅ Successfully listed deployments:")
            for deployment in response.results:
                print(f"  - {deployment.name}")

                # Test input variable handling
                if hasattr(deployment, 'input_variables'):
                    print("    Input variables:")
                    for var in deployment.input_variables:
                        var_name = var.name if hasattr(var, 'name') else str(var)
                        print(f"      - {var_name}")

        except Exception as e:
            print(f"\n❌ Error testing Vellum client: {str(e)}")
    else:
        print("\n⚠️ No API key found, skipping client tests")


if __name__ == "__main__":
    test_vellum_types()
