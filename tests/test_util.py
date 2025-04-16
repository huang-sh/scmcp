from scmcp.util import add_op_log
import anndata
import numpy as np
from functools import partial


def test_add_op_log():
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    
    # Test case 1: Adding operation log when there's no initial record
    def test_func1():
        pass
    
    add_op_log(adata, test_func1, {"param1": "value1"})
    
    # Verify operation record is correctly created
    assert "operation" in adata.uns
    assert "adata" in adata.uns["operation"]
    assert len(adata.uns["operation"]["adata"]) == 1
    assert "0" in adata.uns["operation"]["adata"]
    assert "test_func1" in adata.uns["operation"]["adata"]["0"]
    assert adata.uns["operation"]["adata"]["0"]["test_func1"] == {"param1": "value1"}
    
    # Test case 2: Adding operation log when there's existing record
    def test_func2():
        pass
    
    add_op_log(adata, test_func2, {"param2": "value2"})
    
    # Verify new operation record is correctly added
    assert len(adata.uns["operation"]["adata"]) == 2
    assert "1" in adata.uns["operation"]["adata"]
    assert "test_func2" in adata.uns["operation"]["adata"]["1"]
    assert adata.uns["operation"]["adata"]["1"]["test_func2"] == {"param2": "value2"}
    
    # Test case 3: Using partial function
    test_partial = partial(test_func1, extra_arg="value")
    add_op_log(adata, test_partial, {"param3": "value3"})
    
    # Verify operation record is correctly added when using partial function
    assert len(adata.uns["operation"]["adata"]) == 3
    assert "2" in adata.uns["operation"]["adata"]
    assert "test_func1" in adata.uns["operation"]["adata"]["2"]
    assert adata.uns["operation"]["adata"]["2"]["test_func1"] == {"param3": "value3"}
