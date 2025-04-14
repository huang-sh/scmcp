from functools import partial
from pathlib import Path
import mcp.types as types
import scanpy as sc
import os
import inspect
from ..schema.pp import *
import os
from ..logging_config import setup_logger
from ..util import add_op_log

logger = setup_logger(log_file=os.environ.get("SCMCP_LOG_FILE", None))


filter_cells = types.Tool(
    name="filter_cells",
    description="Filter cells based on counts and numbers of genes expressed.",
    inputSchema=FilterCells.model_json_schema(),
)

filter_genes = types.Tool(
    name="filter_genes",
    description="Filter genes based on number of cells or counts",
    inputSchema=FilterGenes.model_json_schema(),
)

calculate_qc_metrics = types.Tool(
    name="calculate_qc_metrics",
    description="Calculate quality control metrics(common metrics: total counts, gene number, percentage of counts in ribosomal and mitochondrial) for AnnData.",
    inputSchema=CalculateQCMetrics.model_json_schema(),
)

log1p = types.Tool(
    name="log1p",
    description="Logarithmize the data matrix (X = log(X + 1))",
    inputSchema=Log1PModel.model_json_schema(),
)

normalize_total = types.Tool(
    name="normalize_total",
    description="Normalize counts per cell to the same total count",
    inputSchema=NormalizeTotalModel.model_json_schema(),
)

pca = types.Tool(
    name="pca",
    description="Principal component analysis",
    inputSchema=PCAModel.model_json_schema(),
)

highly_variable_genes = types.Tool(
    name="highly_variable_genes",
    description="Annotate highly variable genes",
    inputSchema=HighlyVariableGenesModel.model_json_schema(),
)

regress_out = types.Tool(
    name="regress_out",
    description="Regress out (mostly) unwanted sources of variation.",
    inputSchema=RegressOutModel.model_json_schema(),
)

scale = types.Tool(
    name="scale",
    description="Scale data to unit variance and zero mean",
    inputSchema=ScaleModel.model_json_schema(),
)

combat = types.Tool(
    name="combat",
    description="ComBat function for batch effect correction",
    inputSchema=CombatModel.model_json_schema(),
)

scrublet = types.Tool(
    name="scrublet",
    description="Predict doublets using Scrublet",
    inputSchema=ScrubletModel.model_json_schema(),
)

neighbors = types.Tool(
    name="neighbors",
    description="Compute nearest neighbors distance matrix and neighborhood graph",
    inputSchema=NeighborsModel.model_json_schema(),
)


pp_func = {
    "filter_genes": sc.pp.filter_genes,
    "filter_cells": sc.pp.filter_cells,
    "calculate_qc_metrics": partial(sc.pp.calculate_qc_metrics, inplace=True),
    "log1p": sc.pp.log1p,
    "normalize_total": sc.pp.normalize_total,
    "pca": sc.pp.pca,
    "highly_variable_genes": sc.pp.highly_variable_genes,
    "regress_out": sc.pp.regress_out,
    "scale": sc.pp.scale,
    "combat": sc.pp.combat,
    "scrublet": sc.pp.scrublet,
    "neighbors": sc.pp.neighbors,
}

# 模型与函数名称的映射
pp_tools = {
    "filter_genes": filter_genes,
    "filter_cells": filter_cells,
    "calculate_qc_metrics": calculate_qc_metrics,
    "log1p": log1p,
    "normalize_total": normalize_total,
    "pca": pca,
    "highly_variable_genes": highly_variable_genes,
    "regress_out": regress_out,
    "scale": scale,
    "combat": combat,
    "scrublet": scrublet,
    "neighbors": neighbors,
}


def run_pp_func(adata, func, arguments):
    if func not in pp_func:
        raise ValueError(f"不支持的函数: {func}")
    
    run_func = pp_func[func]
    parameters = inspect.signature(run_func).parameters
    kwargs = {k: arguments.get(k) for k in parameters if k in arguments}    
    if "inplace" in parameters:
        kwargs["inplace"] = True
    try:
        res = run_func(adata, **kwargs)
        add_op_log(adata, run_func, kwargs)
    except KeyError as e:
        raise KeyError(f"Can not foud {e} column in adata.obs or adata.var")
    except Exception as e:
       raise e
    return res
