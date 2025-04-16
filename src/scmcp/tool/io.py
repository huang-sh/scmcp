import os
import inspect
import mcp.types as types
import scanpy as sc
from pathlib import Path
from ..schema.io import *
from ..util import add_op_log
from ..logging_config import setup_logger



logger = setup_logger(log_file=os.environ.get("SCMCP_LOG_FILE", None))


read_tool = types.Tool(
    name="read_tool",
    description="Read data from various file formats (h5ad, 10x, text files, etc.) or directory path.",
    inputSchema=ReadModel.model_json_schema(),
)

write_tool = types.Tool(
    name="write_tool",
    description="Write AnnData objects to file.",
    inputSchema=WriteModel.model_json_schema(),
)


def read_func(**kwargs):
    file = Path(kwargs["filename"])
    if file.is_dir():
        kwargs["path"] = kwargs["filename"] 
        parameters = inspect.signature(sc.read_10x_mtx).parameters
        func_kwargs = {k: kwargs.get(k) for k in parameters if k in kwargs}
        adata = sc.read_10x_mtx(**func_kwargs)
    elif file.is_file():
        parameters = inspect.signature(sc.read).parameters
        func_kwargs = {k: kwargs.get(k) for k in parameters if k in kwargs}
        logger.info(func_kwargs)
        adata = sc.read(**func_kwargs)
        if not kwargs.get("first_column_obs", True):
            adata = adata.T
    else:
        adata = "there are no file"
    return adata


io_func = {
    "read_tool": read_func,
    "write_tool": sc.write,
}

io_tools = {
    "read_tool": read_tool,
    "write_tool": write_tool,
}


def write_func(adata, func, arguments):
    if func not in io_func:
        raise ValueError(f"不支持的函数: {func}")
    
    field_keys = io_tools.get(func).inputSchema["properties"].keys()
    kwargs = {k: arguments.get(k) for k in field_keys if k in arguments}

    kwargs["adata"] = adata
    sc.write(kwargs["filename"], adata)
    return {"filename": kwargs["filename"], "msg": "success to save file"}


def run_io_func(ads, func, arguments):
    if func == "read_tool":
        adata_id = f"adata{len(ads.adata_dic)}"
        if arguments.get("sampleid", None) is not None:
            adata_id = arguments["sampleid"]
        else:
            adata_id = f"adata{len(ads.adata_dic)}"
        res = read_func(**arguments)
        ads.active = adata_id
        ads.adata_dic[adata_id] = res
        return res
    else:
        adata = ads.adata_dic[ads.active]
        return write_func(adata, func, arguments)

