from typing import Optional, Union, List, Literal, Any, Collection, Tuple, Sequence, Mapping
from pydantic import Field, field_validator
from .base import JSONParsingModel


from typing import Optional, Union, List, Literal, Any, Collection, Tuple, Sequence, Mapping
from pydantic import Field, field_validator
from .base import JSONParsingModel

from typing import Optional, Union, List, Literal, Any, Collection, Tuple, Sequence, Mapping
from pydantic import Field, field_validator
from .base import JSONParsingModel


# 创建 Mixin 类处理特定功能
class LegendMixin:
    """处理图例相关的字段"""
    
    legend_fontsize: Optional[Union[int, float, str]] = Field(
        default=None,
        description="Numeric size in pt or string describing the size."
    )
    
    legend_fontweight: Union[int, str] = Field(
        default='bold',
        description="Legend font weight. A numeric value in range 0-1000 or a string."
    )
    
    legend_loc: str = Field(
        default='right margin',
        description="Location of legend, either 'on data', 'right margin' or a valid keyword for the loc parameter."
    )
    
    legend_fontoutline: Optional[int] = Field(
        default=None,
        description="Line width of the legend font outline in pt."
    )


class ColorMappingMixin:
    """处理颜色映射相关的字段"""
    
    color_map: Optional[str] = Field(
        default=None,
        description="Color map to use for continuous variables."
    )
    
    palette: Optional[Union[str, List[str], Mapping[str, str]]] = Field(
        default=None,
        description="Colors to use for plotting categorical annotation groups."
    )
    
    vmax: Optional[Union[str, float, List[Union[str, float]]]] = Field(
        default=None,
        description="The value representing the upper limit of the color scale."
    )
    
    vmin: Optional[Union[str, float, List[Union[str, float]]]] = Field(
        default=None,
        description="The value representing the lower limit of the color scale."
    )
    
    vcenter: Optional[Union[str, float, List[Union[str, float]]]] = Field(
        default=None,
        description="The value representing the center of the color scale."
    )


class FigureSizeMixin:
    """处理图形大小相关的字段"""
    
    figsize: Optional[Tuple[float, float]] = Field(
        default=None,
        description="Figure size. Format is (width, height)."
    )


# 基础可视化模型，包含所有可视化工具共享的字段
class BaseVisualizationModel(JSONParsingModel, LegendMixin, ColorMappingMixin, FigureSizeMixin):
    """基础可视化模型，包含所有可视化工具共享的字段"""    
    pass

# 基础嵌入可视化模型，包含所有嵌入可视化工具共享的字段
class BaseEmbeddingModel(BaseVisualizationModel):
    """基础嵌入可视化模型，包含所有嵌入可视化工具共享的字段"""
    
    color: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Keys for annotations of observations/cells or variables/genes."
    )
    
    gene_symbols: Optional[str] = Field(
        default=None,
        description="Column name in .var DataFrame that stores gene symbols."
    )
    
    use_raw: Optional[bool] = Field(
        default=None,
        description="Use .raw attribute of adata for coloring with gene expression."
    )
    
    sort_order: bool = Field(
        default=True,
        description="For continuous annotations used as color parameter, plot data points with higher values on top of others."
    )
    
    edges: bool = Field(
        default=False,
        description="Show edges between nodes."
    )
    
    edges_width: float = Field(
        default=0.1,
        description="Width of edges."
    )
    
    edges_color: Union[str, List[float], List[str]] = Field(
        default='grey',
        description="Color of edges."
    )
    
    neighbors_key: Optional[str] = Field(
        default=None,
        description="Where to look for neighbors connectivities."
    )
    
    arrows: bool = Field(
        default=False,
        description="Show arrows."
    )
    
    groups: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Restrict to a few categories in categorical observation annotation."
    )
    
    components: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="For instance, ['1,2', '2,3']. To plot all available components use components='all'."
    )
    
    dimensions: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]] = Field(
        default=None,
        description="0-indexed dimensions of the embedding to plot as integers. E.g. [(0, 1), (1, 2)]."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="Name of the AnnData object layer that wants to be plotted."
    )
    
    projection: Literal['2d', '3d'] = Field(
        default='2d',
        description="Projection of plot."
    )
    
    size: Optional[Union[float, List[float]]] = Field(
        default=None,
        description="Point size. If None, is automatically computed."
    )
    
    frameon: Optional[bool] = Field(
        default=None,
        description="Draw a frame around the scatter plot."
    )
    
    add_outline: Optional[bool] = Field(
        default=False,
        description="Add outline to scatter plot points."
    )
    
    ncols: int = Field(
        default=4,
        description="Number of columns for multiple plots."
    )
    
    marker: Union[str, List[str]] = Field(
        default='.',
        description="Matplotlib marker style for points."
    )


# 重构 ScatterModel 作为基础散点图模型
class BaseScatterModel(BaseVisualizationModel):
    """基础散点图模型"""
    
    x: Optional[str] = Field(
        default=None,
        description="x coordinate."
    )    
    
    y: Optional[str] = Field(
        default=None,
        description="y coordinate."
    )
    
    color: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Keys for annotations of observations/cells or variables/genes, or a hex color specification."
    )
    
    use_raw: Optional[bool] = Field(
        default=None,
        description="Whether to use raw attribute of adata. Defaults to True if .raw is present."
    )
    
    layers: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Use the layers attribute of adata if present: specify the layer for x, y and color."
    )
    
    basis: Optional[str] = Field(
        default=None,
        description="Basis to use for embedding."
    )


# 使用继承关系重构 EnhancedScatterModel
class EnhancedScatterModel(BaseScatterModel):
    """Input schema for the enhanced scatter plotting tool."""
    
    sort_order: bool = Field(
        default=True,
        description="For continuous annotations used as color parameter, plot data points with higher values on top of others."
    )
    
    alpha: Optional[float] = Field(
        default=None,
        description="Alpha value for the plot.",
        ge=0,
        le=1
    )
    
    groups: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Restrict to a few categories in categorical observation annotation."
    )
    
    components: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="For instance, ['1,2', '2,3']. To plot all available components use components='all'."
    )
    
    projection: Literal['2d', '3d'] = Field(
        default='2d',
        description="Projection of plot."
    )
    
    right_margin: Optional[float] = Field(
        default=None,
        description="Adjust the width of the right margin."
    )
    
    left_margin: Optional[float] = Field(
        default=None,
        description="Adjust the width of the left margin."
    )
    
    @field_validator('alpha')
    def validate_alpha(cls, v: Optional[float]) -> Optional[float]:
        """Validate alpha is between 0 and 1"""
        if v is not None and (v < 0 or v > 1):
            raise ValueError("alpha must be between 0 and 1")
        return v


# 创建基础统计可视化模型
class BaseStatPlotModel(BaseVisualizationModel):
    """基础统计可视化模型，包含统计图表共享的字段"""
    
    groupby: Optional[str] = Field(
        default=None,
        description="The key of the observation grouping to consider."
    )
    
    log: bool = Field(
        default=False,
        description="Plot on logarithmic axis."
    )
    
    use_raw: Optional[bool] = Field(
        default=None,
        description="Use raw attribute of adata if present."
    )
    
    var_names: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="var_names should be a valid subset of adata.var_names."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="Name of the AnnData object layer that wants to be plotted."
    )
    
    gene_symbols: Optional[str] = Field(
        default=None,
        description="Column name in .var DataFrame that stores gene symbols."
    )
    
    # 添加共享的小提琴图相关字段
    stripplot: bool = Field(
        default=True,
        description="Add a stripplot on top of the violin plot."
    )
    
    jitter: Union[float, bool] = Field(
        default=True,
        description="Add jitter to the stripplot (only when stripplot is True)."
    )
    
    size: int = Field(
        default=1,
        description="Size of the jitter points.",
        gt=0
    )
    
    order: Optional[List[str]] = Field(
        default=None,
        description="Order in which to show the categories."
    )
    
    scale: Literal['area', 'count', 'width'] = Field(
        default='width',
        description="The method used to scale the width of each violin."
    )
    
    @field_validator('size')
    def validate_size(cls, v: int) -> int:
        """Validate size is positive"""
        if v <= 0:
            raise ValueError("size must be a positive integer")
        return v

# 添加缺失的 BaseMatrixModel 类
class BaseMatrixModel(BaseVisualizationModel):
    """基础矩阵可视化模型，包含所有矩阵可视化工具共享的字段"""
    
    var_names: Union[List[str], Mapping[str, List[str]]] = Field(
        ...,  # Required field
        description="var_names should be a valid subset of adata.var_names or a mapping where the key is used as label to group the values."
    )    
    groupby: Union[str, List[str]] = Field(
        ...,  # Required field
        description="The key of the observation grouping to consider."
    )
    use_raw: Optional[bool] = Field(
        default=None,
        description="Use raw attribute of adata if present."
    )
    log: bool = Field(
        default=False,
        description="Plot on logarithmic axis."
    )
    dendrogram: Union[bool, str] = Field(
        default=False,
        description="If True or a valid dendrogram key, a dendrogram based on the hierarchical clustering between the groupby categories is added."
    )
    
    gene_symbols: Optional[str] = Field(
        default=None,
        description="Column name in .var DataFrame that stores gene symbols."
    )
    
    var_group_positions: Optional[List[Tuple[int, int]]] = Field(
        default=None,
        description="Use this parameter to highlight groups of var_names with brackets or color blocks between the given start and end positions."
    )
    
    var_group_labels: Optional[List[str]] = Field(
        default=None,
        description="Labels for each of the var_group_positions that want to be highlighted."
    )
    
    layer: Optional[str] = Field(
        default=None,
        description="Name of the AnnData object layer that wants to be plotted."
    )


# 重构 HeatmapModel
class HeatmapModel(BaseMatrixModel):
    """Input schema for the heatmap plotting tool."""
    
    num_categories: int = Field(
        default=7,
        description="Only used if groupby observation is not categorical. This value determines the number of groups into which the groupby observation should be subdivided.",
        gt=0
    )
    
    var_group_rotation: Optional[float] = Field(
        default=None,
        description="Label rotation degrees. By default, labels larger than 4 characters are rotated 90 degrees."
    )
    
    standard_scale: Optional[Literal['var', 'obs']] = Field(
        default=None,
        description="Whether or not to standardize that dimension between 0 and 1."
    )
    
    swap_axes: bool = Field(
        default=False,
        description="By default, the x axis contains var_names and the y axis the groupby categories. By setting swap_axes then x are the groupby categories and y the var_names."
    )
    
    show_gene_labels: Optional[bool] = Field(
        default=None,
        description="By default gene labels are shown when there are 50 or less genes. Otherwise the labels are removed."
    )
    
    @field_validator('num_categories')
    def validate_num_categories(cls, v: int) -> int:
        """Validate num_categories is positive"""
        if v <= 0:
            raise ValueError("num_categories must be a positive integer")
        return v


# 重构 TracksplotModel
class TracksplotModel(BaseMatrixModel):
    """Input schema for the tracksplot plotting tool."""
    # 所有需要的字段已经在 BaseMatrixModel 中定义


# 重构 ViolinModel
class ViolinModel(BaseStatPlotModel):
    """Input schema for the violin plotting tool."""
    
    keys: Union[str, List[str]] = Field(
        ...,  # Required field
        description="Keys for accessing variables of .var_names or fields of .obs."
    )
    stripplot: bool = Field(
        default=True,
        description="Add a stripplot on top of the violin plot."
    )
    jitter: Union[float, bool] = Field(
        default=True,
        description="Add jitter to the stripplot (only when stripplot is True)."
    )
    size: int = Field(
        default=1,
        description="Size of the jitter points.",
        gt=0
    )
    scale: Literal['area', 'count', 'width'] = Field(
        default='width',
        description="The method used to scale the width of each violin."
    )
    order: Optional[List[str]] = Field(
        default=None,
        description="Order in which to show the categories."
    )
    multi_panel: Optional[bool] = Field(
        default=None,
        description="Display keys in multiple panels also when groupby is not None."
    )
    xlabel: str = Field(
        default='',
        description="Label of the x axis. Defaults to groupby if rotation is None, otherwise, no label is shown."
    )    
    ylabel: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Label of the y axis."
    )
    
    rotation: Optional[float] = Field(
        default=None,
        description="Rotation of xtick labels."
    )
    
    @field_validator('size')
    def validate_size(cls, v: int) -> int:
        """Validate size is positive"""
        if v <= 0:
            raise ValueError("size must be a positive integer")
        return v


# 重构 MatrixplotModel
class MatrixplotModel(BaseMatrixModel):
    """Input schema for the matrixplot plotting tool."""
    
    num_categories: int = Field(
        default=7,
        description="Only used if groupby observation is not categorical. This value determines the number of groups into which the groupby observation should be subdivided.",
        gt=0
    )
    
    cmap: Optional[str] = Field(
        default='viridis',
        description="String denoting matplotlib color map."
    )
    
    colorbar_title: Optional[str] = Field(
        default='Mean expression\nin group',
        description="Title for the color bar. New line character (\\n) can be used."
    )
    
    var_group_rotation: Optional[float] = Field(
        default=None,
        description="Label rotation degrees. By default, labels larger than 4 characters are rotated 90 degrees."
    )
    
    standard_scale: Optional[Literal['var', 'group']] = Field(
        default=None,
        description="Whether or not to standardize the given dimension between 0 and 1."
    )
    
    swap_axes: bool = Field(
        default=False,
        description="By default, the x axis contains var_names and the y axis the groupby categories. By setting swap_axes then x are the groupby categories and y the var_names."
    )
    
    @field_validator('num_categories')
    def validate_num_categories(cls, v: int) -> int:
        """Validate num_categories is positive"""
        if v <= 0:
            raise ValueError("num_categories must be a positive integer")
        return v


# 重构 DotplotModel
class DotplotModel(BaseMatrixModel):
    """Input schema for the dotplot plotting tool."""
    
    expression_cutoff: float = Field(
        default=0.0,
        description="Expression cutoff that is used for binarizing the gene expression."
    )
    
    mean_only_expressed: bool = Field(
        default=False,
        description="If True, gene expression is averaged only over the cells expressing the given genes."
    )
    
    standard_scale: Optional[Literal['var', 'group']] = Field(
        default=None,
        description="Whether or not to standardize that dimension between 0 and 1."
    )
    
    swap_axes: bool = Field(
        default=False,
        description="By default, the x axis contains var_names and the y axis the groupby categories. By setting swap_axes then x are the groupby categories and y the var_names."
    )
    
    dot_max: Optional[float] = Field(
        default=None,
        description="The maximum size of the dots."
    )
    
    dot_min: Optional[float] = Field(
        default=None,
        description="The minimum size of the dots."
    )
    
    smallest_dot: Optional[float] = Field(
        default=None,
        description="The smallest dot size."
    )
    var_group_rotation: Optional[float] = Field(
        default=None,
        description="Label rotation degrees. By default, labels larger than 4 characters are rotated 90 degrees."
    )
    
    colorbar_title: Optional[str] = Field(
        default='Mean expression\nin group',
        description="Title for the color bar. New line character (\\n) can be used."
    )
    
    size_title: Optional[str] = Field(
        default='Fraction of cells\nin group (%)',
        description="Title for the size legend. New line character (\\n) can be used."
    )


# 重构 RankGenesGroupsModel
class RankGenesGroupsModel(BaseVisualizationModel):
    """Input schema for the rank_genes_groups plotting tool."""
    
    n_genes: int = Field(
        default=20,
        description="Number of genes to show.",
        gt=0
    )
    
    gene_symbols: Optional[str] = Field(
        default=None,
        description="Column name in `.var` DataFrame that stores gene symbols."
    )
    
    groupby: Optional[str] = Field(
        default=None,
        description="The key of the observation grouping to consider."
    )
    
    groups: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="Subset of groups, e.g. ['g1', 'g2', 'g3']."
    )
    
    key: Optional[str] = Field(
        default='rank_genes_groups',
        description="Key used to store the rank_genes_groups parameters."
    )
    
    fontsize: int = Field(
        default=8,
        description="Fontsize for gene names."
    )
    
    ncols: int = Field(
        default=4,
        description="Number of columns."
    )
    
    sharey: bool = Field(
        default=True,
        description="Controls if the y-axis of each panels should be shared."
    )
    
    @field_validator('n_genes', 'fontsize')
    def validate_positive_int(cls, v: int) -> int:
        """Validate positive integers"""
        if v <= 0:
            raise ValueError(f"Value must be a positive integer")
        return v


# 重构 ClusterMapModel
class ClusterMapModel(JSONParsingModel):
    """Input schema for the clustermap plotting tool."""

    obs_keys: Optional[str] = Field(
        default=None,
        description="key column in adata.obs, categorical annotation to plot with a different color map."
    )
    use_raw: Optional[bool] = Field(
        default=None,
        description="Whether to use `raw` attribute of `adata`. Defaults to `True` if `.raw` is present."
    )



# 重构 StackedViolinModel
class StackedViolinModel(BaseStatPlotModel):
    """Input schema for the stacked_violin plotting tool."""
    
    stripplot: bool = Field(
        default=True,
        description="Add a stripplot on top of the violin plot."
    )
    
    jitter: Union[float, bool] = Field(
        default=True,
        description="Add jitter to the stripplot (only when stripplot is True)."
    )
    
    size: int = Field(
        default=1,
        description="Size of the jitter points.",
        gt=0
    )
    
    order: Optional[List[str]] = Field(
        default=None,
        description="Order in which to show the categories."
    )
    
    scale: Literal['area', 'count', 'width'] = Field(
        default='width',
        description="The method used to scale the width of each violin."
    )
    
    swap_axes: bool = Field(
        default=False,
        description="Swap axes such that observations are on the x-axis."
    )
    
    @field_validator('size')
    def validate_size(cls, v: int) -> int:
        """Validate size is positive"""
        if v <= 0:
            raise ValueError("size must be a positive integer")
        return v


# 重构 TrackingModel
class TrackingModel(BaseVisualizationModel):
    """Input schema for the tracking plotting tool."""
    
    groupby: str = Field(
        ...,  # Required field
        description="The key of the observation grouping to consider."
    )
    
    min_group_size: int = Field(
        default=1,
        description="Minimal number of cells in a group for the group to be considered.",
        gt=0
    )
    
    min_split_size: int = Field(
        default=1,
        description="Minimal number of cells in a split for the split to be shown.",
        gt=0
    )
    
    @field_validator('min_group_size', 'min_split_size')
    def validate_positive_int(cls, v: int) -> int:
        """Validate positive integers"""
        if v <= 0:
            raise ValueError(f"Value must be a positive integer")
        return v


# 重构 EmbeddingDensityModel
class EmbeddingDensityModel(BaseEmbeddingModel):
    """Input schema for the embedding_density plotting tool."""
    
    basis: str = Field(
        ...,  # Required field
        description="Basis to use for embedding."
    )
    
    key: Optional[str] = Field(
        default=None,
        description="Key for annotation of observations/cells or variables/genes."
    )
    
    convolve: Optional[float] = Field(
        default=None,
        description="Sigma for Gaussian kernel used for convolution."
    )
    
    alpha: float = Field(
        default=0.5,
        description="Alpha value for the plot.",
        ge=0,
        le=1
    )
    
    @field_validator('alpha')
    def validate_alpha(cls, v: float) -> float:
        """Validate alpha is between 0 and 1"""
        if v < 0 or v > 1:
            raise ValueError("alpha must be between 0 and 1")
        return v


class PCAModel(BaseEmbeddingModel):
    """Input schema for the PCA plotting tool."""
    
    annotate_var_explained: bool = Field(
        default=False,
        description="Annotate the explained variance."
    )


# 重构 UMAP 模型
class UMAPModel(BaseEmbeddingModel):
    """Input schema for the UMAP plotting tool."""
    # 所有需要的字段已经在 BaseEmbeddingModel 中定义


# 重构 TSNE 模型
class TSNEModel(BaseEmbeddingModel):
    """Input schema for the TSNE plotting tool."""
    # 所有需要的字段已经在 BaseEmbeddingModel 中定义


# 重构 DiffusionMapModel
class DiffusionMapModel(BaseEmbeddingModel):
    """Input schema for the diffusion map plotting tool."""
    # 所有需要的字段已经在 BaseEmbeddingModel 中定义

class HighestExprGenesModel(BaseVisualizationModel):
    """Input schema for the highest_expr_genes plotting tool."""
    
    n_top: int = Field(
        default=30,
        description="Number of top genes to plot.",
        gt=0
    )
    
    gene_symbols: Optional[str] = Field(
        default=None,
        description="Key for field in .var that stores gene symbols if you do not want to use .var_names."
    )
    
    log: bool = Field(
        default=False,
        description="Plot x-axis in log scale."
    )
    
    @field_validator('n_top')
    def validate_n_top(cls, v: int) -> int:
        """Validate n_top is positive"""
        if v <= 0:
            raise ValueError("n_top must be a positive integer")
        return v


class HighlyVariableGenesModel(BaseVisualizationModel):
    """Input schema for the highly_variable_genes plotting tool."""
    
    log: bool = Field(
        default=False,
        description="Plot on logarithmic axes."
    )
    
    highly_variable_genes: bool = Field(
        default=True,
        description="Whether to plot highly variable genes or all genes."
    )

class PCAVarianceRatioModel(BaseVisualizationModel):
    """Input schema for the pca_variance_ratio plotting tool."""
    
    n_pcs: int = Field(
        default=30,
        description="Number of PCs to show.",
        gt=0
    )
    
    log: bool = Field(
        default=False,
        description="Plot on logarithmic scale."
    )
    
    @field_validator('n_pcs')
    def validate_n_pcs(cls, v: int) -> int:
        """Validate n_pcs is positive"""
        if v <= 0:
            raise ValueError("n_pcs must be a positive integer")
        return v

# ... existing code ...

class RankGenesGroupsDotplotModel(BaseMatrixModel):
    """Input schema for the rank_genes_groups_dotplot plotting tool."""
    
    groups: Optional[Union[str, List[str]]] = Field(
        default=None,
        description="The groups for which to show the gene ranking."
    )    
    n_genes: Optional[int] = Field(
        default=None,
        description="Number of genes to show. This can be a negative number to show down regulated genes. Ignored if var_names is passed."
    )
    values_to_plot: Optional[Literal['scores', 'logfoldchanges', 'pvals', 'pvals_adj', 'log10_pvals', 'log10_pvals_adj']] = Field(
        default=None,
        description="Instead of the mean gene value, plot the values computed by sc.rank_genes_groups."
    )
    min_logfoldchange: Optional[float] = Field(
        default=None,
        description="Value to filter genes in groups if their logfoldchange is less than the min_logfoldchange."
    )
    key: Optional[str] = Field(
        default=None,
        description="Key used to store the ranking results in adata.uns."
    )
    var_names: Union[List[str], Mapping[str, List[str]]] = Field(
        default=None,
        description="Genes to plot. Sometimes is useful to pass a specific list of var names (e.g. genes) to check their fold changes or p-values"
    )        
    @field_validator('n_genes')
    def validate_n_genes(cls, v: Optional[int]) -> Optional[int]:
        """Validate n_genes"""
        # n_genes can be positive or negative, so no validation needed
        return v