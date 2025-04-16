import os
from pathlib import Path
from starlette.responses import FileResponse, Response


def add_op_log(adata, func, kwargs):
    if "operation" not in adata.uns:
        adata.uns["operation"] = {}
        adata.uns["operation"]["adata"] = {}
    
    # Handle different function types to get the function name
    if hasattr(func, "func") and hasattr(func.func, "__name__"):
        # For partial functions, use the original function name
        func_name = func.func.__name__
    elif hasattr(func, "__name__"):
        func_name = func.__name__
    elif hasattr(func, "__class__"):
        func_name = func.__class__.__name__
    else:
        # Fallback for other cases
        func_name = str(func)
    if not adata.uns["operation"]["adata"]:
        op_num = "0"
    else:
        op_num = str(int(list(adata.uns["operation"]["adata"].keys())[-1])+1)
    adata.uns["operation"]["adata"][op_num] = {func_name: kwargs}


def set_fig_path(func, **kwargs):
    fig_dir = Path(os.getcwd()) / "figures"

    if func == "pl_rank_genes_groups_dotplot":
        old_path = fig_dir / 'dotplot_.png'
        fig_path = fig_dir / f"{func[3:]}.png"
    elif func in ["pl_scatter", "pl_embedding"]:
        if "basis" in kwargs and kwargs['basis'] is not None:
            old_path = fig_dir / f"{kwargs['basis']}.png"
            fig_path = fig_dir / f"{func[3:]}_{kwargs['basis']}.png"
    else:
        old_path = fig_dir / f"{func[3:]}_.png"
        fig_path = fig_dir / f"{func[3:]}.png"        
    try:
        os.rename(old_path, fig_path)
    except FileNotFoundError:
        print(f"The file {old_path} does not exist")
    except FileExistsError:
        print(f"The file {fig_path} already exists")
    except PermissionError:
        print("You don't have permission to rename this file")

    if os.environ.get("SCMCP_TRANSPORT") == "stdio":
        return fig_path
    else:
        host = os.environ.get("SCMCP_HOST")
        port = os.environ.get("SCMCP_PORT")
        fig_path = f"http://{host}:{port}/figures/{Path(fig_path).name}"
        return fig_path


def savefig(fig, file, format="png"):
    try:
        # 确保父目录存在
        file_path = Path(file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if hasattr(fig, 'figure'):  # if Axes
            fig.figure.savefig(file, format=format)
        elif hasattr(fig, 'save'):  # for plotnine.ggplot.ggplot
            fig.save(file, format=format)
        else:  # if Figure 
            fig.savefig(file, format=format)
        return file
    except Exception as e:
        raise e





async def get_figure(request):
    figure_name = request.path_params["figure_name"]
    figure_path = f"./figures/{figure_name}"
    
    # 检查文件是否存在
    if not os.path.isfile(figure_path):
        return Response(content={"error": "figure not found"}, media_type="application/json")
    
    return FileResponse(figure_path)