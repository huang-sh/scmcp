import pytest
import numpy as np
import anndata
import os
import scanpy as sc
from scmcp.tool.tl import run_tl_func, tl_func
from unittest.mock import patch, MagicMock


def test_run_tl_func():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    
    # Test case 1: Successfully running umap function
    with patch.dict(tl_func, {"umap": MagicMock()}):
        tl_func["umap"].__name__ = "umap"  # Add __name__ attribute for add_op_log
        
        # 创建一个模拟的signature对象，包含我们期望的参数
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "n_components": MagicMock(),
            "random_state": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_tl_func(adata, "umap", {"n_components": 2, "random_state": 42})
            tl_func["umap"].assert_called_once()
            args, kwargs = tl_func["umap"].call_args
            assert args[0] is adata
            assert kwargs.get("n_components") == 2
            assert kwargs.get("random_state") == 42
    
    # Test case 2: Successfully running leiden function
    with patch.dict(tl_func, {"leiden": MagicMock()}):
        tl_func["leiden"].__name__ = "leiden"
        
        # 同样为leiden函数创建模拟signature
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "resolution": MagicMock(),
            "random_state": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_tl_func(adata, "leiden", {"resolution": 0.8, "random_state": 42})
            tl_func["leiden"].assert_called_once()
            args, kwargs = tl_func["leiden"].call_args
            assert args[0] is adata
            assert kwargs.get("resolution") == 0.8
            assert kwargs.get("random_state") == 42
    
    # Test case 3: Error handling for unsupported function
    with pytest.raises(ValueError, match="Unsupported function: unsupported_func"):
        run_tl_func(adata, "unsupported_func", {})
    
    # Test case 4: Error handling for function execution errors
    with patch.dict(tl_func, {"tsne": MagicMock(side_effect=Exception("Test error"))}):
        tl_func["tsne"].__name__ = "tsne"
        with pytest.raises(Exception, match="Test error"):
            run_tl_func(adata, "tsne", {})
    
    # Test case 5: Verify that only valid parameters are passed to the function
    with patch.dict(tl_func, {"rank_genes_groups": MagicMock()}):
        tl_func["rank_genes_groups"].__name__ = "rank_genes_groups"
        
        # Create a mock signature with specific parameters
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "groupby": MagicMock(),
            "method": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_tl_func(adata, "rank_genes_groups", {
                "groupby": "leiden", 
                "method": "wilcoxon",
                "invalid_param": "value"
            })
            
            tl_func["rank_genes_groups"].assert_called_once()
            args, kwargs = tl_func["rank_genes_groups"].call_args
            assert args[0] is adata
            assert kwargs.get("groupby") == "leiden"
            assert kwargs.get("method") == "wilcoxon"
            assert "invalid_param" not in kwargs


def test_run_tl_func_with_real_data():
    """使用真实数据测试工具链函数"""
    # 加载测试数据
    data_path = os.path.join(os.path.dirname(__file__), "data", "hg19")
    adata = sc.read_10x_mtx(data_path)
    
    # 预处理数据，为后续分析做准备
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    sc.pp.pca(adata, n_comps=50)
    sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
    
    # 测试 umap 函数
    result = run_tl_func(adata, "umap", {"n_components": 2, "random_state": 42})
    assert result is None  # 函数应该返回None（原地修改）
    assert "X_umap" in adata.obsm
    
    # 测试 tsne 函数
    result = run_tl_func(adata, "tsne", {"n_pcs": 30, "random_state": 42})
    assert result is None
    assert "X_tsne" in adata.obsm
    
    # 测试 leiden 聚类
    result = run_tl_func(adata, "leiden", {"resolution": 0.5, "random_state": 42})
    assert result is None
    assert "leiden" in adata.obs.columns
    
    # 测试 rank_genes_groups 函数
    result = run_tl_func(adata, "rank_genes_groups", {
        "groupby": "leiden", 
        "method": "wilcoxon",
        "n_genes": 50
    })
    assert result is None
    assert "rank_genes_groups" in adata.uns
    
    # 测试 dendrogram 函数
    result = run_tl_func(adata, "dendrogram", {"groupby": "leiden"})
    assert result is None
    assert "dendrogram_leiden" in adata.uns