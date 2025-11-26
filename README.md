# Scold

## About 

`scold` is a CLI tool for reducing manual copy-pasting of boilerplate/scaffolding code, it let's developers define custom templates for different kinds of objects (services, database entities, etc) that `scold` will render when running `scold new <object_type>`, while prompting for questions in the template.

### Usage

We first define a `scold.toml` file at the root of our project:
```toml
[project]
root_dir = "./src/scold/"  # object dirs get this value prepended
# how files get named by default, is overrided by some `file_naming` scoped prop.
# so `SampleRepository` -> `sample_repository` automatically
default_file_naming = "snake_case"

[objects.repository]
dir = "services/repositories/"
# vars get converted into a form that will be prompted when running cli
vars = [
  { field = "object_name", desc = "Name", type = "text", default = "SampleRepository" },  # required for all objects
  { field = "feature_toggles", desc = "Feature Toggles", group = [
    { field = "allow_deletion", desc = "Allow deletion", type = "bool", default = true },
    { field = "allow_extinction", desc = "Allow extinction", type = "bool", default = false },
  ] },
]
```

Then, in the directory for our object 'repository', we must have a `__template` folder (whole folder will be copied) OR a `__template.*` file (only file will be copied). Then you can use Mako's syntax in the template, benefitting from the variables declared in the `scold.toml` file.

## Installation

As Scold is still in active development, if you want to use it you must clone the repository, after that you should be able to install the `scold` cli with:
```bash
uv tool install -e .
```
