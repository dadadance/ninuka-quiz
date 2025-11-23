"""Main script to generate questions from gap analysis."""

import sys
from pathlib import Path
from question_generator.question_generator import generate_questions_from_gaps
from question_generator.question_validator import validate_dataframe, filter_valid_questions
from question_generator.question_exporter import export_to_excel, export_to_csv


def generate_questions(num_questions: int = 100, output_format: str = "excel", 
                      min_tags: int = 2, max_tags: int = 5):
    """
    Generate questions from gap analysis.
    
    Args:
        num_questions: Number of questions to generate
        output_format: Output format ('excel', 'csv', or 'both')
        min_tags: Minimum number of tags per question
        max_tags: Maximum number of tags per question
    """
    print("=" * 70)
    print("QUESTION GENERATOR - FROM GAP ANALYSIS")
    print("=" * 70)
    print()
    
    # Check if gap analysis exists
    gap_report = Path("outputs/gap_analysis_report.md")
    if not gap_report.exists():
        print("⚠️  Warning: Gap analysis report not found.")
        print("   Running with limited gap data. For best results, run gap analysis first.")
        print()
    
    # Generate questions
    print(f"Generating {num_questions} questions from gap analysis...")
    df = generate_questions_from_gaps(num_questions)
    
    if len(df) == 0:
        print("❌ No questions generated. Check gap analysis results.")
        sys.exit(1)
    
    print(f"✓ Generated {len(df)} questions")
    
    # Validate questions
    print("\nValidating questions...")
    df_validated = validate_dataframe(df)
    
    # Filter to only valid questions
    df_valid = filter_valid_questions(df_validated)
    
    if len(df_valid) == 0:
        print("❌ No valid questions after validation.")
        print("   Check validation errors above.")
        sys.exit(1)
    
    print(f"✓ {len(df_valid)} valid questions ready for export")
    
    # Export
    print(f"\nExporting questions ({output_format})...")
    print(f"Applying tags: {min_tags} to {max_tags} per question")
    
    if output_format in ['excel', 'both']:
        export_to_excel(df_valid, "outputs/generated_questions.xlsx", 
                       min_tags=min_tags, max_tags=max_tags)
    
    if output_format in ['csv', 'both']:
        export_to_csv(df_valid, "outputs/generated_questions.csv",
                     min_tags=min_tags, max_tags=max_tags)
    
    # Summary
    print("\n" + "=" * 70)
    print("QUESTION GENERATION COMPLETE")
    print("=" * 70)
    print(f"Total generated: {len(df)}")
    print(f"Valid questions: {len(df_valid)}")
    print(f"Invalid questions: {len(df) - len(df_valid)}")
    print(f"\nOutput files:")
    if output_format in ['excel', 'both']:
        print(f"  - outputs/generated_questions.xlsx (Includes 'tags' sheet)")
    if output_format in ['csv', 'both']:
        print(f"  - outputs/generated_questions.csv")
    print("=" * 70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate questions from gap analysis")
    parser.add_argument(
        "--num",
        type=int,
        default=100,
        help="Number of questions to generate (default: 100)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=['excel', 'csv', 'both'],
        default='excel',
        help="Output format (default: excel)"
    )
    parser.add_argument(
        "--min-tags",
        type=int,
        default=2,
        help="Minimum number of tags per question (default: 2)"
    )
    parser.add_argument(
        "--max-tags",
        type=int,
        default=5,
        help="Maximum number of tags per question (default: 5)"
    )
    
    args = parser.parse_args()
    generate_questions(args.num, args.format, args.min_tags, args.max_tags)
