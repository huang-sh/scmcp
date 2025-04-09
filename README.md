# Scanpy MCP server

An MCP server for scRNA-Seq analysis software Scanpy with natural language!

## 🪩 What can it do?

- IO module like read and write scRNA-Seq data with natural language
- Preprocessing module,like filtering, quality control, normalization, scaling, highly-variable genes, PCA, Neighbors,...
- Tool module, like clustering, differential expression, trajectory inference, marker gene identification, etc.
- Plotting module, like violin, heatmap, dotplot

## ❓ Who is this for?

- Anyone who wants to do scRNA-Seq analysis natural language!
- Agent developers who want to call scanpy's functions for their applications

## 🌐 Where to use it?

You can use scanpy-mcp in most AI clients, plugins, or agent frameworks that support the MCP:

- AI clients, like Cherry Studio
- Plugins, like Cline
- Agent frameworks, like Agno 

## Demo

A demo showing scRNA-Seq cell cluster analysis in a AI client Cherry Studio using natural language based on scanpy-mcp

https://github.com/user-attachments/assets/93a8fcd8-aa38-4875-a147-a5eeff22a559

## 🏎️ Quickstart

### Install

Install from PyPI
```
pip install scanpy-mcp
```


You configure MCP servers like this:

```
"mcpServers": {
  "mcp-server-docker": {
    "command": "uvx",
    "args": [
      "mcp-server-docker"
    ]
  }
}
```

## 🤝 Contributing

If you have any questions, welcome to submit an issue, or contact me(hsh-me@outlook.com). Contributions to the code are also welcome!