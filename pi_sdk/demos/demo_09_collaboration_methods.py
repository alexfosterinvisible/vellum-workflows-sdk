"""Demo 9: Collaboration Methods Analysis.

This demo shows:
1. Testing different collaboration approaches
2. Analyzing effectiveness of group learning
3. Optimizing collaboration strategies
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
    "name": "Math Collaboration Patterns",
    "description": """Evaluate mathematical explanations with a focus on collaboration.
    Test various collaboration strategies to identify the most effective
    approaches for group learning and peer interaction."""
}

TEST_CASES = [
    {
        "style": "Group Collaboration",
        "input": "Explain how to solve systems of equations using substitution.",
        "output": """Let's solve this together as a group! ����

Group Activity: System of Equations
---------------------------------
Problem to solve:
x + 2y = 7
2x - y = 1

👤 Student 1 (Leader):
"Let's organize our approach:
1. Choose an equation to start with
2. Solve for one variable
3. Substitute into other equation
4. Solve for remaining variable"

👤 Student 2 (Equation Expert):
"I suggest starting with the second equation:
2x - y = 1
Solving for y:
y = 2x - 1"

👤 Student 3 (Substitution Specialist):
"Great! Now let's substitute y into first equation:
x + 2(2x - 1) = 7
x + 4x - 2 = 7
5x - 2 = 7"

👤 Student 4 (Solution Checker):
"Let's solve for x:
5x = 9
x = 9/5"

Group Verification:
------------------
👥 Together, let's check our work:

1. We found x = 9/5
2. Substitute back to find y:
   y = 2(9/5) - 1
   y = 18/5 - 1
   y = 13/5

3. Check in original equations:
   * 9/5 + 2(13/5) = 7 ✓
   * 2(9/5) - 13/5 = 1 ✓

🤝 Group Learning Points:
1. Clear role assignment helps
2. Step-by-step verification
3. Everyone contributes
4. Shared understanding

💡 Collaboration Tips:
* Listen to all suggestions
* Build on others' ideas
* Verify together
* Share different approaches

Group Practice:
Try these systems together:
1. x + y = 5
   x - y = 1

2. 2x + y = 8
   x - 2y = -1

Remember:
* Take turns leading
* Explain your thinking
* Ask questions
* Help others understand"""
    },
    {
        "style": "Peer Review",
        "input": "Explain how to find the area of irregular shapes.",
        "output": """Let's use peer review to explore area calculations! 👥

Student A's Solution:
-------------------
"To find irregular shape areas:
1. Break into basic shapes
2. Find each area
3. Add them together"

Peer Review by Student B:
------------------------
✅ Strong points:
* Clear basic strategy
* Simple step-by-step approach
* Easy to follow

💭 Suggestions:
* Add examples
* Include formulas
* Show a diagram

Student B's Addition:
-------------------
"Here's an example:
┌─────┐
│     │____
│     │    │
└─────┘    │
     │     │
     └─────┘

Break into:
1. Rectangle: length × width
2. Second rectangle: length × width
Add areas together!"

Peer Review by Student A:
------------------------
✅ Good additions:
* Visual representation
* Specific example
* Clear breakdown

💭 Could improve:
* Add measurements
* Show calculations
* Include more shapes

Combined Solution:
----------------
Let's merge our best ideas:

1. Strategy:
   * Identify basic shapes
   * Use appropriate formulas
   * Add areas together

2. Example with numbers:
   ┌─────┐  5
   │     │____
   │  8  │    │ 3
   └─────┘    │
        4│    │
         └────┘
           6

   Area 1 = 8 × 5 = 40
   Area 2 = 6 × 3 = 18
   Total = 40 + 18 = 58

3. Verification:
   * Check measurements
   * Confirm calculations
   * Compare to estimates

🤝 Peer Review Benefits:
1. Multiple perspectives
2. Improved clarity
3. Added examples
4. Better explanations

Practice Together:
----------------
Review these shapes:
1. L-shaped garden
2. T-shaped room
3. U-shaped pool

Exchange solutions and:
* Offer constructive feedback
* Suggest improvements
* Share alternative methods
* Help clarify confusion"""
    },
    {
        "style": "Team Discussion",
        "input": "Explain the concept of probability using real-world examples.",
        "output": """Let's explore probability through team discussion! 🗣️

Team Brainstorming Session
-------------------------
🎲 Topic: Understanding Probability

Team Member 1 (Sports Fan):
"In basketball, a player has an 80% free throw average.
This means:
* 0.8 probability of success
* 8 out of 10 shots likely go in
* Can predict long-term performance"

Team Member 2 (Weather Enthusiast):
"Weather forecasts use probability too!
* 30% chance of rain means
* In similar conditions
* It rains 3 out of 10 times"

Team Member 3 (Game Player):
"Card games are perfect examples:
* 1/52 chance of specific card
* 1/4 chance of specific suit
* 1/13 chance of specific value"

Team Discussion Points:
---------------------
1. Common Themes:
   * Frequency of events
   * Long-term patterns
   * Ratio representation

2. Key Insights:
   * Probability = favorable/total
   * Always between 0 and 1
   * Can be shown as %

3. Real Applications:
   * Sports statistics
   * Weather forecasts
   * Games of chance
   * Insurance rates

Team Activity:
------------
Let's analyze this game:
Rolling two dice

👥 Group Analysis:
1. Possible outcomes: 36
2. Getting a sum of 7:
   * Team Member 1: "List combinations"
   * Team Member 2: "Count favorable"
   * Team Member 3: "Calculate probability"

Combined Solution:
6/36 = 1/6 chance of rolling 7

🤝 Team Learning Benefits:
1. Multiple examples
2. Different perspectives
3. Rich discussion
4. Deeper understanding

Practice as Team:
---------------
Analyze these scenarios:
1. Drawing cards
2. Spinning wheels
3. Flipping coins

Team Roles:
* Example provider
* Calculator
* Verifier
* Explainer

Remember:
* Share ideas freely
* Build on others' thoughts
* Ask questions
* Help explain"""
    },
    {
        "style": "Individual Reflection",
        "input": "Guide students through understanding the concept of functions.",
        "output": """Let's explore functions through individual reflection and sharing! 🤔

Personal Understanding Check
--------------------------
📝 Reflect on your knowledge:

1. What do you know about functions?
   * Relationship between inputs/outputs
   * Like a machine that processes values
   * Each input has exactly one output

✍️ Write your thoughts:
"A function is like a recipe:
* Ingredients (inputs)
* Instructions (process)
* Final dish (output)"

2. Real-life Connections
-----------------------
Think about your daily life:
* Temperature converter
* Price calculator
* Time zone converter

🤔 Personal Example:
"My morning routine is a function:
Input: Wake-up time
Process: Get ready steps
Output: Arrival time"

3. Visual Understanding
----------------------
Draw your own diagram:
     INPUT → [FUNCTION] → OUTPUT
     x → [  f(x)  ] → y

✏️ Reflection Questions:
* Why is this useful?
* How does it work?
* Where do you see this?

4. Knowledge Integration
-----------------------
Connect to what you know:
* Math operations
* Computer programs
* Cause and effect

💭 Personal Insights:
"Functions help organize:
* Clear inputs
* Defined process
* Predictable outputs"

5. Application Practice
----------------------
Try these examples:
* f(x) = 2x + 3
* g(x) = x²
* h(x) = 3x - 1

🤔 For each one:
1. What's the input?
2. What's the process?
3. What's the output?

6. Understanding Check
---------------------
Ask yourself:
□ Can I explain functions?
□ Can I identify them?
□ Can I create them?
□ Can I use them?

7. Growth Areas
--------------
Note where you need help:
* Graphing functions
* Composite functions
* Inverse functions

8. Learning Journal
------------------
Record your progress:
* What was new?
* What clicked today?
* What needs work?

9. Share and Compare
-------------------
After reflection:
* Compare with peers
* Share insights
* Ask questions
* Offer help

💡 Personal Growth Tips:
1. Keep notes
2. Make examples
3. Practice regularly
4. Connect ideas

Remember:
* Understanding > memorizing
* Examples help
* Practice matters
* Questions are good

Next Steps:
1. Create your examples
2. Explain to someone
3. Solve new problems
4. Review regularly"""
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
logger = logging.getLogger("demo_09")


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


def analyze_collaboration(results: List[Dict]) -> Dict:
    """Analyze effectiveness of collaboration methods."""
    analysis = {
        "overall_scores": {},
        "collaboration_elements": {},
        "element_effectiveness": {},
        "recommendations": []
    }

    # Track collaboration elements
    element_scores = {
        "group_work": [],
        "peer_feedback": [],
        "discussion": [],
        "reflection": [],
        "interaction": []
    }

    for result in results:
        style = result["style"]
        scores = result["scores"]
        output = result["output"].lower()

        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]

        # Track elements used
        elements_used = []
        if "group" in output or "team" in output or "together" in output:
            elements_used.append("group_work")
            element_scores["group_work"].append(scores["total_score"])
        if "review" in output or "feedback" in output or "suggest" in output:
            elements_used.append("peer_feedback")
            element_scores["peer_feedback"].append(scores["total_score"])
        if "discuss" in output or "share" in output or "talk" in output:
            elements_used.append("discussion")
            element_scores["discussion"].append(scores["total_score"])
        if "reflect" in output or "think" in output or "consider" in output:
            elements_used.append("reflection")
            element_scores["reflection"].append(scores["total_score"])
        if "respond" in output or "ask" in output or "answer" in output:
            elements_used.append("interaction")
            element_scores["interaction"].append(scores["total_score"])

        analysis["collaboration_elements"][style] = elements_used

    # Analyze element effectiveness
    for element, scores in element_scores.items():
        if scores:
            analysis["element_effectiveness"][element] = sum(scores) / len(scores)

    # Generate recommendations
    sorted_elements = sorted(
        analysis["element_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    analysis["recommendations"].extend([
        f"Most effective element: {sorted_elements[0][0]} ({sorted_elements[0][1]:.2f})",
        "Combine multiple collaboration methods",
        "Start with clear group roles",
        "Include peer feedback opportunities",
        "End with individual reflection"
    ])

    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Collaboration Methods Analysis")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Elements Used", style="yellow")

    for result in results:
        style = result["style"]
        elements = analysis["collaboration_elements"][style]
        scores_table.add_row(
            style,
            f"{analysis['overall_scores'][style]:.2f}",
            "\n".join(elements)
        )

    # Elements table
    elements_table = Table(title="Collaboration Element Effectiveness")
    elements_table.add_column("Element", style="cyan")
    elements_table.add_column("Average Score", style="green")

    for element, score in sorted(
        analysis["element_effectiveness"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        elements_table.add_row(
            element.title(),
            f"{score:.2f}"
        )

    # Recommendations table
    recommendations_table = Table(title="Best Practices")
    recommendations_table.add_column("Category", style="cyan")
    recommendations_table.add_column("Details", style="yellow")

    recommendations_table.add_row(
        "Top Element",
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
    console.print(elements_table)
    console.print("\n")
    console.print(recommendations_table)


def save_results(results: Dict):
    """Save results to file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / "demo_09_results.json"

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
            console.print("\n[bold]Testing Collaboration Methods[/bold]")
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
                analysis = analyze_collaboration(scored_cases)
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
    console.print("\n[bold]Running Demo 9: Collaboration Methods Analysis[/bold]")
    asyncio.run(main())
