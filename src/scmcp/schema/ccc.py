from .base import JSONParsingModel
from pydantic import Field
from typing import Optional, List, Dict, Union, Literal, Tuple


class ListCCCMethodModel(JSONParsingModel):
    """ListCCCMethodModel"""    
    pass    


class RankAggregateModel(JSONParsingModel):
    """Input schema for LIANA's rank_aggregate method for cell-cell communication analysis."""
    
    groupby: str = Field(
        ...,  # Required field
        description="Key to be used for grouping or clustering cells (e.g., cell type annotations)."
    )
    
    resource_name: str = Field(
        default="consensus",
        description="Name of the resource to be used for ligand-receptor inference. See `li.rs.show_resources()` for available resources."
    )
    
    expr_prop: float = Field(
        default=0.1,
        description="Minimum expression proportion for the ligands and receptors in the corresponding cell identities. Set to 0 to return unfiltered results."
    )
    
    min_cells: int = Field(
        default=5,
        description="Minimum cells per cell identity to be considered for downstream analysis."
    )
    
    base: float = Field(
        default=2.718281828459045,  # e
        description="Exponent base used to reverse the log-transformation of the matrix. Relevant only for the `logfc` method."
    )
    
    aggregate_method: Literal["rra", "mean"] = Field(
        default="rra",
        description="Method aggregation approach: 'mean' for mean rank, 'rra' for RobustRankAggregate."
    )
    
    return_all_lrs: bool = Field(
        default=False,
        description="Whether to return all ligand-receptor pairs, or only those that surpass the expr_prop threshold."
    )
    
    key_added: str = Field(
        default="liana_res",
        description="Key under which the results will be stored in adata.uns."
    )
    
    use_raw: Optional[bool] = Field(
        default=True,
        description="Use raw attribute of adata if present."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="Layer in AnnData.layers to use. If None, use AnnData.X."
    )
    
    de_method: str = Field(
        default="t-test",
        description="Differential expression method used to rank genes according to 1vsRest."
    )
    
    n_perms: int = Field(
        default=1000,
        description="Number of permutations for permutation-based methods. If None, no permutation testing is performed."
    )

    n_jobs: int = Field(
        default=1,
        description="Number of jobs to run in parallel."
    )



class CCCModel(JSONParsingModel):
    """Input schema for LIANA's cell-cell communication analysis."""
    
    method: Literal[
        "singlecellsignalr", 
        "connectome", 
        "cellphonedb", 
        "natmi", 
        "logfc", 
        "cellchat", 
        "geometric_mean", 
        "scseqcomm"
    ] = Field(
        default="cellphonedb",
        description="cell-cell communication method"
    )
    
    groupby: str = Field(
        ...,  # Required field
        description="Key to be used for grouping cells (e.g., cell type annotations)."
    )
    
    resource_name: str = Field(
        default="consensus",
        description="Name of the resource to be used for ligand-receptor inference. See `li.rs.show_resources()` for available resources."
    )
    
    expr_prop: float = Field(
        default=0.1,
        description="Minimum expression proportion for the ligands and receptors in the corresponding cell identities. Set to 0 to return unfiltered results."
    )
    
    min_cells: int = Field(
        default=5,
        description="Minimum cells per cell identity to be considered for downstream analysis."
    )
    
    base: float = Field(
        default=2.718281828459045,  # e
        description="Exponent base used to reverse the log-transformation of the matrix. Relevant only for the `logfc` method."
    )
    
    return_all_lrs: bool = Field(
        default=False,
        description="Whether to return all ligand-receptor pairs, or only those that surpass the expr_prop threshold."
    )
    
    key_added: str = Field(
        default="liana_res",
        description="Key under which the results will be stored in adata.uns."
    )
    
    use_raw: Optional[bool] = Field(
        default=True,
        description="Use raw attribute of adata if present."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="Layer in AnnData.layers to use. If None, use AnnData.X."
    )
    
    de_method: str = Field(
        default="t-test",
        description="Differential expression method used to rank genes according to 1vsRest."
    )
    
    n_perms: int = Field(
        default=1000,
        description="Number of permutations for the permutation test. Relevant for CellPhoneDB method."
    )
    
    seed: int = Field(
        default=1337,
        description="Random seed for reproducibility."
    )
    
    n_jobs: int = Field(
        default=1,
        description="Number of jobs to run in parallel."
    )
    
    verbose: Optional[bool] = Field(
        default=False,
        description="Whether to print verbose output."
    )
    
    inplace: bool = Field(
        default=True,
        description="Whether to store results in place, or return them."
    )
    
    supp_columns: Optional[List[str]] = Field(
        default=None,
        description="Additional columns to be added from methods in liana, or columns from scanpy.tl.rank_genes_groups."
    )




class CirclePlotModel(JSONParsingModel):
    """Input schema for LIANA's circle_plot visualization for cell-cell communication networks."""
    
    uns_key: Optional[str] = Field(
        default="liana_res",
        description="Key in adata.uns that contains the LIANA results."
    )
    
    groupby: Optional[str] = Field(
        default=None,
        description="Key to be used for grouping or clustering cells."
    )
    
    source_key: str = Field(
        default="source",
        description="Column name of the sender/source cell types in liana_res."
    )
    
    target_key: str = Field(
        default="target",
        description="Column name of the receiver/target cell types in liana_res."
    )
    
    score_key: Optional[str] = Field(
        default=None,
        description="Column name of the score in liana_res. If None, the score is inferred from the method."
    )
    
    inverse_score: bool = Field(
        default=False,
        description="Whether to invert the score. If True, the score will be -log10(score)."
    )
    
    top_n: Optional[int] = Field(
        default=None,
        description="Top N entities to plot."
    )
    
    orderby: Optional[str] = Field(
        default=None,
        description="If top_n is not None, order the interactions by this column."
    )
    
    orderby_ascending: Optional[bool] = Field(
        default=None,
        description="If top_n is not None, specify how to order the interactions."
    )
    
    orderby_absolute: bool = Field(
        default=False,
        description="If top_n is not None, whether to order by the absolute value of the orderby column."
    )
    
    source_labels: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of labels to use as source, the rest are filtered out."
    )
    
    target_labels: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of labels to use as target, the rest are filtered out."
    )
    
    ligand_complex: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of ligand complexes to filter the interactions to be plotted."
    )
    
    receptor_complex: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of receptor complexes to filter the interactions to be plotted."
    )
    
    pivot_mode: Literal["counts", "mean"] = Field(
        default="counts",
        description="The mode of the pivot table: 'counts' for number of connections, 'mean' for mean of score values."
    )
    
    mask_mode: Literal["and", "or"] = Field(
        default="or",
        description="The mode of the mask: 'or' to include source or target, 'and' to include source and target."
    )
    
    specificity_cutoff: float = Field(
        default=0.05,
        description="specificity or pval threshold for filtering results. "
    )
    
    figure_size: Tuple[float, float] = Field(
        default=(5, 5),
        description="Figure x,y size."
    )
    
    edge_alpha: float = Field(
        default=0.5,
        description="The transparency of the edges."
    )
    
    edge_arrow_size: int = Field(
        default=10,
        description="The size of the arrow."
    )
    
    edge_width_scale: Tuple[float, float] = Field(
        default=(1, 5),
        description="The scale of the edge width."
    )
    
    node_alpha: float = Field(
        default=1.0,
        description="The transparency of the nodes."
    )
    
    node_size_scale: Tuple[float, float] = Field(
        default=(100, 400),
        description="The scale of the node size."
    )
    
    node_label_offset: Tuple[float, float] = Field(
        default=(0.1, -0.2),
        description="The offset of the node label."
    )
    
    node_label_size: int = Field(
        default=8,
        description="The size of the node label."
    )
    
    node_label_alpha: float = Field(
        default=0.7,
        description="The transparency of the node label."
    )


class DotPlotModel(JSONParsingModel):
    """Input schema for LIANA's dotplot visualization for cell-cell communication networks."""
    
    uns_key: str = Field(
        default="liana_res",
        description="Key in adata.uns that contains the LIANA results."
    )
    
    specificity_cutoff: float = Field(
        default=0.05,
        description="specificity or pval threshold for filtering results. "
    )
        
    colour: Optional[str] = Field(
        default=None,
        description="Column in liana_res to define the colours of the dots."
    )
    
    size: Optional[str] = Field(
        default=None,
        description="Column in liana_res to define the size of the dots."
    )
    
    source_labels: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of labels to use as source, the rest are filtered out."
    )
    
    target_labels: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of labels to use as target, the rest are filtered out."
    )
    
    top_n: Optional[int] = Field(
        default=None,
        description="Top N entities to plot."
    )
    
    orderby: Optional[str] = Field(
        default=None,
        description="If top_n is not None, order the interactions by this column."
    )
    
    orderby_ascending: Optional[bool] = Field(
        default=None,
        description="If top_n is not None, specify how to order the interactions."
    )
    
    orderby_absolute: bool = Field(
        default=False,
        description="If top_n is not None, whether to order by the absolute value of the orderby column."
    )
    
    ligand_complex: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of ligand complexes to filter the interactions to be plotted."
    )
    
    receptor_complex: Optional[Union[List[str], str]] = Field(
        default=None,
        description="List of receptor complexes to filter the interactions to be plotted."
    )
    
    inverse_colour: bool = Field(
        default=False,
        description="Whether to -log10 the colour column for plotting."
    )
    
    inverse_size: bool = Field(
        default=False,
        description="Whether to -log10 the size column for plotting."
    )
    
    cmap: str = Field(
        default="viridis",
        description="Colour map to use for plotting."
    )
    
    size_range: Tuple[int, int] = Field(
        default=(2, 9),
        description="Define size range. Tuple of (min, max) integers."
    )
    
    figure_size: Tuple[float, float] = Field(
        default=(8, 6),
        description="Figure x,y size."
    )
    
    specificity_cutoff: float = Field(
        default=0.05,
        description="Specificity or p-value threshold for filtering results."
    )

