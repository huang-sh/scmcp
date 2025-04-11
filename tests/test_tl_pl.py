import pytest
import numpy as np
import anndata
from scanpy_mcp.tool.pl import run_pl_func, pl_func
from scanpy_mcp.util import set_fig_path, add_op_log
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import os
import matplotlib.pyplot as plt


def test_run_pl_func():
    os.environ['SCANPY_MCP_TRANSPORT'] = "stdio"
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    
    # Test case 1: Successfully running pl_pca function
    mock_fig = MagicMock()
    mock_fig_path = Path("/data20T/dev/scanpy-mcp/scanpy-mcp/figures/pca.png")
    
    with patch.dict(pl_func, {"pl_pca": MagicMock(return_value=mock_fig)}):
        pl_func["pl_pca"].__name__ = "pl_pca"
        
        # Create a mock signature with specific parameters
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "color": MagicMock(),
            "use_raw": MagicMock(),
            "show": MagicMock(),
            "save": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with patch("scanpy_mcp.util.set_fig_path", return_value=mock_fig_path):
                with patch("scanpy_mcp.tool.pl.add_op_log"):
                    result = run_pl_func(adata, "pl_pca", {"color": "leiden", "use_raw": True})
                    
                    # Verify function was called with correct parameters
                    pl_func["pl_pca"].assert_called_once()
                    args, kwargs = pl_func["pl_pca"].call_args
                    assert args[0] is adata
                    assert kwargs.get("color") == "leiden"
                    assert kwargs.get("use_raw") is True
                    assert kwargs.get("show") is False
                    assert kwargs.get("save") == ".png"
                    
                    # Verify result
                    assert result.name == mock_fig_path.name
    
    # Test case 2: Successfully running pl_umap function
    mock_fig = MagicMock()
    # 使用模拟路径
    mock_fig_path = Path("/mock/path/to/figures/umap.png")
    
    with patch.dict(pl_func, {"pl_umap": MagicMock(return_value=mock_fig)}):
        pl_func["pl_umap"].__name__ = "pl_umap"
        
        # Create a mock signature
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "color": MagicMock(),
            "title": MagicMock(),  # Include title parameter
            "show": MagicMock(),
            "save": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            # 确保set_fig_path返回我们设置的模拟路径
            with patch("scanpy_mcp.util.set_fig_path", return_value=mock_fig_path):
                with patch("scanpy_mcp.tool.pl.add_op_log"):
                    result = run_pl_func(adata, "pl_umap", {"color": "leiden", "title": "UMAP Plot"})
                    
                    # Verify function was called with correct parameters
                    pl_func["pl_umap"].assert_called_once()
                    args, kwargs = pl_func["pl_umap"].call_args
                    assert args[0] is adata
                    assert kwargs.get("color") == "leiden"
                    assert kwargs.get("title") == "UMAP Plot"  # Title should be preserved
                    assert kwargs.get("show") is False
                    assert kwargs.get("save") == ".png"
                    
                    # Verify result
                    assert result.name == mock_fig_path.name
    
    # Test case 3: Error handling for unsupported function
    with pytest.raises(ValueError, match="Unsupported function: unsupported_func"):
        run_pl_func(adata, "unsupported_func", {})
    
    # Test case 4: Error handling for exceptions during plotting
    with patch.dict(pl_func, {"pl_violin": MagicMock(side_effect=Exception("Plotting error"))}):
        pl_func["pl_violin"].__name__ = "pl_violin"
        
        mock_signature = MagicMock()
        mock_parameters = {"adata": MagicMock(), "show": MagicMock(), "save": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with pytest.raises(Exception, match="Plotting error"):
                run_pl_func(adata, "pl_violin", {})



