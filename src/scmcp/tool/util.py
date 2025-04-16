import inspect
from ..schema.util import *
import mcp.types as types
import os
from ..util import add_op_log
from ..logging_config import setup_logger

logger = setup_logger(log_file=os.environ.get("SCMCP_LOG_FILE", None))


mark_var_tool = types.Tool(
    name="mark_var",
    description=(
        "Determine if each gene meets specific conditions and store results in adata.var as boolean values."
        "for example: mitochondrion genes startswith MT-."
        "the tool should be call first when calculate quality control metrics for mitochondrion, ribosomal, harhemoglobin genes. or other qc_vars"
    ),
    inputSchema=MarkVarModel.model_json_schema(),
)

list_var_tool = types.Tool(
    name="list_var",
    description="list key columns in adata.var. it should be called for checking when other tools need var key column names input",
    inputSchema=ListVarModel.model_json_schema(),
)

# Add list_obs tool
list_obs_tool = types.Tool(
    name="list_obs",
    description="List key columns in adata.obs. It should be called before other tools need obs key column names input",
    inputSchema=ListObsModel.model_json_schema(),
)

check_gene_tool = types.Tool(
    name="check_gene",
    description="Check if genes exist in adata.var_names. This tool should be called before gene expression visualizations or color by genes.",
    inputSchema=VarNamesModel.model_json_schema(),
)

merge_adata_tool = types.Tool(
    name="merge_adata",
    description="merge multiple adata",
    inputSchema=ConcatAdataModel.model_json_schema(),
)


def mark_var(adata, var_name: str = None, gene_class: str = None, 
             pattern_type: str = None, patterns: str = None):
    if gene_class is not None:
        if gene_class == "mitochondrion":
            adata.var["mt"] = adata.var_names.str.startswith(('MT-', 'Mt','mt-'))
            var_name = "mt"
        elif gene_class == "ribosomal":
            adata.var["ribo"] = adata.var_names.str.startswith(("RPS", "RPL"))
            var_name = "ribo"
        elif gene_class == "hemoglobin":
            adata.var["hb"] = adata.var_names.str.contains("^HB[^(P)]", case=False)
            var_name = "hb"
    
    if pattern_type is not None and patterns is not None:
        if pattern_type == "startswith":
            adata.var[var_name] = adata.var_names.str.startswith(patterns)
        elif pattern_type == "endswith":
            adata.var[var_name] = adata.var_names.str.endswith(patterns)
        elif pattern_type == "contains":
            adata.var[var_name] = adata.var_names.str.contains(patterns)
        else:
            raise ValueError(f"Did not support pattern_type: {pattern_type}")
    return {var_name: adata.var[var_name].value_counts().to_dict(), "msg": f"add '{var_name}' column  in adata.var"}


def list_var(adata):
    return list(adata.var.columns)

# Add list_obs function
def list_obs(adata):
    return list(adata.obs.columns)

# Add list_obs function
def check_gene(adata, var_names):
    return {v: v in adata.var_names for v in var_names}


def merge_adata(adata_dic, **kwargs):
    import anndata as ad
    adata =  ad.concat(adata_dic, **kwargs)
    return adata


util_func = {
    "mark_var": mark_var,
    "list_var": list_var,
    "list_obs": list_obs,
    "check_gene": check_gene,
    "merge_adata": merge_adata,
}

util_tools = {
    "mark_var": mark_var_tool,
    "list_var": list_var_tool,
    "list_obs": list_obs_tool,  
    "check_gene": check_gene_tool,
    "merge_adata": merge_adata_tool,
}

def run_util_func(adata, func, arguments):
    # pp_logger.info(f"{func} at {arguments}")
    if func not in util_func:
        raise ValueError(f"不支持的函数: {func}")
    run_func = util_func[func]
    parameters = inspect.signature(run_func).parameters
    kwargs = {k: arguments.get(k) for k in parameters if k in arguments}    
    try:
        res = run_func(adata, **kwargs)
        add_op_log(adata, run_func, kwargs)
    except Exception as e:
        logger.error(f"Error running function {func}: {e}")
        raise e
    return res
