# Content Gap Analysis Assignment - Strategic Breakdown

## Part 1: Assignment Analysis

### Current Dataset Profile
- **Size**: 12,909 questions (not 20k, but substantial)
- **Question Types**: photo, text, video, audio
- **Structure**: Questions (QEN), Correct Answer (ACEN), Wrong Answers (AW1EN, AW2EN)
- **Categories**: 7 main categories (Education, Entertainment, Travel, Technology, Sports, Nature, Business&Politics)
- **Tags**: 24 tags with hierarchical structure (e.g., :PEOPLE, ED:HISTORY)

### Constraints & Requirements
1. **Brevity**: <100 characters per question/answer
2. **Difficulty**: Easy/casual for retention
3. **Engagement**: Universal appeal (pop culture, lifestyle, common facts)
4. **Goal**: Identify missing themes, sub-cultures, question formats

---

## Part 2: Strategic Framework

### A. Comprehensive Taxonomy (Multi-Tiered Classification)

#### Tier 1: Macro-Domains (8 categories)
1. **Digital Culture** - Internet, social media, memes, apps
2. **Pop Culture** - Music, movies, TV, celebrities, trends
3. **Lifestyle** - Food, fashion, home, wellness, daily life
4. **Visual Memory** - Logos, colors, brands, icons, emojis
5. **Nostalgia** - Decades (90s, 2000s), childhood, retro
6. **Common Knowledge** - Everyday facts, adulting, practical
7. **Social Phenomena** - Trends, slang, viral content, communities
8. **Sensory Knowledge** - Sounds, lyrics, textures, smells

#### Tier 2: Micro-Niches (40+ subcategories)
**Digital Culture:**
- Social Media Platforms & Features
- Memes & Viral Content
- App Icons & UI Elements
- Internet Slang (Gen Z/Alpha)
- Influencer Culture
- Gaming Culture (Mobile, Console, PC)

**Pop Culture:**
- Music Charts & Streaming
- Movie Franchises & Sequels
- TV Shows & Streaming Originals
- Celebrity Relationships & Drama
- Award Shows & Events
- Fashion Trends & Brands

**Lifestyle:**
- Food & Cooking Hacks
- Home & Decor Trends
- Wellness & Self-Care
- Shopping & Retail
- Travel Destinations (Instagram-worthy)
- Fitness & Health Trends

**Visual Memory:**
- Brand Logos & Colors
- Product Packaging
- Street Signs & Symbols
- Emoji Meanings & Usage
- UI/UX Elements
- Visual Patterns

**Nostalgia:**
- 90s Pop Culture
- 2000s Trends
- Childhood Toys & Games
- Retro Technology
- Old School Music
- Vintage Fashion

**Common Knowledge:**
- Adulting Skills
- Basic Science (Everyday)
- Common Sense Facts
- Practical Life Hacks
- Weather & Nature Basics
- Time & Calendar Facts

**Social Phenomena:**
- TikTok Trends
- YouTube Culture
- Twitter/X Moments
- Reddit Culture
- Online Communities
- Digital Etiquette

**Sensory Knowledge:**
- Song Lyrics & Hooks
- Sound Effects
- Commercial Jingles
- Theme Songs
- Audio Branding

---

### B. Negative Space: 10 Missing Micro-Niches

Based on traditional trivia gaps but high mobile engagement:

1. **Emoji Semantics** - "What does this emoji sequence mean?" (e.g., 🍕💔 = pizza breakup)
2. **App Icon Recognition** - "Which app has this icon?" (visual memory, universal)
3. **Brand Color Palettes** - "What color is Spotify's logo?" (visual, accessible)
4. **TikTok Sound Trends** - "Complete this TikTok audio: 'Oh no, oh no, oh no no no...'"
5. **Gen Z Slang** - "What does 'no cap' mean?" (cultural currency)
6. **Product Packaging** - "Which brand uses this bottle shape?" (visual memory)
7. **Lyric Completion** - "Complete: 'I'm a Barbie girl, in a...'" (nostalgia + memory)
8. **Common Sense Adulting** - "How often should you change your bed sheets?" (practical)
9. **Viral Meme Formats** - "What meme format is this?" (cultural literacy)
10. **UI/UX Patterns** - "What does this icon mean in apps?" (digital literacy)

---

### C. Format Variations (5 Unique Structures)

1. **Fill-in-the-Blank (Lyric/Quote)**
   - "Complete: 'To infinity and _____!'" (Toy Story)
   - Character limit: ~60 chars

2. **Odd One Out (Visual/Conceptual)**
   - "Which doesn't belong: 🍕 🍔 🌮 🍎"
   - Character limit: ~50 chars

3. **True/False with Twist**
   - "True or False: The 'like' button was originally a star on Facebook"
   - Character limit: ~80 chars

4. **Ranking/Ordering**
   - "Put these in order: Instagram, TikTok, Facebook (by launch date)"
   - Character limit: ~70 chars

5. **Visual Description**
   - "What color combination is McDonald's logo?" (Red + Yellow)
   - Character limit: ~60 chars

---

## Part 3: Implementation Strategy

### Python Workflow Architecture

#### Phase 1: Data Preparation & Exploration
- Load and clean question text
- Extract metadata (categories, tags, question types)
- Character length analysis
- Basic keyword extraction

#### Phase 2: Strategy A - Semantic Clustering
**Tools Needed:**
- `sentence-transformers` (for embeddings)
- `scikit-learn` (KMeans, HDBSCAN)
- `umap-learn` or `matplotlib` (visualization)

**Process:**
1. Generate embeddings for all questions
2. Cluster into 50-100 semantic groups
3. Extract keywords per cluster
4. Visualize with t-SNE/UMAP
5. Identify sparse regions (gaps)

#### Phase 3: Strategy B - Named Entity Recognition
**Tools Needed:**
- `spacy` (NER model)
- Reference lists (countries, celebrities, brands)

**Process:**
1. Extract entities (PERSON, ORG, GPE, PRODUCT)
2. Count frequency distributions
3. Compare against "expected" lists:
   - Top 50 countries by tourism
   - Top 100 Spotify artists
   - Top 50 movies (box office)
   - Top brands by recognition
4. Flag missing/underrepresented entities

#### Phase 4: Strategy C - Sociological Taxonomy
**Tools Needed:**
- Custom keyword dictionaries
- Regex patterns for domain detection

**Process:**
1. Create keyword dictionaries for each social field:
   - Domestic Sphere (cooking, cleaning, pets, gardening)
   - Digital Life (emojis, apps, slang, memes)
   - Nostalgia (90s, 2000s, toys, cartoons)
   - Somatic/Body (sleep, anatomy, fitness, health)
2. Search questions for keyword matches
3. Count coverage per field
4. Identify underrepresented fields

#### Phase 5: Gap Analysis & Reporting
- Combine results from all three strategies
- Generate gap report with:
  - Missing themes
  - Underrepresented entities
  - Format diversity analysis
  - Character length compliance check
  - Difficulty assessment (if possible)

---

## Part 4: Implementation Plan

### Dependencies to Add
```toml
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
spacy>=3.7.0
umap-learn>=0.5.0
matplotlib>=3.8.0
seaborn>=0.13.0
numpy>=1.26.0
```

### File Structure
```
ninuka-quiz/
├── main.py (existing)
├── gap_analysis/
│   ├── __init__.py
│   ├── semantic_clustering.py (Strategy A)
│   ├── entity_recognition.py (Strategy B)
│   ├── sociological_taxonomy.py (Strategy C)
│   └── gap_reporter.py (combine & report)
├── data/
│   └── reference_lists/ (countries, artists, etc.)
└── outputs/
    ├── clusters_visualization.png
    ├── entity_coverage.csv
    ├── taxonomy_coverage.csv
    └── gap_analysis_report.md
```

### Execution Flow
1. **Data Loading** - Load Excel, clean text
2. **Parallel Analysis** - Run all 3 strategies
3. **Synthesis** - Combine findings
4. **Visualization** - Generate charts/maps
5. **Reporting** - Create actionable gap report

---

## Next Steps

1. **Review this analysis** - Confirm taxonomy and approach
2. **Approve dependencies** - Add required packages
3. **Implement incrementally** - Start with one strategy, validate, then expand
4. **Iterate** - Refine based on initial results

---

## Key Questions for Validation

1. Should we focus on all 12,909 questions or sample for clustering?
2. What's the target number of clusters? (50-100 suggested)
3. Do you have reference lists for comparison, or should we generate them?
4. What's the priority: speed (sampling) vs. accuracy (full dataset)?
5. Should we also analyze answer quality/character limits?

