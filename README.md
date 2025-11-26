# Scold

## About 

This is **Scold** (name comes from sc(aff)old) and it handles code generation of types of code objects in your project, similar to what is seen in frameworks like Django or Laravel, 
but generalized in a way to fit whatever are your needs.

`scold` helps in reducing manual copy-pasting of boilerplate/scaffolding code, it let's developers define custom templates for different kinds of objects (services, database entities, etc) that `scold` will render when running `scold new <object_type>`, while prompting for questions in the template.

I wasn't satisfied with the solutions I found online, the few I saw are in Javascript, but I wanted something native in Python that could be more easily included in projects without external dependencies. For the life of me I couldn't find something in Python, so I made this.

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

When running `scold new repository`, we get a form prompting for our inputs:
<img width="453" height="213" alt="image" src="https://github.com/user-attachments/assets/aa784321-651b-4789-aea5-88105fe7603d" />


## Installation

The easiest way to install the `scold` cli is with [uv](https://docs.astral.sh/uv/getting-started/installation/). You can do the following to install it in your system:
```bash
uv tool install scold-cli
```

## Acknowledgements

This project would not be possible if not for:
- [Hygen](https://github.com/jondot/hygen) - similar tool (although seems abandoned) written in the JS ecossystem, inspired Scold and its idea of templates within directories
- [Copier](https://github.com/copier-org/copier) - project templating tool for Python, doesn't focus in smaller pieces of code as Scold does, but Scold's means to render templates implicitly and the declarative form configs were inspired from this tool as well.
- [uv](https://docs.astral.sh/uv/) - my beloved python tooling stack
