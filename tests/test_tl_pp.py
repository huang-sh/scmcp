import pytest
import numpy as np
import anndata
import os
import scanpy as sc
from scanpy_mcp.tool.pp import run_pp_func, pp_func
from unittest.mock import patch, MagicMock


def test_run_pp_func():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    
    # Test case 1: Successfully running normalize_total function
    with patch.dict(pp_func, {"normalize_total": MagicMock()}):
        pp_func["normalize_total"].__name__ = "normalize_total"
        
        # Create a mock signature with specific parameters
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "target_sum": MagicMock(),
            "inplace": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_pp_func(adata, "normalize_total", {"target_sum": 1e4})
            pp_func["normalize_total"].assert_called_once()
            args, kwargs = pp_func["normalize_total"].call_args
            assert args[0] is adata
            assert kwargs.get("target_sum") == 1e4
            assert kwargs.get("inplace") is True
    
    # Test case 2: Successfully running highly_variable_genes function
    with patch.dict(pp_func, {"highly_variable_genes": MagicMock()}):
        pp_func["highly_variable_genes"].__name__ = "highly_variable_genes"
        
        # Create a mock signature
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "n_top_genes": MagicMock(),
            "flavor": MagicMock(),
            "inplace": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_pp_func(adata, "highly_variable_genes", {
                "n_top_genes": 2000, 
                "flavor": "seurat"
            })
            pp_func["highly_variable_genes"].assert_called_once()
            args, kwargs = pp_func["highly_variable_genes"].call_args
            assert args[0] is adata
            assert kwargs.get("n_top_genes") == 2000
            assert kwargs.get("flavor") == "seurat"
            assert kwargs.get("inplace") is True
    
    # Test case 3: Error handling for unsupported function
    with pytest.raises(ValueError, match="不支持的函数: unsupported_func"):
        run_pp_func(adata, "unsupported_func", {})
    
    # Test case 4: Error handling for KeyError
    with patch.dict(pp_func, {"filter_cells": MagicMock(side_effect=KeyError("test_col"))}):
        pp_func["filter_cells"].__name__ = "filter_cells"
        
        mock_signature = MagicMock()
        mock_parameters = {"adata": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with pytest.raises(KeyError, match="Can not foud \'test_col\' column in adata.obs or adata.var"):
                run_pp_func(adata, "filter_cells", {})
    
    # Test case 5: Error handling for general exceptions
    with patch.dict(pp_func, {"pca": MagicMock(side_effect=Exception("Test error"))}):
        pp_func["pca"].__name__ = "pca"
        
        mock_signature = MagicMock()
        mock_parameters = {"adata": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with pytest.raises(Exception, match="Test error"):
                run_pp_func(adata, "pca", {})
    
    # Test case 6: Verify that only valid parameters are passed to the function
    with patch.dict(pp_func, {"log1p": MagicMock()}):
        pp_func["log1p"].__name__ = "log1p"
        
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "base": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_pp_func(adata, "log1p", {
                "base": 10,
                "invalid_param": "value"
            })
            
            pp_func["log1p"].assert_called_once()
            args, kwargs = pp_func["log1p"].call_args
            assert args[0] is adata
            assert kwargs.get("base") == 10
            assert "invalid_param" not in kwargs


def test_run_pp_func_with_real_data():

    
    # 加载已有的测试数据
    adata = sc.read_10x_mtx("tests/data/hg19")
    
    # 测试 normalize_total 函数

    result = run_pp_func(adata, "normalize_total", {"target_sum": 1e4})
    assert result is None  # 函数应该返回None（原地修改）
    
    # 修改断言检查，适应实际的数据结构
    assert "operation" in adata.uns
    assert "adata" in adata.uns["operation"]
    assert any("normalize_total" in op for op in adata.uns["operation"]["adata"])
    

    # 先过滤掉NaN值
    run_pp_func(adata, "filter_cells", {"min_counts": 1})  # 过滤掉没有计数的细胞
    run_pp_func(adata, "filter_genes", {"min_cells": 1})   # 过滤掉没有表达的基因
    # 确保数据中没有NaN值
    adata.X = np.nan_to_num(adata.X)
    
    result = run_pp_func(adata, "log1p", {})
    assert result is None
    assert "operation" in adata.uns
    assert "adata" in adata.uns["operation"]
    assert any("log1p" in op for op in adata.uns["operation"]["adata"])
    
    result = run_pp_func(adata, "highly_variable_genes", {"n_top_genes": 500})
    assert result is None
    assert "operation" in adata.uns
    assert "adata" in adata.uns["operation"]
    assert any("highly_variable_genes" in op for op in adata.uns["operation"]["adata"])
    assert "highly_variable" in adata.var.columns
    

    result = run_pp_func(adata, "pca", {"n_comps": 20})
    assert result is None
    assert "operation" in adata.uns
    assert "adata" in adata.uns["operation"]
    assert any("pca" in op for op in adata.uns["operation"]["adata"])
    assert "X_pca" in adata.obsm
    
    result = run_pp_func(adata, "neighbors", {"n_neighbors": 15})
    assert result is None
    assert "operation" in adata.uns
    assert "adata" in adata.uns["operation"]
    assert any("neighbors" in op for op in adata.uns["operation"]["adata"])
    assert "neighbors" in adata.uns