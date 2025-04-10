

def add_op_log(adata, func, kwargs):
    if "operation" not in adata.uns:
        adata.uns["operation"] = {}
        adata.uns["operation"]["running"] = []
    if hasattr(func, "__name__"):
        func_name = func.__name__
    else:
        func_name = func.func.__name__
    adata.uns["operation"]["running"].append({func_name: kwargs})
    