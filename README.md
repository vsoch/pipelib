# Pipelib


[![PyPI version](https://badge.fury.io/py/pipelib.svg)](https://badge.fury.io/py/pipelib)

Pipelib is a library for creating pipelines. You can parse, compare, and order iterables. With Pipelib you can:

1. Create a custom pipeline to parse and compare version strings
2. Use a collection of provided sorting functions for custom sorts.
3. Assemble different processing blocks to pre-process inputs first.

The initial ideas came from [Singularity Registry HPC (shpc)](https://github.com/singularityhub/singularity-hpc/blob/main/shpc/main/container/update/versions.py) that had a need to parse and compare version strings from docker container tags.


**under development**

## Design

```
import pipelib.main.steps as steps
import pipelib.main.pipeline as pipeline

# A pipeline to process a list of strings
steps = (

   # A step that converts everything to lowercase
   steps.AllLowercase(),

   # step that includes anything with "two"
   (steps.ExcludeFilter(), {"filters": ['two']})
)

# Strings to process
items = ['item-ONE', 'item-TWO', 'item-two-THREE']

p = pipeline.Pipeline(steps)

# The updated and transformed items
updated = p.run(items)
# ['item-one']
```

## TODO

 - automated discovery of steps
 - automated testing for structure / output of each test
 - docstrings should have examples to show usage
 - custom version parsing / comparson class
 - pipeline steps will need a way to sort / compare / filter

## Contributors

We use the [all-contributors](https://github.com/all-contributors/all-contributors) 
tool to generate a contributors graphic below.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://vsoch.github.io"><img src="https://avatars.githubusercontent.com/u/814322?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Vanessasaurus</b></sub></a><br /><a href="https://github.com/vsoch/pipelib/commits?author=vsoch" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
