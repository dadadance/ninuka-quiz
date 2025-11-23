"""Semantic clustering: map existing tags and identify missing clusters."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from collections import Counter
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans, HDBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
import umap
import matplotlib.pyplot as plt
import seaborn as sns


def load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """Load sentence transformer model for embeddings."""
    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)
    return model


def generate_embeddings(texts: List[str], model) -> np.ndarray:
    """
    Generate embeddings for texts.
    
    Args:
        texts: List of text strings
        model: SentenceTransformer model
        
    Returns:
        Array of embeddings
    """
    print(f"Generating embeddings for {len(texts)} texts...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    return embeddings


def find_optimal_k(embeddings: np.ndarray, max_k: int = 20) -> int:
    """
    Find optimal number of clusters using elbow method.
    
    Args:
        embeddings: Embedding vectors
        max_k: Maximum k to test
        
    Returns:
        Optimal k value
    """
    inertias = []
    k_range = range(2, min(max_k + 1, len(embeddings) // 10))
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(embeddings)
        inertias.append(kmeans.inertia_)
    
    # Simple elbow detection: find point with maximum curvature
    if len(inertias) < 3:
        return 2
    
    # Calculate second derivative
    diffs = np.diff(inertias)
    second_diffs = np.diff(diffs)
    if len(second_diffs) > 0:
        optimal_idx = np.argmax(second_diffs) + 2
        return list(k_range)[optimal_idx]
    
    return 5  # Default


def extract_keywords_from_cluster(texts: List[str], top_n: int = 10) -> List[str]:
    """
    Extract top keywords from a cluster using TF-IDF.
    
    Args:
        texts: List of texts in cluster
        top_n: Number of keywords to extract
        
    Returns:
        List of top keywords
    """
    if len(texts) == 0:
        return []
    
    vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english', ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top features
        scores = tfidf_matrix.sum(axis=0).A1
        top_indices = scores.argsort()[-top_n:][::-1]
        keywords = [feature_names[i] for i in top_indices]
        
        return keywords
    except:
        # Fallback: simple word frequency
        all_words = ' '.join(texts).lower().split()
        word_freq = Counter(all_words)
        return [word for word, _ in word_freq.most_common(top_n)]


def map_existing_tags_to_clusters(df: pd.DataFrame, model) -> Dict[str, Any]:
    """
    Map existing tags to semantic clusters.
    
    Args:
        df: Questions dataframe
        model: Embedding model
        
    Returns:
        Dictionary with tag-based cluster analysis
    """
    print("Mapping existing tags to semantic clusters...")
    
    tag_clusters = {}
    
    # Group by existing tags
    if 'tag_ids' in df.columns:
        # Get unique tag combinations
        df['tag_ids_str'] = df['tag_ids'].apply(lambda x: ','.join(map(str, sorted(x))) if x else 'no_tags')
        
        for tag_combo, group_df in df.groupby('tag_ids_str'):
            if len(group_df) < 2:  # Skip groups with too few questions
                continue
            
            texts = group_df['combined_text'].tolist()
            embeddings = generate_embeddings(texts, model)
            
            # Find optimal k for this tag group
            optimal_k = find_optimal_k(embeddings, max_k=min(10, len(group_df) // 5))
            optimal_k = max(2, min(optimal_k, len(group_df) // 2))
            
            # Cluster
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(embeddings)
            
            # Extract keywords for each cluster
            cluster_keywords = {}
            for cluster_id in range(optimal_k):
                cluster_texts = [texts[i] for i in range(len(texts)) if cluster_labels[i] == cluster_id]
                keywords = extract_keywords_from_cluster(cluster_texts, top_n=10)
                cluster_keywords[cluster_id] = {
                    'keywords': keywords,
                    'size': len(cluster_texts),
                    'sample_questions': group_df.iloc[[i for i in range(len(texts)) if cluster_labels[i] == cluster_id][:3]]['QEN'].tolist()
                }
            
            tag_clusters[tag_combo] = {
                'total_questions': len(group_df),
                'num_clusters': optimal_k,
                'clusters': cluster_keywords,
                'tag_names': group_df.iloc[0]['tag_names'] if 'tag_names' in group_df.columns else []
            }
    
    return tag_clusters


def identify_missing_clusters(df: pd.DataFrame, model, min_cluster_size: int = 10) -> Dict[str, Any]:
    """
    Identify missing semantic clusters using HDBSCAN.
    
    Args:
        df: Questions dataframe
        model: Embedding model
        min_cluster_size: Minimum cluster size for HDBSCAN
        
    Returns:
        Dictionary with missing cluster analysis
    """
    print("Identifying missing semantic clusters...")
    
    # Generate embeddings for all questions
    texts = df['combined_text'].tolist()
    embeddings = generate_embeddings(texts, model)
    
    # Reduce dimensionality for HDBSCAN
    print("Reducing dimensionality with UMAP...")
    reducer = umap.UMAP(n_components=50, random_state=42, n_neighbors=15, min_dist=0.1)
    reduced_embeddings = reducer.fit_transform(embeddings)
    
    # Cluster with HDBSCAN
    print("Clustering with HDBSCAN...")
    clusterer = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=5)
    cluster_labels = clusterer.fit_predict(reduced_embeddings)
    
    # Analyze clusters
    unique_clusters = set(cluster_labels)
    if -1 in unique_clusters:
        unique_clusters.remove(-1)  # Remove noise label
    
    discovered_clusters = {}
    for cluster_id in unique_clusters:
        cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
        cluster_texts = [texts[i] for i in cluster_indices]
        cluster_questions = df.iloc[cluster_indices]
        
        # Extract keywords
        keywords = extract_keywords_from_cluster(cluster_texts, top_n=10)
        
        # Check if this cluster matches existing tags
        if 'tag_ids' in cluster_questions.columns:
            tag_ids_in_cluster = set()
            for tag_list in cluster_questions['tag_ids']:
                tag_ids_in_cluster.update(tag_list)
        else:
            tag_ids_in_cluster = set()
        
        discovered_clusters[cluster_id] = {
            'keywords': keywords,
            'size': len(cluster_indices),
            'tag_ids': list(tag_ids_in_cluster),
            'sample_questions': cluster_questions['QEN'].head(5).tolist(),
            'question_ids': cluster_questions['QID'].head(10).tolist()
        }
    
    # Identify orphan clusters (those not well-covered by existing tags)
    orphan_clusters = {}
    for cluster_id, cluster_data in discovered_clusters.items():
        # If cluster has few or no tags, it's potentially a gap
        if len(cluster_data['tag_ids']) == 0 or cluster_data['size'] > 20:
            orphan_clusters[cluster_id] = cluster_data
    
    return {
        'all_clusters': discovered_clusters,
        'orphan_clusters': orphan_clusters,
        'cluster_labels': cluster_labels,
        'reduced_embeddings': reduced_embeddings,
        'num_clusters': len(unique_clusters),
        'noise_points': list(cluster_labels).count(-1)
    }


def visualize_clusters(cluster_analysis: Dict[str, Any],
                       tag_clusters: Dict[str, Any],
                       output_path: str = "outputs/clusters_visualization.png"):
    """
    Visualize clusters using UMAP.
    
    Args:
        cluster_analysis: Missing cluster analysis results
        tag_clusters: Tag-based cluster analysis
        output_path: Output file path
    """
    print("Creating cluster visualization...")
    
    reduced_embeddings = cluster_analysis['reduced_embeddings']
    cluster_labels = cluster_analysis['cluster_labels']
    
    # Further reduce to 2D for visualization
    reducer_2d = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.1)
    embeddings_2d = reducer_2d.fit_transform(reduced_embeddings)
    
    plt.figure(figsize=(14, 10))
    
    # Plot clusters
    unique_labels = set(cluster_labels)
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_labels)))
    
    for i, label in enumerate(unique_labels):
        if label == -1:
            # Noise points
            mask = cluster_labels == label
            plt.scatter(embeddings_2d[mask, 0], embeddings_2d[mask, 1],
                       c='gray', alpha=0.1, s=10, label='Noise' if i == 0 else '')
        else:
            mask = cluster_labels == label
            plt.scatter(embeddings_2d[mask, 0], embeddings_2d[mask, 1],
                       c=[colors[i]], alpha=0.6, s=20, label=f'Cluster {label}')
    
    plt.title('Semantic Clusters Visualization (UMAP)', fontsize=16)
    plt.xlabel('UMAP Dimension 1', fontsize=12)
    plt.ylabel('UMAP Dimension 2', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Cluster visualization saved to {output_path}")


def analyze_semantic_clustering(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Complete semantic clustering analysis pipeline.
    
    Args:
        df: Questions dataframe
        
    Returns:
        Dictionary with all clustering analysis results
    """
    model = load_embedding_model()
    
    # Part A: Map existing tags to clusters
    tag_clusters = map_existing_tags_to_clusters(df, model)
    
    # Part B: Identify missing clusters
    missing_clusters = identify_missing_clusters(df, model)
    
    # Visualize
    visualize_clusters(missing_clusters, tag_clusters)
    
    return {
        'tag_clusters': tag_clusters,
        'missing_clusters': missing_clusters,
        'model': model
    }

