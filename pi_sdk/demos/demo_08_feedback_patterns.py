"""Demo 8: Feedback Pattern Analysis.

This demo shows:
1. Testing different feedback approaches
2. Analyzing effectiveness of feedback types
3. Optimizing feedback strategies
v1 - Initial implementation
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import aiohttp
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

# Configuration
API_KEY = "pilabs_key_epc8PlKUV7BzrsVJUJRzE3h3XLgxXa2zC6Hh7RSkIEo"
BASE_URL = "https://api.withpi.ai/v1"
OUTPUT_DIR = Path("demo_results")

# Test data
MATH_CONTRACT = {
    "name": "Math Feedback Patterns",
    "description": """Evaluate mathematical explanations with a focus on feedback.
    Test various feedback strategies to identify the most effective
    approaches for promoting understanding and confidence."""
}

TEST_CASES = [
    {
        "style": "Immediate Corrective",
        "input": "Explain common mistakes when solving equations with negative numbers.",
        "output": """Let's explore common mistakes and their corrections! 🔍

1. Sign Errors in Addition
-------------------------
Common Mistake:
-3 + (-5) = -2
❌ Incorrect! Here's why:
* Students often think negatives cancel out
* They subtract instead of adding negatives

Correct Solution:
-3 + (-5) = -8
✅ Remember:
* Adding negatives means going further negative
* Think of debt: owing $3 plus owing $5 means owing $8

2. Multiplication Sign Rules
--------------------------
Common Mistake:
-2 × -3 = -6
❌ Incorrect! Here's what went wrong:
* Forgetting that negative × negative = positive
* Not applying the sign rule consistently

Correct Solution:
-2 × -3 = 6
✅ Think about it:
* First negative reverses -3 to 3
* Second negative reverses again to 6
* Two reversals lead to positive

3. Distributing Negatives
------------------------
Common Mistake:
-(2 + 3) = -2 + 3
❌ Watch out! This is incorrect because:
* The negative must distribute to ALL terms
* Each term inside parentheses gets negated

Correct Solution:
-(2 + 3) = -2 + (-3) = -5
✅ Key points:
* Distribute the negative to each term
* Think: opposite of (2 + 3)
* Check: -5 is opposite of 5

4. Order of Operations
---------------------
Common Mistake:
-3² = 9
❌ Hold on! Let's see why this is wrong:
* The negative isn't part of the base
* Exponent applies to 3, not -3

Correct Solution:
-3² = -(3²) = -9
✅ Remember:
* Exponents before negation
* Think: negative of (3 × 3)
* Unless parentheses change order: (-3)² = 9

5. Subtracting Negatives
-----------------------
Common Mistake:
5 - (-2) = 3
❌ Not quite! Here's the issue:
* Confusing subtraction of negative
* Missing the double negative rule

Correct Solution:
5 - (-2) = 5 + 2 = 7
✅ Understanding why:
* Subtracting a negative means adding
* Like removing a debt is the same as gaining money

💡 General Tips for Success:
1. Always check if your answer makes sense
2. Use number lines for visualization
3. Think about real-world analogies
4. Write out steps clearly
5. Double-check sign rules

✅ Practice Strategy:
When you see a negative number:
1. Pause and identify the operation
2. Apply sign rules step by step
3. Verify your answer
4. Look for patterns in similar problems

Want to test your understanding?
Try these problems:
1. What's -4 + (-3)?
2. Simplify: -2 × 3 × (-4)
3. Solve: -(5 - 2)

Remember:
* Take your time with signs
* Write out each step
* Check your work
* Practice regularly

Need more help? Let's explore:
1. How do you visualize negative numbers?
2. What real-world examples help you?
3. Which rules are most challenging?"""
    },
    {
        "style": "Progressive Feedback",
        "input": "Guide a student through solving: 2x + 5 = 13",
        "output": """Let's solve this step by step with guided feedback! 📝

Step 1: Identify the Goal
------------------------
Q: What are we trying to find?
A: We need to find the value of x.

✅ Great start! Having a clear goal helps us stay focused.

Step 2: Plan Our Strategy
------------------------
Q: What should we do first?
A: Get the variable (x) term by itself.
   We need to subtract 5 from both sides.

✅ Excellent thinking! This is exactly how we isolate variables.

Step 3: Execute First Step
-------------------------
2x + 5 - 5 = 13 - 5
2x = 8

✅ Perfect! Notice how:
* We subtracted 5 from both sides
* This maintains equation balance
* The left side simplified nicely

Step 4: Solve for x
------------------
Q: How do we get x by itself?
A: Divide both sides by 2.

2x ÷ 2 = 8 ÷ 2
x = 4

✅ Outstanding work! You:
* Identified the correct operation
* Applied it to both sides
* Simplified correctly

Step 5: Verify Solution
----------------------
Let's check our answer:
* Put x = 4 back in original equation
* 2(4) + 5 = 13
* 8 + 5 = 13
* 13 = 13 ✓

✅ Excellent verification! This confirms our solution.

🌟 Progress Check:
You've mastered:
1. Identifying the goal
2. Planning your approach
3. Executing steps correctly
4. Verifying your answer

💡 Key Insights:
* Each step had a clear purpose
* We maintained equation balance
* Verification confirms our work

Ready for more challenge?
Try these similar equations:
1. 3x + 2 = 14
2. 5x - 3 = 12
3. 4x + 6 = 22

Remember these success strategies:
1. Always write out each step
2. Check your work
3. Look for patterns
4. Practice regularly

Need help? Ask yourself:
* What's my goal?
* What's my first step?
* How can I check my work?"""
    },
    {
        "style": "Growth-Oriented",
        "input": "Explain how to approach word problems about percentages.",
        "output": """Let's develop your percentage problem-solving skills! 🌱

Level 1: Building Confidence
---------------------------
Start here:
"What is 10% of 100?"

Your approach:
1. Convert 10% to decimal (0.10)
2. Multiply: 0.10 × 100 = 10

✅ Great start! You've mastered:
* Basic percentage conversion
* Simple multiplication
* Clear step-by-step thinking

🌟 Growth Point:
This foundation will help with harder problems!

Level 2: Expanding Skills
------------------------
Try this:
"15% of what number is 30?"

Strategy development:
1. Let's call the unknown number n
2. Write equation: 0.15 × n = 30
3. Solve: n = 30 ÷ 0.15 = 200

✅ You're growing! Notice how:
* You used variables effectively
* You worked backwards
* You applied division correctly

🌟 Growth Point:
You're ready for more complex problems!

Level 3: Advanced Application
---------------------------
Challenge yourself:
"A shirt's price increased by 20% to $60. What was the original price?"

Advanced strategy:
1. Understand: $60 is 120% of original
2. Let x be original price
3. Write: 1.20x = 60
4. Solve: x = 60 ÷ 1.20 = $50

✅ Excellent progress! You've learned:
* Working with price increases
* Understanding percentage relationships
* Solving real-world problems

🌟 Growth Point:
You're developing strong problem-solving skills!

Level 4: Mastery Development
---------------------------
Expert challenge:
"If 85% of students passed, and 45 failed, how many students total?"

Master strategy:
1. Understand: 85% passed, 15% failed
2. Know: 45 is 15% of total
3. Let t be total students
4. Write: 0.15t = 45
5. Solve: t = 45 ÷ 0.15 = 300

✅ Outstanding thinking! You've mastered:
* Complex percentage relationships
* Working backwards
* Real-world applications

💡 Your Growth Journey:
1. Started with basic conversions
2. Progressed to equations
3. Mastered real-world applications
4. Developed problem-solving strategies

🌟 Skills You're Building:
* Percentage conversion
* Equation writing
* Critical thinking
* Problem analysis
* Solution verification

Next Growth Steps:
1. Try more complex problems
2. Create your own examples
3. Explain concepts to others
4. Look for patterns

Remember:
* Each mistake is a learning opportunity
* Complex problems build on simple ones
* Understanding > memorizing
* Practice leads to mastery

Want to grow more?
Try these challenges:
1. Calculate percentage decrease
2. Work with multiple percentages
3. Solve compound percentage problems

You're doing great! Keep growing! 🌱"""
    },
    {
        "style": "Metacognitive",
        "input": "Help students understand why the Pythagorean theorem works.",
        "output": """Let's think about how we think about the Pythagorean theorem! 🤔

1. Initial Understanding Check
----------------------------
Q: What do you already know?
* a² + b² = c²
* Works for right triangles
* c is the hypotenuse

✅ Reflection Point:
How did you learn these facts?
What makes them stick in your mind?

2. Building Visual Understanding
------------------------------
Draw a right triangle:
      C
      |\\
    b |  \\ c
      |    \\
      |______\\
    A    a    B

🤔 Think About:
* Why are the squares important?
* What do a², b², and c² represent?
* How do areas relate to the theorem?

✅ Mental Model Check:
Can you visualize squares on each side?

3. Exploring the Proof
---------------------
Look at this square arrangement:
┌─────┬─────┐
│ a²  │     │
│     │     │
├─────┼─────┤
│     │ b²  │
│     │     │
└─────┴─────┘

🤔 Consider:
* How does this relate to c²?
* Why does rearrangement work?
* What patterns do you notice?

✅ Understanding Check:
Can you explain why area is preserved?

4. Real-world Connection
-----------------------
Think about:
* Carpenter's square tool
* TV screen dimensions
* Satellite dish positioning

🤔 Reflection Questions:
* Why do these applications work?
* How does the theorem help?
* What other uses can you think of?

5. Pattern Recognition
--------------------
Special cases:
* 3-4-5 triangle
* 5-12-13 triangle
* 8-15-17 triangle

🤔 Meta-analysis:
* What patterns do you see?
* How could you find more?
* Why do these work?

✅ Learning Progress:
Notice how your understanding deepens
as you connect different aspects.

6. Self-Assessment Guide
-----------------------
Can you:
□ Explain the theorem in your own words?
□ Draw and label a proof diagram?
□ Find real-world applications?
□ Generate your own examples?

🤔 Reflection on Learning:
* Which parts were challenging?
* What helped most?
* How has your understanding changed?

7. Knowledge Integration
----------------------
Connect to other concepts:
* Similar triangles
* Trigonometry
* Area calculations

🤔 Think About:
* How do these connect?
* Why are these relationships important?
* What new insights do you gain?

8. Learning Strategy Review
-------------------------
What helped you understand:
* Visual diagrams?
* Algebraic proofs?
* Real examples?
* Pattern recognition?

✅ Process Check:
Which strategies work best for you?

9. Future Application
-------------------
Think ahead:
* How will you use this?
* When might you need it?
* What else can you learn from it?

🤔 Meta-learning Questions:
* How do you learn math best?
* What helps you remember?
* How do you overcome challenges?

💡 Final Reflection:
1. How has your understanding grown?
2. What questions remain?
3. Where will you go next?

Remember:
* Understanding > memorizing
* Connections enhance learning
* Questions drive discovery
* Reflection deepens knowledge

Want to explore more?
1. How would you teach this?
2. What other proofs exist?
3. How does this connect to your interests?"""
    }
]

# Logging setup
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("demo_08")


async def generate_dimensions(session: aiohttp.ClientSession, contract: Dict) -> Optional[Dict]:
    """Generate dimensions for a contract."""
    try:
        async with session.post(
            f"{BASE_URL}/contracts/generate_dimensions",
            json={"contract": contract}
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error(f"Failed to generate dimensions: {await resp.text()}")
                return None
    except Exception as e:
        logger.error(f"Error generating dimensions: {e}")
        return None


async def score_response(
    session: aiohttp.ClientSession,
    contract: Dict,
    test_case: Dict
) -> Optional[Dict]:
    """Score a test response."""
    try:
        async with session.post(
            f"{BASE_URL}/contracts/score",
            json={
                "contract": contract,
                "llm_input": test_case["input"],
                "llm_output": test_case["output"]
            }
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error(f"Failed to score response: {await resp.text()}")
                return None
    except Exception as e:
        logger.error(f"Error scoring response: {e}")
        return None


def analyze_feedback(results: List[Dict]) -> Dict:
    """Analyze effectiveness of feedback patterns."""
    analysis = {
        "overall_scores": {},
        "feedback_types": {},
        "type_effectiveness": {},
        "recommendations": []
    }
    
    # Track feedback types
    type_scores = {
        "corrective": [],
        "reinforcement": [],
        "explanatory": [],
        "reflective": [],
        "progressive": []
    }
    
    for result in results:
        style = result["style"]
        scores = result["scores"]
        output = result["output"].lower()
        
        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]
        
        # Track feedback types used
        types_used = []
        if "incorrect" in output or "wrong" in output or "mistake" in output:
            types_used.append("corrective")
            type_scores["corrective"].append(scores["total_score"])
        if "great" in output or "excellent" in output or "perfect" in output:
            types_used.append("reinforcement")
            type_scores["reinforcement"].append(scores["total_score"])
        if "because" in output or "reason" in output or "why" in output:
            types_used.append("explanatory")
            type_scores["explanatory"].append(scores["total_score"])
        if "think about" in output or "consider" in output or "reflect" in output:
            types_used.append("reflective")
            type_scores["reflective"].append(scores["total_score"])
        if "next" in output or "ready for" in output or "try this" in output:
            types_used.append("progressive")
            type_scores["progressive"].append(scores["total_score"])
        
        analysis["feedback_types"][style] = types_used
    
    # Analyze type effectiveness
    for ftype, scores in type_scores.items():
        if scores:
            analysis["type_effectiveness"][ftype] = sum(scores) / len(scores)
    
    # Generate recommendations
    sorted_types = sorted(
        analysis["type_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    analysis["recommendations"].extend([
        f"Most effective type: {sorted_types[0][0]} ({sorted_types[0][1]:.2f})",
        "Balance different feedback types",
        "Start with positive reinforcement",
        "Include specific corrections",
        "End with reflection and next steps"
    ])
    
    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Feedback Pattern Analysis")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Feedback Types", style="yellow")
    
    for result in results:
        style = result["style"]
        types = analysis["feedback_types"][style]
        scores_table.add_row(
            style,
            f"{analysis['overall_scores'][style]:.2f}",
            "\n".join(types)
        )
    
    # Types table
    types_table = Table(title="Feedback Type Effectiveness")
    types_table.add_column("Type", style="cyan")
    types_table.add_column("Average Score", style="green")
    
    for ftype, score in sorted(
        analysis["type_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        types_table.add_row(
            ftype.title(),
            f"{score:.2f}"
        )
    
    # Recommendations table
    recommendations_table = Table(title="Best Practices")
    recommendations_table.add_column("Category", style="cyan")
    recommendations_table.add_column("Details", style="yellow")
    
    recommendations_table.add_row(
        "Top Type",
        analysis["recommendations"][0]
    )
    recommendations_table.add_row(
        "Best Practices",
        "\n".join(analysis["recommendations"][1:])
    )
    
    # Display all tables
    console.print("\n")
    console.print(scores_table)
    console.print("\n")
    console.print(types_table)
    console.print("\n")
    console.print(recommendations_table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_08_results.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to {output_file}")


async def main():
    """Run the demo."""
    results = {
        "contract": MATH_CONTRACT,
        "test_cases": [],
        "success": False
    }
    
    # Create session with auth
    async with aiohttp.ClientSession(headers={
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }) as session:
        # Generate dimensions
        console.print("\n[bold]Generating Contract Dimensions[/bold]")
        if contract_with_dims := await generate_dimensions(session, MATH_CONTRACT):
            results["dimensions"] = contract_with_dims.get("dimensions", [])
            console.print("[green]✓ Generated dimensions[/green]")
            
            # Test each case
            console.print("\n[bold]Testing Feedback Patterns[/bold]")
            scored_cases = []
            for case in TEST_CASES:
                if scores := await score_response(session, contract_with_dims, case):
                    scored_case = {
                        "style": case["style"],
                        "input": case["input"],
                        "output": case["output"],
                        "scores": scores
                    }
                    results["test_cases"].append(scored_case)
                    scored_cases.append(scored_case)
                    console.print(f"[green]✓ Scored {case['style']}[/green]")
            
            # Analyze and display results
            if scored_cases:
                analysis = analyze_feedback(scored_cases)
                results["analysis"] = analysis
                
                console.print("\n[bold]Analysis Results[/bold]")
                display_results(scored_cases, analysis)
                results["success"] = True
        
        # Save results
        save_results(results)
        
        if results["success"]:
            console.print("\n[bold green]Demo completed successfully![/bold green]")
        else:
            console.print("\n[bold red]Demo failed![/bold red]")


if __name__ == "__main__":
    console.print("\n[bold]Running Demo 8: Feedback Pattern Analysis[/bold]")
    asyncio.run(main()) 