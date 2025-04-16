import pytest
import numpy as np
import anndata
import os
import scanpy as sc
from scmcp.tool.pp import run_pp_func, pp_func
from unittest.mock import patch, MagicMock


class MockAnnDataStore:
    def __init__(self, adata=None):
        self.adata_dic = {}
        self.active = "test_adata"
        if adata is not None:
            self.adata_dic[self.active] = adata


def test_run_pp_func():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    # Create a mock AnnDataStore with the test AnnData
    ads = MockAnnDataStore(adata)
    
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
            run_pp_func(ads, "normalize_total", {"target_sum": 1e4})
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
            run_pp_func(ads, "highly_variable_genes", {
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
        run_pp_func(ads, "unsupported_func", {})
    
    # Test case 4: Error handling for KeyError
    with patch.dict(pp_func, {"filter_cells": MagicMock(side_effect=KeyError("test_col"))}):
        pp_func["filter_cells"].__name__ = "filter_cells"
        
        mock_signature = MagicMock()
        mock_parameters = {"adata": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with pytest.raises(KeyError, match="Can not foud \'test_col\' column in adata.obs or adata.var"):
                run_pp_func(ads, "filter_cells", {})
    
    # Test case 5: Error handling for general exceptions
    with patch.dict(pp_func, {"pca": MagicMock(side_effect=Exception("Test error"))}):
        pp_func["pca"].__name__ = "pca"
        
        mock_signature = MagicMock()
        mock_parameters = {"adata": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with pytest.raises(Exception, match="Test error"):
                run_pp_func(ads, "pca", {})
    
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
            run_pp_func(ads, "log1p", {
                "base": 10,
                "invalid_param": "value"
            })
            
            pp_func["log1p"].assert_called_once()
            args, kwargs = pp_func["log1p"].call_args
            assert args[0] is adata
            assert kwargs.get("base") == 10
            assert "invalid_param" not in kwargs


def test_run_pp_func_with_multiple_adatas():
    # Test with multiple AnnData objects in the store
    adata1 = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata2 = anndata.AnnData(X=np.array([[5, 6], [7, 8]]))
    
    # Create a mock AnnDataStore with multiple AnnData objects
    ads = MockAnnDataStore()
    ads.adata_dic["adata1"] = adata1
    ads.adata_dic["adata2"] = adata2
    ads.active = "adata2"  # Set active to adata2
    
    with patch.dict(pp_func, {"normalize_total": MagicMock()}):
        pp_func["normalize_total"].__name__ = "normalize_total"
        
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "target_sum": MagicMock(),
            "inplace": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_pp_func(ads, "normalize_total", {"target_sum": 1e4})
            
            # Verify function was called with the active AnnData (adata2)
            pp_func["normalize_total"].assert_called_once()
            args, kwargs = pp_func["normalize_total"].call_args
            assert args[0] is adata2  # Should use the active AnnData
            assert kwargs.get("target_sum") == 1e4
            assert kwargs.get("inplace") is True


@pytest.mark.skip(reason="Requires real data and takes time to run")
def test_run_pp_func_with_real_data():
    # Load test data
    adata = sc.read_10x_mtx(os.path.join(os.path.dirname(__file__), "data", "hg19"))
    # Create a mock AnnDataStore with the test AnnData
    ads = MockAnnDataStore(adata)
    
    # Test normalize_total function
    result = run_pp_func(ads, "normalize_total", {"target_sum": 1e4})
    assert result is None  # Function should return None (in-place modification)
    
    # Filter out NaN values
    run_pp_func(ads, "filter_cells", {"min_counts": 1})  # Filter cells with no counts
    run_pp_func(ads, "filter_genes", {"min_cells": 1})   # Filter genes with no expression
    # Ensure data has no NaN values
    ads.adata_dic[ads.active].X = np.nan_to_num(ads.adata_dic[ads.active].X)
    
    result = run_pp_func(ads, "log1p", {})
    assert result is None
    
    result = run_pp_func(ads, "highly_variable_genes", {"n_top_genes": 500})
    assert result is None
    assert "highly_variable" in ads.adata_dic[ads.active].var.columns
    
    result = run_pp_func(ads, "pca", {"n_comps": 20})
    assert result is None
    assert "X_pca" in ads.adata_dic[ads.active].obsm
    
    result = run_pp_func(ads, "neighbors", {"n_neighbors": 15})
    assert result is None
    assert "neighbors" in ads.adata_dic[ads.active].uns