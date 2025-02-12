# Configuration

## Configuring Your Project

All Vellum configuration is done via the `pyproject.toml` file. The Vellum CLI will automatically read any `[tool.vellum]` table sections in the file when a command is run.

## Workflows

To explicitly define Workflows in your project and map them to resources in Vellum, you can add a `[[tool.vellum.workflows]]` table to your `pyproject.toml` file:

```toml
[[tool.vellum.workflows]]
module = "examples.my_workflow"
workflow_sandbox_id = "<workflow-sandbox-id>"
```

Now, when you run `vellum workflows push examples.my_workflow`, Vellum will know exactly which local Workflow to source from and which Workflow Sandbox in Vellum to update.

## Multiple Workflows

You may want to define multiple Workflows in your project and configure them within the same `pyproject.toml` file. You can use the double bracket syntax in `pyproject.toml` for this:

```toml
[[tool.vellum.workflows]]
module = "examples.my_workflow"
workflow_sandbox_id = "<workflow-sandbox-id-1>"

[[tool.vellum.workflows]]
module = "examples.my_other_workflow"
workflow_sandbox_id = "<workflow-sandbox-id-2>"
```

## Pulling Workflows

The configuration above works not only for pushing Workflows from local to Vellum, but also for pulling them from Vellum to a local code representation. If you have a Vellum Workflow that is already defined in Vellum, you can specify which module to pull the Workflow into using the same configuration above.

Once configured, you can run `vellum workflows pull examples.my_workflow` to pull a specific Workflow into your local project.

## Ignoring Files

The pull command will do a full directory replace, meaning it will overwrite and delete any files in the local directory that are not part of the Vellum Workflow's code generation.

To protect specific files or directories from being overwritten, you can add them to the ignore list in your `pyproject.toml` file:

```toml
[[tool.vellum.workflows]]
module = "examples.my_other_workflow"
workflow_sandbox_id = "<workflow-sandbox-id>"
ignore = "tests/*"
```

This ignore command accepts either a single glob pattern or a list of glob patterns. As shown above, this can be useful in situations where you want to colocate related files with the Workflow, such as tests.

## State Lock File

The `pyproject.toml` file is used for user-defined configuration. However, Vellum also uses a `vellum.lock.json` file to track the state of your project. This file is automatically generated and maintained when you run `vellum workflows push` or `vellum workflows pull`. You should not modify this file manually.

The lock file is updated automatically as part of running various commands in the Vellum CLI (for example, when running `vellum workflows pull --workflow-sandbox-id <id>`). Once a Workflow has been added to a `vellum.lock.json` file, it can be referenced by module name in push and pull commands as if it were defined in the `[[tool.vellum.workflows]]` table, even if it wasn't yet explicitly defined in the `pyproject.toml` file.

Was this page helpful?

Yes

No 