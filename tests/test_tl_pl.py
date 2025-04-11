import pytest
import numpy as np
import anndata
from scanpy_mcp.tool.pl import run_pl_func, pl_func, fig_rename
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import os


def test_run_pl_func():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    
    # Test case 1: Successfully running pl_pca function
    mock_fig = MagicMock()
    mock_fig_path = Path("/path/to/figures/pca.png")
    
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
            with patch("scanpy_mcp.tool.pl.fig_rename", return_value=mock_fig_path):
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
                    assert result == mock_fig_path
    
    # Test case 2: Successfully running pl_umap function
    mock_fig = MagicMock()
    mock_fig_path = Path("/path/to/figures/umap.png")
    
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
            with patch("scanpy_mcp.tool.pl.fig_rename", return_value=mock_fig_path):
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
                    assert result == mock_fig_path
    
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


def test_fig_rename():
    # Test successful file rename
    with patch("os.getcwd", return_value="/path/to/project"):
        with patch("os.path.exists", return_value=True):
            with patch("os.rename") as mock_rename:
                with patch("pathlib.Path.exists", return_value=True):
                    result = fig_rename("pl_pca")
                    
                    # Verify rename was called with correct paths
                    expected_src = Path("/path/to/project/figures/pca_.png")
                    expected_dst = Path("/path/to/project/figures/pca.png")
                    mock_rename.assert_called_once_with(expected_src, expected_dst)
                    
                    # Verify result
                    assert result == expected_dst
    
    # Test handling of FileNotFoundError
    with patch("os.getcwd", return_value="/path/to/project"):
        with patch("os.rename", side_effect=FileNotFoundError):
            with patch("builtins.print") as mock_print:
                result = fig_rename("pl_umap")
                
                # Verify print was called with correct message
                mock_print.assert_called_once()
                assert "does not exist" in mock_print.call_args[0][0]
                
                # Verify result
                assert result == Path("/path/to/project/figures/umap.png")