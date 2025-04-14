
from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
    model_validator,
)
from typing import Optional, Union, List
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