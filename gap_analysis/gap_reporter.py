"""Gap reporter: synthesize all analyses and generate comprehensive reports."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def prioritize_gaps(semantic_gaps: Dict[str, Any],
                   entity_gaps: Dict[str, Any],
                   taxonomy_gaps: Dict[str, Any],
                   ngram_gaps: Dict[str, Any]) -> Dict[str, List[Any]]:
    """
    Prioritize gaps by engagement potential and ease of creation.
    
    Args:
        semantic_gaps: Semantic clustering gap analysis
        entity_gaps: Entity recognition gap analysis
        taxonomy_gaps: Sociological taxonomy gap analysis
        ngram_gaps: N-gram pattern gap analysis
        
    Returns:
        Dictionary with prioritized gaps
    """
    prioritized = {
        'high_priority_themes': [],
        'missing_entities': [],
        'underrepresented_fields': [],
        'format_recommendations': []
    }
    
    # Extract orphan clusters (missing themes)
    if 'orphan_clusters' in semantic_gaps:
        for cluster_id, cluster_data in semantic_gaps['orphan_clusters'].items():
            if cluster_data['size'] >= 10:  # Only significant clusters
                prioritized['high_priority_themes'].append({
                    'theme': ' '.join(cluster_data['keywords'][:5]),
                    'keywords': cluster_data['keywords'],
                    'size': cluster_data['size'],
                    'priority': 'high' if cluster_data['size'] > 20 else 'medium'
                })
    
    # Sort by size
    prioritized['high_priority_themes'].sort(key=lambda x: x['size'], reverse=True)
    prioritized['high_priority_themes'] = prioritized['high_priority_themes'][:20]
    
    # Missing entities
    for category in ['countries', 'artists', 'movies', 'brands']:
        if category in entity_gaps:
            missing = entity_gaps[category].get('missing', [])[:10]
            prioritized['missing_entities'].extend([
                {'entity': e, 'category': category, 'priority': 'high'}
                for e in missing
            ])
    
    # Underrepresented fields
    if 'underrepresented_fields' in taxonomy_gaps:
        prioritized['underrepresented_fields'] = [
            {'field': field, 'priority': 'high'}
            for field in taxonomy_gaps['underrepresented_fields']
        ]
    
    return prioritized


def create_visualizations(quality_results: Dict[str, Any],
                         entity_results: Dict[str, Any],
                         taxonomy_results: Dict[str, Any],
                         output_dir: str = "outputs"):
    """
    Create visualization charts.
    
    Args:
        quality_results: Quality analysis results
        entity_results: Entity analysis results
        taxonomy_results: Taxonomy analysis results
        output_dir: Output directory
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # 1. Entity Coverage Chart
    if 'coverage_analysis' in entity_results:
        coverage = entity_results['coverage_analysis']
        categories = ['countries', 'artists', 'movies', 'brands']
        coverage_pcts = [
            coverage.get(cat, {}).get('coverage_pct', 0)
            for cat in categories
        ]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, coverage_pcts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
        plt.ylabel('Coverage Percentage (%)', fontsize=12)
        plt.title('Entity Coverage by Category', fontsize=14, fontweight='bold')
        plt.ylim(0, 100)
        
        # Add value labels on bars
        for bar, pct in zip(bars, coverage_pcts):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{pct:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(output_path / 'entity_coverage_chart.png', dpi=300)
        plt.close()
    
    # 2. Taxonomy Coverage Radar Chart
    if 'coverage_results' in taxonomy_results:
        fields = list(taxonomy_results['coverage_results'].keys())
        percentages = [taxonomy_results['coverage_results'][f]['percentage'] for f in fields]
        
        # Create bar chart (radar charts are complex, bar is clearer)
        plt.figure(figsize=(12, 6))
        colors = ['#FF6B6B' if p < 5 else '#4ECDC4' for p in percentages]
        bars = plt.barh(fields, percentages, color=colors)
        plt.xlabel('Coverage Percentage (%)', fontsize=12)
        plt.title('Sociological Taxonomy Coverage', fontsize=14, fontweight='bold')
        plt.axvline(x=5, color='red', linestyle='--', alpha=0.5, label='5% Threshold')
        plt.legend()
        
        # Add value labels
        for bar, pct in zip(bars, percentages):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{pct:.1f}%', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig(output_path / 'taxonomy_coverage_chart.png', dpi=300)
        plt.close()
    
    # 3. Quality Metrics Chart
    if 'metrics' in quality_results:
        metrics = quality_results['metrics']
        quality_items = [
            ('Question Complete', metrics.get('qen_complete_pct', 0)),
            ('Correct Answer Complete', metrics.get('acen_complete_pct', 0)),
            ('Wrong Answer 1 Complete', metrics.get('aw1en_complete_pct', 0)),
            ('Wrong Answer 2 Complete', metrics.get('aw2en_complete_pct', 0))
        ]
        
        items, percentages = zip(*quality_items)
        
        plt.figure(figsize=(10, 6))
        bars = plt.barh(items, percentages, color='#45B7D1')
        plt.xlabel('Completion Percentage (%)', fontsize=12)
        plt.title('Data Quality Metrics', fontsize=14, fontweight='bold')
        plt.xlim(0, 100)
        
        for bar, pct in zip(bars, percentages):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{pct:.1f}%', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig(output_path / 'quality_metrics_chart.png', dpi=300)
        plt.close()


def generate_gap_report(semantic_results: Dict[str, Any],
                       entity_results: Dict[str, Any],
                       taxonomy_results: Dict[str, Any],
                       quality_results: Dict[str, Any],
                       ngram_results: Dict[str, Any],
                       output_path: str = "outputs/gap_analysis_report.md") -> str:
    """
    Generate comprehensive gap analysis report.
    
    Args:
        semantic_results: Semantic clustering results
        entity_results: Entity recognition results
        taxonomy_results: Taxonomy analysis results
        quality_results: Quality analysis results
        ngram_results: N-gram analysis results
        output_path: Output file path
        
    Returns:
        Report content as string
    """
    prioritized = prioritize_gaps(
        semantic_results.get('missing_clusters', {}),
        entity_results.get('coverage_analysis', {}),
        taxonomy_results,
        ngram_results
    )
    
    report_lines = []
    report_lines.append("# Content Gap Analysis Report\n")
    report_lines.append("## Executive Summary\n")
    report_lines.append("This report identifies content gaps in the quiz dataset using multiple analytical strategies.\n")
    
    # Missing Themes
    report_lines.append("\n## 1. Missing Themes (Top 20)\n")
    report_lines.append("Themes identified through semantic clustering that are not well-covered by existing tags:\n\n")
    
    for i, theme in enumerate(prioritized['high_priority_themes'], 1):
        report_lines.append(f"### {i}. {theme['theme']}\n")
        report_lines.append(f"- **Keywords**: {', '.join(theme['keywords'][:10])}\n")
        report_lines.append(f"- **Cluster Size**: {theme['size']} questions\n")
        report_lines.append(f"- **Priority**: {theme['priority'].upper()}\n\n")
    
    # Missing Entities
    report_lines.append("\n## 2. Missing Entities (Top 30)\n")
    report_lines.append("Entities from reference lists that are missing or underrepresented:\n\n")
    
    for category in ['countries', 'artists', 'movies', 'brands']:
        if category in entity_results.get('coverage_analysis', {}):
            coverage = entity_results['coverage_analysis'][category]
            missing = coverage.get('missing', [])[:10]
            if missing:
                report_lines.append(f"### {category.capitalize()}\n")
                report_lines.append(f"- **Coverage**: {coverage.get('coverage_pct', 0):.1f}%\n")
                report_lines.append(f"- **Missing**: {', '.join(missing)}\n\n")
    
    # Underrepresented Fields
    report_lines.append("\n## 3. Underrepresented Social Fields\n")
    if prioritized['underrepresented_fields']:
        for field in prioritized['underrepresented_fields']:
            field_name = field['field']
            coverage = taxonomy_results.get('coverage_results', {}).get(field_name, {})
            report_lines.append(f"### {field_name}\n")
            report_lines.append(f"- **Coverage**: {coverage.get('percentage', 0):.1f}%\n")
            report_lines.append(f"- **Question Count**: {coverage.get('count', 0)}\n\n")
    else:
        report_lines.append("All fields have adequate coverage (>=5%).\n\n")
    
    # Format Recommendations
    report_lines.append("\n## 4. Format Diversity Recommendations\n")
    if 'formats' in quality_results:
        formats = quality_results['formats']
        format_counts = formats.get('format_counts', {})
        report_lines.append("Current question format distribution:\n\n")
        for format_name, count in sorted(format_counts.items(), key=lambda x: x[1], reverse=True):
            report_lines.append(f"- **{format_name}**: {count} questions\n")
        
        report_lines.append("\n### Recommended New Formats:\n")
        report_lines.append("1. **Fill-in-the-Blank (Lyric/Quote)**: Complete popular song lyrics or movie quotes\n")
        report_lines.append("2. **Odd One Out**: Visual or conceptual grouping questions\n")
        report_lines.append("3. **True/False with Twist**: Interesting true/false statements\n")
        report_lines.append("4. **Ranking/Ordering**: Put items in chronological or hierarchical order\n")
        report_lines.append("5. **Visual Description**: Questions about colors, logos, visual elements\n\n")
    
    # Quality Issues
    report_lines.append("\n## 5. Quality Issues\n")
    if 'metrics' in quality_results:
        metrics = quality_results['metrics']
        violations = quality_results.get('dataframe', pd.DataFrame()).get('has_violation', pd.Series()).sum()
        report_lines.append(f"- **Character Limit Violations**: {violations} questions\n")
        report_lines.append(f"- **Duplicate Answers**: {metrics.get('duplicate_answers_count', 0)} questions ({metrics.get('duplicate_answers_pct', 0):.1f}%)\n")
        report_lines.append(f"- **Average Question Length**: {metrics.get('avg_qen_length', 0):.1f} characters\n")
        report_lines.append(f"- **Average Answer Length**: {metrics.get('avg_acen_length', 0):.1f} characters\n\n")
    
    # Actionable Recommendations
    report_lines.append("\n## 6. Actionable Recommendations\n")
    report_lines.append("### High Priority (Immediate Action)\n")
    report_lines.append("1. Create content for top 5 missing themes identified in semantic clustering\n")
    report_lines.append("2. Add questions featuring missing high-profile entities (artists, movies, brands)\n")
    report_lines.append("3. Expand underrepresented social fields (especially those <2% coverage)\n\n")
    
    report_lines.append("### Medium Priority (Short-term)\n")
    report_lines.append("1. Implement new question formats to increase diversity\n")
    report_lines.append("2. Fix character limit violations\n")
    report_lines.append("3. Address duplicate answer issues\n\n")
    
    report_lines.append("### Low Priority (Long-term)\n")
    report_lines.append("1. Continuously monitor n-gram patterns for emerging topics\n")
    report_lines.append("2. Update reference lists based on current trends\n")
    report_lines.append("3. Refine clustering parameters based on new content\n\n")
    
    # Write report
    report_content = '\n'.join(report_lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"Gap analysis report saved to {output_path}")
    
    return report_content


def synthesize_analyses(semantic_results: Dict[str, Any],
                       entity_results: Dict[str, Any],
                       taxonomy_results: Dict[str, Any],
                       quality_results: Dict[str, Any],
                       ngram_results: Dict[str, Any],
                       output_dir: str = "outputs") -> Dict[str, Any]:
    """
    Synthesize all analyses and generate comprehensive reports.
    
    Args:
        semantic_results: Semantic clustering results
        entity_results: Entity recognition results
        taxonomy_results: Taxonomy analysis results
        quality_results: Quality analysis results
        ngram_results: N-gram analysis results
        output_dir: Output directory
        
    Returns:
        Dictionary with synthesized results
    """
    print("Synthesizing all analyses...")
    
    # Create visualizations
    create_visualizations(quality_results, entity_results, taxonomy_results, output_dir)
    
    # Generate comprehensive report
    report_content = generate_gap_report(
        semantic_results, entity_results, taxonomy_results,
        quality_results, ngram_results,
        output_path=f"{output_dir}/gap_analysis_report.md"
    )
    
    # Prioritize gaps
    prioritized = prioritize_gaps(
        semantic_results.get('missing_clusters', {}),
        entity_results.get('coverage_analysis', {}),
        taxonomy_results,
        ngram_results
    )
    
    return {
        'prioritized_gaps': prioritized,
        'report_content': report_content,
        'summary': {
            'missing_themes': len(prioritized['high_priority_themes']),
            'missing_entities': len(prioritized['missing_entities']),
            'underrepresented_fields': len(prioritized['underrepresented_fields'])
        }
    }

