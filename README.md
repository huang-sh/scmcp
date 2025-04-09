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

<div style="position: relative; padding-bottom: 56.25%; height: 0;">
  <iframe src="https://www.loom.com/embed/5b8fcbf34226447da0027c056acdda86" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>


## 🏎️ Quickstart

### Install

Install from PyPI
```
pip install scanpy-mcp
```
#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Install from PyPi with uv</summary>

If you don't have `uv` installed, follow the installation instructions for your
system:
[link](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

Then add the following to your MCP servers file:

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

</details>

<details>
  <summary>Install with Docker</summary>

Purely for convenience, the server can run in a Docker container.

After cloning this repository, build the Docker image:

```bash
docker build -t mcp-server-docker .
```

And then add the following to your MCP servers file:

```
"mcpServers": {
  "mcp-server-docker": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-v",
      "/var/run/docker.sock:/var/run/docker.sock",
      "mcp-server-docker:latest"
    ]
  }
}
```

Note that we mount the Docker socket as a volume; this ensures the MCP server
can connect to and control the local Docker daemon.

</details>

## 📝 Prompts

### 🎻 `docker_compose`

Use natural language to compose containers. [See above](#demo) for a demo.

Provide a Project Name, and a description of desired containers, and let the LLM
do the rest.

This prompt instructs the LLM to enter a `plan+apply` loop. Your interaction
with the LLM will involve the following steps:

1. You give the LLM instructions for which containers to bring up
2. The LLM calculates a concise natural language plan and presents it to you
3. You either:
   - Apply the plan
   - Provide the LLM feedback, and the LLM recalculates the plan

#### Examples

- name: `nginx`, containers: "deploy an nginx container exposing it on port
  9000"
- name: `wordpress`, containers: "deploy a WordPress container and a supporting
  MySQL container, exposing Wordpress on port 9000"

#### Resuming a Project

When starting a new chat with this prompt, the LLM will receive the status of
any containers, volumes, and networks created with the given project `name`.

This is mainly useful for cleaning up, in-case you lose a chat that was
responsible for many containers.

## 📔 Resources

The server implements a couple resources for every container:

- Stats: CPU, memory, etc. for a container
- Logs: tail some logs from a container

## 🔨 Tools

### Containers

- `list_containers`
- `create_container`
- `run_container`
- `recreate_container`
- `start_container`
- `fetch_container_logs`
- `stop_container`
- `remove_container`

### Images

- `list_images`
- `pull_image`
- `push_image`
- `build_image`
- `remove_image`

### Networks

- `list_networks`
- `create_network`
- `remove_network`

### Volumes

- `list_volumes`
- `create_volume`
- `remove_volume`

## 🚧 Disclaimers

### Sensitive Data

**DO NOT CONFIGURE CONTAINERS WITH SENSITIVE DATA.** This includes API keys,
database passwords, etc.

Any sensitive data exchanged with the LLM is inherently compromised, unless the
LLM is running on your local machine.

If you are interested in securely passing secrets to containers, file an issue
on this repository with your use-case.

### Reviewing Created Containers

Be careful to review the containers that the LLM creates. Docker is not a secure
sandbox, and therefore the MCP server can potentially impact the host machine
through Docker.

For safety reasons, this MCP server doesn't support sensitive Docker options
like `--privileged` or `--cap-add/--cap-drop`. If these features are of interest
to you, file an issue on this repository with your use-case.

## 🛠️ Configuration

This server uses the Python Docker SDK's `from_env` method. For configuration
details, see
[the documentation](https://docker-py.readthedocs.io/en/stable/client.html#docker.client.from_env).

## 💻 Development

Prefer using Devbox to configure your development environment.

See the `devbox.json` for helpful development commands.

After setting up devbox you can configure your Claude MCP config to use it:

```
  "docker": {
    "command": "/path/to/repo/.devbox/nix/profile/default/bin/uv",
    "args": [
      "--directory",
      "/path/to/repo/",
      "run",
      "mcp-server-docker"
    ]
  },
```