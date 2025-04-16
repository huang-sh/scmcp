
from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
    model_validator,
)
from typing import Optional, Union, List, Dict, Any, Callable, Collection
from typing import Literal
from .base import JSONParsingModel


class MarkVarModel(JSONParsingModel):
    """Determine or mark if each gene meets specific conditions and store results in adata.var as boolean values"""
    
    var_name: str = Field(
        default=None,
        description="Column name that will be added to adata.var, do not set if user does not ask"
    )
    pattern_type: Optional[Literal["startswith", "endswith", "contains"]] = Field(
        default=None,
        description="Pattern matching type (startswith/endswith/contains), it should be None when gene_class is not None"
    )    
    patterns: str = Field(
        default=None,
        description="gene pattern to match, must be a string, it should be None when gene_class is not None"
    )
    
    gene_class: Optional[Literal["mitochondrion", "ribosomal", "hemoglobin"]] = Field(
        default=None,
        description="Gene class type (Mitochondrion/Ribosomal/Hemoglobin)"
    )


class ListVarModel(JSONParsingModel):
    """ListVarModel"""    
    pass

class ListObsModel(JSONParsingModel):
    """ListObsModel"""    
    pass    

class VarNamesModel(JSONParsingModel):
    """ListObsModel"""    
    var_names: List[str] = Field(
            default=None,
            description="gene names."
        )


class ConcatAdataModel(JSONParsingModel):
    """Model for concatenating AnnData objects"""
    
    axis: Literal['obs', 0, 'var', 1] = Field(
        default='obs',
        description="Which axis to concatenate along. 'obs' or 0 for observations, 'var' or 1 for variables."
    )
    join: Literal['inner', 'outer'] = Field(
        default='inner',
        description="How to align values when concatenating. If 'outer', the union of the other axis is taken. If 'inner', the intersection."
    )
    merge: Optional[Literal['same', 'unique', 'first', 'only']] = Field(
        default=None,
        description="How elements not aligned to the axis being concatenated along are selected."
    )
    uns_merge: Optional[Literal['same', 'unique', 'first', 'only']] = Field(
        default=None,
        description="How the elements of .uns are selected. Uses the same set of strategies as the merge argument, except applied recursively."
    )
    label: Optional[str] = Field(
        default=None,
        description="label different adata, Column in axis annotation (i.e. .obs or .var) to place batch information in. "
    )
    keys: Optional[List[str]] = Field(
        default=None,
        description="Names for each object being added. These values are used for column values for label or appended to the index if index_unique is not None."
    )
    index_unique: Optional[str] = Field(
        default=None,
        description="Whether to make the index unique by using the keys. If provided, this is the delimiter between '{orig_idx}{index_unique}{key}'."
    )
    fill_value: Optional[Any] = Field(
        default=None,
        description="When join='outer', this is the value that will be used to fill the introduced indices."
    )
    pairwise: bool = Field(
        default=False,
        description="Whether pairwise elements along the concatenated dimension should be included."
    )
