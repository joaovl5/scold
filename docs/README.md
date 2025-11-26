# Scold Prototype Docs

- I want to:
    ```
    $ scold new repository
    ```
- and `scold` attempts to find a template file for the `repository` object type
- will first attempting finding the root `scold.toml` file of the project (starting in current directory then going up)
```toml
# scold.toml - example
[project]
root_dir = "./src/scold/"  # object dirs get this value prepended
# how files get named by default, is overrided by some `file_naming` scoped prop.
# so `SampleRepository` -> `sample_repository` automatically
default_file_naming = "snake_case"

[objects.repository]
dir = "services/repositories/"
vars = [
  { field = "object_name", desc = "Name", type = "text", default = "SampleRepository" },  # required for all objects
  { field = "feature_toggles", desc = "Feature Toggles", group = [
    { field = "allow_deletion", desc = "Allow deletion", type = "bool", default = true },
    { field = "allow_extinction", desc = "Allow extinction", type = "bool", default = false },
  ] },
]
```
- within the directory, `scold` looks for a `__template.py` or `__template` directory, which will then use as scaffold for copies
- the template file(s) will be treated as mako templates and rendered into a new file/directory
