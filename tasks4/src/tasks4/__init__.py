import os
from openai import OpenAI

def inc(n: int) -> int:
    """Required function for assignment pattern."""
    return n + 1


def summarize_task(description: str, api_key: str = None) -> str:
    """
    Send a paragraph-length task description to OpenAI and get a short phrase summary.
    
    Args:
        description: A paragraph-length description of a task
        api_key: OpenAI API key (if None, tries to get from OPENAI_API_KEY env var)
    
    Returns:
        A short phrase summary of the task
    """
    # Get API key from parameter or environment variable
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable "
            "or pass it as a parameter."
        )
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create the prompt for summarization
    prompt = f"""Summarize the following task description into a short, concise phrase (3-8 words).
    
Task description:
{description}

Short phrase summary:"""
    
    try:
        # Call OpenAI Chat Completions API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using gpt-3.5-turbo (ChatGPT-3.5-mini equivalent)
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes task descriptions into short, actionable phrases."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=50,  # Keep summaries short
            temperature=0.3  # Lower temperature for more consistent summaries
        )
        
        # Extract the summary from the response
        summary = response.choices[0].message.content.strip()
        return summary
    
    except Exception as e:
        return f"Error: {str(e)}"


def main() -> None:
    """Main entry point for tasks4 - AI Task Summarization."""
    print("=" * 70)
    print("Task 4: AI-Powered Task Summarization")
    print("=" * 70)
    print("\nThis experiment uses OpenAI's Chat Completions API to summarize")
    print("paragraph-length task descriptions into short, actionable phrases.\n")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: OPENAI_API_KEY environment variable not set.")
        print("   Please set it before running this script:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\n   For now, showing demo mode (will show error messages).\n")
        api_key = None
    
    # Sample paragraph-length task descriptions
    sample_descriptions = [
        """I need to complete my computer science assignment for CSC299. This involves 
creating a comprehensive task management system using Python, writing thorough test 
cases with pytest to ensure all functionality works correctly, documenting everything 
in a detailed README file, and making sure the code follows best practices. The deadline 
is next week and I need to make sure all features are implemented and tested properly.""",
        
        """I have to prepare for my upcoming job interview at a tech company. This means 
I should review common interview questions, practice coding problems on platforms like 
LeetCode, update my resume and portfolio website to highlight my recent projects, 
research the company's products and culture, and prepare thoughtful questions to ask 
the interviewers. I want to make a great impression and show that I'm well-prepared."""
    ]
    
    print(f"Processing {len(sample_descriptions)} task descriptions...\n")
    print("-" * 70)
    
    # Loop through each description and summarize independently
    for i, description in enumerate(sample_descriptions, 1):
        print(f"\n📝 Task Description #{i}:")
        print("-" * 70)
        print(description)
        print("-" * 70)
        
        print("\n🤖 Sending to OpenAI API for summarization...")
        
        try:
            summary = summarize_task(description, api_key)
            print(f"\n✅ Summary: {summary}\n")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
        
        print("=" * 70)
    
    print("\n✨ Summarization complete!")
    print("=" * 70)
