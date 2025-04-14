import pytest
import numpy as np
import anndata
import os
from scmcp.tool.io import run_io_func, run_read_func, run_write_func, io_func, io_tools, read_text_func
from unittest.mock import patch, MagicMock, mock_open


def test_run_read_func():
    # Test case 1: Successfully reading h5ad file
    mock_adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    with patch.dict(io_func, {"read_h5ad": MagicMock(return_value=mock_adata)}):
        io_func["read_h5ad"].__name__ = "read_h5ad"
        
        # Create a mock signature
        mock_signature = MagicMock()
        mock_parameters = {
            "filename": MagicMock(),
            "backed": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            result = run_read_func("read_h5ad", {"filename": "test.h5ad", "backed": None})
            io_func["read_h5ad"].assert_called_once()
            args, kwargs = io_func["read_h5ad"].call_args
            assert kwargs.get("filename") == "test.h5ad"
            assert result is mock_adata
    
    # Test case 2: Error handling for unsupported function
    with pytest.raises(ValueError, match="不支持的函数: unsupported_func"):
        run_read_func("unsupported_func", {})
    
    # Test case 3: Error handling for exceptions during reading
    with patch.dict(io_func, {"read_10x_mtx": MagicMock(side_effect=Exception("File not found"))}):
        io_func["read_10x_mtx"].__name__ = "read_10x_mtx"
        
        mock_signature = MagicMock()
        mock_parameters = {"path": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with pytest.raises(ValueError, match="Running: File not found"):
                run_read_func("read_10x_mtx", {"path": "nonexistent_path"})


def test_run_write_func():
    # Create a test AnnData object
    adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata.uns["operation"] = {"adata": []}
    
    # Test case 1: Successfully writing h5ad file
    with patch.dict(io_func, {"write_h5ad": "write_h5ad"}):
        # Mock the inputSchema properties
        mock_schema = {"properties": {"filename": {}}}
        mock_tool = MagicMock()
        mock_tool.inputSchema = mock_schema
        
        with patch.dict(io_tools, {"write_h5ad": mock_tool}):
            result = run_write_func(adata, "write_h5ad", {"filename": "test_output.h5ad"})
            assert "operation" not in adata.uns
            assert result == {"filename": "test_output.h5ad", "msg": "success to save file"}
    
    # Test case 2: Successfully using write function
    with patch("scanpy.write") as mock_write:
        with patch.dict(io_func, {"write": mock_write}):
            # Mock the inputSchema properties
            mock_schema = {"properties": {"filename": {}}}
            mock_tool = MagicMock()
            mock_tool.inputSchema = mock_schema
            
            with patch.dict(io_tools, {"write": mock_tool}):
                result = run_write_func(adata, "write", {"filename": "test_output.h5"})
                mock_write.assert_called_once()
                args, kwargs = mock_write.call_args
                assert kwargs.get("adata") is adata
                assert kwargs.get("filename") == "test_output.h5"
                assert result == {"filename": "test_output.h5", "msg": "success to save file"}
    
    # Test case 3: Error handling for unsupported function
    with pytest.raises(ValueError, match="不支持的函数: unsupported_func"):
        run_write_func(adata, "unsupported_func", {})


def test_run_io_func():
    # Create a test AnnData object
    adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    
    # Test case 1: Calling write function
    with patch("scmcp.tool.io.run_write_func") as mock_write_func:
        mock_write_func.return_value = {"filename": "test.h5ad", "msg": "success"}
        result = run_io_func(adata, "write_h5ad", {"filename": "test.h5ad"})
        mock_write_func.assert_called_once_with(adata, "write_h5ad", {"filename": "test.h5ad"})
        assert result == {"filename": "test.h5ad", "msg": "success"}
    
    # Test case 2: Calling read function
    mock_adata = anndata.AnnData(X=np.array([[5, 6], [7, 8]]))
    with patch("scmcp.tool.io.run_read_func") as mock_read_func:
        mock_read_func.return_value = mock_adata
        result = run_io_func(None, "read_h5ad", {"filename": "test.h5ad"})
        mock_read_func.assert_called_once_with("read_h5ad", {"filename": "test.h5ad"})
        assert result is mock_adata


def test_read_text():
    file = os.path.join(os.path.dirname(__file__), "data", "test.txt")
    adata = read_text_func(file, delimiter="comma", first_column_names=True, first_column_obs=False) 
    assert "A1CF" in adata.var_names