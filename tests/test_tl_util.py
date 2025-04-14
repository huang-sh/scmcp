import pytest
import numpy as np
import anndata
from scmcp.tool.util import run_util_func, util_func
from unittest.mock import patch, MagicMock


def test_run_util_func():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata.var_names = ['gene1', 'MT-gene2']
    
    # Test case 1: Successfully running mark_var function
    result = run_util_func(adata, "mark_var", {"var_name": "mt_genes", "pattern_type": "startswith", "patterns": "MT-"})
    assert "mt_genes" in adata.var.columns
    assert result["msg"] == "add 'mt_genes' column  in adata.var"
    
    # Test case 2: Successfully running list_var function
    result = run_util_func(adata, "list_var", {})
    assert "mt_genes" in result
    
    # Test case 3: Successfully running check_gene function
    result = run_util_func(adata, "check_gene", {"var_names": ["gene1", "nonexistent_gene"]})
    assert result["gene1"] is True
    assert result["nonexistent_gene"] is False
    
    # Test case 4: Error handling for unsupported function
    with pytest.raises(ValueError, match="不支持的函数: unsupported_func"):
        run_util_func(adata, "unsupported_func", {})
    
    # Test case 5: Error handling for function execution errors
    mock_list_var = MagicMock(side_effect=Exception("Test error"))
    mock_list_var.__name__ = "list_var"  # 添加__name__属性
    with patch.dict(util_func, {"list_var": mock_list_var}):
        with pytest.raises(Exception, match="Test error"):
            run_util_func(adata, "list_var", {})
    
    # Test case 6: Verify that only valid parameters are passed to the function
    mock_mark_var = MagicMock(return_value={"msg": "success"})
    mock_mark_var.__name__ = "mark_var"  # 添加__name__属性
    
    # 创建一个模拟的inspect.signature对象，使其返回包含var_name参数的签名
    mock_signature = MagicMock()
    mock_parameters = {"adata": MagicMock(), "var_name": MagicMock()}
    mock_signature.parameters = mock_parameters
    
    with patch("inspect.signature", return_value=mock_signature):
        with patch.dict(util_func, {"mark_var": mock_mark_var}):
            run_util_func(adata, "mark_var", {"var_name": "test", "invalid_param": "value"})
            mock_mark_var.assert_called_once()
            # Check that invalid_param was not passed to the function
            args, kwargs = mock_mark_var.call_args
            assert "invalid_param" not in kwargs
            assert "var_name" in kwargs