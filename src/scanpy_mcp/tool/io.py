import os
import inspect
import mcp.types as types
import scanpy as sc
from ..schema.io import *
from ..util import add_op_log
from ..logging_config import setup_logger



logger = setup_logger(log_file=os.environ.get("SCANPY_MCP_LOG_FILE", None))

read_h5ad = types.Tool(
    name="read_h5ad",
    description="Read .h5ad-formatted hdf5 file",
    inputSchema=ReadH5adInput.model_json_schema(),
)

read_10x_mtx = types.Tool(
    name="read_10x_mtx",
    description="Read 10x-Genomics-formatted mtx directory.",
    inputSchema=Read10xMtxInput.model_json_schema(),
)

read_10x_h5 = types.Tool(
    name="read_10x_h5",
    description="Read 10x-Genomics-formatted hdf5 file",
    inputSchema=Read10xH5Input.model_json_schema(),
)

read_text = types.Tool(
    name="read_text",
    description="Read gene expression from  .txt, .csv, .tsv file.",
    inputSchema=ReadTextInput.model_json_schema(),
)

write_h5ad = types.Tool(
    name="write_h5ad",
    description="Write AnnData objects inot .h5ad-formatted hdf5 file",
    inputSchema=WriteH5adModel.model_json_schema(),
)

write = types.Tool(
    name="write",
    description="Write AnnData objects to file.",
    inputSchema=WriteModel.model_json_schema(),
)


def read_text_func(filename, delimiter=None, first_column_names=None, first_column_obs=True):
    """
    Read text file and optionally transpose the data
    
    Args:
        filename: Path to the text file
        delimiter: Delimiter that separates data
        first_column_names: Assume the first column stores row names
        first_column_obs: If False, transpose the data

    Returns:
        AnnData object
    """
    if delimiter == "comma":
        delimiter = ","
    elif delimiter == "tab":
        delimiter = "\t"
    elif delimiter == "space":
        delimiter = " "
    elif delimiter == "semicolon":
        delimiter = ";"
    elif delimiter == "colon":
        delimiter = ":"
    else:
        delimiter = None
    try:
        logger.info(f"sc.read_text({filename}, delimiter={delimiter}, first_column_names={first_column_names})")
        adata = sc.read_text(filename, delimiter=delimiter, first_column_names=first_column_names)
    except Exception as e:
        logger.error(f"Error converting figure to bytes: {e}")
    if not first_column_obs:
        adata = adata.T
    return adata


io_func = {
    "read_10x_mtx": sc.read_10x_mtx,
    "read_10x_h5": sc.read_10x_h5,
    "read_h5ad": sc.read_h5ad,
    "read_text": read_text_func,
    "write": sc.write,
    "write_h5ad": "write_h5ad",
}

io_tools = {
    "read_h5ad": read_h5ad,
    "read_10x_h5": read_10x_h5,
    "read_10x_mtx": read_10x_mtx,
    "read_text": read_text,
    "write_h5ad": write_h5ad,
    "write": write,
}

def run_read_func(func, arguments):
    """
    根据函数名和参数执行相应的IO函数
    
    Args:
        func: 函数名称，如 'read_h5ad'
        arguments: 包含参数的字典
    
    Returns:
        AnnData 对象
    """
    if func not in io_func:
        raise ValueError(f"不支持的函数: {func}")
    
    run_func = io_func[func]
    parameters = inspect.signature(run_func).parameters
    kwargs = {k: arguments.get(k) for k in parameters if k in arguments}
    try:        
        adata = run_func(**kwargs)
        add_op_log(adata, run_func, kwargs)
    except Exception as e:
        raise ValueError(f"Running: {str(e)}")
    return adata


def run_write_func(adata, func, arguments):
    if func not in io_func:
        raise ValueError(f"不支持的函数: {func}")
    
    field_keys = io_tools.get(func).inputSchema["properties"].keys()
    kwargs = {k: arguments.get(k) for k in field_keys if k in arguments}
    
    if func == "write_h5ad":
        del adata.uns["operation"]
        return {"filename": kwargs["filename"], "msg": "success to save file"}
    else:
        kwargs["adata"] = adata
        sc.write(**kwargs)
        return {"filename": kwargs["filename"], "msg": "success to save file"}


def run_io_func(adata, func, arguments):
    if func.startswith("write"):
        return run_write_func(adata, func, arguments)
    else:
        return run_read_func(func, arguments)
