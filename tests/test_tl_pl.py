import pytest
import numpy as np
import anndata
from scmcp.tool.pl import run_pl_func, pl_func
from scmcp.util import set_fig_path, add_op_log
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import os
import matplotlib.pyplot as plt


class MockAnnDataStore:
    def __init__(self, adata=None):
        self.adata_dic = {}
        self.active = "test_adata"
        if adata is not None:
            self.adata_dic[self.active] = adata


def test_run_pl_func():
    os.environ['SCMCP_TRANSPORT'] = "stdio"
    # Create a simple AnnData object for testing
    adata = anndata.AnnData(X=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    # Create a mock AnnDataStore with the test AnnData
    ads = MockAnnDataStore(adata)
    
    # Test case 1: Successfully running pl_pca function
    mock_fig = MagicMock()
    mock_fig_path = Path("./figures/pca.png")
    
    with patch.dict(pl_func, {"pl_pca": MagicMock(return_value=mock_fig)}):
        pl_func["pl_pca"].__name__ = "pl_pca"
        
        # Create a mock signature with specific parameters
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "color": MagicMock(),
            "use_raw": MagicMock(),
            "show": MagicMock(),
            "save": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with patch("scmcp.util.set_fig_path", return_value=mock_fig_path):
                with patch("scmcp.util.add_op_log"):
                    result = run_pl_func(ads, "pl_pca", {"color": "leiden", "use_raw": True})
                    
                    # Verify function was called with correct parameters
                    pl_func["pl_pca"].assert_called_once()
                    args, kwargs = pl_func["pl_pca"].call_args
                    assert args[0] is adata
                    assert kwargs.get("color") == "leiden"
                    assert kwargs.get("use_raw") is True
                    assert kwargs.get("show") is False
                    assert kwargs.get("save") == ".png"
                    

    
    # Test case 2: Successfully running pl_embedding function
    mock_fig = MagicMock()
    # Use a mock path
    mock_fig_path = Path("/mock/path/to/figures/embedding.png")
    
    with patch.dict(pl_func, {"pl_embedding": MagicMock(return_value=mock_fig)}):
        pl_func["pl_embedding"].__name__ = "pl_embedding"
        
        # Create a mock signature
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "basis": MagicMock(),
            "color": MagicMock(),
            "title": MagicMock(),  # Include title parameter
            "show": MagicMock(),
            "save": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            # Ensure set_fig_path returns our mock path
            with patch("scmcp.util.set_fig_path", return_value=mock_fig_path):
                with patch("scmcp.util.add_op_log"):
                    result = run_pl_func(ads, "pl_embedding", {
                        "basis": "umap", 
                        "color": "leiden", 
                        "title": "UMAP Plot"
                    })
                    
                    # Verify function was called with correct parameters
                    pl_func["pl_embedding"].assert_called_once()
                    args, kwargs = pl_func["pl_embedding"].call_args
                    assert args[0] is adata
                    assert kwargs.get("basis") == "umap"
                    assert kwargs.get("color") == "leiden"
                    assert kwargs.get("title") == "UMAP Plot"  # Title should be preserved
                    assert kwargs.get("show") is False
                    assert kwargs.get("save") == ".png"
                    

    
    # Test case 3: Error handling for unsupported function
    with pytest.raises(ValueError, match="Unsupported function: unsupported_func"):
        run_pl_func(ads, "unsupported_func", {})
    
    # Test case 4: Error handling for exceptions during plotting
    with patch.dict(pl_func, {"pl_violin": MagicMock(side_effect=Exception("Plotting error"))}):
        pl_func["pl_violin"].__name__ = "pl_violin"
        
        mock_signature = MagicMock()
        mock_parameters = {"adata": MagicMock(), "show": MagicMock(), "save": MagicMock()}
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            with pytest.raises(Exception, match="Plotting error"):
                run_pl_func(ads, "pl_violin", {})


def test_run_pl_func_with_multiple_adatas():
    # Test with multiple AnnData objects in the store
    adata1 = anndata.AnnData(X=np.array([[1, 2], [3, 4]]))
    adata2 = anndata.AnnData(X=np.array([[5, 6], [7, 8]]))
    
    # Create a mock AnnDataStore with multiple AnnData objects
    ads = MockAnnDataStore()
    ads.adata_dic["adata1"] = adata1
    ads.adata_dic["adata2"] = adata2
    ads.active = "adata2"  # Set active to adata2
    
    mock_fig = MagicMock()
    mock_fig_path = Path("./figures/scatter.png")
    
    with patch.dict(pl_func, {"pl_scatter": MagicMock(return_value=mock_fig)}):
        pl_func["pl_scatter"].__name__ = "pl_scatter"
        
        mock_signature = MagicMock()
        mock_parameters = {
            "adata": MagicMock(),
            "x": MagicMock(),
            "y": MagicMock(),
            "show": MagicMock(),
            "save": MagicMock()
        }
        mock_signature.parameters = mock_parameters
        
        with patch("inspect.signature", return_value=mock_signature):
            # Use patch.object to mock the set_fig_path function directly
            with patch("scmcp.tool.pl.set_fig_path", return_value=mock_fig_path):
                with patch("scmcp.tool.pl.add_op_log"):
                    result = run_pl_func(ads, "pl_scatter", {"x": "gene1", "y": "gene2"})
                    
                    # Verify function was called with the active AnnData (adata2)
                    pl_func["pl_scatter"].assert_called_once()
                    args, kwargs = pl_func["pl_scatter"].call_args
                    assert args[0] is adata2  # Should use the active AnnData
                    assert kwargs.get("x") == "gene1"
                    assert kwargs.get("y") == "gene2"
                    


def test_fig_to_bytes():
    from scmcp.tool.pl import fig_to_bytes
    
    # Create a simple matplotlib figure
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    
    # Test with a Figure object
    with patch("matplotlib.figure.Figure.savefig") as mock_savefig:
        fig_to_bytes(fig)
        mock_savefig.assert_called_once()
    
    # Test with an Axes object
    with patch("matplotlib.figure.Figure.savefig") as mock_savefig:
        fig_to_bytes(ax)
        mock_savefig.assert_called_once()
    
    # Test error handling
    with patch("matplotlib.figure.Figure.savefig", side_effect=Exception("Error saving figure")):
        with pytest.raises(Exception, match="Error saving figure"):
            fig_to_bytes(fig)
    
    plt.close(fig)  # Clean up

