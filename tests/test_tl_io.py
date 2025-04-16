import pytest
import numpy as np
import anndata
import os
from pathlib import Path
from scmcp.tool.io import run_io_func, read_func, write_func, io_func, io_tools
from unittest.mock import patch, MagicMock, mock_open


class MockAnnDataStore:
    def __init__(self):
        self.adata_dic = {}
        self.active = None


def test_read_func():
    # Test case 1: Reading a directory (10x mtx format)
    with patch('pathlib.Path.is_dir', return_value=True), \
         patch('pathlib.Path.is_file', return_value=False), \
         patch('scanpy.read_10x_mtx') as mock_read_10x:
        
        mock_adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
        mock_read_10x.return_value = mock_adata
        
        result = read_func(filename="test_dir")
        mock_read_10x.assert_called_once()
        assert result is mock_adata
    
    # Test case 2: Reading a file
    with patch('pathlib.Path.is_dir', return_value=False), \
         patch('pathlib.Path.is_file', return_value=True), \
         patch('scanpy.read') as mock_read:
        
        mock_adata = anndata.AnnData(X=np.array([[5, 6], [7, 8]]))
        mock_read.return_value = mock_adata
        
        result = read_func(filename="test.h5ad")
        mock_read.assert_called_once()
        assert result is mock_adata
    
    # Test case 3: File not found
    with patch('pathlib.Path.is_dir', return_value=False), \
         patch('pathlib.Path.is_file', return_value=False):
        
        result = read_func(filename="nonexistent_file")
        assert result == "there are no file"


def test_write_func():
    # Create a test AnnData object
    adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    
    with patch('scanpy.write') as mock_write, \
         patch.dict(io_tools, {"write_tool": MagicMock()}):
        
        # Mock the inputSchema
        io_tools["write_tool"].inputSchema = {"properties": {"filename": {}}}
        
        result = write_func(adata, "write_tool", {"filename": "test.h5ad"})
        mock_write.assert_called_once_with("test.h5ad", adata)
        assert result["msg"] == "success to save file"


def test_run_io_func():
    # Create a mock AnnDataStore
    ads = MockAnnDataStore()
    
    # Test case 1: Reading a file
    with patch('scmcp.tool.io.read_func') as mock_read_func:
        mock_adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
        mock_read_func.return_value = mock_adata
        
        result = run_io_func(ads, "read_tool", {"filename": "test.h5ad"})
        mock_read_func.assert_called_once_with(filename="test.h5ad")
        assert result is mock_adata
        assert ads.active == "adata0"
        assert ads.adata_dic["adata0"] is mock_adata
    
    # Test case 2: Reading a file with sampleid
    ads = MockAnnDataStore()
    with patch('scmcp.tool.io.read_func') as mock_read_func:
        mock_adata = anndata.AnnData(X=np.array([[5, 6], [7, 8]]))
        mock_read_func.return_value = mock_adata
        
        result = run_io_func(ads, "read_tool", {"filename": "test.h5ad", "sampleid": "sample1"})
        mock_read_func.assert_called_once_with(filename="test.h5ad", sampleid="sample1")
        assert result is mock_adata
        assert ads.active == "sample1"
        assert ads.adata_dic["sample1"] is mock_adata
    
    # Test case 3: Writing a file
    ads = MockAnnDataStore()
    mock_adata = anndata.AnnData(X=np.array([[9, 10], [11, 12]]))
    ads.adata_dic["active_sample"] = mock_adata
    ads.active = "active_sample"
    
    with patch('scmcp.tool.io.write_func') as mock_write_func:
        mock_write_func.return_value = {"filename": "test.h5ad", "msg": "success"}
        
        result = run_io_func(ads, "write_tool", {"filename": "test.h5ad"})
        mock_write_func.assert_called_once_with(mock_adata, "write_tool", {"filename": "test.h5ad"})
        assert result == {"filename": "test.h5ad", "msg": "success"}