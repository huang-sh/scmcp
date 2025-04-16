import pytest
import numpy as np
import anndata
import os
import scanpy as sc
from scmcp.tool.tl import run_tl_func, tl_func
from unittest.mock import patch, MagicMock


class MockAnnDataStore:
    def __init__(self, adata=None):
        self.adata_dic = {}
        self.active = "test_adata"
        if adata is not None:
            self.adata_dic[self.active] = adata


def test_run_tl_func():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    # Create a mock AnnDataStore with the test AnnData
    ads = MockAnnDataStore(adata)
    
    # Test case 1: Successfully running umap function
    with patch.dict(tl_func, {"umap": MagicMock()}):
        tl_func["umap"].__name__ = "umap"  # Add __name__ attribute for add_op_log
        
        # Create a mock signature object with expected parameters
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "n_components": MagicMock(),
            "random_state": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_tl_func(ads, "umap", {"n_components": 2, "random_state": 42})
            tl_func["umap"].assert_called_once()
            args, kwargs = tl_func["umap"].call_args
            assert args[0] is adata
            assert kwargs.get("n_components") == 2
            assert kwargs.get("random_state") == 42
    
    # Test case 2: Successfully running leiden function
    with patch.dict(tl_func, {"leiden": MagicMock()}):
        tl_func["leiden"].__name__ = "leiden"
        
        # Create mock signature for leiden function
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "resolution": MagicMock(),
            "random_state": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_tl_func(ads, "leiden", {"resolution": 0.8, "random_state": 42})
            tl_func["leiden"].assert_called_once()
            args, kwargs = tl_func["leiden"].call_args
            assert args[0] is adata
            assert kwargs.get("resolution") == 0.8
            assert kwargs.get("random_state") == 42
    
    # Test case 3: Error handling for unsupported function
    with pytest.raises(ValueError, match="Unsupported function: unsupported_func"):
        run_tl_func(ads, "unsupported_func", {})
    
    # Test case 4: Error handling for function execution errors
    with patch.dict(tl_func, {"tsne": MagicMock(side_effect=Exception("Test error"))}):
        tl_func["tsne"].__name__ = "tsne"
        with pytest.raises(Exception, match="Test error"):
            run_tl_func(ads, "tsne", {})
    
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
            run_tl_func(ads, "rank_genes_groups", {
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


def test_run_tl_func_with_multiple_adatas():
    # Test with multiple AnnData objects in the store
    adata1 = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata2 = anndata.AnnData(X=np.array([[5, 6], [7, 8]]))
    
    # Create a mock AnnDataStore with multiple AnnData objects
    ads = MockAnnDataStore()
    ads.adata_dic["adata1"] = adata1
    ads.adata_dic["adata2"] = adata2
    ads.active = "adata2"  # Set active to adata2
    
    with patch.dict(tl_func, {"leiden": MagicMock()}):
        tl_func["leiden"].__name__ = "leiden"
        
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "resolution": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with patch("scmcp.util.add_op_log"):
                run_tl_func(ads, "leiden", {"resolution": 0.5})
                
                # Verify function was called with the active AnnData (adata2)
                tl_func["leiden"].assert_called_once()
                args, kwargs = tl_func["leiden"].call_args
                assert args[0] is adata2  # Should use the active AnnData
                assert kwargs.get("resolution") == 0.5


@pytest.mark.skip(reason="Requires real data and takes time to run")
def test_run_tl_func_with_real_data():
    """Test tool chain functions with real data"""
    # Load test data
    data_path = os.path.join(os.path.dirname(__file__), "data", "hg19")
    adata = sc.read_10x_mtx(data_path)
    
    # Create a mock AnnDataStore with the test AnnData
    ads = MockAnnDataStore(adata)
    
    # Preprocess data for subsequent analysis
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    sc.pp.pca(adata, n_comps=50)
    sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
    
    # Test umap function
    run_tl_func(ads, "umap", {"n_components": 2, "random_state": 42})
    assert "X_umap" in adata.obsm
    
    # Test tsne function
    run_tl_func(ads, "tsne", {"n_pcs": 30, "random_state": 42})
    assert "X_tsne" in adata.obsm
    
    # Test leiden clustering
    run_tl_func(ads, "leiden", {"resolution": 0.5, "random_state": 42})
    assert "leiden" in adata.obs.columns
    
    # Test rank_genes_groups function
    run_tl_func(ads, "rank_genes_groups", {
        "groupby": "leiden", 
        "method": "wilcoxon",
        "n_genes": 50
    })
    assert "rank_genes_groups" in adata.uns
    
    # Test dendrogram function
    run_tl_func(ads, "dendrogram", {"groupby": "leiden"})
    assert "dendrogram_leiden" in adata.uns