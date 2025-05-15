> ⚠️ **Important Notice**: This repository is no longer maintained. Please visit [SCMCPHub](https://github.com/scmcphub) for the latest version of MCP servers.

SCMCP is a powerful Machine Conversation Protocol (MCP) server designed specifically for single-cell RNA sequencing (scRNA-Seq) analysis. It enables users to perform complex scRNA-Seq analyses using natural language commands, making bioinformatics more accessible to researchers without extensive programming experience.


# SCMCP

An MCP server for scRNA-Seq analysis  with natural language!

## 🪩 What can it do?

- IO module like read and write scRNA-Seq data with natural language
- Preprocessing module,like filtering, quality control, normalization, scaling, highly-variable genes, PCA, Neighbors,...
- Tool module, like clustering, differential expression etc.
- Plotting module, like violin, heatmap, dotplot
- cell-cell communication analysis

## ❓ Who is this for?

- Anyone who wants to do scRNA-Seq analysis natural language!
- Agent developers who want to call scanpy's functions for their applications

## 🌐 Where to use it?

You can use scmcp in most AI clients, plugins, or agent frameworks that support the MCP:

- AI clients, like Cherry Studio
- Plugins, like Cline
- Agent frameworks, like Agno 

## 🎬 Demo

A demo showing scRNA-Seq cell cluster analysis in a AI client Cherry Studio using natural language based on scmcp

https://github.com/user-attachments/assets/93a8fcd8-aa38-4875-a147-a5eeff22a559

## 🏎️ Quickstart

### Install

Install from PyPI
```
pip install scmcp
```
you can test it by running
```
scmcp run
```

#### run scnapy-server locally
Refer to the following configuration in your MCP client:

```
"mcpServers": {
  "scmcp": {
    "command": "scmcp",
    "args": [
      "run"
    ]
  }
}
```

#### run scnapy-server remotely
Refer to the following configuration in your MCP client:

run it in your server
```
scmcp run --transport sse --port 8000
```

Then configure your MCP client, like this:
```
http://localhost:8000/sse
```

## 🤝 Contributing

If you have any questions, welcome to submit an issue, or contact me(hsh-me@outlook.com). Contributions to the code are also welcome!
