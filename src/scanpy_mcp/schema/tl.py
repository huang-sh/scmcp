from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator
from .base import JSONParsingModel
from typing import Optional, Union, List, Dict, Any, Tuple, Literal, Mapping
from pydantic import ValidationInfo


class TSNEModel(JSONParsingModel):
    """Input schema for the t-SNE dimensionality reduction tool."""
    n_pcs: Optional[int] = Field(
        default=None,
        description="Number of PCs to use. If None, automatically determined.",
        ge=0
    )
    use_rep: Optional[str] = Field(
        default=None,
        description="Key for .obsm to use as representation."
    )
    perplexity: Union[float, int] = Field(
        default=30,
        description="Related to number of nearest neighbors, typically between 5-50.",
        gt=0
    )
    early_exaggeration: Union[float, int] = Field(
        default=12,
        description="Controls space between natural clusters in embedded space.",
        gt=0
    )
    learning_rate: Union[float, int] = Field(
        default=1000,
        description="Learning rate for optimization, typically between 100-1000.",
        gt=0
    )
    random_state: int = Field(
        default=0,
        description="Random seed for reproducibility."
    )
    use_fast_tsne: bool = Field(
        default=False,
        description="Whether to use Multicore-tSNE implementation."
    )
    n_jobs: Optional[int] = Field(
        default=None,
        description="Number of jobs for parallel computation.",
        gt=0
    )
    metric: str = Field(
        default='euclidean',
        description="Distance metric to use."
    )
    
    @field_validator('n_pcs', 'perplexity', 'early_exaggeration', 
                   'learning_rate', 'n_jobs')
    def validate_positive_numbers(cls, v: Optional[Union[int, float]]) -> Optional[Union[int, float]]:
        """Validate positive numbers where applicable"""
        if v is not None and v <= 0:
            raise ValueError("must be a positive number")
        return v
    
    @field_validator('metric')
    def validate_metric(cls, v: str) -> str:
        """Validate distance metric is supported"""
        valid_metrics = ['euclidean', 'cosine', 'manhattan', 'l1', 'l2']
        if v.lower() not in valid_metrics:
            raise ValueError(f"metric must be one of {valid_metrics}")
        return v.lower()


class UMAPModel(JSONParsingModel):
    """Input schema for the UMAP dimensionality reduction tool."""
    
    min_dist: float = Field(
        default=0.5,
        description="Minimum distance between embedded points.",
        gt=0
    )
    
    spread: float = Field(
        default=1.0,
        description="Scale of embedded points.",
        gt=0
    )
    
    n_components: int = Field(
        default=2,
        description="Number of dimensions of the embedding.",
        gt=0
    )
    
    maxiter: Optional[int] = Field(
        default=None,
        description="Number of iterations (epochs) of the optimization.",
        gt=0
    )
    
    alpha: float = Field(
        default=1.0,
        description="Initial learning rate for the embedding optimization.",
        gt=0
    )
    
    gamma: float = Field(
        default=1.0,
        description="Weighting applied to negative samples.",
        gt=0
    )
    negative_sample_rate: int = Field(
        default=5,
        description="Number of negative samples per positive sample.",
        gt=0
    )
    init_pos: str = Field(
        default='spectral',
        description="How to initialize the low dimensional embedding.",
    )
    random_state: int = Field(
        default=0,
        description="Random seed for reproducibility."
    )
    a: Optional[float] = Field(
        default=None,
        description="Parameter controlling the embedding.",
        gt=0
    )
    b: Optional[float] = Field(
        default=None,
        description="Parameter controlling the embedding.",
        gt=0
    )
    method: str = Field(
        default='umap',
        description="Implementation to use ('umap' or 'rapids')."
    )
    neighbors_key: Optional[str] = Field(
        default=None,
        description="Key for neighbors settings in .uns."
    )
    
    @field_validator('min_dist', 'spread', 'n_components', 'maxiter', 
                   'alpha', 'gamma', 'negative_sample_rate', 'a', 'b')
    def validate_positive_numbers(cls, v: Optional[Union[int, float]]) -> Optional[Union[int, float]]:
        """Validate positive numbers where applicable"""
        if v is not None and v <= 0:
            raise ValueError("must be a positive number")
        return v
    
    @field_validator('method')
    def validate_method(cls, v: str) -> str:
        """Validate implementation method is supported"""
        if v.lower() not in ['umap', 'rapids']:
            raise ValueError("method must be either 'umap' or 'rapids'")
        return v.lower()


class DrawGraphModel(JSONParsingModel):
    """Input schema for the force-directed graph drawing tool."""
    
    layout: str = Field(
        default='fa',
        description="Graph layout algorithm ('fa', 'fr', 'kk', etc.)",
    )
    init_pos: Optional[Union[str, bool]] = Field(
        default=None,
        description="Initial position for nodes ('paga'/True, False, or .obsm key)",
    )
    root: Optional[int] = Field(
        default=None,
        description="Root node for tree layouts",
        ge=0
    )
    random_state: int = Field(
        default=0,
        description="Random seed for reproducibility"
    )
    n_jobs: Optional[int] = Field(
        default=None,
        description="Number of jobs for parallel computation",
        gt=0
    )
    key_added_ext: Optional[str] = Field(
        default=None,
        description="Suffix for storing results in .obsm"
    )
    neighbors_key: Optional[str] = Field(
        default=None,
        description="Key for neighbors settings in .uns"
    )
    obsp: Optional[str] = Field(
        default=None,
        description="Key for adjacency matrix in .obsp"
    )
    
    @field_validator('layout')
    def validate_layout(cls, v: str) -> str:
        """Validate layout is supported"""
        valid_layouts = ['fa', 'fr', 'grid_fr', 'kk', 'lgl', 'drl', 'rt']
        if v.lower() not in valid_layouts:
            raise ValueError(f"layout must be one of {valid_layouts}")
        return v.lower()
    
    @field_validator('root', 'n_jobs')
    def validate_positive_integers(cls, v: Optional[int]) -> Optional[int]:
        """Validate positive integers where applicable"""
        if v is not None and v <= 0:
            raise ValueError("must be a positive integer")
        return v


class DiffMapModel(JSONParsingModel):
    """Input schema for the Diffusion Maps dimensionality reduction tool."""
    
    n_comps: int = Field(
        default=15,
        description="The number of dimensions of the representation.",
        gt=0
    )
    neighbors_key: Optional[str] = Field(
        default=None,
        description=(
            "If not specified, diffmap looks .uns['neighbors'] for neighbors settings "
            "and .obsp['connectivities'], .obsp['distances'] for connectivities and "
            "distances respectively. If specified, diffmap looks .uns[neighbors_key] for "
            "neighbors settings and uses the corresponding connectivities and distances."
        )
    )
    random_state: int = Field(
        default=0,
        description="Random seed for reproducibility."
    )
    
    @field_validator('n_comps')
    def validate_positive_integers(cls, v: int) -> int:
        """Validate positive integers"""
        if v <= 0:
            raise ValueError("n_comps must be a positive integer")
        return v


class EmbeddingDensityModel(JSONParsingModel):
    """Input schema for the embedding density calculation tool."""
    
    basis: str = Field(
        default='umap',
        description="The embedding over which the density will be calculated. This embedded representation should be found in `adata.obsm['X_[basis]']`."
    )
    groupby: Optional[str] = Field(
        default=None,
        description="Key for categorical observation/cell annotation for which densities are calculated per category."
    )
    key_added: Optional[str] = Field(
        default=None,
        description="Name of the `.obs` covariate that will be added with the density estimates."
    )
    components: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="The embedding dimensions over which the density should be calculated. This is limited to two components."
    )
    
    @field_validator('components')
    def validate_components(cls, v: Optional[Union[str, List[str]]]) -> Optional[Union[str, List[str]]]:
        """Validate that components are limited to two dimensions"""
        if v is not None and isinstance(v, list) and len(v) > 2:
            raise ValueError("components is limited to two dimensions")
        return v


class LeidenModel(JSONParsingModel):
    """Input schema for the Leiden clustering algorithm."""
    
    resolution: float = Field(
        default=1.0,
        description="A parameter value controlling the coarseness of the clustering. Higher values lead to more clusters."
    )
    
    random_state: int = Field(
        default=0,
        description="Change the initialization of the optimization."
    )
    
    key_added: str = Field(
        default='leiden',
        description="`adata.obs` key under which to add the cluster labels."
    )
    
    directed: Optional[bool] = Field(
        default=None,
        description="Whether to treat the graph as directed or undirected."
    )
    
    use_weights: bool = Field(
        default=True,
        description="If `True`, edge weights from the graph are used in the computation (placing more emphasis on stronger edges)."
    )
    
    n_iterations: int = Field(
        default=-1,
        description="How many iterations of the Leiden clustering algorithm to perform. -1 runs until optimal clustering."
    )
    
    neighbors_key: Optional[str] = Field(
        default=None,
        description="Use neighbors connectivities as adjacency. If specified, leiden looks .obsp[.uns[neighbors_key]['connectivities_key']] for connectivities."
    )
    
    obsp: Optional[str] = Field(
        default=None,
        description="Use .obsp[obsp] as adjacency. You can't specify both `obsp` and `neighbors_key` at the same time."
    )
    
    flavor: Literal['leidenalg', 'igraph'] = Field(
        default='igraph',
        description="Which package's implementation to use."
    )
    
    clustering_args: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Any further arguments to pass to the clustering algorithm."
    )
    
    @field_validator('resolution')
    def validate_resolution(cls, v: float) -> float:
        """Validate resolution is positive"""
        if v <= 0:
            raise ValueError("resolution must be a positive number")
        return v
    
    @field_validator('obsp', 'neighbors_key')
    def validate_graph_source(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validate that obsp and neighbors_key are not both specified"""
        values = info.data
        if v is not None and 'obsp' in values and 'neighbors_key' in values:
            if values['obsp'] is not None and values['neighbors_key'] is not None:
                raise ValueError("Cannot specify both obsp and neighbors_key")
        return v
    
    @field_validator('flavor')
    def validate_flavor(cls, v: str) -> str:
        """Validate flavor is supported"""
        if v not in ['leidenalg', 'igraph']:
            raise ValueError("flavor must be either 'leidenalg' or 'igraph'")
        return v


class LouvainModel(JSONParsingModel):
    """Input schema for the Louvain clustering algorithm."""
    
    resolution: Optional[float] = Field(
        default=None,
        description="For the default flavor ('vtraag') or for 'RAPIDS', you can provide a resolution (higher resolution means finding more and smaller clusters), which defaults to 1.0."
    )
    
    random_state: int = Field(
        default=0,
        description="Change the initialization of the optimization."
    )
    
    key_added: str = Field(
        default='louvain',
        description="Key under which to add the cluster labels."
    )
    
    flavor: Literal['vtraag', 'igraph', 'rapids'] = Field(
        default='vtraag',
        description="Package for computing the clustering: 'vtraag' (default, more powerful), 'igraph' (built-in method), or 'rapids' (GPU accelerated)."
    )
    
    directed: bool = Field(
        default=True,
        description="Interpret the adjacency matrix as directed graph."
    )
    
    use_weights: bool = Field(
        default=False,
        description="Use weights from knn graph."
    )
    
    partition_kwargs: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Key word arguments to pass to partitioning, if 'vtraag' method is being used."
    )
    
    neighbors_key: Optional[str] = Field(
        default=None,
        description="Use neighbors connectivities as adjacency. If specified, louvain looks .obsp[.uns[neighbors_key]['connectivities_key']] for connectivities."
    )
    
    obsp: Optional[str] = Field(
        default=None,
        description="Use .obsp[obsp] as adjacency. You can't specify both `obsp` and `neighbors_key` at the same time."
    )
    
    @field_validator('resolution')
    def validate_resolution(cls, v: Optional[float]) -> Optional[float]:
        """Validate resolution is positive if provided"""
        if v is not None and v <= 0:
            raise ValueError("resolution must be a positive number")
        return v
    
    @field_validator('obsp', 'neighbors_key')
    def validate_graph_source(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validate that obsp and neighbors_key are not both specified"""
        values = info.data
        if v is not None and 'obsp' in values and 'neighbors_key' in values:
            if values['obsp'] is not None and values['neighbors_key'] is not None:
                raise ValueError("Cannot specify both obsp and neighbors_key")
        return v
    
    @field_validator('flavor')
    def validate_flavor(cls, v: str) -> str:
        """Validate flavor is supported"""
        if v not in ['vtraag', 'igraph', 'rapids']:
            raise ValueError("flavor must be one of 'vtraag', 'igraph', or 'rapids'")
        return v


class DendrogramModel(JSONParsingModel):
    """Input schema for the hierarchical clustering dendrogram tool."""
    
    groupby: str = Field(
        ...,  # Required field
        description="The categorical observation annotation to use for grouping."
    )
    n_pcs: Optional[int] = Field(
        default=None,
        description="Use this many PCs. If n_pcs==0 use .X if use_rep is None.",
        ge=0
    )
    use_rep: Optional[str] = Field(
        default=None,
        description="Use the indicated representation. 'X' or any key for .obsm is valid."
    )
    var_names: Optional[List[str]] = Field(
        default=None,
        description="List of var_names to use for computing the hierarchical clustering. If provided, use_rep and n_pcs are ignored."
    )
    use_raw: Optional[bool] = Field(
        default=None,
        description="Only when var_names is not None. Use raw attribute of adata if present."
    )
    cor_method: str = Field(
        default='pearson',
        description="Correlation method to use: 'pearson', 'kendall', or 'spearman'."
    )
    linkage_method: str = Field(
        default='complete',
        description="Linkage method to use for hierarchical clustering."
    )
    optimal_ordering: bool = Field(
        default=False,
        description="Reorders the linkage matrix so that the distance between successive leaves is minimal."
    )
    key_added: Optional[str] = Field(
        default=None,
        description="By default, the dendrogram information is added to .uns[f'dendrogram_{groupby}']."
    )
    
    @field_validator('cor_method')
    def validate_cor_method(cls, v: str) -> str:
        """Validate correlation method is supported"""
        valid_methods = ['pearson', 'kendall', 'spearman']
        if v.lower() not in valid_methods:
            raise ValueError(f"cor_method must be one of {valid_methods}")
        return v.lower()
    
    @field_validator('linkage_method')
    def validate_linkage_method(cls, v: str) -> str:
        """Validate linkage method is supported"""
        valid_methods = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']
        if v.lower() not in valid_methods:
            raise ValueError(f"linkage_method must be one of {valid_methods}")
        return v.lower()
    
    @field_validator('n_pcs')
    def validate_n_pcs(cls, v: Optional[int]) -> Optional[int]:
        """Validate n_pcs is non-negative"""
        if v is not None and v < 0:
            raise ValueError("n_pcs must be a non-negative integer")
        return v


class DPTModel(JSONParsingModel):
    """Input schema for the Diffusion Pseudotime (DPT) tool."""
    
    n_dcs: int = Field(
        default=10,
        description="The number of diffusion components to use.",
        gt=0
    )
    n_branchings: int = Field(
        default=0,
        description="Number of branchings to detect.",
        ge=0
    )
    min_group_size: float = Field(
        default=0.01,
        description="During recursive splitting of branches, do not consider groups that contain less than min_group_size data points. If a float, refers to a fraction of the total number of data points.",
        gt=0,
        le=1.0
    )
    allow_kendall_tau_shift: bool = Field(
        default=True,
        description="If a very small branch is detected upon splitting, shift away from maximum correlation in Kendall tau criterion to stabilize the splitting."
    )
    neighbors_key: Optional[str] = Field(
        default=None,
        description="If specified, dpt looks .uns[neighbors_key] for neighbors settings and uses the corresponding connectivities and distances."
    )
    
    @field_validator('n_dcs')
    def validate_n_dcs(cls, v: int) -> int:
        """Validate n_dcs is positive"""
        if v <= 0:
            raise ValueError("n_dcs must be a positive integer")
        return v
    
    @field_validator('n_branchings')
    def validate_n_branchings(cls, v: int) -> int:
        """Validate n_branchings is non-negative"""
        if v < 0:
            raise ValueError("n_branchings must be a non-negative integer")
        return v
    
    @field_validator('min_group_size')
    def validate_min_group_size(cls, v: float) -> float:
        """Validate min_group_size is between 0 and 1"""
        if v <= 0 or v > 1:
            raise ValueError("min_group_size must be between 0 and 1")
        return v

class PAGAModel(JSONParsingModel):
    """Input schema for the Partition-based Graph Abstraction (PAGA) tool."""
    
    groups: Optional[str] = Field(
        default=None,
        description="Key for categorical in adata.obs. You can pass your predefined groups by choosing any categorical annotation of observations. Default: The first present key of 'leiden' or 'louvain'."
    )
    use_rna_velocity: bool = Field(
        default=False,
        description="Use RNA velocity to orient edges in the abstracted graph and estimate transitions. Requires that adata.uns contains a directed single-cell graph with key ['velocity_graph']."
    )
    model: Literal['v1.2', 'v1.0'] = Field(
        default='v1.2',
        description="The PAGA connectivity model."
    )
    neighbors_key: Optional[str] = Field(
        default=None,
        description="If specified, paga looks .uns[neighbors_key] for neighbors settings and uses the corresponding connectivities and distances."
    )
    
    @field_validator('model')
    def validate_model(cls, v: str) -> str:
        """Validate model version is supported"""
        if v not in ['v1.2', 'v1.0']:
            raise ValueError("model must be either 'v1.2' or 'v1.0'")
        return v


class IngestModel(JSONParsingModel):
    """Input schema for the ingest tool that maps labels and embeddings from reference data to new data."""
    
    obs: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Labels' keys in adata_ref.obs which need to be mapped to adata.obs (inferred for observation of adata)."
    )
    
    embedding_method: Union[str, List[str]] = Field(
        default=['umap', 'pca'],
        description="Embeddings in adata_ref which need to be mapped to adata. The only supported values are 'umap' and 'pca'."
    )
    
    labeling_method: str = Field(
        default='knn',
        description="The method to map labels in adata_ref.obs to adata.obs. The only supported value is 'knn'."
    )
    
    neighbors_key: Optional[str] = Field(
        default=None,
        description="If specified, ingest looks adata_ref.uns[neighbors_key] for neighbors settings and uses the corresponding distances."
    )
    
    @field_validator('embedding_method')
    def validate_embedding_method(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        """Validate embedding method is supported"""
        valid_methods = ['umap', 'pca']
        
        if isinstance(v, str):
            if v.lower() not in valid_methods:
                raise ValueError(f"embedding_method must be one of {valid_methods}")
            return v.lower()
        
        elif isinstance(v, list):
            for method in v:
                if method.lower() not in valid_methods:
                    raise ValueError(f"embedding_method must contain only values from {valid_methods}")
            return [method.lower() for method in v]
        
        return v
    
    @field_validator('labeling_method')
    def validate_labeling_method(cls, v: str) -> str:
        """Validate labeling method is supported"""
        if v.lower() != 'knn':
            raise ValueError("labeling_method must be 'knn'")
        return v.lower()


class RankGenesGroupsModel(JSONParsingModel):
    """Input schema for the rank_genes_groups tool."""
    
    groupby: str = Field(
        ...,  # Required field
        description="The key of the observations grouping to consider."
    )
    mask_var: Optional[Union[str, List[bool]]] = Field(
        default=None,
        description="Select subset of genes to use in statistical tests."
    )
    use_raw: Optional[bool] = Field(
        default=None,
        description="Use raw attribute of adata if present."
    )
    groups: Union[Literal['all'], List[str]] = Field(
        default='all',
        description="Subset of groups to which comparison shall be restricted, or 'all' for all groups."
    )
    reference: str = Field(
        default='rest',
        description="If 'rest', compare each group to the union of the rest of the group. If a group identifier, compare with respect to this group."
    )
    n_genes: Optional[int] = Field(
        default=None,
        description="The number of genes that appear in the returned tables. Defaults to all genes.",
        gt=0
    )
    rankby_abs: bool = Field(
        default=False,
        description="Rank genes by the absolute value of the score, not by the score."
    )
    pts: bool = Field(
        default=False,
        description="Compute the fraction of cells expressing the genes."
    )
    key_added: Optional[str] = Field(
        default=None,
        description="The key in adata.uns information is saved to."
    )
    method: Optional[str] = Field(
        default=None,
        description="Method for differential expression analysis. Default is 't-test'."
    )
    corr_method: str = Field(
        default='benjamini-hochberg',
        description="p-value correction method. Used only for 't-test', 't-test_overestim_var', and 'wilcoxon'."
    )
    tie_correct: bool = Field(
        default=False,
        description="Use tie correction for 'wilcoxon' scores. Used only for 'wilcoxon'."
    )
    layer: Optional[str] = Field(
        default=None,
        description="Key from adata.layers whose value will be used to perform tests on."
    )
    
    @field_validator('method')
    def validate_method(cls, v: Optional[str]) -> Optional[str]:
        """Validate method is supported"""
        if v is not None:
            valid_methods = ['t-test', 't-test_overestim_var', 'wilcoxon', 'logreg']
            if v not in valid_methods:
                raise ValueError(f"method must be one of {valid_methods}")
        return v
    
    @field_validator('corr_method')
    def validate_corr_method(cls, v: str) -> str:
        """Validate correction method is supported"""
        valid_methods = ['benjamini-hochberg', 'bonferroni']
        if v not in valid_methods:
            raise ValueError(f"corr_method must be one of {valid_methods}")
        return v
    
    @field_validator('n_genes')
    def validate_n_genes(cls, v: Optional[int]) -> Optional[int]:
        """Validate n_genes is positive"""
        if v is not None and v <= 0:
            raise ValueError("n_genes must be a positive integer")
        return v


class FilterRankGenesGroupsModel(JSONParsingModel):
    """Input schema for filtering ranked genes groups."""
    
    key: Optional[str] = Field(
        default=None,
        description="Key from adata.uns where rank_genes_groups output is stored."
    )
    
    groupby: Optional[str] = Field(
        default=None,
        description="The key of the observations grouping to consider."
    )
    
    use_raw: Optional[bool] = Field(
        default=None,
        description="Use raw attribute of adata if present."
    )
    
    key_added: str = Field(
        default='rank_genes_groups_filtered',
        description="The key in adata.uns information is saved to."
    )
    
    min_in_group_fraction: float = Field(
        default=0.25,
        description="Minimum fraction of cells expressing the gene within the group.",
        ge=0.0,
        le=1.0
    )
    
    min_fold_change: Union[int, float] = Field(
        default=1,
        description="Minimum fold change for a gene to be considered significant.",
        gt=0
    )
    
    max_out_group_fraction: float = Field(
        default=0.5,
        description="Maximum fraction of cells expressing the gene outside the group.",
        ge=0.0,
        le=1.0
    )
    
    compare_abs: bool = Field(
        default=False,
        description="If True, compare absolute values of log fold change with min_fold_change."
    )
    
    @field_validator('min_in_group_fraction', 'max_out_group_fraction')
    def validate_fractions(cls, v: float) -> float:
        """Validate fractions are between 0 and 1"""
        if v < 0 or v > 1:
            raise ValueError("Fraction values must be between 0 and 1")
        return v
    
    @field_validator('min_fold_change')
    def validate_fold_change(cls, v: Union[int, float]) -> Union[int, float]:
        """Validate min_fold_change is positive"""
        if v <= 0:
            raise ValueError("min_fold_change must be a positive number")
        return v


class MarkerGeneOverlapModel(JSONParsingModel):
    """Input schema for the marker gene overlap tool."""
    
    key: str = Field(
        default='rank_genes_groups',
        description="The key in adata.uns where the rank_genes_groups output is stored."
    )
    
    method: str = Field(
        default='overlap_count',
        description="Method to calculate marker gene overlap: 'overlap_count', 'overlap_coef', or 'jaccard'."
    )
    
    normalize: Optional[Literal['reference', 'data']] = Field(
        default=None,
        description="Normalization option for the marker gene overlap output. Only applicable when method is 'overlap_count'."
    )
    
    top_n_markers: Optional[int] = Field(
        default=None,
        description="The number of top data-derived marker genes to use. By default the top 100 marker genes are used.",
        gt=0
    )
    
    adj_pval_threshold: Optional[float] = Field(
        default=None,
        description="A significance threshold on the adjusted p-values to select marker genes.",
        gt=0,
        le=1.0
    )
    
    key_added: str = Field(
        default='marker_gene_overlap',
        description="Name of the .uns field that will contain the marker overlap scores."
    )
    
    @field_validator('method')
    def validate_method(cls, v: str) -> str:
        """Validate method is supported"""
        valid_methods = ['overlap_count', 'overlap_coef', 'jaccard']
        if v not in valid_methods:
            raise ValueError(f"method must be one of {valid_methods}")
        return v
    
    @field_validator('normalize')
    def validate_normalize(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Validate normalize is only used with overlap_count method"""
        if v is not None:
            if v not in ['reference', 'data']:
                raise ValueError("normalize must be either 'reference' or 'data'")
            
            values = info.data
            if 'method' in values and values['method'] != 'overlap_count':
                raise ValueError("normalize can only be used when method is 'overlap_count'")
        return v
    
    @field_validator('top_n_markers')
    def validate_top_n_markers(cls, v: Optional[int]) -> Optional[int]:
        """Validate top_n_markers is positive"""
        if v is not None and v <= 0:
            raise ValueError("top_n_markers must be a positive integer")
        return v
    
    @field_validator('adj_pval_threshold')
    def validate_adj_pval_threshold(cls, v: Optional[float]) -> Optional[float]:
        """Validate adj_pval_threshold is between 0 and 1"""
        if v is not None and (v <= 0 or v > 1):
            raise ValueError("adj_pval_threshold must be between 0 and 1")
        return v


class ScoreGenesModel(JSONParsingModel):
    """Input schema for the score_genes tool that calculates gene scores based on average expression."""
    
    ctrl_size: int = Field(
        default=50,
        description="Number of reference genes to be sampled from each bin.",
        gt=0
    )
    
    gene_pool: Optional[List[str]] = Field(
        default=None,
        description="Genes for sampling the reference set. Default is all genes."
    )
    
    n_bins: int = Field(
        default=25,
        description="Number of expression level bins for sampling.",
        gt=0
    )
    
    score_name: str = Field(
        default='score',
        description="Name of the field to be added in .obs."
    )
    
    random_state: int = Field(
        default=0,
        description="The random seed for sampling."
    )
    
    use_raw: Optional[bool] = Field(
        default=None,
        description="Whether to use raw attribute of adata. Defaults to True if .raw is present."
    )
    
    @field_validator('ctrl_size', 'n_bins')
    def validate_positive_integers(cls, v: int) -> int:
        """Validate positive integers"""
        if v <= 0:
            raise ValueError("must be a positive integer")
        return v


class ScoreGenesCellCycleModel(JSONParsingModel):
    """Input schema for the score_genes_cell_cycle tool that scores cell cycle genes."""
    
    s_genes: List[str] = Field(
        ...,  # Required field
        description="List of genes associated with S phase."
    )
    g2m_genes: List[str] = Field(
        ...,  # Required field
        description="List of genes associated with G2M phase."
    )
    gene_pool: Optional[List[str]] = Field(
        default=None,
        description="Genes for sampling the reference set. Default is all genes."
    )
    n_bins: int = Field(
        default=25,
        description="Number of expression level bins for sampling.",
        gt=0
    )
    score_name: Optional[str] = Field(
        default=None,
        description="Name of the field to be added in .obs. If None, the scores are added as 'S_score' and 'G2M_score'."
    )
    random_state: int = Field(
        default=0,
        description="The random seed for sampling."
    )
    use_raw: Optional[bool] = Field(
        default=None,
        description="Whether to use raw attribute of adata. Defaults to True if .raw is present."
    )
    
    @field_validator('s_genes', 'g2m_genes')
    def validate_gene_lists(cls, v: List[str]) -> List[str]:
        """Validate gene lists are not empty"""
        if len(v) == 0:
            raise ValueError("Gene list cannot be empty")
        return v
    
    @field_validator('n_bins')
    def validate_positive_integers(cls, v: int) -> int:
        """Validate positive integers"""
        if v <= 0:
            raise ValueError("n_bins must be a positive integer")
        return v


