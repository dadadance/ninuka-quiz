"""Main script to run complete gap analysis pipeline."""

import sys
import traceback
from pathlib import Path
import pandas as pd

# Import gap analysis modules
from gap_analysis.data_loader import load_and_prepare_data
from gap_analysis.quality_checker import analyze_quality
from gap_analysis.ngram_analysis import analyze_ngrams
from gap_analysis.entity_recognition import analyze_entities
from gap_analysis.sociological_taxonomy import analyze_sociological_taxonomy
from gap_analysis.semantic_clustering import analyze_semantic_clustering
from gap_analysis.gap_reporter import synthesize_analyses


def create_output_directories():
    """Create output directories if they don't exist."""
    Path("outputs").mkdir(exist_ok=True)
    print("Output directories created.")


def run_gap_analysis(excel_path: str = "ninouk2.xlsx"):
    """
    Run complete gap analysis pipeline.
    
    Args:
        excel_path: Path to Excel file
    """
    print("=" * 70)
    print("CONTENT GAP ANALYSIS - COMPLETE PIPELINE")
    print("=" * 70)
    print()
    
    try:
        # Create output directories
        create_output_directories()
        
        # Phase 1: Data Preparation
        print("\n" + "=" * 70)
        print("PHASE 1: DATA PREPARATION")
        print("=" * 70)
        df = load_and_prepare_data(excel_path)
        print(f"✓ Loaded and prepared {len(df)} questions")
        
        # Phase 2: Quality Analysis
        print("\n" + "=" * 70)
        print("PHASE 2: QUALITY ANALYSIS")
        print("=" * 70)
        quality_results = analyze_quality(df)
        print("✓ Quality analysis complete")
        
        # Phase 3: N-gram Analysis
        print("\n" + "=" * 70)
        print("PHASE 3: N-GRAM ANALYSIS")
        print("=" * 70)
        ngram_results = analyze_ngrams(df)
        print("✓ N-gram analysis complete")
        
        # Phase 4: Entity Recognition
        print("\n" + "=" * 70)
        print("PHASE 4: ENTITY RECOGNITION")
        print("=" * 70)
        entity_results = analyze_entities(df)
        print("✓ Entity recognition complete")
        
        # Phase 5: Sociological Taxonomy
        print("\n" + "=" * 70)
        print("PHASE 5: SOCIOLOGICAL TAXONOMY")
        print("=" * 70)
        taxonomy_results = analyze_sociological_taxonomy(df)
        print("✓ Sociological taxonomy analysis complete")
        
        # Phase 6: Semantic Clustering
        print("\n" + "=" * 70)
        print("PHASE 6: SEMANTIC CLUSTERING")
        print("=" * 70)
        print("Note: This phase may take several minutes due to embedding generation...")
        semantic_results = analyze_semantic_clustering(df)
        print("✓ Semantic clustering complete")
        
        # Phase 7: Gap Synthesis
        print("\n" + "=" * 70)
        print("PHASE 7: GAP SYNTHESIS & REPORTING")
        print("=" * 70)
        final_results = synthesize_analyses(
            semantic_results,
            entity_results,
            taxonomy_results,
            quality_results,
            ngram_results
        )
        print("✓ Gap synthesis complete")
        
        # Final Summary
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE - SUMMARY")
        print("=" * 70)
        summary = final_results['summary']
        print(f"Missing Themes Identified: {summary['missing_themes']}")
        print(f"Missing Entities Identified: {summary['missing_entities']}")
        print(f"Underrepresented Fields: {summary['underrepresented_fields']}")
        print("\nAll outputs saved to 'outputs/' directory")
        print("\nKey files:")
        print("  - gap_analysis_report.md (comprehensive report)")
        print("  - entity_coverage.csv (entity analysis)")
        print("  - taxonomy_coverage.csv (field coverage)")
        print("  - quality_report.csv (quality metrics)")
        print("  - ngram_patterns.csv (n-gram patterns)")
        print("  - clusters_visualization.png (cluster map)")
        print("  - entity_coverage_chart.png (entity visualization)")
        print("  - taxonomy_coverage_chart.png (taxonomy visualization)")
        print("  - quality_metrics_chart.png (quality visualization)")
        print("\n" + "=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: File not found - {e}")
        print("Please ensure the Excel file exists in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run content gap analysis on quiz dataset")
    parser.add_argument(
        "--excel",
        type=str,
        default="ninouk2.xlsx",
        help="Path to Excel file (default: ninouk2.xlsx)"
    )
    
    args = parser.parse_args()
    run_gap_analysis(args.excel)

