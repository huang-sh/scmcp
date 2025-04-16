import mcp.types as types
from ..schema.ccc import *
import liana as li
import inspect
from pathlib import Path
import os
from ..util import add_op_log
from ..logging_config import setup_logger


logger = setup_logger(log_file=os.environ.get("SCMCP_LOG_FILE", None))


# Add list_obs tool
ls_ccc_method_tool = types.Tool(
    name="ls_ccc_method",
    description="List cell-cell communication method.",
    inputSchema=ListCCCMethodModel.model_json_schema(),
)

# Add rank_aggregate tool
rank_aggregate_tool = types.Tool(
    name="ccc_rank_aggregate",
    description="Get an aggregate of ligand-receptor scores from multiple  Cell-cell communication methods. ",
    inputSchema=RankAggregateModel.model_json_schema(),
)

# Add circle_plot tool
circle_plot_tool = types.Tool(
    name="ccc_circle_plot",
    description="Visualize cell-cell communication network using a circular plot.",
    inputSchema=CirclePlotModel.model_json_schema(),
)

# Add dot_plot tool
dot_plot_tool = types.Tool(
    name="ccc_dot_plot",
    description="Visualize cell-cell communication interactions using a dotplot.",
    inputSchema=DotPlotModel.model_json_schema(),
)

# Add general CCC tool
ccc_tool = types.Tool(
    name="ccc",
    description="Cell-cell communication analysis with one method (cellphonedb, cellchat,connectome, natmi, etc.)",
    inputSchema=CCCModel.model_json_schema(),
)

def ls_ccc_method():
    return str(li.mt.show_methods())


def run_ccc(adata, method, **kwargs):
    """Run cell-cell communication analysis with the specified method."""
    method_func = getattr(li.mt, method)
    parameters = inspect.signature(method_func).parameters
    filtered_kwargs = {k: kwargs.get(k) for k in parameters if k in kwargs}
    # filtered_kwargs["key_added"] = f"{method}_res"
    method_func(adata, **filtered_kwargs)
    add_op_log(adata, method_func, filtered_kwargs)
    return adata


def plot_circleplot(adata, **kwargs):
    pval = kwargs.pop("specificity_cutoff", 0.05)
    res_key = kwargs.get("uns_key", "liana_res")
    pval_col = adata.uns[res_key].columns[-1]
    kwargs["filter_fun"] = lambda x: x[pval_col] <= pval
    parameters = inspect.signature( li.pl.circle_plot).parameters
    kwargs = {k: kwargs.get(k) for k in parameters if k in kwargs}    
    ax = li.pl.circle_plot(adata, **kwargs)
    return ax


def plot_dotplot(adata, **kwargs):
    pval = kwargs.pop("specificity_cutoff", 0.05)
    res_key = kwargs.get("uns_key", "liana_res")
    pval_col = adata.uns[res_key].columns[-1]
    kwargs["filter_fun"] = lambda x: x[pval_col] <= pval

    if kwargs.get("colour", None) is None:
        kwargs["colour"] = adata.uns[res_key].columns[-2]
    if kwargs.get("size", None) is None:
        kwargs["size"] = adata.uns[res_key].columns[-1]        

    parameters = inspect.signature(li.pl.dotplot).parameters
    kwargs = {k: kwargs.get(k) for k in parameters if k in kwargs}    
    fig = li.pl.dotplot(adata, **kwargs)
    return fig


ccc_func = {
    "ls_ccc_method": ls_ccc_method,
    "ccc_rank_aggregate": li.mt.rank_aggregate,
    "ccc_circle_plot": plot_circleplot,
    "ccc_dot_plot": plot_dotplot,
    "ccc": run_ccc,
}

ccc_tools = {
    "ls_ccc_method": ls_ccc_method_tool,
    "ccc_rank_aggregate": rank_aggregate_tool,
    "ccc_circle_plot": circle_plot_tool,
    "ccc_dot_plot": dot_plot_tool,
    "ccc": ccc_tool,
}


def run_ccc_func(ads, func, arguments):
    
    if func not in ccc_func:
        raise ValueError(f"不支持的函数: {func}")
    run_func = ccc_func[func]
    adata = ads.adata_dic[ads.active]
    try:
        logger.info(f"Running function {func} with arguments {arguments}")
        
        if func == "ls_ccc_method":
            res = run_func()
        elif func == "ccc":
            # Extract method from arguments and pass remaining args
            method = arguments.get("method", "cellphonedb")
            method_args = {k: v for k, v in arguments.items() if k != "method"}
            res = run_func(adata, method, **method_args)
            
        elif "plot" in func:
            from ..util import savefig
            ax = run_func(adata, **arguments)
            fig_path = Path(os.getcwd()) / f"figures/{func}.png"
            res = savefig(ax, fig_path, format="png")
            add_op_log(adata, run_func, arguments)  # 
        else:   
            parameters = inspect.signature(run_func).parameters
            kwargs = {k: arguments.get(k) for k in parameters if k in arguments}
            res = run_func(adata, **kwargs)
            add_op_log(adata, run_func, kwargs)
        return res
    except Exception as e:
        logger.error(f"Error running function {func}: {e}")
        raise e
