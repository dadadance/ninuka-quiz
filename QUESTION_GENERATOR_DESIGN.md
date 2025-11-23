# Question Generator System - Design Document

## Overview
System to automatically generate new quiz questions based on identified content gaps from the gap analysis.

## Requirements
1. **Input**: Gap analysis results (missing themes, entities, fields, formats)
2. **Output**: New questions that fill identified gaps
3. **Constraints**:
   - Questions < 100 characters
   - Answers < 100 characters
   - Easy/casual difficulty
   - Universally engaging topics
   - Format diversity

## Architecture

### Phase 1: Gap Analysis Integration
- Load gap analysis results (CSV, JSON, markdown report)
- Parse missing themes, entities, underrepresented fields
- Prioritize gaps by engagement potential

### Phase 2: Question Templates
Create templates for different question formats:
1. **Fill-in-the-Blank**: "Complete: 'I'm a Barbie girl, in a _____'"
2. **Odd One Out**: "Which doesn't belong: 🍕 🍔 🌮 🍎"
3. **True/False**: "True or False: The 'like' button was originally a star on Facebook"
4. **Visual Description**: "What color is Spotify's logo?"
5. **Standard**: "What is X?", "Which country...", "Name the..."

### Phase 3: Content Sources
- **Missing Entities**: Use reference lists (artists, movies, brands, countries)
- **Missing Themes**: Use semantic cluster keywords
- **Underrepresented Fields**: Use keyword dictionaries from taxonomy
- **Format Gaps**: Use identified missing question patterns

### Phase 4: Question Generation Strategies

#### Strategy A: Entity-Based Generation
- For each missing entity (e.g., "Taylor Swift", "Thailand")
- Generate questions using templates
- Examples:
  - "Which country is Bangkok the capital of?" (Thailand)
  - "Who sang 'Shake It Off'?" (Taylor Swift)

#### Strategy B: Theme-Based Generation
- For each missing theme (e.g., "TikTok trends", "emoji meanings")
- Generate questions about that theme
- Examples:
  - "What does this emoji mean: 🍕💔?" (pizza breakup)
  - "Which app uses this icon?" (visual recognition)

#### Strategy C: Field-Based Generation
- For underrepresented fields (e.g., "Digital Life", "Nostalgia")
- Generate questions using field-specific keywords
- Examples:
  - "What decade was the Walkman popular?" (Nostalgia)
  - "What does 'no cap' mean?" (Digital Life/Gen Z slang)

#### Strategy D: Format-Based Generation
- For missing question formats
- Generate questions using new formats
- Examples:
  - Fill-in-the-blank lyrics
  - Odd one out visual questions

### Phase 5: Answer Generation
- **Correct Answer**: Based on fact/knowledge
- **Wrong Answers**: 
  - Similar but incorrect (same category)
  - Plausible distractors
  - Common misconceptions

### Phase 6: Validation & Quality Control
- Character limit check (< 100 chars)
- Format validation
- Uniqueness check (not duplicate)
- Difficulty assessment (easy/casual)
- Answer quality (no duplicates, plausible)

## Implementation Plan

### Module 1: `gap_loader.py`
- Load and parse gap analysis results
- Extract prioritized gaps
- Structure data for question generation

### Module 2: `question_templates.py`
- Define question templates
- Template selection logic
- Format-specific generators

### Module 3: `content_sources.py`
- Access reference lists
- Entity information lookup
- Theme-specific content

### Module 4: `question_generator.py`
- Main generation logic
- Strategy selection
- Question assembly

### Module 5: `answer_generator.py`
- Correct answer generation
- Wrong answer generation
- Distractor selection

### Module 6: `question_validator.py`
- Character limit validation
- Format validation
- Uniqueness check
- Quality scoring

### Module 7: `question_exporter.py`
- Export to Excel (matching original format)
- Export to CSV
- Export to JSON

## Output Format
Match original Excel structure:
- QTYPE: text, photo, video, audio
- QID: Auto-generated
- category_id: Based on gap category
- QEN: Generated question
- ACEN: Correct answer
- AW1EN: Wrong answer 1
- AW2EN: Wrong answer 2
- tags: Based on gap tags
- ACID, AWID1, AWID2: Auto-generated IDs

## Example Workflow
1. Load gap analysis → Identify "Taylor Swift" is missing
2. Select template → "Who sang '[song]'?"
3. Generate question → "Who sang 'Shake It Off'?"
4. Generate answers → Correct: "Taylor Swift", Wrong: "Ariana Grande", "Selena Gomez"
5. Validate → All < 100 chars, unique, easy difficulty
6. Export → Add to Excel with appropriate tags

## Quality Metrics
- Character compliance: 100%
- Format diversity: Multiple formats used
- Gap coverage: % of identified gaps addressed
- Answer quality: Plausible distractors
- Uniqueness: No duplicates with existing questions

