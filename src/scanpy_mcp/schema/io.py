from pydantic import (
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
    model_validator,
)
from typing import Optional, Union, Literal,Any,Sequence
from .base import JSONParsingModel


class Read10xH5Input(JSONParsingModel):
    """Input schema for the read_10x_h5 tool."""
    filename: str = Field(
        description="Path to the 10x hdf5 file"
    )
    genome: Optional[str] = Field(
        default=None,
        description="Filter expression to genes within this genome. For legacy 10x h5 files containing multiple genomes, this must be provided"
    )
    gex_only: bool = Field(
        default=True,
        description="Only keep 'Gene Expression' data and ignore other feature types, e.g. 'Antibody Capture', 'CRISPR Guide Capture', or 'Custom'"
    )
    backup_url: Optional[str] = Field(
        default=None,
        description="Retrieve the file from this URL if not present on disk"
    )
    @field_validator('filename')
    def validate_filename(cls, v: str) -> str:
        if not v.endswith('.h5'):
            raise ValueError("Filename must have .h5 extension")
        return v


class ReadH5adInput(JSONParsingModel):
    """Input schema for the read_h5ad tool."""
    filename: str = Field(
        description="File name of data file."
    )
    backed: Optional[Union[str, bool]] = Field(
        default=None,
        description="If 'r', load AnnData in 'backed' mode instead of fully loading it into memory ('memory' mode). "
                   "If you want to modify backed attributes of the AnnData object, you need to choose 'r+'. "
                   "Currently, backed only supports updates to X."
    )
    as_sparse: list[str] = Field(
        default_factory=list,
        description="If an array was saved as dense, passing its name here will read it as a sparse_matrix, "
                   "by chunk of size chunk_size."
    )
    as_sparse_fmt: str = Field(
        default="scipy.sparse._csr.csr_matrix",
        description="Sparse format class to read elements from as_sparse in as."
    )
    chunk_size: int = Field(
        default=6000,
        description="Used only when loading sparse dataset that is stored as dense. "
                   "Loading iterates through chunks of the dataset of this row size until it reads the whole dataset. "
                   "Higher size means higher memory consumption and higher (to a point) loading speed."
    )
    
    @field_validator('filename')
    def validate_filename(cls, v: str) -> str:
        if not v.endswith('.h5ad'):
            raise ValueError("Filename must have .h5ad extension")
        return v
    
    @field_validator('backed')
    def validate_backed(cls, v: Optional[Union[str, bool]]) -> Optional[Union[str, bool]]:
        if isinstance(v, str) and v not in ['r', 'r+']:
            raise ValueError("If backed is a string, it must be either 'r' or 'r+'")
        return v


class Read10xMtxInput(JSONParsingModel):
    """Input schema for the read_10x_mtx tool."""
    path: str = Field(
        description="Path to directory for .mtx and .tsv files, e.g. './filtered_gene_bc_matrices/hg19/'."
    )
    var_names: str = Field(
        default="gene_symbols",
        description="The variables index. Either 'gene_symbols' or 'gene_ids'."
    )
    make_unique: bool = Field(
        default=True,
        description="Whether to make the variables index unique by appending '-1', '-2' etc. or not."
    )
    cache: bool = Field(
        default=False,
        description="If False, read from source, if True, read from fast 'h5ad' cache."
    )
    cache_compression: Optional[str] = Field(
        default=None,
        description="See the h5py dataset_compression. (Default: settings.cache_compression)"
    )
    gex_only: bool = Field(
        default=True,
        description="Only keep 'Gene Expression' data and ignore other feature types, e.g. 'Antibody Capture', 'CRISPR Guide Capture', or 'Custom'"
    )
    prefix: Optional[str] = Field(
        default=None,
        description="Any prefix before matrix.mtx, genes.tsv and barcodes.tsv. For instance, if the files are named patientA_matrix.mtx, patientA_genes.tsv and patientA_barcodes.tsv the prefix is patientA_. (Default: no prefix)"
    )
    
    @field_validator('var_names')
    def validate_var_names(cls, v: str) -> str:
        if v not in ['gene_symbols', 'gene_ids']:
            raise ValueError("var_names must be either 'gene_symbols' or 'gene_ids'")
        return v
    
    @field_validator('cache_compression')
    def validate_cache_compression(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ['gzip', 'lzf']:
            raise ValueError("cache_compression must be either 'gzip', 'lzf', or None")
        return v




class WriteModel(JSONParsingModel):
    """Input schema for the write tool."""
    filename: str = Field(
        description="Path to save the file. If no extension is provided, the default format will be used."
    )
    ext: Optional[Literal['h5', 'csv', 'txt', 'npz']] = Field(
        default=None,
        description="File extension to infer file format. If None, defaults to scanpy's settings.file_format_data."
    )
    compression: Optional[Literal['gzip', 'lzf']] = Field(
        default='gzip',
        description="Compression format for h5 files."
    )
    compression_opts: Optional[int] = Field(
        default=None,
        description="Compression options for h5 files."
    )
    
    @field_validator('filename')
    def validate_filename(cls, v: str) -> str:
        # Allow any filename since the extension is optional and can be inferred
        return v
    
    @model_validator(mode='after')
    def validate_extension_compression(self) -> 'WriteInput':
        # If ext is provided and not h5, compression should be None
        if self.ext is not None and self.ext != 'h5' and self.compression is not None:
            raise ValueError("Compression can only be used with h5 files")
        return self


class WriteH5adModel(JSONParsingModel):
    """Input schema for the write_h5ad tool."""
    filename: Optional[str] = Field(
        default=None,
        description="Filename of data file. Defaults to backing file."
    )
    compression: Optional[Union[Literal['gzip', 'lzf'], dict]] = Field(
        default=None,
        description="Compression format for h5 files. Can be 'gzip', 'lzf', or None. "
                   "Alternative compression filters such as 'zstd' can be passed from the hdf5plugin library."
    )
    compression_opts: Optional[Union[int, Any]] = Field(
        default=None,
        description="Compression options for h5 files. For 'gzip', an integer from 0-9 specifying compression level."
    )
    as_dense: Sequence[str] = Field(
        default_factory=list,
        description="Sparse arrays in AnnData object to write as dense. Currently only supports 'X' and 'raw/X'."
    )
    
    @field_validator('filename')
    def validate_filename(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.endswith('.h5ad'):
            raise ValueError("Filename must have .h5ad extension")
        return v
    
    @field_validator('as_dense')
    def validate_as_dense(cls, v: Sequence[str]) -> Sequence[str]:
        valid_options = ['X', 'raw/X']
        for item in v:
            if item not in valid_options:
                raise ValueError(f"as_dense only supports {valid_options}, got {item}")
        return v


class ReadTextInput(JSONParsingModel):
    """Input schema for the read_text tool."""
    filename: str = Field(
        description="Path to the text file (.txt, .tab, .csv) to read"
    )
    delimiter: Optional[Literal["tab", "comma", "space", "semicolon", "colon"]] = Field(
        default=None,
        description="Delimiter that separates data in text files. Options: 'tab' (\t), 'comma' (,), 'space' ( ), 'semicolon' (;), 'colon' (:). If None, splits by arbitrary whitespace."
    )
    first_column_names: Optional[bool] = Field(
        default=None,
        description="Assume the first column stores row names."
    )
    first_column_obs: bool = Field(
        default=True,
        description="If True, assume the first column stores observations(cell or barcode) names. If False, the data will be transposed."
    )
