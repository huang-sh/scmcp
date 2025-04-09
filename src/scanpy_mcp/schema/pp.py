from pydantic import (
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
    model_validator,
)
from typing import Optional, Union, List, Dict, Any
from typing import Literal

from .base import JSONParsingModel



class FilterCells(JSONParsingModel):
    """Input schema for the filter_cells preprocessing tool."""
    
    min_counts: Optional[int] = Field(
        default=None,
        description="Minimum number of counts required for a cell to pass filtering."
    )
    
    min_genes: Optional[int] = Field(
        default=None,
        description="Minimum number of genes expressed required for a cell to pass filtering."
    )
    
    max_counts: Optional[int] = Field(
        default=None,
        description="Maximum number of counts required for a cell to pass filtering."
    )
    
    max_genes: Optional[int] = Field(
        default=None,
        description="Maximum number of genes expressed required for a cell to pass filtering."
    )
    
    @field_validator('min_counts', 'min_genes', 'max_counts', 'max_genes')
    def validate_positive_integers(cls, v: Optional[int]) -> Optional[int]:
        """验证整数参数为正数"""
        if v is not None and v <= 0:
            raise ValueError("过滤参数必须是正整数")
        return v


class FilterGenes(JSONParsingModel):
    """Input schema for the filter_genes preprocessing tool."""
    
    min_counts: Optional[int] = Field(
        default=None,
        description="Minimum number of counts required for a gene to pass filtering."
    )
    
    min_cells: Optional[int] = Field(
        default=None,
        description="Minimum number of cells expressed required for a gene to pass filtering."
    )
    
    max_counts: Optional[int] = Field(
        default=None,
        description="Maximum number of counts required for a gene to pass filtering."
    )
    
    max_cells: Optional[int] = Field(
        default=None,
        description="Maximum number of cells expressed required for a gene to pass filtering."
    )
    
    @field_validator('min_counts', 'min_cells', 'max_counts', 'max_cells')
    def validate_positive_integers(cls, v: Optional[int]) -> Optional[int]:
        """验证整数参数为正数"""
        if v is not None and v <= 0:
            raise ValueError("must be positive_integers")
        return v

class CalculateQCMetrics(JSONParsingModel):
    """Input schema for the calculate_qc_metrics preprocessing tool."""
    
    expr_type: str = Field(
        default="counts",
        description="Name of kind of values in X."
    )
    
    var_type: str = Field(
        default="genes",
        description="The kind of thing the variables are."
    )
    
    qc_vars: Optional[Union[List[str], str]]  = Field(
        default=[],
        description=(
            "Keys for boolean columns of .var which identify variables you could want to control for "
            "mark_var tool should be called frist when you want to calculate mt, ribo, hb, and check tool output for var columns"
        )
    )
    
    percent_top: Optional[List[int]] = Field(
        default=[50, 100, 200, 500],
        description="List of ranks (where genes are ranked by expression) at which the cumulative proportion of expression will be reported as a percentage."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="If provided, use adata.layers[layer] for expression values instead of adata.X"
    )
    
    use_raw: bool = Field(
        default=False,
        description="If True, use adata.raw.X for expression values instead of adata.X"
    )
    log1p: bool = Field(
        default=True,
        description="Set to False to skip computing log1p transformed annotations."
    )
    
    @field_validator('percent_top')
    def validate_percent_top(cls, v: Optional[List[int]]) -> Optional[List[int]]:
        """验证 percent_top 中的值为正整数"""
        if v is not None:
            for rank in v:
                if not isinstance(rank, int) or rank <= 0:
                    raise ValueError("percent_top 中的所有值必须是正整数")
        return v
    


class Log1PModel(JSONParsingModel):
    """Input schema for the log1p preprocessing tool."""
    
    base: Optional[Union[int, float]] = Field(
        default=None,
        description="Base of the logarithm. Natural logarithm is used by default."
    )
    
    chunked: Optional[bool] = Field(
        default=None,
        description="Process the data matrix in chunks, which will save memory."
    )
    
    chunk_size: Optional[int] = Field(
        default=None,
        description="Number of observations in the chunks to process the data in."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="Entry of layers to transform."
    )
    
    obsm: Optional[str] = Field(
        default=None,
        description="Entry of obsm to transform."
    )
    
    @field_validator('chunk_size')
    def validate_chunk_size(cls, v: Optional[int]) -> Optional[int]:
        """Validate chunk_size is positive integer"""
        if v is not None and v <= 0:
            raise ValueError("chunk_size must be a positive integer")
        return v


class PCAModel(JSONParsingModel):
    """Input schema for the PCA preprocessing tool."""
    
    n_comps: Optional[int] = Field(
        default=None,
        description="Number of principal components to compute. Defaults to 50 or 1 - minimum dimension size.",
        gt=0
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="If provided, which element of layers to use for PCA."
    )
    
    zero_center: Optional[bool] = Field(
        default=True,
        description="If True, compute standard PCA from covariance matrix."
    )
    
    svd_solver: Optional[Literal["arpack", "randomized", "auto", "lobpcg", "tsqr"]] = Field(
        default=None,
        description="SVD solver to use."
    )
    mask_var: Optional[Union[str, bool]] = Field(
        default=None,
        description="Boolean mask or string referring to var column for subsetting genes."
    )
    dtype: str = Field(
        default="float32",
        description="Numpy data type string for the result."
    )
    chunked: bool = Field(
        default=False,
        description="If True, perform an incremental PCA on segments."
    )
    
    chunk_size: Optional[int] = Field(
        default=None,
        description="Number of observations to include in each chunk.",
        gt=0
    )
    
    @field_validator('n_comps', 'chunk_size')
    def validate_positive_integers(cls, v: Optional[int]) -> Optional[int]:
        """Validate positive integers"""
        if v is not None and v <= 0:
            raise ValueError("must be a positive integer")
        return v
    
    @field_validator('dtype')
    def validate_dtype(cls, v: str) -> str:
        """Validate numpy dtype"""
        if v not in ["float32", "float64"]:
            raise ValueError("dtype must be either 'float32' or 'float64'")
        return v


class HighlyVariableGenesModel(JSONParsingModel):
    """Input schema for the highly_variable_genes preprocessing tool."""
    
    layer: Optional[str] = Field(
        default=None,
        description="If provided, use adata.layers[layer] for expression values."
    )
    
    n_top_genes: Optional[int] = Field(
        default=None,
        description="Number of highly-variable genes to keep. Mandatory if `flavor='seurat_v3'",
    )
    
    min_disp: float = Field(
        default=0.5,
        description="Minimum dispersion cutoff for gene selection."
    )
    
    max_disp: float = Field(
        default=float('inf'),
        description="Maximum dispersion cutoff for gene selection."
    )
    min_mean: float = Field(
        default=0.0125,
        description="Minimum mean expression cutoff for gene selection."
    )
    max_mean: float = Field(
        default=3,
        description="Maximum mean expression cutoff for gene selection."
    )
    span: float = Field(
        default=0.3,
        description="Fraction of data used for loess model fit in seurat_v3.",
        gt=0,
        lt=1
    )
    n_bins: int = Field(
        default=20,
        description="Number of bins for mean expression binning.",
        gt=0
    )
    flavor: Literal['seurat', 'cell_ranger', 'seurat_v3', 'seurat_v3_paper'] = Field(
        default='seurat',
        description="Method for identifying highly variable genes."
    )
    subset: bool = Field(
        default=False,
        description="Inplace subset to highly-variable genes if True."
    )
    batch_key: Optional[str] = Field(
        default=None,
        description="Key in adata.obs for batch information."
    )
    
    check_values: bool = Field(
        default=True,
        description="Check if counts are integers for seurat_v3 flavor."
    )
    
    @field_validator('n_top_genes', 'n_bins')
    def validate_positive_integers(cls, v: Optional[int]) -> Optional[int]:
        """Validate positive integers"""
        if v is not None and v <= 0:
            raise ValueError("must be a positive integer")
        return v
    
    @field_validator('span')
    def validate_span(cls, v: float) -> float:
        """Validate span is between 0 and 1"""
        if v <= 0 or v >= 1:
            raise ValueError("span must be between 0 and 1")
        return v


class RegressOutModel(JSONParsingModel):
    """Input schema for the regress_out preprocessing tool."""
    
    keys: Union[str, List[str]] = Field(
        description="Keys for observation annotation on which to regress on."
    )
    layer: Optional[str] = Field(
        default=None,
        description="If provided, which element of layers to regress on."
    )
    n_jobs: Optional[int] = Field(
        default=None,
        description="Number of jobs for parallel computation.",
        gt=0
    )
    
    @field_validator('n_jobs')
    def validate_n_jobs(cls, v: Optional[int]) -> Optional[int]:
        """Validate n_jobs is positive integer"""
        if v is not None and v <= 0:
            raise ValueError("n_jobs must be a positive integer")
        return v
    
    @field_validator('keys')
    def validate_keys(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        """Ensure keys is either a string or list of strings"""
        if isinstance(v, str):
            return v
        elif isinstance(v, list) and all(isinstance(item, str) for item in v):
            return v
        raise ValueError("keys must be a string or list of strings")


class ScaleModel(JSONParsingModel):
    """Input schema for the scale preprocessing tool."""
    
    zero_center: bool = Field(
        default=True,
        description="If False, omit zero-centering variables to handle sparse input efficiently."
    )
    
    max_value: Optional[float] = Field(
        default=None,
        description="Clip (truncate) to this value after scaling. If None, do not clip."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="If provided, which element of layers to scale."
    )
    
    obsm: Optional[str] = Field(
        default=None,
        description="If provided, which element of obsm to scale."
    )
    
    mask_obs: Optional[Union[str, bool]] = Field(
        default=None,
        description="Boolean mask or string referring to obs column for subsetting observations."
    )
    
    @field_validator('max_value')
    def validate_max_value(cls, v: Optional[float]) -> Optional[float]:
        """Validate max_value is positive if provided"""
        if v is not None and v <= 0:
            raise ValueError("max_value must be positive if provided")
        return v


class CombatModel(JSONParsingModel):
    """Input schema for the combat batch effect correction tool."""
    
    key: str = Field(
        default='batch',
        description="Key to a categorical annotation from adata.obs that will be used for batch effect removal."
    )
    
    covariates: Optional[List[str]] = Field(
        default=None,
        description="Additional covariates besides the batch variable such as adjustment variables or biological condition."
    )
    
    @field_validator('key')
    def validate_key(cls, v: str) -> str:
        """Validate key is not empty"""
        if not v.strip():
            raise ValueError("key cannot be empty")
        return v
    
    @field_validator('covariates')
    def validate_covariates(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate covariates are non-empty strings if provided"""
        if v is not None:
            if not all(isinstance(item, str) and item.strip() for item in v):
                raise ValueError("covariates must be non-empty strings")
        return v


class ScrubletModel(JSONParsingModel):
    """Input schema for the scrublet doublet prediction tool."""
    
    adata_sim: Optional[str] = Field(
        default=None,
        description="Optional path to AnnData object with simulated doublets."
    )
    
    batch_key: Optional[str] = Field(
        default=None,
        description="Key in adata.obs for batch information."
    )
    
    sim_doublet_ratio: float = Field(
        default=2.0,
        description="Number of doublets to simulate relative to observed transcriptomes.",
        gt=0
    )
    
    expected_doublet_rate: float = Field(
        default=0.05,
        description="Estimated doublet rate for the experiment.",
        ge=0,
        le=1
    )
    
    stdev_doublet_rate: float = Field(
        default=0.02,
        description="Uncertainty in the expected doublet rate.",
        ge=0,
        le=1
    )
    
    synthetic_doublet_umi_subsampling: float = Field(
        default=1.0,
        description="Rate for sampling UMIs when creating synthetic doublets.",
        gt=0,
        le=1
    )
    
    knn_dist_metric: str = Field(
        default="euclidean",
        description="Distance metric used when finding nearest neighbors."
    )
    
    normalize_variance: bool = Field(
        default=True,
        description="Normalize data such that each gene has variance of 1."
    )
    
    log_transform: bool = Field(
        default=False,
        description="Whether to log-transform the data prior to PCA."
    )
    
    mean_center: bool = Field(
        default=True,
        description="Center data such that each gene has mean of 0."
    )
    
    n_prin_comps: int = Field(
        default=30,
        description="Number of principal components used for embedding.",
        gt=0
    )
    
    use_approx_neighbors: Optional[bool] = Field(
        default=None,
        description="Use approximate nearest neighbor method (annoy)."
    )
    
    get_doublet_neighbor_parents: bool = Field(
        default=False,
        description="Return parent transcriptomes that generated doublet neighbors."
    )
    
    n_neighbors: Optional[int] = Field(
        default=None,
        description="Number of neighbors used to construct KNN graph.",
        gt=0
    )
    
    threshold: Optional[float] = Field(
        default=None,
        description="Doublet score threshold for calling a transcriptome a doublet.",
        ge=0,
        le=1
    )
    
    @field_validator('sim_doublet_ratio', 'expected_doublet_rate', 'stdev_doublet_rate',
                   'synthetic_doublet_umi_subsampling', 'n_prin_comps', 'n_neighbors')
    def validate_positive_numbers(cls, v: Optional[Union[int, float]]) -> Optional[Union[int, float]]:
        """Validate positive numbers where applicable"""
        if v is not None and v <= 0:
            raise ValueError("must be a positive number")
        return v
    
    @field_validator('knn_dist_metric')
    def validate_knn_dist_metric(cls, v: str) -> str:
        """Validate distance metric is supported"""
        valid_metrics = ['euclidean', 'manhattan', 'cosine', 'correlation']
        if v.lower() not in valid_metrics:
            raise ValueError(f"knn_dist_metric must be one of {valid_metrics}")
        return v.lower()


class NeighborsModel(JSONParsingModel):
    """Input schema for the neighbors graph construction tool."""
    
    n_neighbors: int = Field(
        default=15,
        description="Size of local neighborhood used for manifold approximation.",
        gt=1,
        le=100
    )
    
    n_pcs: Optional[int] = Field(
        default=None,
        description="Number of PCs to use. If None, automatically determined.",
        ge=0
    )
    
    use_rep: Optional[str] = Field(
        default=None,
        description="Key for .obsm to use as representation."
    )
    
    knn: bool = Field(
        default=True,
        description="Whether to use hard threshold for neighbor restriction."
    )
    
    method: Literal['umap', 'gauss'] = Field(
        default='umap',
        description="Method for computing connectivities ('umap' or 'gauss')."
    )
    
    transformer: Optional[str] = Field(
        default=None,
        description="Approximate kNN search implementation ('pynndescent' or 'rapids')."
    )
    
    metric: str = Field(
        default='euclidean',
        description="Distance metric to use."
    )
    
    metric_kwds: Dict[str, Any] = Field(
        default_factory=dict,
        description="Options for the distance metric."
    )
    
    random_state: int = Field(
        default=0,
        description="Random seed for reproducibility."
    )
    
    key_added: Optional[str] = Field(
        default=None,
        description="Key prefix for storing neighbor results."
    )
    
    @field_validator('n_neighbors', 'n_pcs')
    def validate_positive_integers(cls, v: Optional[int]) -> Optional[int]:
        """Validate positive integers where applicable"""
        if v is not None and v <= 0:
            raise ValueError("must be a positive integer")
        return v
    
    @field_validator('method')
    def validate_method(cls, v: str) -> str:
        """Validate method is supported"""
        if v not in ['umap', 'gauss']:
            raise ValueError("method must be either 'umap' or 'gauss'")
        return v
    
    @field_validator('transformer')
    def validate_transformer(cls, v: Optional[str]) -> Optional[str]:
        """Validate transformer option is supported"""
        if v is not None and v not in ['pynndescent', 'rapids']:
            raise ValueError("transformer must be either 'pynndescent' or 'rapids'")
        return v


class NormalizeTotalModel(JSONParsingModel):
    """Input schema for the normalize_total preprocessing tool."""
    
    target_sum: Optional[float] = Field(
        default=None,
        description="If None, after normalization, each cell has a total count equal to the median of total counts before normalization. If a number is provided, each cell will have this total count after normalization."
    )
    
    exclude_highly_expressed: bool = Field(
        default=False,
        description="Exclude highly expressed genes for the computation of the normalization factor for each cell."
    )
    
    max_fraction: float = Field(
        default=0.05,
        description="If exclude_highly_expressed=True, consider cells as highly expressed that have more counts than max_fraction of the original total counts in at least one cell.",
        gt=0,
        le=1
    )
    
    key_added: Optional[str] = Field(
        default=None,
        description="Name of the field in adata.obs where the normalization factor is stored."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="Layer to normalize instead of X. If None, X is normalized."
    )
    
    layers: Optional[Union[Literal['all'], List[str]]] = Field(
        default=None,
        description="List of layers to normalize. If 'all', normalize all layers."
    )
    
    layer_norm: Optional[str] = Field(
        default=None,
        description="Specifies how to normalize layers."
    )
    
    inplace: bool = Field(
        default=True,
        description="Whether to update adata or return dictionary with normalized copies."
    )
    
    @field_validator('target_sum')
    def validate_target_sum(cls, v: Optional[float]) -> Optional[float]:
        """Validate target_sum is positive if provided"""
        if v is not None and v <= 0:
            raise ValueError("target_sum must be positive")
        return v
    
    @field_validator('max_fraction')
    def validate_max_fraction(cls, v: float) -> float:
        """Validate max_fraction is between 0 and 1"""
        if v <= 0 or v > 1:
            raise ValueError("max_fraction must be between 0 and 1")
        return v


