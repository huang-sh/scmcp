import inspect
import mcp.types as types
import scanpy as sc
from ..schema.tl import *
from ..logging_config import setup_logger
import os
from ..util import add_op_log

logger = setup_logger(log_file=os.environ.get("SCMCP_LOG_FILE", None))


# Define t-SNE tool
tsne_tool = types.Tool(
    name="tsne",
    description="t-distributed stochastic neighborhood embedding (t-SNE), for visualizating single-cell data",
    inputSchema=TSNEModel.model_json_schema(),
)

# Add UMAP tool
umap_tool = types.Tool(
    name="umap",
    description="Uniform Manifold Approximation and Projection (UMAP) for visualization",
    inputSchema=UMAPModel.model_json_schema(),
)

# Add draw_graph tool
draw_graph_tool = types.Tool(
    name="draw_graph",
    description="Force-directed graph drawing for visualization",
    inputSchema=DrawGraphModel.model_json_schema(),
)

# Add diffmap tool
diffmap_tool = types.Tool(
    name="diffmap",
    description="Diffusion Maps for dimensionality reduction",
    inputSchema=DiffMapModel.model_json_schema(),
)

# Add embedding_density tool
embedding_density_tool = types.Tool(
    name="embedding_density",
    description="Calculate the density of cells in an embedding",
    inputSchema=EmbeddingDensityModel.model_json_schema(),
)

# Add leiden tool
leiden_tool = types.Tool(
    name="leiden",
    description="Leiden clustering algorithm for community detection",
    inputSchema=LeidenModel.model_json_schema(),
)

# Add louvain tool
louvain_tool = types.Tool(
    name="louvain",
    description="Louvain clustering algorithm for community detection",
    inputSchema=LouvainModel.model_json_schema(),
)

# Add dendrogram tool
dendrogram_tool = types.Tool(
    name="dendrogram",
    description="Hierarchical clustering dendrogram",
    inputSchema=DendrogramModel.model_json_schema(),
)

# Add dpt tool
dpt_tool = types.Tool(
    name="dpt",
    description="Diffusion Pseudotime (DPT) analysis",
    inputSchema=DPTModel.model_json_schema(),
)

# Add paga tool
paga_tool = types.Tool(
    name="paga",
    description="Partition-based graph abstraction",
    inputSchema=PAGAModel.model_json_schema(),
)

# Add ingest tool
ingest_tool = types.Tool(
    name="ingest",
    description="Map labels and embeddings from reference data to new data",
    inputSchema=IngestModel.model_json_schema(),
)

# Add rank_genes_groups tool
rank_genes_groups_tool = types.Tool(
    name="rank_genes_groups",
    description="Rank genes for characterizing groups, perform differentially expressison analysis",
    inputSchema=RankGenesGroupsModel.model_json_schema(),
)

# Add filter_rank_genes_groups tool
filter_rank_genes_groups_tool = types.Tool(
    name="filter_rank_genes_groups",
    description="Filter out genes based on fold change and fraction of genes",
    inputSchema=FilterRankGenesGroupsModel.model_json_schema(),
)

# Add marker_gene_overlap tool
marker_gene_overlap_tool = types.Tool(
    name="marker_gene_overlap",
    description="Calculate overlap between data-derived marker genes and reference markers",
    inputSchema=MarkerGeneOverlapModel.model_json_schema(),
)

# Add score_genes tool
score_genes_tool = types.Tool(
    name="score_genes",
    description="Score a set of genes based on their average expression",
    inputSchema=ScoreGenesModel.model_json_schema(),
)

# Add score_genes_cell_cycle tool
score_genes_cell_cycle_tool = types.Tool(
    name="score_genes_cell_cycle",
    description="Score cell cycle genes and assign cell cycle phases",
    inputSchema=ScoreGenesCellCycleModel.model_json_schema(),
)

# Dictionary mapping tool names to scanpy functions
tl_func = {
    "tsne": sc.tl.tsne,
    "umap": sc.tl.umap,
    "draw_graph": sc.tl.draw_graph,
    "diffmap": sc.tl.diffmap,
    "embedding_density": sc.tl.embedding_density,
    "leiden": sc.tl.leiden,
    "louvain": sc.tl.louvain,
    "dendrogram": sc.tl.dendrogram,
    "dpt": sc.tl.dpt,
    "paga": sc.tl.paga,
    "ingest": sc.tl.ingest,
    "rank_genes_groups": sc.tl.rank_genes_groups,
    "filter_rank_genes_groups": sc.tl.filter_rank_genes_groups,
    "marker_gene_overlap": sc.tl.marker_gene_overlap,
    "score_genes": sc.tl.score_genes,
    "score_genes_cell_cycle": sc.tl.score_genes_cell_cycle,
}

# Dictionary mapping tool names to tool objects
tl_tools = {
    "tsne": tsne_tool,
    "umap": umap_tool,
    "draw_graph": draw_graph_tool,
    "diffmap": diffmap_tool,
    "embedding_density": embedding_density_tool,
    "leiden": leiden_tool,
    "louvain": louvain_tool,
    "dendrogram": dendrogram_tool,
    "dpt": dpt_tool,
    "paga": paga_tool,
    "ingest": ingest_tool,
    "rank_genes_groups": rank_genes_groups_tool,
    "filter_rank_genes_groups": filter_rank_genes_groups_tool,
    "marker_gene_overlap": marker_gene_overlap_tool,
    "score_genes": score_genes_tool,
    "score_genes_cell_cycle": score_genes_cell_cycle_tool,
}

def run_tl_func(ads, func, arguments):
    adata = ads.adata_dic[ads.active]
    if func not in tl_func:
        raise ValueError(f"Unsupported function: {func}")
    run_func = tl_func[func]
    parameters = inspect.signature(run_func).parameters
    kwargs = {k: arguments.get(k) for k in parameters if k in arguments}    
    try:
        res = run_func(adata, **kwargs)
        add_op_log(adata, run_func, kwargs)
    except Exception as e:
        logger.error(f"Error running function {func}: {e}")
        raise
    return 