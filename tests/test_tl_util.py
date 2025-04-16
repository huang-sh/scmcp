import pytest
import numpy as np
import anndata
from scmcp.tool.util import run_util_func, util_func
from unittest.mock import patch, MagicMock


class MockAnnDataStore:
    def __init__(self, adata=None):
        self.adata_dic = {}
        self.active = "test_adata"
        if adata is not None:
            self.adata_dic[self.active] = adata


def test_run_util_func():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata.var_names = ['gene1', 'MT-gene2']
    
    # Create a mock AnnDataStore with the test AnnData
    ads = MockAnnDataStore(adata)
    
    # Test case 1: Successfully running mark_var function
    result = run_util_func(ads, "mark_var", {"var_name": "mt_genes", "pattern_type": "startswith", "patterns": "MT-"})
    assert "mt_genes" in ads.adata_dic[ads.active].var.columns
    assert result["msg"] == "add 'mt_genes' column  in adata.var"
    
    # Test case 2: Successfully running list_var function
    result = run_util_func(ads, "list_var", {})
    assert "mt_genes" in result
    
    # Test case 3: Successfully running check_gene function
    result = run_util_func(ads, "check_gene", {"var_names": ["gene1", "nonexistent_gene"]})
    assert result["gene1"] is True
    assert result["nonexistent_gene"] is False
    
    # Test case 4: Error handling for unsupported function
    with pytest.raises(ValueError, match="不支持的函数: unsupported_func"):
        run_util_func(ads, "unsupported_func", {})
    
    # Test case 5: Error handling for function execution errors
    with patch.dict(util_func, {"list_var": MagicMock(side_effect=Exception("Test error"))}):
        util_func["list_var"].__name__ = "list_var"  # Add __name__ attribute
        with pytest.raises(Exception, match="Test error"):
            run_util_func(ads, "list_var", {})
    
    # Test case 6: Verify that only valid parameters are passed to the function
    with patch.dict(util_func, {"mark_var": MagicMock(return_value={"msg": "success"})}):
        util_func["mark_var"].__name__ = "mark_var"  # Add __name__ attribute
        
        # Create a mock inspect.signature object that returns a signature with var_name parameter
        mock_signature = MagicMock()
        mock_parameters = {"adata": MagicMock(), "var_name": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            run_util_func(ads, "mark_var", {"var_name": "test", "invalid_param": "value"})
            util_func["mark_var"].assert_called_once()
            # Check that invalid_param was not passed to the function
            args, kwargs = util_func["mark_var"].call_args
            assert args[0] is adata
            assert "invalid_param" not in kwargs
            assert "var_name" in kwargs


def test_run_util_func_with_multiple_adatas():
    # Test with multiple AnnData objects in the store
    adata1 = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata1.var_names = ['gene1', 'gene2']
    
    adata2 = anndata.AnnData(X=np.array([[5, 6], [7, 8]]))
    adata2.var_names = ['gene3', 'gene4']
    
    # Create a mock AnnDataStore with multiple AnnData objects
    ads = MockAnnDataStore()
    ads.adata_dic["adata1"] = adata1
    ads.adata_dic["adata2"] = adata2
    ads.active = "adata2"  # Set active to adata2
    
    # Test list_var on the active AnnData
    result = run_util_func(ads, "list_var", {})
    assert isinstance(result, list)
    assert len(result) == 0  # No columns in adata2.var initially
    
    # Test mark_var on the active AnnData
    result = run_util_func(ads, "mark_var", {"gene_class": "ribosomal"})
    assert "ribo" in ads.adata_dic["adata2"].var.columns
    
    # Test check_gene on the active AnnData
    result = run_util_func(ads, "check_gene", {"var_names": ["gene3", "gene1"]})
    assert result["gene3"] is True  # gene3 is in adata2
    assert result["gene1"] is False  # gene1 is not in adata2
    
    # Test merge_adata
    with patch("scmcp.tool.util.merge_adata", return_value=anndata.AnnData(X=np.array([[1, 2, 3, 4], [5, 6, 7, 8]]))):
        result = run_util_func(ads, "merge_adata", {})
        assert ads.active == "merge_adata"
        assert len(ads.adata_dic) == 1
        assert "merge_adata" in ads.adata_dic


def test_list_obs():
    # Create a simple AnnData object with obs columns
    adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata.obs["cluster"] = ["A", "B"]
    adata.obs["condition"] = ["control", "treatment"]
    
    # Create a mock AnnDataStore with the test AnnData
    ads = MockAnnDataStore(adata)
    
    # Test list_obs function
    result = run_util_func(ads, "list_obs", {})
    assert isinstance(result, list)
    assert "cluster" in result
    assert "condition" in result
    assert len(result) == 2