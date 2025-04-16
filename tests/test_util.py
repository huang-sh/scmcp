from scmcp.util import add_op_log
from scmcp.tool.util import mark_var, list_var, list_obs, check_gene, merge_adata, run_util_func
import anndata
import numpy as np
from functools import partial
import pandas as pd


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


def test_mark_var():
    # Create a test AnnData object with gene names
    var_names = ['MT-1', 'MT-2', 'RPS1', 'RPL2', 'HBA1', 'GENE1']
    adata = anndata.AnnData(
        X=np.random.rand(3, len(var_names)),
        var=pd.DataFrame(index=var_names)
    )
    
    # Test mitochondrial gene marking
    result = mark_var(adata, gene_class="mitochondrion")
    assert "mt" in adata.var.columns
    assert adata.var["mt"].sum() == 2  # Two MT genes
    assert "mt" in result
    assert "msg" in result
    
    # Test ribosomal gene marking
    result = mark_var(adata, gene_class="ribosomal")
    assert "ribo" in adata.var.columns
    assert adata.var["ribo"].sum() == 2  # Two ribosomal genes
    
    # Test hemoglobin gene marking
    result = mark_var(adata, gene_class="hemoglobin")
    assert "hb" in adata.var.columns
    assert adata.var["hb"].sum() == 1  # One hemoglobin gene
    
    # Test custom pattern (startswith)
    result = mark_var(adata, var_name="custom_start", pattern_type="startswith", patterns="GE")
    assert "custom_start" in adata.var.columns
    assert adata.var["custom_start"].sum() == 1  # One gene starting with GE
    
    # Test custom pattern (contains)
    result = mark_var(adata, var_name="custom_contains", pattern_type="contains", patterns="PS")
    assert "custom_contains" in adata.var.columns
    assert adata.var["custom_contains"].sum() == 1  # One gene containing PS


def test_list_var():
    # Create a test AnnData object with var columns
    adata = anndata.AnnData(
        X=np.random.rand(3, 4),
        var=pd.DataFrame({
            "gene_type": ["protein_coding"] * 4,
            "chromosome": ["chr1"] * 4
        })
    )
    
    # Test listing var columns
    result = list_var(adata)
    assert isinstance(result, list)
    assert "gene_type" in result
    assert "chromosome" in result
    assert len(result) == 2


def test_list_obs():
    # Create a test AnnData object with obs columns
    adata = anndata.AnnData(
        X=np.random.rand(3, 4),
        obs=pd.DataFrame({
            "cell_type": ["T-cell"] * 3,
            "condition": ["control"] * 3
        })
    )
    
    # Test listing obs columns
    result = list_obs(adata)
    assert isinstance(result, list)
    assert "cell_type" in result
    assert "condition" in result
    assert len(result) == 2


def test_check_gene():
    # Create a test AnnData object with specific gene names
    var_names = ['GENE1', 'GENE2', 'GENE3']
    adata = anndata.AnnData(
        X=np.random.rand(3, len(var_names)),
        var=pd.DataFrame(index=var_names)
    )
    
    # Test checking existing and non-existing genes
    result = check_gene(adata, var_names=['GENE1', 'GENE4'])
    assert isinstance(result, dict)
    assert result['GENE1'] is True
    assert result['GENE4'] is False


def test_merge_adata():
    # Create two test AnnData objects
    adata1 = anndata.AnnData(
        X=np.random.rand(3, 4),
        obs=pd.DataFrame(index=['cell1', 'cell2', 'cell3']),
        var=pd.DataFrame(index=['gene1', 'gene2', 'gene3', 'gene4'])
    )
    
    adata2 = anndata.AnnData(
        X=np.random.rand(2, 4),
        obs=pd.DataFrame(index=['cell4', 'cell5']),
        var=pd.DataFrame(index=['gene1', 'gene2', 'gene3', 'gene4'])
    )
    
    # Test merging AnnData objects
    adata_dict = {'adata1': adata1, 'adata2': adata2}
    result = merge_adata(adata_dict)
    
    assert isinstance(result, anndata.AnnData)
    assert result.n_obs == 5  # 3 + 2 cells
    assert result.n_vars == 4  # Same genes


class MockAnnDataStore:
    def __init__(self):
        self.adata_dic = {}
        self.active = None


def test_run_util_func():
    # Create a mock AnnDataStore
    ads = MockAnnDataStore()
    
    # Create a test AnnData object
    var_names = ['MT-1', 'GENE1']
    adata = anndata.AnnData(
        X=np.random.rand(3, len(var_names)),
        var=pd.DataFrame(index=var_names)
    )
    
    # Set up the mock AnnDataStore
    ads.active = "test_adata"
    ads.adata_dic["test_adata"] = adata
    
    # Test running mark_var function
    result = run_util_func(ads, "mark_var", {"gene_class": "mitochondrion"})
    assert "mt" in result
    assert "msg" in result
    assert "mt" in ads.adata_dic["test_adata"].var.columns
    
    # Test running list_var function
    result = run_util_func(ads, "list_var", {})
    assert isinstance(result, list)
    assert "mt" in result
    
    # Test running check_gene function
    result = run_util_func(ads, "check_gene", {"var_names": ["MT-1", "NONEXISTENT"]})
    assert result["MT-1"] is True
    assert result["NONEXISTENT"] is False
    
    # Test running merge_adata function
    adata2 = anndata.AnnData(
        X=np.random.rand(2, len(var_names)),
        var=pd.DataFrame(index=var_names)
    )
    ads.adata_dic["test_adata2"] = adata2
    
    result = run_util_func(ads, "merge_adata", {})
    assert isinstance(result, anndata.AnnData)
    assert ads.active == "merge_adata"
    assert "merge_adata" in ads.adata_dic
    assert len(ads.adata_dic) == 1  # Only the merged adata remains
    assert ads.adata_dic["merge_adata"].n_obs == 5  # 3 + 2 cells
