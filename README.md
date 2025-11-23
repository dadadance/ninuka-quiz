# Ninuka Quiz - Content Gap Analysis & Question Generator

A comprehensive Python-based system for analyzing quiz datasets, identifying content gaps, and generating new questions based on discovered gaps. This project uses advanced NLP techniques including semantic clustering, entity recognition, and sociological taxonomy analysis to provide actionable insights for quiz content improvement.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Pipeline](#analysis-pipeline)
- [Output Files](#output-files)
- [Known Issues](#known-issues)
- [Requirements](#requirements)
- [Development](#development)

## 🎯 Overview

This project analyzes a quiz dataset containing ~12,909 questions to identify:
- **Content gaps**: Missing themes, topics, and question formats
- **Quality issues**: Character limit violations, data quality problems
- **Coverage gaps**: Underrepresented entities, fields, and categories
- **Semantic patterns**: Clusters of similar questions and missing clusters

Based on the analysis, the system can automatically generate new questions that fill identified gaps while maintaining quality standards (e.g., <100 character limit per question/answer).

## ✨ Features

### Gap Analysis Pipeline

1. **Data Quality Analysis**
   - Character length validation
   - Missing value detection
   - Data completeness metrics

2. **N-gram Pattern Analysis**
   - Bigram and trigram extraction
   - Common phrase identification
   - Pattern frequency analysis

3. **Entity Recognition**
   - Named entity extraction (PERSON, ORG, GPE, PRODUCT)
   - Entity coverage analysis
   - Comparison against reference lists (artists, brands, countries, movies)

4. **Sociological Taxonomy Analysis**
   - Multi-field coverage assessment
   - Underrepresented field identification
   - Social domain classification

5. **Semantic Clustering**
   - Question embedding generation using sentence transformers
   - K-means clustering for topic discovery
   - Gap identification through cluster analysis
   - Visualization with UMAP dimensionality reduction

6. **Comprehensive Reporting**
   - Markdown gap analysis reports
   - CSV exports for all analyses
   - Visual charts and cluster visualizations

### Question Generator

1. **Gap-Based Generation**
   - Loads identified gaps from analysis
   - Generates questions targeting specific gaps
   - Multiple question templates and formats

2. **Quality Validation**
   - Character limit enforcement
   - Format validation
   - Answer quality checks

3. **Export Options**
   - Excel export (`.xlsx`)
   - CSV export (`.csv`)
   - Both formats simultaneously

## 📁 Project Structure

```
ninuka-quiz/
├── main.py                          # Excel file reader and analyzer
├── run_gap_analysis.py              # Main gap analysis pipeline
├── generate_questions.py            # Question generator script
├── ninouk2.xlsx                     # Input Excel file (quiz dataset)
├── pyproject.toml                   # Project dependencies (uv)
├── uv.lock                          # Dependency lock file
│
├── gap_analysis/                    # Gap analysis modules
│   ├── __init__.py
│   ├── data_loader.py              # Excel data loading and preparation
│   ├── quality_checker.py          # Quality metrics and validation
│   ├── ngram_analysis.py           # N-gram pattern extraction
│   ├── entity_recognition.py       # Named entity recognition
│   ├── sociological_taxonomy.py    # Field coverage analysis
│   ├── semantic_clustering.py      # Semantic clustering and embeddings
│   ├── gap_reporter.py             # Report synthesis and generation
│   └── utils.py                     # Utility functions
│
├── question_generator/              # Question generation modules
│   ├── __init__.py
│   ├── gap_loader.py               # Load gap analysis results
│   ├── question_templates.py      # Question format templates
│   ├── question_generator.py       # Main generation logic
│   ├── answer_generator.py         # Answer generation
│   ├── question_validator.py       # Quality validation
│   └── question_exporter.py        # Export functionality
│
├── data/
│   └── reference_lists/            # Reference data for comparison
│       ├── top_artists.json
│       ├── top_brands.json
│       ├── top_countries.json
│       └── top_movies.json
│
├── outputs/                         # Generated analysis outputs
│   ├── gap_analysis_report.md      # Main comprehensive report
│   ├── quality_report.csv          # Quality metrics
│   ├── quality_report_violations.csv
│   ├── ngram_patterns.csv          # N-gram patterns
│   ├── taxonomy_coverage.csv       # Field coverage analysis
│   ├── entity_coverage.csv         # Entity analysis (if spaCy works)
│   ├── clusters_visualization.png  # Cluster visualization
│   ├── quality_metrics_chart.png   # Quality charts
│   ├── taxonomy_coverage_chart.png # Taxonomy charts
│   ├── entity_coverage_chart.png  # Entity charts
│   └── pipeline_*.log              # Pipeline execution logs
│
└── outputs/                         # Generated questions (after generation)
    ├── generated_questions.xlsx
    └── generated_questions.csv
```

## 🚀 Installation

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd ninuka-quiz
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Install spaCy model (required for entity recognition):**
   ```bash
   uv run python -m spacy download en_core_web_sm
   ```
   
4. **Verify installation:**
   ```bash
   uv run python main.py
   ```

## 💻 Usage

### 1. Basic Excel File Analysis

Analyze the structure and contents of the Excel file:

```bash
uv run python main.py
```

This will:
- Display file information (size, path)
- Show all sheets in the Excel file
- Analyze each sheet with detailed statistics
- Display data previews, column information, and quality metrics

### 2. Run Complete Gap Analysis Pipeline

Run the full gap analysis pipeline:

```bash
uv run python run_gap_analysis.py
```

Or specify a custom Excel file:

```bash
uv run python run_gap_analysis.py --excel path/to/your/file.xlsx
```

**Pipeline Phases:**
1. **Data Preparation** - Loads and prepares the dataset
2. **Quality Analysis** - Validates data quality and character limits
3. **N-gram Analysis** - Extracts common patterns
4. **Entity Recognition** - Identifies named entities (if spaCy model available)
5. **Sociological Taxonomy** - Analyzes field coverage
6. **Semantic Clustering** - Groups questions by semantic similarity
7. **Gap Synthesis** - Combines all analyses into a comprehensive report

**Expected Duration:** 30-60 minutes (depending on hardware, semantic clustering is the slowest phase)

**Output:** All results saved to `outputs/` directory

### 3. Generate Questions from Gaps

Generate new questions based on identified gaps:

```bash
# Generate 100 questions (default)
uv run python generate_questions.py

# Generate specific number of questions
uv run python generate_questions.py --num 200

# Export in different formats
uv run python generate_questions.py --num 100 --format excel
uv run python generate_questions.py --num 100 --format csv
uv run python generate_questions.py --num 100 --format both
```

**Requirements:** Gap analysis should be run first (generates `outputs/gap_analysis_report.md`)

**Output:** 
- `outputs/generated_questions.xlsx` (if Excel format)
- `outputs/generated_questions.csv` (if CSV format)

## 🔬 Analysis Pipeline Details

### Phase 1: Data Preparation
- Loads Excel file with multiple sheets
- Cleans and standardizes text data
- Extracts metadata (categories, tags, question types)
- Prepares data for analysis

### Phase 2: Quality Analysis
- **Character Limit Check**: Validates <100 character requirement
- **Missing Value Detection**: Identifies incomplete records
- **Data Completeness**: Calculates coverage metrics
- **Violation Reporting**: Lists all records that violate constraints

### Phase 3: N-gram Analysis
- Extracts bigrams and trigrams from questions
- Identifies most common phrases
- Analyzes pattern frequencies
- Exports top patterns for review

### Phase 4: Entity Recognition
- Uses spaCy NER model to extract entities
- Categories: PERSON, ORG, GPE (location), PRODUCT
- Compares against reference lists:
  - Top artists (Spotify)
  - Top brands (recognition)
  - Top countries (tourism)
  - Top movies (box office)
- Identifies missing/underrepresented entities

### Phase 5: Sociological Taxonomy
- Analyzes coverage across social fields:
  - Domestic Sphere (cooking, cleaning, pets)
  - Digital Life (emojis, apps, memes)
  - Nostalgia (90s, 2000s, retro)
  - Somatic/Body (health, fitness, anatomy)
- Identifies underrepresented fields
- Generates coverage metrics

### Phase 6: Semantic Clustering
- Generates embeddings for all questions using `sentence-transformers`
- Applies K-means clustering (configurable number of clusters)
- Uses UMAP for dimensionality reduction and visualization
- Identifies:
  - Dense clusters (well-covered topics)
  - Sparse regions (content gaps)
  - Missing semantic themes

**Performance Note:** This is the slowest phase (20-40 minutes) due to embedding generation for ~12,909 questions.

### Phase 7: Gap Synthesis
- Combines results from all phases
- Generates comprehensive markdown report
- Creates visualizations (charts, cluster maps)
- Exports CSV files for further analysis

## 📊 Output Files

### Reports

- **`gap_analysis_report.md`** - Main comprehensive report with:
  - Executive summary
  - Missing themes (top 20)
  - Missing entities
  - Underrepresented fields
  - Quality metrics summary
  - Recommendations

### Data Exports

- **`quality_report.csv`** - Quality metrics per question
- **`quality_report_violations.csv`** - Questions violating constraints
- **`ngram_patterns.csv`** - Top n-gram patterns with frequencies
- **`taxonomy_coverage.csv`** - Field coverage statistics
- **`entity_coverage.csv`** - Entity frequency and coverage

### Visualizations

- **`clusters_visualization.png`** - UMAP visualization of semantic clusters
- **`quality_metrics_chart.png`** - Quality metrics bar charts
- **`taxonomy_coverage_chart.png`** - Field coverage visualization
- **`entity_coverage_chart.png`** - Entity coverage charts

### Logs

- **`pipeline_YYYYMMDD_HHMMSS.log`** - Detailed execution logs for each pipeline run

### Generated Questions

- **`generated_questions.xlsx`** - Excel file with generated questions
- **`generated_questions.csv`** - CSV file with generated questions

## ⚠️ Known Issues

*(No known major issues currently)*

## 📦 Requirements

### Python Version
- **Required:** Python 3.12+ (Python 3.13 is supported)

### Dependencies

All dependencies are managed via `uv` and specified in `pyproject.toml`:

- `pandas>=2.3.3` - Data manipulation
- `openpyxl>=3.1.5` - Excel file reading
- `sentence-transformers>=2.2.0` - Semantic embeddings
- `scikit-learn>=1.3.0` - Clustering and ML
- `spacy>=3.7.0` - Named entity recognition
- `umap-learn>=0.5.0` - Dimensionality reduction
- `matplotlib>=3.8.0` - Visualization
- `seaborn>=0.13.0` - Statistical visualization
- `numpy>=1.26.0` - Numerical computing
- `nltk>=3.8.0` - Natural language processing
- `wordcloud>=1.9.0` - Word cloud generation

### Package Management

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management:

```bash
# Add a new dependency
uv add package-name

# Run a script
uv run python script.py

# Sync dependencies
uv sync
```

## 🛠️ Development

### Project Status

✅ **Completed:**
- Gap analysis pipeline (all phases)
- Question generator system
- Quality validation
- Comprehensive reporting
- Visualization generation
- Entity recognition (spaCy model integrated)

### Adding New Analysis Modules

1. Create a new module in `gap_analysis/`
2. Implement analysis function that returns a dictionary of results
3. Add import and call in `run_gap_analysis.py`
4. Update `gap_reporter.py` to include new results in synthesis

### Extending Question Templates

1. Edit `question_generator/question_templates.py`
2. Add new template functions
3. Update `question_generator/question_generator.py` to use new templates

### Running Tests

Currently, no formal test suite is included. Manual testing is done by:
1. Running the pipeline on sample data
2. Validating output files
3. Checking log files for errors

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines if applicable]

## 📧 Contact

[Add contact information if applicable]

---

**Last Updated:** 2025-11-23

**Project Version:** 0.1.0

