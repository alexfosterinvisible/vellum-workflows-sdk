"""Demo 4: Engagement Score Optimization.

This demo shows:
1. Testing engagement-focused response patterns
2. Analyzing interaction elements
3. Optimizing for user engagement
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
    "name": "Math Engagement Optimization",
    "description": """Evaluate mathematical explanations with a focus on engagement.
    Test various interactive elements, questioning strategies, and engagement patterns
    to identify optimal approaches for maintaining user interest and participation."""
}

TEST_CASES = [
    {
        "style": "Interactive Discovery",
        "input": "What is 12 divided by 4?",
        "output": """Let's discover this together! 🎯

🤔 First, let's think: What does division mean to you?
(It's like sharing things equally among friends!)

Let's explore with a game:
Imagine you have 12 cookies: 🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪

Question 1: If you share them with 4 friends, how many piles would you make?
[Wait for it...]
Answer: We'd make 4 piles!

Question 2: Now, can you help me put the cookies in equal piles?
Let's do it together:
Pile 1: 🍪🍪🍪
Pile 2: 🍪🍪🍪
Pile 3: 🍪🍪🍪
Pile 4: 🍪🍪🍪

Amazing! What do you notice? Each pile has exactly 3 cookies!

So, 12 ÷ 4 = 3 because when we share 12 cookies among 4 friends,
each friend gets 3 cookies! 

🌟 Bonus Challenge: Can you think of another real-life situation
where you might need to divide 12 by 4?"""
    },
    {
        "style": "Story-based Learning",
        "input": "What is 12 divided by 4?",
        "output": """🎮 Welcome to the Pizza Party Adventure! 🍕

Our story begins at Alex's birthday party...

Alex has ordered 12 slices of pizza for their 4 best friends.
Being a fair host, Alex wants everyone to get the same amount.

Let's help Alex solve this puzzle:

1. Count the pizza slices: 
   🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕
   "Wow, that's a lot of pizza!" says Alex.

2. Look at the friends waiting:
   👧 Sarah is hungry!
   👦 Tom can't wait!
   👧 Maya is excited!
   👦 Jack is ready!

3. Time to share:
   Sarah gets: 🍕🍕🍕
   Tom gets: 🍕🍕🍕
   Maya gets: 🍕🍕🍕
   Jack gets: 🍕🍕🍕

"Perfect!" Alex exclaims. "Everyone got 3 slices!"

🎯 The Math Magic:
12 pizza slices ÷ 4 friends = 3 slices each

🌟 Party Success! Everyone's happy because:
- Each friend got the same amount (3 slices)
- All 12 slices were shared
- The party was fair and fun!

Can you help plan the next party? How many slices would we need for 6 friends?"""
    },
    {
        "style": "Challenge-based",
        "input": "What is 12 divided by 4?",
        "output": """🎮 Welcome to the Division Challenge! 

Level 1: The Setup
-----------------
Mission: Divide 12 objects into 4 equal groups
Tools: 12 stars ⭐
Goal: Find how many stars each group gets

Level 2: Visual Challenge
------------------------
Can you spot the pattern?

⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐

🏆 Achievement Unlocked: Pattern Recognition!
Each group has exactly 3 stars!

Level 3: Verification
--------------------
Let's check our answer:
✓ Groups: 4
✓ Stars per group: 3
✓ Total stars: 4 × 3 = 12

🎯 Final Answer: 12 ÷ 4 = 3

🌟 Bonus Challenges:
1. Can you rearrange the stars differently while keeping groups equal?
2. What if we had 16 stars and 4 groups?
3. Try creating your own division puzzle!

Level Complete! 🎉
Score: ⭐⭐⭐
You've mastered 12 ÷ 4 = 3!"""
    },
    {
        "style": "Guided Discovery",
        "input": "What is 12 divided by 4?",
        "output": """🔍 Let's solve this mystery together!

Step 1: Understanding Our Goal
-----------------------------
Q: What are we trying to find out?
A: How many items each group gets when we divide 12 by 4

Step 2: Visualization
--------------------
Here's our starting point:
🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵

Think & Try:
1. Can you mentally group these into 4 equal parts?
2. How many would be in each group?

Step 3: Interactive Grouping
---------------------------
Let's group them together:

Group 1: 🔵🔵🔵
Group 2: 🔵🔵🔵
Group 3: 🔵🔵🔵
Group 4: 🔵🔵🔵

Quick Check:
- Did we use all 12 circles? ✓
- Do all groups have the same amount? ✓
- How many groups did we make? ✓

Step 4: Discovery
----------------
What did we discover?
Each group has exactly 3 circles!

Therefore: 12 ÷ 4 = 3

💡 Think About It:
- Why does this make sense?
- Where might you use this in real life?
- Can you create a similar problem?

🌟 You've solved it! The answer is 3, and now you know why!"""
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
logger = logging.getLogger("demo_04")


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


def analyze_engagement(results: List[Dict]) -> Dict:
    """Analyze engagement patterns across styles."""
    analysis = {
        "overall_scores": {},
        "engagement_patterns": [],
        "interactive_elements": {},
        "recommendations": []
    }
    
    # Track engagement elements
    element_scores = {
        "questions": [],
        "challenges": [],
        "storytelling": [],
        "visuals": [],
        "feedback": []
    }
    
    for result in results:
        style = result["style"]
        scores = result["scores"]
        
        # Overall scores
        analysis["overall_scores"][style] = scores["total_score"]
        
        # Extract engagement-related dimensions
        engagement_dims = {
            k: v["total_score"]
            for k, v in scores["dimension_scores"].items()
            if "engagement" in k.lower() or "interaction" in k.lower()
        }
        
        # Track elements
        output = result["output"].lower()
        if "?" in output:
            element_scores["questions"].append(scores["total_score"])
        if "challenge" in output or "try" in output:
            element_scores["challenges"].append(scores["total_score"])
        if "story" in output or "adventure" in output:
            element_scores["storytelling"].append(scores["total_score"])
        if any(emoji in output for emoji in ["🌟", "⭐", "🔵", "🍕", "🍪"]):
            element_scores["visuals"].append(scores["total_score"])
        if "amazing" in output or "perfect" in output or "great" in output:
            element_scores["feedback"].append(scores["total_score"])
    
    # Analyze element effectiveness
    for element, scores in element_scores.items():
        if scores:
            avg_score = sum(scores) / len(scores)
            analysis["interactive_elements"][element] = avg_score
    
    # Sort styles by score
    sorted_styles = sorted(
        analysis["overall_scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # Generate recommendations
    top_elements = sorted(
        analysis["interactive_elements"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    analysis["engagement_patterns"] = [
        f"{style} ({score:.2f})"
        for style, score in sorted_styles
    ]
    
    analysis["recommendations"] = [
        f"Use {element} (score: {score:.2f})"
        for element, score in top_elements[:3]
    ]
    
    return analysis


def display_results(results: List[Dict], analysis: Dict):
    """Display results and analysis."""
    # Scores table
    scores_table = Table(title="Engagement Style Comparison")
    scores_table.add_column("Style", style="cyan")
    scores_table.add_column("Total Score", style="green")
    scores_table.add_column("Engagement Elements", style="yellow")
    
    for result in results:
        style = result["style"]
        scores = result["scores"]
        
        # Count engagement elements
        output = result["output"].lower()
        elements = []
        if "?" in output:
            elements.append("Questions")
        if "challenge" in output or "try" in output:
            elements.append("Challenges")
        if "story" in output or "adventure" in output:
            elements.append("Storytelling")
        if any(emoji in output for emoji in ["🌟", "⭐", "🔵", "🍕", "🍪"]):
            elements.append("Visuals")
        if "amazing" in output or "perfect" in output or "great" in output:
            elements.append("Feedback")
        
        scores_table.add_row(
            style,
            f"{scores['total_score']:.2f}",
            "\n".join(elements)
        )
    
    # Elements table
    elements_table = Table(title="Interactive Elements Analysis")
    elements_table.add_column("Element", style="cyan")
    elements_table.add_column("Average Score", style="green")
    
    for element, score in sorted(
        analysis["interactive_elements"].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        elements_table.add_row(
            element.title(),
            f"{score:.2f}"
        )
    
    # Recommendations table
    recommendations_table = Table(title="Engagement Recommendations")
    recommendations_table.add_column("Category", style="cyan")
    recommendations_table.add_column("Details", style="yellow")
    
    recommendations_table.add_row(
        "Top Styles",
        "\n".join(analysis["engagement_patterns"][:2])
    )
    recommendations_table.add_row(
        "Best Elements",
        "\n".join(analysis["recommendations"])
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
    output_file = OUTPUT_DIR / "demo_04_results.json"
    
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
            console.print("\n[bold]Testing Engagement Styles[/bold]")
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
                analysis = analyze_engagement(scored_cases)
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
    console.print("\n[bold]Running Demo 4: Engagement Optimization[/bold]")
    asyncio.run(main()) 