"""Main script to run complete gap analysis pipeline."""

import sys
import traceback
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

# Import gap analysis modules
from gap_analysis.data_loader import load_and_prepare_data
from gap_analysis.quality_checker import analyze_quality
from gap_analysis.ngram_analysis import analyze_ngrams
from gap_analysis.entity_recognition import analyze_entities
from gap_analysis.sociological_taxonomy import analyze_sociological_taxonomy
from gap_analysis.semantic_clustering import analyze_semantic_clustering
from gap_analysis.gap_reporter import synthesize_analyses


def setup_logging():
    """Setup logging to both file and console."""
    log_dir = Path("outputs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Create logger
    logger = logging.getLogger('gap_analysis')
    logger.setLevel(logging.DEBUG)
    
    # File handler with detailed logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler with simpler format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger


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
    logger = setup_logging()
    
    logger.info("=" * 70)
    logger.info("CONTENT GAP ANALYSIS - COMPLETE PIPELINE")
    logger.info("=" * 70)
    logger.info("")
    
    start_time = datetime.now()
    logger.info(f"Pipeline started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Create output directories
        create_output_directories()
        logger.debug("Output directories created")
        
        # Phase 1: Data Preparation
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 1: DATA PREPARATION")
        logger.info("=" * 70)
        phase_start = datetime.now()
        df = load_and_prepare_data(excel_path)
        phase_duration = (datetime.now() - phase_start).total_seconds()
        logger.info(f"✓ Loaded and prepared {len(df)} questions (took {phase_duration:.1f}s)")
        logger.debug(f"DataFrame shape: {df.shape}, columns: {list(df.columns)}")
        
        # Phase 2: Quality Analysis
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 2: QUALITY ANALYSIS")
        logger.info("=" * 70)
        phase_start = datetime.now()
        quality_results = analyze_quality(df)
        phase_duration = (datetime.now() - phase_start).total_seconds()
        logger.info(f"✓ Quality analysis complete (took {phase_duration:.1f}s)")
        logger.debug(f"Quality metrics: {quality_results.get('metrics', {})}")
        
        # Phase 3: N-gram Analysis
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 3: N-GRAM ANALYSIS")
        logger.info("=" * 70)
        phase_start = datetime.now()
        ngram_results = analyze_ngrams(df)
        phase_duration = (datetime.now() - phase_start).total_seconds()
        logger.info(f"✓ N-gram analysis complete (took {phase_duration:.1f}s)")
        logger.debug(f"Extracted n-grams: {len(ngram_results.get('question_ngrams', {}).get('top_bigrams', []))} bigrams")
        
        # Phase 4: Entity Recognition
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 4: ENTITY RECOGNITION")
        logger.info("=" * 70)
        logger.info("This phase processes all questions with spaCy NER (may take 5-10 minutes)...")
        phase_start = datetime.now()
        entity_results = analyze_entities(df)
        phase_duration = (datetime.now() - phase_start).total_seconds()
        logger.info(f"✓ Entity recognition complete (took {phase_duration:.1f}s)")
        logger.debug(f"Entity coverage: {entity_results.get('coverage_analysis', {})}")
        
        # Phase 5: Sociological Taxonomy
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 5: SOCIOLOGICAL TAXONOMY")
        logger.info("=" * 70)
        phase_start = datetime.now()
        taxonomy_results = analyze_sociological_taxonomy(df)
        phase_duration = (datetime.now() - phase_start).total_seconds()
        logger.info(f"✓ Sociological taxonomy analysis complete (took {phase_duration:.1f}s)")
        logger.debug(f"Underrepresented fields: {taxonomy_results.get('underrepresented_fields', [])}")
        
        # Phase 6: Semantic Clustering
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 6: SEMANTIC CLUSTERING")
        logger.info("=" * 70)
        logger.info("Note: This phase may take 20-40 minutes due to embedding generation for 12,909 questions...")
        logger.info("Progress will be shown as embeddings are generated...")
        phase_start = datetime.now()
        semantic_results = analyze_semantic_clustering(df)
        phase_duration = (datetime.now() - phase_start).total_seconds()
        logger.info(f"✓ Semantic clustering complete (took {phase_duration:.1f}s)")
        logger.debug(f"Discovered clusters: {semantic_results.get('missing_clusters', {}).get('num_clusters', 0)}")
        
        # Phase 7: Gap Synthesis
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 7: GAP SYNTHESIS & REPORTING")
        logger.info("=" * 70)
        phase_start = datetime.now()
        final_results = synthesize_analyses(
            semantic_results,
            entity_results,
            taxonomy_results,
            quality_results,
            ngram_results
        )
        phase_duration = (datetime.now() - phase_start).total_seconds()
        logger.info(f"✓ Gap synthesis complete (took {phase_duration:.1f}s)")
        
        # Final Summary
        total_duration = (datetime.now() - start_time).total_seconds()
        logger.info("\n" + "=" * 70)
        logger.info("ANALYSIS COMPLETE - SUMMARY")
        logger.info("=" * 70)
        summary = final_results['summary']
        logger.info(f"Missing Themes Identified: {summary['missing_themes']}")
        logger.info(f"Missing Entities Identified: {summary['missing_entities']}")
        logger.info(f"Underrepresented Fields: {summary['underrepresented_fields']}")
        logger.info(f"\nTotal pipeline duration: {total_duration/60:.1f} minutes ({total_duration:.1f} seconds)")
        logger.info("\nAll outputs saved to 'outputs/' directory")
        logger.info("\nKey files:")
        logger.info("  - gap_analysis_report.md (comprehensive report)")
        logger.info("  - entity_coverage.csv (entity analysis)")
        logger.info("  - taxonomy_coverage.csv (field coverage)")
        logger.info("  - quality_report.csv (quality metrics)")
        logger.info("  - ngram_patterns.csv (n-gram patterns)")
        logger.info("  - clusters_visualization.png (cluster map)")
        logger.info("  - entity_coverage_chart.png (entity visualization)")
        logger.info("  - taxonomy_coverage_chart.png (taxonomy visualization)")
        logger.info("  - quality_metrics_chart.png (quality visualization)")
        logger.info("\n" + "=" * 70)
        logger.info(f"Pipeline completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error("Please ensure the Excel file exists in the current directory.")
        logger.exception("Full error details:")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.warning("\nPipeline interrupted by user (Ctrl+C)")
        logger.info("Partial results may be available in outputs/ directory")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        logger.exception("Full traceback:")
        logger.error(f"Pipeline failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("Check the log file for detailed error information")
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

