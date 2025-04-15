import os
from pathlib import Path
from starlette.responses import FileResponse, Response


def add_op_log(adata, func, kwargs):
    if "operation" not in adata.uns:
        adata.uns["operation"] = {}
        adata.uns["operation"]["adata"] = []
    if hasattr(func, "__name__"):
        func_name = func.__name__
    else:
        func_name = func.func.__name__
    adata.uns["operation"]["adata"].append({func_name: kwargs})


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







async def get_figure(request):
    figure_name = request.path_params["figure_name"]
    figure_path = f"./figures/{figure_name}"
    
    # 检查文件是否存在
    if not os.path.isfile(figure_path):
        return Response(content={"error": "figure not found"}, media_type="application/json")
    
    return FileResponse(figure_path)