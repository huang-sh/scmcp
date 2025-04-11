import os
import inspect
from functools import partial
import mcp.types as types
import scanpy as sc
from ..schema.pl import *
import os
from pathlib import Path
from ..logging_config import setup_logger
from ..util import add_op_log


logger = setup_logger(log_file=os.environ.get("SCANPY_MCP_LOG_FILE", None))

pl_pca_tool = types.Tool(
    name="pl_pca",
    description="Scatter plot in PCA coordinates. default figure for PCA plot",
    inputSchema=PCAModel.model_json_schema(),
)

pl_umap_tool = types.Tool(
    name="pl_umap",
    description="Scatter plot in UMAP basis. default visualization plot for cell cluster if not specified by user",
    inputSchema=UMAPModel.model_json_schema(),
)

pl_tsne = types.Tool(
    name="pl_tsne",
    description="Plot t-SNE embedding of cells.",
    inputSchema=TSNEModel.model_json_schema(),
)

diffmap = types.Tool(
    name="diffmap",
    description="Plot diffusion map embedding of cells.",
    inputSchema=DiffusionMapModel.model_json_schema(),
)

# Define tools for statistical visualizations
pl_violin = types.Tool(
    name="pl_violin",
    description="Plot violin plot of one or more variables.",
    inputSchema=ViolinModel.model_json_schema(),
)

pl_stacked_violin = types.Tool(
    name="pl_stacked_violin",
    description="Plot stacked violin plots. Makes a compact image composed of individual violin plots stacked on top of each other.",
    inputSchema=StackedViolinModel.model_json_schema(),
)

# Define tools for matrix visualizations
pl_heatmap = types.Tool(
    name="pl_heatmap",
    description="Heatmap of the expression values of genes.",
    inputSchema=HeatmapModel.model_json_schema(),
)

pl_dotplot = types.Tool(
    name="pl_dotplot",
    description="Plot dot plot of expression values per gene for each group.",
    inputSchema=DotplotModel.model_json_schema(),
)

pl_matrixplot = types.Tool(
    name="pl_matrixplot",
    description="matrixplot, Create a heatmap of the mean expression values per group of each var_names.",
    inputSchema=MatrixplotModel.model_json_schema(),
)

pl_tracksplot = types.Tool(
    name="pl_tracksplot",
    description="tracksplot,compact plot of expression of a list of genes..",
    inputSchema=TracksplotModel.model_json_schema(),
)

# Define tools for other visualizations
pl_scatter = types.Tool(
    name="pl_scatter",
    description="Plot a scatter plot of two variables, Scatter plot along observations or variables axes.",
    inputSchema=EnhancedScatterModel.model_json_schema(),
)

embedding_density = types.Tool(
    name="embedding_density",
    description="Plot the density of cells in an embedding.",
    inputSchema=EmbeddingDensityModel.model_json_schema(),
)

rank_genes_groups = types.Tool(
    name="rank_genes_groups",
    description="Plot ranking of genes based on differential expression.",
    inputSchema=RankGenesGroupsModel.model_json_schema(),
)

# Add rank_genes_groups_dotplot tool
pl_rank_genes_groups_dotplot = types.Tool(
    name="pl_rank_genes_groups_dotplot",
    description="Plot ranking of genes(DEGs) using dotplot visualization. Defualt plot DEGs for rank_genes_groups tool",
    inputSchema=RankGenesGroupsDotplotModel.model_json_schema(),
)

pl_clustermap = types.Tool(
    name="pl_clustermap",
    description="Plot hierarchical clustering of cells and genes.",
    inputSchema=ClusterMapModel.model_json_schema(),
)

# 添加 highly_variable_genes 工具
pl_highly_variable_genes = types.Tool(
    name="pl_highly_variable_genes",
    description="plot highly variable genes; Plot dispersions or normalized variance versus means for genes.",
    inputSchema=HighlyVariableGenesModel.model_json_schema(),
)

# Add pca_variance_ratio tool
pl_pca_variance_ratio = types.Tool(
    name="pl_pca_variance_ratio",
    description="Plot the PCA variance ratio to visualize explained variance.",
    inputSchema=PCAVarianceRatioModel.model_json_schema(),
)

# Map tool names to Scanpy plotting functions
pl_func = {
    "pl_pca": sc.pl.pca,
    "pl_umap": sc.pl.umap,
    "pl_tsne": sc.pl.tsne,
    "diffmap": sc.pl.diffmap,
    "pl_violin": sc.pl.violin,
    "pl_stacked_violin": sc.pl.stacked_violin,
    "pl_heatmap": sc.pl.heatmap,
    "pl_dotplot": sc.pl.dotplot,
    "pl_matrixplot": sc.pl.matrixplot,
    "pl_tracksplot": sc.pl.tracksplot,
    "pl_scatter": sc.pl.scatter,
    "embedding_density": sc.pl.embedding_density,
    "rank_genes_groups": sc.pl.rank_genes_groups,
    "pl_rank_genes_groups_dotplot": sc.pl.rank_genes_groups_dotplot,  # Add function mapping
    "pl_clustermap": sc.pl.clustermap,
    "pl_highly_variable_genes": sc.pl.highly_variable_genes,
    "pl_pca_variance_ratio": sc.pl.pca_variance_ratio,
}

# Map tool names to tool objects
pl_tools = {
    "pl_pca": pl_pca_tool,
    "pl_umap": pl_umap_tool,
    "pl_tsne": pl_tsne,
    # "diffmap": diffmap,
    "pl_violin": pl_violin,
    "pl_stacked_violin": pl_stacked_violin,
    "pl_heatmap": pl_heatmap,
    "pl_dotplot": pl_dotplot,
    "pl_matrixplot": pl_matrixplot,
    "pl_tracksplot": pl_tracksplot,
    "pl_scatter": pl_scatter,
    # "embedding_density": embedding_density,
    # "spatial": spatial,
    # "rank_genes_groups": rank_genes_groups,
    "pl_rank_genes_groups_dotplot": pl_rank_genes_groups_dotplot,  # Add tool mapping
    # "pl_clustermap": pl_clustermap,
    "pl_highly_variable_genes": pl_highly_variable_genes,
    "pl_pca_variance_ratio": pl_pca_variance_ratio,
}

def fig_to_bytes(fig, format='png'):
    try:
        import matplotlib.pyplot as plt
        from io import BytesIO
        buf = BytesIO()
        
        if hasattr(fig, 'figure'):  # if Axes
            fig.figure.savefig(buf, format=format)
        else:  # if Figure 
            fig.savefig(buf, format=format)
            
        buf.seek(0)
        return buf.read()
    except Exception as e:
        logger.error(f"Error converting figure to bytes: {e}")
        raise e


def savefig(fig, file, format="png"):
    try:
        import matplotlib.pyplot as plt
        
        if hasattr(fig, 'figure'):  # if Axes
            fig.figure.savefig(buf, format=format)
        else:  # if Figure 
            fig.savefig(buf, format=format)
            

        return file
    except Exception as e:
        logger.error(f"Error save figure: {e}")
        raise e


def fig_rename(func):
        fig_dir = Path(os.getcwd()) / "figures"
        fig_path = fig_dir / f"{func[3:]}.png"
        try:
            os.rename(fig_dir/f'{func[3:]}_.png', fig_path)
        except FileNotFoundError:
            print(f"The file {fig_dir/f'{func[3:]}_.png'} does not exist")
        except FileExistsError:
            print(f"The file {fig_path} already exists")
        except PermissionError:
            print("You don't have permission to rename this file")   
        return fig_path


def run_pl_func(adata, func, arguments):
    """
    Execute a Scanpy plotting function with the given arguments.
    
    Parameters
    ----------
    adata : AnnData
        Annotated data matrix.
    func : str
        Name of the plotting function to execute.
    arguments : dict
        Arguments to pass to the plotting function.
        
    Returns
    -------
    The result of the plotting function.
    """
    if func not in pl_func:
        raise ValueError(f"Unsupported function: {func}")

    run_func = pl_func[func]
    parameters = inspect.signature(run_func).parameters
    kwargs = {k: arguments.get(k) for k in parameters if k in arguments}    

    if "title" not in parameters:
        kwargs.pop("title", False)    
    kwargs.pop("return_fig", True)
    kwargs["show"] = False
    kwargs["save"] = ".png"
    try:
        fig = run_func(adata, **kwargs)
        fig_path = fig_rename(func)
        add_op_log(adata, run_func, kwargs)
        return fig_path 
    except Exception as e:
        raise e
    return fig_path
