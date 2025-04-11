from pathlib import Path

def add_op_log(adata, func, kwargs):
    if "operation" not in adata.uns:
        adata.uns["operation"] = {}
        adata.uns["operation"]["adata"] = []
    if hasattr(func, "__name__"):
        func_name = func.__name__
    else:
        func_name = func.func.__name__
    adata.uns["operation"]["adata"].append({func_name: kwargs})


def set_fig_path(func):
    fig_dir = Path(os.getcwd()) / "figures"
    fig_path = fig_dir / f"{func[3:]}.png"
    try:
        if func == "pl_rank_genes_groups_dotplot":
            os.rename(fig_dir/'dotplot_.png', fig_path)
        else:
            os.rename(fig_dir/f'{func[3:]}_.png', fig_path)
    except FileNotFoundError:
        print(f"The file {fig_dir/f'{func[3:]}_.png'} does not exist")
    except FileExistsError:
        print(f"The file {fig_path} already exists")
    except PermissionError:
        print("You don't have permission to rename this file")

    if os.environ.get("SCANPY_MCP_TRANSPORT") == "stdio":
        return fig_path
    else:
        host = os.environ.get("SCANPY_MCP_HOST")
        port = os.environ.get("SCANPY_MCP_PORT")
        fig_path = f"http://{host}:{port}/figures/{func[3:]}.png"
        return fig_path


from starlette.applications import Starlette
from starlette.responses import FileResponse, Response
from starlette.routing import Route
import os
from io import BytesIO
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("请安装Pillow: pip install pillow")


async def get_figure(request):
    figure_name = request.path_params["figure_name"]
    figure_path = f"./figures/{figure_name}"
    
    # 检查文件是否存在
    if not os.path.isfile(figure_path):
        return Response(content={"error": "figure not found"}, media_type="application/json")
    
    return FileResponse(figure_path)