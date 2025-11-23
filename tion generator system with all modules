[1mdiff --git a/gap_analysis/entity_recognition.py b/gap_analysis/entity_recognition.py[m
[1mindex 075e8ba..de84c26 100644[m
[1m--- a/gap_analysis/entity_recognition.py[m
[1m+++ b/gap_analysis/entity_recognition.py[m
[36m@@ -53,7 +53,9 @@[m [mdef extract_all_entities(df: pd.DataFrame, nlp) -> Dict[str, Any]:[m
     Returns:[m
         Dictionary with entity analysis[m
     """[m
[31m-    print("Extracting entities from questions and answers...")[m
[32m+[m[32m    total = len(df)[m[41m[m
[32m+[m[32m    print(f"Extracting entities from {total} questions and answers...")[m[41m[m
[32m+[m[32m    print("This may take several minutes. Progress will be shown every 1000 questions...")[m[41m[m
     [m
     all_entities = defaultdict(lambda: Counter())[m
     question_entities = defaultdict(lambda: Counter())[m
[36m@@ -61,6 +63,9 @@[m [mdef extract_all_entities(df: pd.DataFrame, nlp) -> Dict[str, Any]:[m
     [m
     # Extract from questions[m
     for idx, row in df.iterrows():[m
[32m+[m[32m        if (idx + 1) % 1000 == 0:[m[41m[m
[32m+[m[32m            print(f"  Processed {idx + 1}/{total} questions ({(idx+1)/total*100:.1f}%)...")[m[41m[m
[32m+[m[41m        [m
         q_entities = extract_entities(row.get('QEN', ''), nlp)[m
         for ent_type, ent_list in q_entities.items():[m
             question_entities[ent_type].update(ent_list)[m
[36m@@ -74,6 +79,8 @@[m [mdef extract_all_entities(df: pd.DataFrame, nlp) -> Dict[str, Any]:[m
                     answer_entities[ent_type].update(ent_list)[m
                     all_entities[ent_type].update(ent_list)[m
     [m
[32m+[m[32m    print(f"✓ Completed entity extraction for all {total} questions")[m[41m[m
[32m+[m[41m    [m
     return {[m
         'all_entities': dict(all_entities),[m
         'question_entities': dict(question_entities),[m
[36m@@ -249,7 +256,22 @@[m [mdef analyze_entities(df: pd.DataFrame) -> Dict[str, Any]:[m
         Dictionary with all entity analysis results[m
     """[m
     print("Loading spaCy model...")[m
[31m-    nlp = load_spacy_model()[m
[32m+[m[32m    try:[m[41m[m
[32m+[m[32m        nlp = load_spacy_model()[m[41m[m
[32m+[m[32m    except Exception as e:[m[41m[m
[32m+[m[32m        print(f"⚠️  Warning: Could not load spaCy model: {e}")[m[41m[m
[32m+[m[32m        print("   Skipping entity recognition. Using reference lists only.")[m[41m[m
[32m+[m[32m        # Return empty structure so pipeline can continue[m[41m[m
[32m+[m[32m        return {[m[41m[m
[32m+[m[32m            'coverage_analysis': {[m[41m[m
[32m+[m[32m                'entity_data': {},[m[41m[m
[32m+[m[32m                'countries': {'missing': [], 'found': [], 'coverage_pct': 0.0},[m[41m[m
[32m+[m[32m                'artists': {'missing': [], 'found': [], 'coverage_pct': 0.0},[m[41m[m
[32m+[m[32m                'movies': {'missing': [], 'found': [], 'coverage_pct': 0.0},[m[41m[m
[32m+[m[32m                'brands': {'missing': [], 'found': [], 'coverage_pct': 0.0}[m[41m[m
[32m+[m[32m            },[m[41m[m
[32m+[m[32m            'report_df': pd.DataFrame()[m[41m[m
[32m+[m[32m        }[m[41m[m
     [m
     coverage_analysis = analyze_entity_coverage(df, nlp)[m
     [m
[1mdiff --git a/run_gap_analysis.py b/run_gap_analysis.py[m
[1mindex 6c4c32a..a44b6eb 100644[m
[1m--- a/run_gap_analysis.py[m
[1m+++ b/run_gap_analysis.py[m
[36m@@ -2,7 +2,9 @@[m
 [m
 import sys[m
 import traceback[m
[32m+[m[32mimport logging[m[41m[m
 from pathlib import Path[m
[32m+[m[32mfrom datetime import datetime[m[41m[m
 import pandas as pd[m
 [m
 # Import gap analysis modules[m
[36m@@ -15,6 +17,39 @@[m [mfrom gap_analysis.semantic_clustering import analyze_semantic_clustering[m
 from gap_analysis.gap_reporter import synthesize_analyses[m
 [m
 [m
[32m+[m[32mdef setup_logging():[m[41m[m
[32m+[m[32m    """Setup logging to both file and console."""[m[41m[m
[32m+[m[32m    log_dir = Path("outputs")[m[41m[m
[32m+[m[32m    log_dir.mkdir(exist_ok=True)[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    # Create logger[m[41m[m
[32m+[m[32m    logger = logging.getLogger('gap_analysis')[m[41m[m
[32m+[m[32m    logger.setLevel(logging.DEBUG)[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    # File handler with detailed logging[m[41m[m
[32m+[m[32m    file_handler = logging.FileHandler(log_file)[m[41m[m
[32m+[m[32m    file_handler.setLevel(logging.DEBUG)[m[41m[m
[32m+[m[32m    file_formatter = logging.Formatter([m[41m[m
[32m+[m[32m        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',[m[41m[m
[32m+[m[32m        datefmt='%Y-%m-%d %H:%M:%S'[m[41m[m
[32m+[m[32m    )[m[41m[m
[32m+[m[32m    file_handler.setFormatter(file_formatter)[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    # Console handler with simpler format[m[41m[m
[32m+[m[32m    console_handler = logging.StreamHandler(sys.stdout)[m[41m[m
[32m+[m[32m    console_handler.setLevel(logging.INFO)[m[41m[m
[32m+[m[32m    console_formatter = logging.Formatter('%(message)s')[m[41m[m
[32m+[m[32m    console_handler.setFormatter(console_formatter)[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    logger.addHandler(file_handler)[m[41m[m
[32m+[m[32m    logger.addHandler(console_handler)[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    logger.info(f"Logging initialized. Log file: {log_file}")[m[41m[m
[32m+[m[32m    return logger[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
 def create_output_directories():[m
     """Create output directories if they don't exist."""[m
     Path("outputs").mkdir(exist_ok=True)[m
[36m@@ -28,62 +63,89 @@[m [mdef run_gap_analysis(excel_path: str = "ninouk2.xlsx"):[m
     Args:[m
         excel_path: Path to Excel file[m
     """[m
[31m-    print("=" * 70)[m
[31m-    print("CONTENT GAP ANALYSIS - COMPLETE PIPELINE")[m
[31m-    print("=" * 70)[m
[31m-    print()[m
[32m+[m[32m    logger = setup_logging()[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    logger.info("=" * 70)[m[41m[m
[32m+[m[32m    logger.info("CONTENT GAP ANALYSIS - COMPLETE PIPELINE")[m[41m[m
[32m+[m[32m    logger.info("=" * 70)[m[41m[m
[32m+[m[32m    logger.info("")[m[41m[m
[32m+[m[41m    [m
[32m+[m[32m    start_time = datetime.now()[m[41m[m
[32m+[m[32m    logger.info(f"Pipeline started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")[m[41m[m
     [m
     try:[m
         # Create output directories[m
         create_output_directories()[m
[32m+[m[32m        logger.debug("Output directories created")[m[41m[m
         [m
         # Phase 1: Data Preparation[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("PHASE 1: DATA PREPARATION")[m
[31m-        print("=" * 70)[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("PHASE 1: DATA PREPARATION")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
[32m+[m[32m        phase_start = datetime.now()[m[41m[m
         df = load_and_prepare_data(excel_path)[m
[31m-        print(f"✓ Loaded and prepared {len(df)} questions")[m
[32m+[m[32m        phase_duration = (datetime.now() - phase_start).total_seconds()[m[41m[m
[32m+[m[32m        logger.info(f"✓ Loaded and prepared {len(df)} questions (took {phase_duration:.1f}s)")[m[41m[m
[32m+[m[32m        logger.debug(f"DataFrame shape: {df.shape}, columns: {list(df.columns)}")[m[41m[m
         [m
         # Phase 2: Quality Analysis[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("PHASE 2: QUALITY ANALYSIS")[m
[31m-        print("=" * 70)[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("PHASE 2: QUALITY ANALYSIS")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
[32m+[m[32m        phase_start = datetime.now()[m[41m[m
         quality_results = analyze_quality(df)[m
[31m-        print("✓ Quality analysis complete")[m
[32m+[m[32m        phase_duration = (datetime.now() - phase_start).total_seconds()[m[41m[m
[32m+[m[32m        logger.info(f"✓ Quality analysis complete (took {phase_duration:.1f}s)")[m[41m[m
[32m+[m[32m        logger.debug(f"Quality metrics: {quality_results.get('metrics', {})}")[m[41m[m
         [m
         # Phase 3: N-gram Analysis[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("PHASE 3: N-GRAM ANALYSIS")[m
[31m-        print("=" * 70)[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("PHASE 3: N-GRAM ANALYSIS")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
[32m+[m[32m        phase_start = datetime.now()[m[41m[m
         ngram_results = analyze_ngrams(df)[m
[31m-        print("✓ N-gram analysis complete")[m
[32m+[m[32m        phase_duration = (datetime.now() - phase_start).total_seconds()[m[41m[m
[32m+[m[32m        logger.info(f"✓ N-gram analysis complete (took {phase_duration:.1f}s)")[m[41m[m
[32m+[m[32m        logger.debug(f"Extracted n-grams: {len(ngram_results.get('question_ngrams', {}).get('top_bigrams', []))} bigrams")[m[41m[m
         [m
         # Phase 4: Entity Recognition[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("PHASE 4: ENTITY RECOGNITION")[m
[31m-        print("=" * 70)[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("PHASE 4: ENTITY RECOGNITION")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
[32m+[m[32m        logger.info("This phase processes all questions with spaCy NER (may take 5-10 minutes)...")[m[41m[m
[32m+[m[32m        phase_start = datetime.now()[m[41m[m
         entity_results = analyze_entities(df)[m
[31m-        print("✓ Entity recognition complete")[m
[32m+[m[32m        phase_duration = (datetime.now() - phase_start).total_seconds()[m[41m[m
[32m+[m[32m        logger.info(f"✓ Entity recognition complete (took {phase_duration:.1f}s)")[m[41m[m
[32m+[m[32m        logger.debug(f"Entity coverage: {entity_results.get('coverage_analysis', {})}")[m[41m[m
         [m
         # Phase 5: Sociological Taxonomy[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("PHASE 5: SOCIOLOGICAL TAXONOMY")[m
[31m-        print("=" * 70)[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("PHASE 5: SOCIOLOGICAL TAXONOMY")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
[32m+[m[32m        phase_start = datetime.now()[m[41m[m
         taxonomy_results = analyze_sociological_taxonomy(df)[m
[31m-        print("✓ Sociological taxonomy analysis complete")[m
[32m+[m[32m        phase_duration = (datetime.now() - phase_start).total_seconds()[m[41m[m
[32m+[m[32m        logger.info(f"✓ Sociological taxonomy analysis complete (took {phase_duration:.1f}s)")[m[41m[m
[32m+[m[32m        logger.debug(f"Underrepresented fields: {taxonomy_results.get('underrepresented_fields', [])}")[m[41m[m
         [m
         # Phase 6: Semantic Clustering[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("PHASE 6: SEMANTIC CLUSTERING")[m
[31m-        print("=" * 70)[m
[31m-        print("Note: This phase may take several minutes due to embedding generation...")[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("PHASE 6: SEMANTIC CLUSTERING")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
[32m+[m[32m        logger.info("Note: This phase may take 20-40 minutes due to embedding generation for 12,909 questions...")[m[41m[m
[32m+[m[32m        logger.info("Progress will be shown as embeddings are generated...")[m[41m[m
[32m+[m[32m        phase_start = datetime.now()[m[41m[m
         semantic_results = analyze_semantic_clustering(df)[m
[31m-        print("✓ Semantic clustering complete")[m
[32m+[m[32m        phase_duration = (datetime.now() - phase_start).total_seconds()[m[41m[m
[32m+[m[32m        logger.info(f"✓ Semantic clustering complete (took {phase_duration:.1f}s)")[m[41m[m
[32m+[m[32m        logger.debug(f"Discovered clusters: {semantic_results.get('missing_clusters', {}).get('num_clusters', 0)}")[m[41m[m
         [m
         # Phase 7: Gap Synthesis[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("PHASE 7: GAP SYNTHESIS & REPORTING")[m
[31m-        print("=" * 70)[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("PHASE 7: GAP SYNTHESIS & REPORTING")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
[32m+[m[32m        phase_start = datetime.now()[m[41m[m
         final_results = synthesize_analyses([m
             semantic_results,[m
             entity_results,[m
[36m@@ -91,37 +153,47 @@[m [mdef run_gap_analysis(excel_path: str = "ninouk2.xlsx"):[m
             quality_results,[m
             ngram_results[m
         )[m
[31m-        print("✓ Gap synthesis complete")[m
[32m+[m[32m        phase_duration = (datetime.now() - phase_start).total_seconds()[m[41m[m
[32m+[m[32m        logger.info(f"✓ Gap synthesis complete (took {phase_duration:.1f}s)")[m[41m[m
         [m
         # Final Summary[m
[31m-        print("\n" + "=" * 70)[m
[31m-        print("ANALYSIS COMPLETE - SUMMARY")[m
[31m-        print("=" * 70)[m
[32m+[m[32m        total_duration = (datetime.now() - start_time).total_seconds()[m[41m[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info("ANALYSIS COMPLETE - SUMMARY")[m[41m[m
[32m+[m[32m        logger.info("=" * 70)[m[41m[m
         summary = final_results['summary'][m
[31m-        print(f"Missing Themes Identified: {summary['missing_themes']}")[m
[31m-        print(f"Missing Entities Identified: {summary['missing_entities']}")[m
[31m-        print(f"Underrepresented Fields: {summary['underrepresented_fields']}")[m
[31m-        print("\nAll outputs saved to 'outputs/' directory")[m
[31m-        print("\nKey files:")[m
[31m-        print("  - gap_analysis_report.md (comprehensive report)")[m
[31m-        print("  - entity_coverage.csv (entity analysis)")[m
[31m-        print("  - taxonomy_coverage.csv (field coverage)")[m
[31m-        print("  - quality_report.csv (quality metrics)")[m
[31m-        print("  - ngram_patterns.csv (n-gram patterns)")[m
[31m-        print("  - clusters_visualization.png (cluster map)")[m
[31m-        print("  - entity_coverage_chart.png (entity visualization)")[m
[31m-        print("  - taxonomy_coverage_chart.png (taxonomy visualization)")[m
[31m-        print("  - quality_metrics_chart.png (quality visualization)")[m
[31m-        print("\n" + "=" * 70)[m
[32m+[m[32m        logger.info(f"Missing Themes Identified: {summary['missing_themes']}")[m[41m[m
[32m+[m[32m        logger.info(f"Missing Entities Identified: {summary['missing_entities']}")[m[41m[m
[32m+[m[32m        logger.info(f"Underrepresented Fields: {summary['underrepresented_fields']}")[m[41m[m
[32m+[m[32m        logger.info(f"\nTotal pipeline duration: {total_duration/60:.1f} minutes ({total_duration:.1f} seconds)")[m[41m[m
[32m+[m[32m        logger.info("\nAll outputs saved to 'outputs/' directory")[m[41m[m
[32m+[m[32m        logger.info("\nKey files:")[m[41m[m
[32m+[m[32m        logger.info("  - gap_analysis_report.md (comprehensive report)")[m[41m[m
[32m+[m[32m        logger.info("  - entity_coverage.csv (entity analysis)")[m[41m[m
[32m+[m[32m        logger.info("  - taxonomy_coverage.csv (field coverage)")[m[41m[m
[32m+[m[32m        logger.info("  - quality_report.csv (quality metrics)")[m[41m[m
[32m+[m[32m        logger.info("  - ngram_patterns.csv (n-gram patterns)")[m[41m[m
[32m+[m[32m        logger.info("  - clusters_visualization.png (cluster map)")[m[41m[m
[32m+[m[32m        logger.info("  - entity_coverage_chart.png (entity visualization)")[m[41m[m
[32m+[m[32m        logger.info("  - taxonomy_coverage_chart.png (taxonomy visualization)")[m[41m[m
[32m+[m[32m        logger.info("  - quality_metrics_chart.png (quality visualization)")[m[41m[m
[32m+[m[32m        logger.info("\n" + "=" * 70)[m[41m[m
[32m+[m[32m        logger.info(f"Pipeline completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")[m[41m[m
         [m
     except FileNotFoundError as e:[m
[31m-        print(f"\n❌ Error: File not found - {e}")[m
[31m-        print("Please ensure the Excel file exists in the current directory.")[m
[32m+[m[32m        logger.error(f"File not found: {e}")[m[41m[m
[32m+[m[32m        logger.error("Please ensure the Excel file exists in the current directory.")[m[41m[m
[32m+[m[32m        logger.exception("Full error details:")[m[41m[m
         sys.exit(1)[m
[32m+[m[32m    except KeyboardInterrupt:[m[41m[m
[32m+[m[32m        logger.warning("\nPipeline interrupted by user (Ctrl+C)")[m[41m[m
[32m+[m[32m        logger.info("Partial results may be available in outputs/ directory")[m[41m[m
[32m+[m[32m        sys.exit(130)[m[41m[m
     except Exception as e:[m
[31m-        print(f"\n❌ Error during analysis: {e}")[m
[31m-        print("\nFull traceback:")[m
[31m-        traceback.print_exc()[m
[32m+[m[32m        logger.error(f"Error during analysis: {e}")[m[41m[m
[32m+[m[32m        logger.exception("Full traceback:")[m[41m[m
[32m+[m[32m        logger.error(f"Pipeline failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")[m[41m[m
[32m+[m[32m        logger.info("Check the log file for detailed error information")[m[41m[m
         sys.exit(1)[m
 [m
 [m
[1mdiff --git a/uv.lock b/uv.lock[m
[1mindex 504d81c..f4c4c44 100644[m
[1m--- a/uv.lock[m
[1m+++ b/uv.lock[m
[36m@@ -2,6 +2,246 @@[m [mversion = 1[m
 revision = 2[m
 requires-python = ">=3.13"[m
 [m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "annotated-types"[m
[32m+[m[32mversion = "0.7.0"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/ee/67/531ea369ba64dcff5ec9c3402f9f51bf748cec26dde048a2f973a4eea7f5/annotated_types-0.7.0.tar.gz", hash = "sha256:aff07c09a53a08bc8cfccb9c85b05f1aa9a2a6f23728d790723543408344ce89", size = 16081, upload_time = "2024-05-20T21:33:25.928Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/78/b6/6307fbef88d9b5ee7421e68d78a9f162e0da4900bc5f5793f6d3d0e34fb8/annotated_types-0.7.0-py3-none-any.whl", hash = "sha256:1f02e8b43a8fbbc3f3e0d4f0f4bfc8131bcb4eebe8849b8e5c773f3a1c582a53", size = 13643, upload_time = "2024-05-20T21:33:24.1Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "blis"[m
[32m+[m[32mversion = "1.3.3"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32mdependencies = [[m
[32m+[m[32m    { name = "numpy" },[m
[32m+[m[32m][m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/d0/d0/d8cc8c9a4488a787e7fa430f6055e5bd1ddb22c340a751d9e901b82e2efe/blis-1.3.3.tar.gz", hash = "sha256:034d4560ff3cc43e8aa37e188451b0440e3261d989bb8a42ceee865607715ecd", size = 2644873, upload_time = "2025-11-17T12:28:30.511Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e6/f7/d26e62d9be3d70473a63e0a5d30bae49c2fe138bebac224adddcdef8a7ce/blis-1.3.3-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:1e647341f958421a86b028a2efe16ce19c67dba2a05f79e8f7e80b1ff45328aa", size = 6928322, upload_time = "2025-11-17T12:27:57.965Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/4a/78/750d12da388f714958eb2f2fd177652323bbe7ec528365c37129edd6eb84/blis-1.3.3-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:d563160f874abb78a57e346f07312c5323f7ad67b6370052b6b17087ef234a8e", size = 1229635, upload_time = "2025-11-17T12:28:00.118Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e8/36/eac4199c5b200a5f3e93cad197da8d26d909f218eb444c4f552647c95240/blis-1.3.3-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:30b8a5b90cb6cb81d1ada9ae05aa55fb8e70d9a0ae9db40d2401bb9c1c8f14c4", size = 2815650, upload_time = "2025-11-17T12:28:02.544Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/bf/51/472e7b36a6bedb5242a9757e7486f702c3619eff76e256735d0c8b1679c6/blis-1.3.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:e9f5c53b277f6ac5b3ca30bc12ebab7ea16c8f8c36b14428abb56924213dc127", size = 11359008, upload_time = "2025-11-17T12:28:04.589Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/84/da/d0dfb6d6e6321ae44df0321384c32c322bd07b15740d7422727a1a49fc5d/blis-1.3.3-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:6297e7616c158b305c9a8a4e47ca5fc9b0785194dd96c903b1a1591a7ca21ddf", size = 3011959, upload_time = "2025-11-17T12:28:06.862Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/20/c5/2b0b5e556fa0364ed671051ea078a6d6d7b979b1cfef78d64ad3ca5f0c7f/blis-1.3.3-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:3f966ca74f89f8a33e568b9a1d71992fc9a0d29a423e047f0a212643e21b5458", size = 14232456, upload_time = "2025-11-17T12:28:08.779Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/31/07/4cdc81a47bf862c0b06d91f1bc6782064e8b69ac9b5d4ff51d97e4ff03da/blis-1.3.3-cp313-cp313-win_amd64.whl", hash = "sha256:7a0fc4b237a3a453bdc3c7ab48d91439fcd2d013b665c46948d9eaf9c3e45a97", size = 6192624, upload_time = "2025-11-17T12:28:14.197Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/5f/8a/80f7c68fbc24a76fc9c18522c46d6d69329c320abb18e26a707a5d874083/blis-1.3.3-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:c3e33cfbf22a418373766816343fcfcd0556012aa3ffdf562c29cddec448a415", size = 6934081, upload_time = "2025-11-17T12:28:16.436Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e5/52/d1aa3a51a7fc299b0c89dcaa971922714f50b1202769eebbdaadd1b5cff7/blis-1.3.3-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:6f165930e8d3a85c606d2003211497e28d528c7416fbfeafb6b15600963f7c9b", size = 1231486, upload_time = "2025-11-17T12:28:18.008Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/99/4f/badc7bd7f74861b26c10123bba7b9d16f99cd9535ad0128780360713820f/blis-1.3.3-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:878d4d96d8f2c7a2459024f013f2e4e5f46d708b23437dae970d998e7bff14a0", size = 2814944, upload_time = "2025-11-17T12:28:19.654Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/72/a6/f62a3bd814ca19ec7e29ac889fd354adea1217df3183e10217de51e2eb8b/blis-1.3.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:f36c0ca84a05ee5d3dbaa38056c4423c1fc29948b17a7923dd2fed8967375d74", size = 11345825, upload_time = "2025-11-17T12:28:21.354Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/d4/6c/671af79ee42bc4c968cae35c091ac89e8721c795bfa4639100670dc59139/blis-1.3.3-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:e5a662c48cd4aad5dae1a950345df23957524f071315837a4c6feb7d3b288990", size = 3008771, upload_time = "2025-11-17T12:28:23.637Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/be/92/7cd7f8490da7c98ee01557f2105885cc597217b0e7fd2eeb9e22cdd4ef23/blis-1.3.3-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:9de26fbd72bac900c273b76d46f0b45b77a28eace2e01f6ac6c2239531a413bb", size = 14219213, upload_time = "2025-11-17T12:28:26.143Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/0a/de/acae8e9f9a1f4bb393d41c8265898b0f29772e38eac14e9f69d191e2c006/blis-1.3.3-cp314-cp314-win_amd64.whl", hash = "sha256:9e5fdf4211b1972400f8ff6dafe87cb689c5d84f046b4a76b207c0bd2270faaf", size = 6324695, upload_time = "2025-11-17T12:28:28.401Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "catalogue"[m
[32m+[m[32mversion = "2.0.10"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/38/b4/244d58127e1cdf04cf2dc7d9566f0d24ef01d5ce21811bab088ecc62b5ea/catalogue-2.0.10.tar.gz", hash = "sha256:4f56daa940913d3f09d589c191c74e5a6d51762b3a9e37dd53b7437afd6cda15", size = 19561, upload_time = "2023-09-25T06:29:24.962Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/9e/96/d32b941a501ab566a16358d68b6eb4e4acc373fab3c3c4d7d9e649f7b4bb/catalogue-2.0.10-py3-none-any.whl", hash = "sha256:58c2de0020aa90f4a2da7dfad161bf7b3b054c86a5f09fcedc0b2b740c109a9f", size = 17325, upload_time = "2023-09-25T06:29:23.337Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "certifi"[m
[32m+[m[32mversion = "2025.11.12"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/a2/8c/58f469717fa48465e4a50c014a0400602d3c437d7c0c468e17ada824da3a/certifi-2025.11.12.tar.gz", hash = "sha256:d8ab5478f2ecd78af242878415affce761ca6bc54a22a27e026d7c25357c3316", size = 160538, upload_time = "2025-11-12T02:54:51.517Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/70/7d/9bc192684cea499815ff478dfcdc13835ddf401365057044fb721ec6bddb/certifi-2025.11.12-py3-none-any.whl", hash = "sha256:97de8790030bbd5c2d96b7ec782fc2f7820ef8dba6db909ccf95449f2d062d4b", size = 159438, upload_time = "2025-11-12T02:54:49.735Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "charset-normalizer"[m
[32m+[m[32mversion = "3.4.4"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/13/69/33ddede1939fdd074bce5434295f38fae7136463422fe4fd3e0e89b98062/charset_normalizer-3.4.4.tar.gz", hash = "sha256:94537985111c35f28720e43603b8e7b43a6ecfb2ce1d3058bbe955b73404e21a", size = 129418, upload_time = "2025-10-14T04:42:32.879Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/97/45/4b3a1239bbacd321068ea6e7ac28875b03ab8bc0aa0966452db17cd36714/charset_normalizer-3.4.4-cp313-cp313-macosx_10_13_universal2.whl", hash = "sha256:e1f185f86a6f3403aa2420e815904c67b2f9ebc443f045edd0de921108345794", size = 208091, upload_time = "2025-10-14T04:41:13.346Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/7d/62/73a6d7450829655a35bb88a88fca7d736f9882a27eacdca2c6d505b57e2e/charset_normalizer-3.4.4-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:6b39f987ae8ccdf0d2642338faf2abb1862340facc796048b604ef14919e55ed", size = 147936, upload_time = "2025-10-14T04:41:14.461Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/89/c5/adb8c8b3d6625bef6d88b251bbb0d95f8205831b987631ab0c8bb5d937c2/charset_normalizer-3.4.4-cp313-cp313-manylinux2014_armv7l.manylinux_2_17_armv7l.manylinux_2_31_armv7l.whl", hash = "sha256:3162d5d8ce1bb98dd51af660f2121c55d0fa541b46dff7bb9b9f86ea1d87de72", size = 144180, upload_time = "2025-10-14T04:41:15.588Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/91/ed/9706e4070682d1cc219050b6048bfd293ccf67b3d4f5a4f39207453d4b99/charset_normalizer-3.4.4-cp313-cp313-manylinux2014_ppc64le.manylinux_2_17_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:81d5eb2a312700f4ecaa977a8235b634ce853200e828fbadf3a9c50bab278328", size = 161346, upload_time = "2025-10-14T04:41:16.738Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/d5/0d/031f0d95e4972901a2f6f09ef055751805ff541511dc1252ba3ca1f80cf5/charset_normalizer-3.4.4-cp313-cp313-manylinux2014_s390x.manylinux_2_17_s390x.manylinux_2_28_s390x.whl", hash = "sha256:5bd2293095d766545ec1a8f612559f6b40abc0eb18bb2f5d1171872d34036ede", size = 158874, upload_time = "2025-10-14T04:41:17.923Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/f5/83/6ab5883f57c9c801ce5e5677242328aa45592be8a00644310a008d04f922/charset_normalizer-3.4.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:a8a8b89589086a25749f471e6a900d3f662d1d3b6e2e59dcecf787b1cc3a1894", size = 153076, upload_time = "2025-10-14T04:41:19.106Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/75/1e/5ff781ddf5260e387d6419959ee89ef13878229732732ee73cdae01800f2/charset_normalizer-3.4.4-cp313-cp313-manylinux_2_31_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:bc7637e2f80d8530ee4a78e878bce464f70087ce73cf7c1caf142416923b98f1", size = 150601, upload_time = "2025-10-14T04:41:20.245Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/d7/57/71be810965493d3510a6ca79b90c19e48696fb1ff964da319334b12677f0/charset_normalizer-3.4.4-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:f8bf04158c6b607d747e93949aa60618b61312fe647a6369f88ce2ff16043490", size = 150376, upload_time = "2025-10-14T04:41:21.398Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e5/d5/c3d057a78c181d007014feb7e9f2e65905a6c4ef182c0ddf0de2924edd65/charset_normalizer-3.4.4-cp313-cp313-musllinux_1_2_armv7l.whl", hash = "sha256:554af85e960429cf30784dd47447d5125aaa3b99a6f0683589dbd27e2f45da44", size = 144825, upload_time = "2025-10-14T04:41:22.583Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e6/8c/d0406294828d4976f275ffbe66f00266c4b3136b7506941d87c00cab5272/charset_normalizer-3.4.4-cp313-cp313-musllinux_1_2_ppc64le.whl", hash = "sha256:74018750915ee7ad843a774364e13a3db91682f26142baddf775342c3f5b1133", size = 162583, upload_time = "2025-10-14T04:41:23.754Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/d7/24/e2aa1f18c8f15c4c0e932d9287b8609dd30ad56dbe41d926bd846e22fb8d/charset_normalizer-3.4.4-cp313-cp313-musllinux_1_2_riscv64.whl", hash = "sha256:c0463276121fdee9c49b98908b3a89c39be45d86d1dbaa22957e38f6321d4ce3", size = 150366, upload_time = "2025-10-14T04:41:25.27Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e4/5b/1e6160c7739aad1e2df054300cc618b06bf784a7a164b0f238360721ab86/charset_normalizer-3.4.4-cp313-cp313-musllinux_1_2_s390x.whl", hash = "sha256:362d61fd13843997c1c446760ef36f240cf81d3ebf74ac62652aebaf7838561e", size = 160300, upload_time = "2025-10-14T04:41:26.725Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/7a/10/f882167cd207fbdd743e55534d5d9620e095089d176d55cb22d5322f2afd/charset_normalizer-3.4.4-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:9a26f18905b8dd5d685d6d07b0cdf98a79f3c7a918906af7cc143ea2e164c8bc", size = 154465, upload_time = "2025-10-14T04:41:28.322Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/89/66/c7a9e1b7429be72123441bfdbaf2bc13faab3f90b933f664db506dea5915/charset_normalizer-3.4.4-cp313-cp313-win32.whl", hash = "sha256:9b35f4c90079ff2e2edc5b26c0c77925e5d2d255c42c74fdb70fb49b172726ac", size = 99404, upload_time = "2025-10-14T04:41:29.95Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/c4/26/b9924fa27db384bdcd97ab83b4f0a8058d96ad9626ead570674d5e737d90/charset_normalizer-3.4.4-cp313-cp313-win_amd64.whl", hash = "sha256:b435cba5f4f750aa6c0a0d92c541fb79f69a387c91e61f1795227e4ed9cece14", size = 107092, upload_time = "2025-10-14T04:41:31.188Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/af/8f/3ed4bfa0c0c72a7ca17f0380cd9e4dd842b09f664e780c13cff1dcf2ef1b/charset_normalizer-3.4.4-cp313-cp313-win_arm64.whl", hash = "sha256:542d2cee80be6f80247095cc36c418f7bddd14f4a6de45af91dfad36d817bba2", size = 100408, upload_time = "2025-10-14T04:41:32.624Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/2a/35/7051599bd493e62411d6ede36fd5af83a38f37c4767b92884df7301db25d/charset_normalizer-3.4.4-cp314-cp314-macosx_10_13_universal2.whl", hash = "sha256:da3326d9e65ef63a817ecbcc0df6e94463713b754fe293eaa03da99befb9a5bd", size = 207746, upload_time = "2025-10-14T04:41:33.773Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/10/9a/97c8d48ef10d6cd4fcead2415523221624bf58bcf68a802721a6bc807c8f/charset_normalizer-3.4.4-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:8af65f14dc14a79b924524b1e7fffe304517b2bff5a58bf64f30b98bbc5079eb", size = 147889, upload_time = "2025-10-14T04:41:34.897Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/10/bf/979224a919a1b606c82bd2c5fa49b5c6d5727aa47b4312bb27b1734f53cd/charset_normalizer-3.4.4-cp314-cp314-manylinux2014_armv7l.manylinux_2_17_armv7l.manylinux_2_31_armv7l.whl", hash = "sha256:74664978bb272435107de04e36db5a9735e78232b85b77d45cfb38f758efd33e", size = 143641, upload_time = "2025-10-14T04:41:36.116Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/ba/33/0ad65587441fc730dc7bd90e9716b30b4702dc7b617e6ba4997dc8651495/charset_normalizer-3.4.4-cp314-cp314-manylinux2014_ppc64le.manylinux_2_17_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:752944c7ffbfdd10c074dc58ec2d5a8a4cd9493b314d367c14d24c17684ddd14", size = 160779, upload_time = "2025-10-14T04:41:37.229Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/67/ed/331d6b249259ee71ddea93f6f2f0a56cfebd46938bde6fcc6f7b9a3d0e09/charset_normalizer-3.4.4-cp314-cp314-manylinux2014_s390x.manylinux_2_17_s390x.manylinux_2_28_s390x.whl", hash = "sha256:d1f13550535ad8cff21b8d757a3257963e951d96e20ec82ab44bc64aeb62a191", size = 159035, upload_time = "2025-10-14T04:41:38.368Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/67/ff/f6b948ca32e4f2a4576aa129d8bed61f2e0543bf9f5f2b7fc3758ed005c9/charset_normalizer-3.4.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:ecaae4149d99b1c9e7b88bb03e3221956f68fd6d50be2ef061b2381b61d20838", size = 152542, upload_time = "2025-10-14T04:41:39.862Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/16/85/276033dcbcc369eb176594de22728541a925b2632f9716428c851b149e83/charset_normalizer-3.4.4-cp314-cp314-manylinux_2_31_riscv64.manylinux_2_39_riscv64.whl", hash = "sha256:cb6254dc36b47a990e59e1068afacdcd02958bdcce30bb50cc1700a8b9d624a6", size = 149524, upload_time = "2025-10-14T04:41:41.319Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/9e/f2/6a2a1f722b6aba37050e626530a46a68f74e63683947a8acff92569f979a/charset_normalizer-3.4.4-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:c8ae8a0f02f57a6e61203a31428fa1d677cbe50c93622b4149d5c0f319c1d19e", size = 150395, upload_time = "2025-10-14T04:41:42.539Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/60/bb/2186cb2f2bbaea6338cad15ce23a67f9b0672929744381e28b0592676824/charset_normalizer-3.4.4-cp314-cp314-musllinux_1_2_armv7l.whl", hash = "sha256:47cc91b2f4dd2833fddaedd2893006b0106129d4b94fdb6af1f4ce5a9965577c", size = 143680, upload_time = "2025-10-14T04:41:43.661Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/7d/a5/bf6f13b772fbb2a90360eb620d52ed8f796f3c5caee8398c3b2eb7b1c60d/charset_normalizer-3.4.4-cp314-cp314-musllinux_1_2_ppc64le.whl", hash = "sha256:82004af6c302b5d3ab2cfc4cc5f29db16123b1a8417f2e25f9066f91d4411090", size = 162045, upload_time = "2025-10-14T04:41:44.821Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/df/c5/d1be898bf0dc3ef9030c3825e5d3b83f2c528d207d246cbabe245966808d/charset_normalizer-3.4.4-cp314-cp314-musllinux_1_2_riscv64.whl", hash = "sha256:2b7d8f6c26245217bd2ad053761201e9f9680f8ce52f0fcd8d0755aeae5b2152", size = 149687, upload_time = "2025-10-14T04:41:46.442Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/a5/42/90c1f7b9341eef50c8a1cb3f098ac43b0508413f33affd762855f67a410e/charset_normalizer-3.4.4-cp314-cp314-musllinux_1_2_s390x.whl", hash = "sha256:799a7a5e4fb2d5898c60b640fd4981d6a25f1c11790935a44ce38c54e985f828", size = 160014, upload_time = "2025-10-14T04:41:47.631Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/76/be/4d3ee471e8145d12795ab655ece37baed0929462a86e72372fd25859047c/charset_normalizer-3.4.4-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:99ae2cffebb06e6c22bdc25801d7b30f503cc87dbd283479e7b606f70aff57ec", size = 154044, upload_time = "2025-10-14T04:41:48.81Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/b0/6f/8f7af07237c34a1defe7defc565a9bc1807762f672c0fde711a4b22bf9c0/charset_normalizer-3.4.4-cp314-cp314-win32.whl", hash = "sha256:f9d332f8c2a2fcbffe1378594431458ddbef721c1769d78e2cbc06280d8155f9", size = 99940, upload_time = "2025-10-14T04:41:49.946Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/4b/51/8ade005e5ca5b0d80fb4aff72a3775b325bdc3d27408c8113811a7cbe640/charset_normalizer-3.4.4-cp314-cp314-win_amd64.whl", hash = "sha256:8a6562c3700cce886c5be75ade4a5db4214fda19fede41d9792d100288d8f94c", size = 107104, upload_time = "2025-10-14T04:41:51.051Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/da/5f/6b8f83a55bb8278772c5ae54a577f3099025f9ade59d0136ac24a0df4bde/charset_normalizer-3.4.4-cp314-cp314-win_arm64.whl", hash = "sha256:de00632ca48df9daf77a2c65a484531649261ec9f25489917f09e455cb09ddb2", size = 100743, upload_time = "2025-10-14T04:41:52.122Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/0a/4c/925909008ed5a988ccbb72dcc897407e5d6d3bd72410d69e051fc0c14647/charset_normalizer-3.4.4-py3-none-any.whl", hash = "sha256:7a32c560861a02ff789ad905a2fe94e3f840803362c84fecf1851cb4cf3dc37f", size = 53402, upload_time = "2025-10-14T04:42:31.76Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "click"[m
[32m+[m[32mversion = "8.3.1"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32mdependencies = [[m
[32m+[m[32m    { name = "colorama", marker = "sys_platform == 'win32'" },[m
[32m+[m[32m][m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/3d/fa/656b739db8587d7b5dfa22e22ed02566950fbfbcdc20311993483657a5c0/click-8.3.1.tar.gz", hash = "sha256:12ff4785d337a1bb490bb7e9c2b1ee5da3112e94a8622f26a6c77f5d2fc6842a", size = 295065, upload_time = "2025-11-15T20:45:42.706Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/98/78/01c019cdb5d6498122777c1a43056ebb3ebfeef2076d9d026bfe15583b2b/click-8.3.1-py3-none-any.whl", hash = "sha256:981153a64e25f12d547d3426c367a4857371575ee7ad18df2a6183ab0545b2a6", size = 108274, upload_time = "2025-11-15T20:45:41.139Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "cloudpathlib"[m
[32m+[m[32mversion = "0.23.0"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/f4/18/2ac35d6b3015a0c74e923d94fc69baf8307f7c3233de015d69f99e17afa8/cloudpathlib-0.23.0.tar.gz", hash = "sha256:eb38a34c6b8a048ecfd2b2f60917f7cbad4a105b7c979196450c2f541f4d6b4b", size = 53126, upload_time = "2025-10-07T22:47:56.278Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/ae/8a/c4bb04426d608be4a3171efa2e233d2c59a5c8937850c10d098e126df18e/cloudpathlib-0.23.0-py3-none-any.whl", hash = "sha256:8520b3b01468fee77de37ab5d50b1b524ea6b4a8731c35d1b7407ac0cd716002", size = 62755, upload_time = "2025-10-07T22:47:54.905Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "colorama"[m
[32m+[m[32mversion = "0.4.6"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz", hash = "sha256:08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44", size = 27697, upload_time = "2022-10-25T02:36:22.414Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl", hash = "sha256:4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6", size = 25335, upload_time = "2022-10-25T02:36:20.889Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "confection"[m
[32m+[m[32mversion = "0.1.5"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32mdependencies = [[m
[32m+[m[32m    { name = "pydantic" },[m
[32m+[m[32m    { name = "srsly" },[m
[32m+[m[32m][m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/51/d3/57c6631159a1b48d273b40865c315cf51f89df7a9d1101094ef12e3a37c2/confection-0.1.5.tar.gz", hash = "sha256:8e72dd3ca6bd4f48913cd220f10b8275978e740411654b6e8ca6d7008c590f0e", size = 38924, upload_time = "2024-05-31T16:17:01.559Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/0c/00/3106b1854b45bd0474ced037dfe6b73b90fe68a68968cef47c23de3d43d2/confection-0.1.5-py3-none-any.whl", hash = "sha256:e29d3c3f8eac06b3f77eb9dfb4bf2fc6bcc9622a98ca00a698e3d019c6430b14", size = 35451, upload_time = "2024-05-31T16:16:59.075Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "contourpy"[m
[32m+[m[32mversion = "1.3.3"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32mdependencies = [[m
[32m+[m[32m    { name = "numpy" },[m
[32m+[m[32m][m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/58/01/1253e6698a07380cd31a736d248a3f2a50a7c88779a1813da27503cadc2a/contourpy-1.3.3.tar.gz", hash = "sha256:083e12155b210502d0bca491432bb04d56dc3432f95a979b429f2848c3dbe880", size = 13466174, upload_time = "2025-07-26T12:03:12.549Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/68/35/0167aad910bbdb9599272bd96d01a9ec6852f36b9455cf2ca67bd4cc2d23/contourpy-1.3.3-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:177fb367556747a686509d6fef71d221a4b198a3905fe824430e5ea0fda54eb5", size = 293257, upload_time = "2025-07-26T12:01:39.367Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/96/e4/7adcd9c8362745b2210728f209bfbcf7d91ba868a2c5f40d8b58f54c509b/contourpy-1.3.3-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:d002b6f00d73d69333dac9d0b8d5e84d9724ff9ef044fd63c5986e62b7c9e1b1", size = 274034, upload_time = "2025-07-26T12:01:40.645Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/73/23/90e31ceeed1de63058a02cb04b12f2de4b40e3bef5e082a7c18d9c8ae281/contourpy-1.3.3-cp313-cp313-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:348ac1f5d4f1d66d3322420f01d42e43122f43616e0f194fc1c9f5d830c5b286", size = 334672, upload_time = "2025-07-26T12:01:41.942Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/ed/93/b43d8acbe67392e659e1d984700e79eb67e2acb2bd7f62012b583a7f1b55/contourpy-1.3.3-cp313-cp313-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:655456777ff65c2c548b7c454af9c6f33f16c8884f11083244b5819cc214f1b5", size = 381234, upload_time = "2025-07-26T12:01:43.499Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/46/3b/bec82a3ea06f66711520f75a40c8fc0b113b2a75edb36aa633eb11c4f50f/contourpy-1.3.3-cp313-cp313-manylinux_2_26_s390x.manylinux_2_28_s390x.whl", hash = "sha256:644a6853d15b2512d67881586bd03f462c7ab755db95f16f14d7e238f2852c67", size = 385169, upload_time = "2025-07-26T12:01:45.219Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/4b/32/e0f13a1c5b0f8572d0ec6ae2f6c677b7991fafd95da523159c19eff0696a/contourpy-1.3.3-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:4debd64f124ca62069f313a9cb86656ff087786016d76927ae2cf37846b006c9", size = 362859, upload_time = "2025-07-26T12:01:46.519Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/33/71/e2a7945b7de4e58af42d708a219f3b2f4cff7386e6b6ab0a0fa0033c49a9/contourpy-1.3.3-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:a15459b0f4615b00bbd1e91f1b9e19b7e63aea7483d03d804186f278c0af2659", size = 1332062, upload_time = "2025-07-26T12:01:48.964Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/12/fc/4e87ac754220ccc0e807284f88e943d6d43b43843614f0a8afa469801db0/contourpy-1.3.3-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:ca0fdcd73925568ca027e0b17ab07aad764be4706d0a925b89227e447d9737b7", size = 1403932, upload_time = "2025-07-26T12:01:51.979Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/a6/2e/adc197a37443f934594112222ac1aa7dc9a98faf9c3842884df9a9d8751d/contourpy-1.3.3-cp313-cp313-win32.whl", hash = "sha256:b20c7c9a3bf701366556e1b1984ed2d0cedf999903c51311417cf5f591d8c78d", size = 185024, upload_time = "2025-07-26T12:01:53.245Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/18/0b/0098c214843213759692cc638fce7de5c289200a830e5035d1791d7a2338/contourpy-1.3.3-cp313-cp313-win_amd64.whl", hash = "sha256:1cadd8b8969f060ba45ed7c1b714fe69185812ab43bd6b86a9123fe8f99c3263", size = 226578, upload_time = "2025-07-26T12:01:54.422Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/8a/9a/2f6024a0c5995243cd63afdeb3651c984f0d2bc727fd98066d40e141ad73/contourpy-1.3.3-cp313-cp313-win_arm64.whl", hash = "sha256:fd914713266421b7536de2bfa8181aa8c699432b6763a0ea64195ebe28bff6a9", size = 193524, upload_time = "2025-07-26T12:01:55.73Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/c0/b3/f8a1a86bd3298513f500e5b1f5fd92b69896449f6cab6a146a5d52715479/contourpy-1.3.3-cp313-cp313t-macosx_10_13_x86_64.whl", hash = "sha256:88df9880d507169449d434c293467418b9f6cbe82edd19284aa0409e7fdb933d", size = 306730, upload_time = "2025-07-26T12:01:57.051Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/3f/11/4780db94ae62fc0c2053909b65dc3246bd7cecfc4f8a20d957ad43aa4ad8/contourpy-1.3.3-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:d06bb1f751ba5d417047db62bca3c8fde202b8c11fb50742ab3ab962c81e8216", size = 287897, upload_time = "2025-07-26T12:01:58.663Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/ae/15/e59f5f3ffdd6f3d4daa3e47114c53daabcb18574a26c21f03dc9e4e42ff0/contourpy-1.3.3-cp313-cp313t-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:e4e6b05a45525357e382909a4c1600444e2a45b4795163d3b22669285591c1ae", size = 326751, upload_time = "2025-07-26T12:02:00.343Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/0f/81/03b45cfad088e4770b1dcf72ea78d3802d04200009fb364d18a493857210/contourpy-1.3.3-cp313-cp313t-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:ab3074b48c4e2cf1a960e6bbeb7f04566bf36b1861d5c9d4d8ac04b82e38ba20", size = 375486, upload_time = "2025-07-26T12:02:02.128Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/0c/ba/49923366492ffbdd4486e970d421b289a670ae8cf539c1ea9a09822b371a/contourpy-1.3.3-cp313-cp313t-manylinux_2_26_s390x.manylinux_2_28_s390x.whl", hash = "sha256:6c3d53c796f8647d6deb1abe867daeb66dcc8a97e8455efa729516b997b8ed99", size = 388106, upload_time = "2025-07-26T12:02:03.615Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/9f/52/5b00ea89525f8f143651f9f03a0df371d3cbd2fccd21ca9b768c7a6500c2/contourpy-1.3.3-cp313-cp313t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:50ed930df7289ff2a8d7afeb9603f8289e5704755c7e5c3bbd929c90c817164b", size = 352548, upload_time = "2025-07-26T12:02:05.165Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/32/1d/a209ec1a3a3452d490f6b14dd92e72280c99ae3d1e73da74f8277d4ee08f/contourpy-1.3.3-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:4feffb6537d64b84877da813a5c30f1422ea5739566abf0bd18065ac040e120a", size = 1322297, upload_time = "2025-07-26T12:02:07.379Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/bc/9e/46f0e8ebdd884ca0e8877e46a3f4e633f6c9c8c4f3f6e72be3fe075994aa/contourpy-1.3.3-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:2b7e9480ffe2b0cd2e787e4df64270e3a0440d9db8dc823312e2c940c167df7e", size = 1391023, upload_time = "2025-07-26T12:02:10.171Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/b9/70/f308384a3ae9cd2209e0849f33c913f658d3326900d0ff5d378d6a1422d2/contourpy-1.3.3-cp313-cp313t-win32.whl", hash = "sha256:283edd842a01e3dcd435b1c5116798d661378d83d36d337b8dde1d16a5fc9ba3", size = 196157, upload_time = "2025-07-26T12:02:11.488Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/b2/dd/880f890a6663b84d9e34a6f88cded89d78f0091e0045a284427cb6b18521/contourpy-1.3.3-cp313-cp313t-win_amd64.whl", hash = "sha256:87acf5963fc2b34825e5b6b048f40e3635dd547f590b04d2ab317c2619ef7ae8", size = 240570, upload_time = "2025-07-26T12:02:12.754Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/80/99/2adc7d8ffead633234817ef8e9a87115c8a11927a94478f6bb3d3f4d4f7d/contourpy-1.3.3-cp313-cp313t-win_arm64.whl", hash = "sha256:3c30273eb2a55024ff31ba7d052dde990d7d8e5450f4bbb6e913558b3d6c2301", size = 199713, upload_time = "2025-07-26T12:02:14.4Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/72/8b/4546f3ab60f78c514ffb7d01a0bd743f90de36f0019d1be84d0a708a580a/contourpy-1.3.3-cp314-cp314-macosx_10_13_x86_64.whl", hash = "sha256:fde6c716d51c04b1c25d0b90364d0be954624a0ee9d60e23e850e8d48353d07a", size = 292189, upload_time = "2025-07-26T12:02:16.095Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/fd/e1/3542a9cb596cadd76fcef413f19c79216e002623158befe6daa03dbfa88c/contourpy-1.3.3-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:cbedb772ed74ff5be440fa8eee9bd49f64f6e3fc09436d9c7d8f1c287b121d77", size = 273251, upload_time = "2025-07-26T12:02:17.524Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/b1/71/f93e1e9471d189f79d0ce2497007731c1e6bf9ef6d1d61b911430c3db4e5/contourpy-1.3.3-cp314-cp314-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:22e9b1bd7a9b1d652cd77388465dc358dafcd2e217d35552424aa4f996f524f5", size = 335810, upload_time = "2025-07-26T12:02:18.9Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/91/f9/e35f4c1c93f9275d4e38681a80506b5510e9327350c51f8d4a5a724d178c/contourpy-1.3.3-cp314-cp314-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:a22738912262aa3e254e4f3cb079a95a67132fc5a063890e224393596902f5a4", size = 382871, upload_time = "2025-07-26T12:02:20.418Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/b5/71/47b512f936f66a0a900d81c396a7e60d73419868fba959c61efed7a8ab46/contourpy-1.3.3-cp314-cp314-manylinux_2_26_s390x.manylinux_2_28_s390x.whl", hash = "sha256:afe5a512f31ee6bd7d0dda52ec9864c984ca3d66664444f2d72e0dc4eb832e36", size = 386264, upload_time = "2025-07-26T12:02:21.916Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/04/5f/9ff93450ba96b09c7c2b3f81c94de31c89f92292f1380261bd7195bea4ea/contourpy-1.3.3-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:f64836de09927cba6f79dcd00fdd7d5329f3fccc633468507079c829ca4db4e3", size = 363819, upload_time = "2025-07-26T12:02:23.759Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/3e/a6/0b185d4cc480ee494945cde102cb0149ae830b5fa17bf855b95f2e70ad13/contourpy-1.3.3-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:1fd43c3be4c8e5fd6e4f2baeae35ae18176cf2e5cced681cca908addf1cdd53b", size = 1333650, upload_time = "2025-07-26T12:02:26.181Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/43/d7/afdc95580ca56f30fbcd3060250f66cedbde69b4547028863abd8aa3b47e/contourpy-1.3.3-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:6afc576f7b33cf00996e5c1102dc2a8f7cc89e39c0b55df93a0b78c1bd992b36", size = 1404833, upload_time = "2025-07-26T12:02:28.782Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e2/e2/366af18a6d386f41132a48f033cbd2102e9b0cf6345d35ff0826cd984566/contourpy-1.3.3-cp314-cp314-win32.whl", hash = "sha256:66c8a43a4f7b8df8b71ee1840e4211a3c8d93b214b213f590e18a1beca458f7d", size = 189692, upload_time = "2025-07-26T12:02:30.128Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/7d/c2/57f54b03d0f22d4044b8afb9ca0e184f8b1afd57b4f735c2fa70883dc601/contourpy-1.3.3-cp314-cp314-win_amd64.whl", hash = "sha256:cf9022ef053f2694e31d630feaacb21ea24224be1c3ad0520b13d844274614fd", size = 232424, upload_time = "2025-07-26T12:02:31.395Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/18/79/a9416650df9b525737ab521aa181ccc42d56016d2123ddcb7b58e926a42c/contourpy-1.3.3-cp314-cp314-win_arm64.whl", hash = "sha256:95b181891b4c71de4bb404c6621e7e2390745f887f2a026b2d99e92c17892339", size = 198300, upload_time = "2025-07-26T12:02:32.956Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/1f/42/38c159a7d0f2b7b9c04c64ab317042bb6952b713ba875c1681529a2932fe/contourpy-1.3.3-cp314-cp314t-macosx_10_13_x86_64.whl", hash = "sha256:33c82d0138c0a062380332c861387650c82e4cf1747aaa6938b9b6516762e772", size = 306769, upload_time = "2025-07-26T12:02:34.2Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/c3/6c/26a8205f24bca10974e77460de68d3d7c63e282e23782f1239f226fcae6f/contourpy-1.3.3-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:ea37e7b45949df430fe649e5de8351c423430046a2af20b1c1961cae3afcda77", size = 287892, upload_time = "2025-07-26T12:02:35.807Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/66/06/8a475c8ab718ebfd7925661747dbb3c3ee9c82ac834ccb3570be49d129f4/contourpy-1.3.3-cp314-cp314t-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:d304906ecc71672e9c89e87c4675dc5c2645e1f4269a5063b99b0bb29f232d13", size = 326748, upload_time = "2025-07-26T12:02:37.193Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/b4/a3/c5ca9f010a44c223f098fccd8b158bb1cb287378a31ac141f04730dc49be/contourpy-1.3.3-cp314-cp314t-manylinux_2_26_ppc64le.manylinux_2_28_ppc64le.whl", hash = "sha256:ca658cd1a680a5c9ea96dc61cdbae1e85c8f25849843aa799dfd3cb370ad4fbe", size = 375554, upload_time = "2025-07-26T12:02:38.894Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/80/5b/68bd33ae63fac658a4145088c1e894405e07584a316738710b636c6d0333/contourpy-1.3.3-cp314-cp314t-manylinux_2_26_s390x.manylinux_2_28_s390x.whl", hash = "sha256:ab2fd90904c503739a75b7c8c5c01160130ba67944a7b77bbf36ef8054576e7f", size = 388118, upload_time = "2025-07-26T12:02:40.642Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/40/52/4c285a6435940ae25d7410a6c36bda5145839bc3f0beb20c707cda18b9d2/contourpy-1.3.3-cp314-cp314t-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:b7301b89040075c30e5768810bc96a8e8d78085b47d8be6e4c3f5a0b4ed478a0", size = 352555, upload_time = "2025-07-26T12:02:42.25Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/24/ee/3e81e1dd174f5c7fefe50e85d0892de05ca4e26ef1c9a59c2a57e43b865a/contourpy-1.3.3-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:2a2a8b627d5cc6b7c41a4beff6c5ad5eb848c88255fda4a8745f7e901b32d8e4", size = 1322295, upload_time = "2025-07-26T12:02:44.668Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/3c/b2/6d913d4d04e14379de429057cd169e5e00f6c2af3bb13e1710bcbdb5da12/contourpy-1.3.3-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:fd6ec6be509c787f1caf6b247f0b1ca598bef13f4ddeaa126b7658215529ba0f", size = 1391027, upload_time = "2025-07-26T12:02:47.09Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/93/8a/68a4ec5c55a2971213d29a9374913f7e9f18581945a7a31d1a39b5d2dfe5/contourpy-1.3.3-cp314-cp314t-win32.whl", hash = "sha256:e74a9a0f5e3fff48fb5a7f2fd2b9b70a3fe014a67522f79b7cca4c0c7e43c9ae", size = 202428, upload_time = "2025-07-26T12:02:48.691Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/fa/96/fd9f641ffedc4fa3ace923af73b9d07e869496c9cc7a459103e6e978992f/contourpy-1.3.3-cp314-cp314t-win_amd64.whl", hash = "sha256:13b68d6a62db8eafaebb8039218921399baf6e47bf85006fd8529f2a08ef33fc", size = 250331, upload_time = "2025-07-26T12:02:50.137Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/ae/8c/469afb6465b853afff216f9528ffda78a915ff880ed58813ba4faf4ba0b6/contourpy-1.3.3-cp314-cp314t-win_arm64.whl", hash = "sha256:b7448cb5a725bb1e35ce88771b86fba35ef418952474492cf7c764059933ff8b", size = 203831, upload_time = "2025-07-26T12:02:51.449Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "cycler"[m
[32m+[m[32mversion = "0.12.1"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/a9/95/a3dbbb5028f35eafb79008e7522a75244477d2838f38cbb722248dabc2a8/cycler-0.12.1.tar.gz", hash = "sha256:88bb128f02ba341da8ef447245a9e138fae777f6a23943da4540077d3601eb1c", size = 7615, upload_time = "2023-10-07T05:32:18.335Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e7/05/c19819d5e3d95294a6f5947fb9b9629efb316b96de511b418c53d245aae6/cycler-0.12.1-py3-none-any.whl", hash = "sha256:85cef7cff222d8644161529808465972e51340599459b8ac3ccbac5a854e0d30", size = 8321, upload_time = "2023-10-07T05:32:16.783Z" },[m
[32m+[m[32m][m
[32m+[m
[32m+[m[32m[[package]][m
[32m+[m[32mname = "cymem"[m
[32m+[m[32mversion = "2.0.13"[m
[32m+[m[32msource = { registry = "https://pypi.org/simple" }[m
[32m+[m[32msdist = { url = "https://files.pythonhosted.org/packages/c0/8f/2f0fbb32535c3731b7c2974c569fb9325e0a38ed5565a08e1139a3b71e82/cymem-2.0.13.tar.gz", hash = "sha256:1c91a92ae8c7104275ac26bd4d29b08ccd3e7faff5893d3858cb6fadf1bc1588", size = 12320, upload_time = "2025-11-14T14:58:36.902Z" }[m
[32m+[m[32mwheels = [[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/ce/0f/95a4d1e3bebfdfa7829252369357cf9a764f67569328cd9221f21e2c952e/cymem-2.0.13-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:891fd9030293a8b652dc7fb9fdc79a910a6c76fc679cd775e6741b819ffea476", size = 43478, upload_time = "2025-11-14T14:57:42.682Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/bf/a0/8fc929cc29ae466b7b4efc23ece99cbd3ea34992ccff319089c624d667fd/cymem-2.0.13-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:89c4889bd16513ce1644ccfe1e7c473ba7ca150f0621e66feac3a571bde09e7e", size = 42695, upload_time = "2025-11-14T14:57:43.741Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/4a/b3/deeb01354ebaf384438083ffe0310209ef903db3e7ba5a8f584b06d28387/cymem-2.0.13-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:45dcaba0f48bef9cc3d8b0b92058640244a95a9f12542210b51318da97c2cf28", size = 250573, upload_time = "2025-11-14T14:57:44.81Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/36/36/bc980b9a14409f3356309c45a8d88d58797d02002a9d794dd6c84e809d3a/cymem-2.0.13-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:e96848faaafccc0abd631f1c5fb194eac0caee4f5a8777fdbb3e349d3a21741c", size = 254572, upload_time = "2025-11-14T14:57:46.023Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/fd/dd/a12522952624685bd0f8968e26d2ed6d059c967413ce6eb52292f538f1b0/cymem-2.0.13-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:e02d3e2c3bfeb21185d5a4a70790d9df40629a87d8d7617dc22b4e864f665fa3", size = 248060, upload_time = "2025-11-14T14:57:47.605Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/08/11/5dc933ddfeb2dfea747a0b935cb965b9a7580b324d96fc5f5a1b5ff8df29/cymem-2.0.13-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:fece5229fd5ecdcd7a0738affb8c59890e13073ae5626544e13825f26c019d3c", size = 254601, upload_time = "2025-11-14T14:57:48.861Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/70/66/d23b06166864fa94e13a98e5922986ce774832936473578febce64448d75/cymem-2.0.13-cp313-cp313-win_amd64.whl", hash = "sha256:38aefeb269597c1a0c2ddf1567dd8605489b661fa0369c6406c1acd433b4c7ba", size = 40103, upload_time = "2025-11-14T14:57:50.396Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/2f/9e/c7b21271ab88a21760f3afdec84d2bc09ffa9e6c8d774ad9d4f1afab0416/cymem-2.0.13-cp313-cp313-win_arm64.whl", hash = "sha256:717270dcfd8c8096b479c42708b151002ff98e434a7b6f1f916387a6c791e2ad", size = 36016, upload_time = "2025-11-14T14:57:51.611Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/7f/28/d3b03427edc04ae04910edf1c24b993881c3ba93a9729a42bcbb816a1808/cymem-2.0.13-cp313-cp313t-macosx_10_13_x86_64.whl", hash = "sha256:7e1a863a7f144ffb345397813701509cfc74fc9ed360a4d92799805b4b865dd1", size = 46429, upload_time = "2025-11-14T14:57:52.582Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/35/a9/7ed53e481f47ebfb922b0b42e980cec83e98ccb2137dc597ea156642440c/cymem-2.0.13-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:c16cb80efc017b054f78998c6b4b013cef509c7b3d802707ce1f85a1d68361bf", size = 46205, upload_time = "2025-11-14T14:57:53.64Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/61/39/a3d6ad073cf7f0fbbb8bbf09698c3c8fac11be3f791d710239a4e8dd3438/cymem-2.0.13-cp313-cp313t-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:0d78a27c88b26c89bd1ece247d1d5939dba05a1dae6305aad8fd8056b17ddb51", size = 296083, upload_time = "2025-11-14T14:57:55.922Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/36/0c/20697c8bc19f624a595833e566f37d7bcb9167b0ce69de896eba7cfc9c2d/cymem-2.0.13-cp313-cp313t-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:6d36710760f817194dacb09d9fc45cb6a5062ed75e85f0ef7ad7aeeb13d80cc3", size = 286159, upload_time = "2025-11-14T14:57:57.106Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/82/d4/9326e3422d1c2d2b4a8fb859bdcce80138f6ab721ddafa4cba328a505c71/cymem-2.0.13-cp313-cp313t-musllinux_1_2_aarch64.whl", hash = "sha256:c8f30971cadd5dcf73bcfbbc5849b1f1e1f40db8cd846c4aa7d3b5e035c7b583", size = 288186, upload_time = "2025-11-14T14:57:58.334Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/ed/bc/68da7dd749b72884dc22e898562f335002d70306069d496376e5ff3b6153/cymem-2.0.13-cp313-cp313t-musllinux_1_2_x86_64.whl", hash = "sha256:9d441d0e45798ec1fd330373bf7ffa6b795f229275f64016b6a193e6e2a51522", size = 290353, upload_time = "2025-11-14T14:58:00.562Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/50/23/dbf2ad6ecd19b99b3aab6203b1a06608bbd04a09c522d836b854f2f30f73/cymem-2.0.13-cp313-cp313t-win_amd64.whl", hash = "sha256:d1c950eebb9f0f15e3ef3591313482a5a611d16fc12d545e2018cd607f40f472", size = 44764, upload_time = "2025-11-14T14:58:01.793Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/54/3f/35701c13e1fc7b0895198c8b20068c569a841e0daf8e0b14d1dc0816b28f/cymem-2.0.13-cp313-cp313t-win_arm64.whl", hash = "sha256:042e8611ef862c34a97b13241f5d0da86d58aca3cecc45c533496678e75c5a1f", size = 38964, upload_time = "2025-11-14T14:58:02.87Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/a7/2e/f0e1596010a9a57fa9ebd124a678c07c5b2092283781ae51e79edcf5cb98/cymem-2.0.13-cp314-cp314-macosx_10_15_x86_64.whl", hash = "sha256:d2a4bf67db76c7b6afc33de44fb1c318207c3224a30da02c70901936b5aafdf1", size = 43812, upload_time = "2025-11-14T14:58:04.227Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/bc/45/8ccc21df08fcbfa6aa3efeb7efc11a1c81c90e7476e255768bb9c29ba02a/cymem-2.0.13-cp314-cp314-macosx_11_0_arm64.whl", hash = "sha256:92a2ce50afa5625fb5ce7c9302cee61e23a57ccac52cd0410b4858e572f8614b", size = 42951, upload_time = "2025-11-14T14:58:05.424Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/01/8c/fe16531631f051d3d1226fa42e2d76fd2c8d5cfa893ec93baee90c7a9d90/cymem-2.0.13-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:bc116a70cc3a5dc3d1684db5268eff9399a0be8603980005e5b889564f1ea42f", size = 249878, upload_time = "2025-11-14T14:58:06.95Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/47/4b/39d67b80ffb260457c05fcc545de37d82e9e2dbafc93dd6b64f17e09b933/cymem-2.0.13-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:68489bf0035c4c280614067ab6a82815b01dc9fcd486742a5306fe9f68deb7ef", size = 252571, upload_time = "2025-11-14T14:58:08.232Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/53/0e/76f6531f74dfdfe7107899cce93ab063bb7ee086ccd3910522b31f623c08/cymem-2.0.13-cp314-cp314-musllinux_1_2_aarch64.whl", hash = "sha256:03cb7bdb55718d5eb6ef0340b1d2430ba1386db30d33e9134d01ba9d6d34d705", size = 248555, upload_time = "2025-11-14T14:58:09.429Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/c7/7c/eee56757db81f0aefc2615267677ae145aff74228f529838425057003c0d/cymem-2.0.13-cp314-cp314-musllinux_1_2_x86_64.whl", hash = "sha256:1710390e7fb2510a8091a1991024d8ae838fd06b02cdfdcd35f006192e3c6b0e", size = 254177, upload_time = "2025-11-14T14:58:10.594Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/77/e0/a4b58ec9e53c836dce07ef39837a64a599f4a21a134fc7ca57a3a8f9a4b5/cymem-2.0.13-cp314-cp314-win_amd64.whl", hash = "sha256:ac699c8ec72a3a9de8109bd78821ab22f60b14cf2abccd970b5ff310e14158ed", size = 40853, upload_time = "2025-11-14T14:58:12.116Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/61/81/9931d1f83e5aeba175440af0b28f0c2e6f71274a5a7b688bc3e907669388/cymem-2.0.13-cp314-cp314-win_arm64.whl", hash = "sha256:90c2d0c04bcda12cd5cebe9be93ce3af6742ad8da96e1b1907e3f8e00291def1", size = 36970, upload_time = "2025-11-14T14:58:13.114Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/b7/ef/af447c2184dec6dec973be14614df8ccb4d16d1c74e0784ab4f02538433c/cymem-2.0.13-cp314-cp314t-macosx_10_15_x86_64.whl", hash = "sha256:ff036bbc1464993552fd1251b0a83fe102af334b301e3896d7aa05a4999ad042", size = 46804, upload_time = "2025-11-14T14:58:14.113Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/8c/95/e10f33a8d4fc17f9b933d451038218437f9326c2abb15a3e7f58ce2a06ec/cymem-2.0.13-cp314-cp314t-macosx_11_0_arm64.whl", hash = "sha256:fb8291691ba7ff4e6e000224cc97a744a8d9588418535c9454fd8436911df612", size = 46254, upload_time = "2025-11-14T14:58:15.156Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/e7/7a/5efeb2d2ea6ebad2745301ad33a4fa9a8f9a33b66623ee4d9185683007a6/cymem-2.0.13-cp314-cp314t-manylinux2014_aarch64.manylinux_2_17_aarch64.whl", hash = "sha256:d8d06ea59006b1251ad5794bcc00121e148434826090ead0073c7b7fedebe431", size = 296061, upload_time = "2025-11-14T14:58:16.254Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/0b/28/2a3f65842cc8443c2c0650cf23d525be06c8761ab212e0a095a88627be1b/cymem-2.0.13-cp314-cp314t-manylinux2014_x86_64.manylinux_2_17_x86_64.whl", hash = "sha256:c0046a619ecc845ccb4528b37b63426a0cbcb4f14d7940add3391f59f13701e6", size = 285784, upload_time = "2025-11-14T14:58:17.412Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/98/73/dd5f9729398f0108c2e71d942253d0d484d299d08b02e474d7cfc43ed0b0/cymem-2.0.13-cp314-cp314t-musllinux_1_2_aarch64.whl", hash = "sha256:18ad5b116a82fa3674bc8838bd3792891b428971e2123ae8c0fd3ca472157c5e", size = 288062, upload_time = "2025-11-14T14:58:20.225Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/5a/01/ffe51729a8f961a437920560659073e47f575d4627445216c1177ecd4a41/cymem-2.0.13-cp314-cp314t-musllinux_1_2_x86_64.whl", hash = "sha256:666ce6146bc61b9318aa70d91ce33f126b6344a25cf0b925621baed0c161e9cc", size = 290465, upload_time = "2025-11-14T14:58:21.815Z" },[m
[32m+[m[32m    { url = "https://files.pythonhosted.org/packages/fd/ac/c9e7d68607f71ef978c81e334ab2898b426944c71950212b1467186f69f9/cymem-2.0.13-cp314-cp314t-win_amd64.whl", hash = "sha256:84c1168c563d9d1e04546cb65e3e54fde2bf814f7c7faf11fc06436598e386d1", size = 46665, upload_time = "2025-11-14T14:58:23.512Z" },[m