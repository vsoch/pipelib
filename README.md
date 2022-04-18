# Pipelib


[![PyPI version](https://badge.fury.io/py/pipelib.svg)](https://badge.fury.io/py/pipelib)

Pipelib is a library for creating pipelines. You can parse, compare, and order iterables. With Pipelib you can:

1. Create a custom pipeline to parse and compare version strings
2. Use a collection of provided sorting functions for custom sorts.
3. Assemble different processing blocks to pre-process inputs first.

The initial ideas came from [Singularity Registry HPC (shpc)](https://github.com/singularityhub/singularity-hpc/blob/main/shpc/main/container/update/versions.py) that had a need to parse and compare version strings from docker container tags.

## User Guide

### A Simple Example

Here is a simple example to process and filter a list of strings:

```python
import pipelib.main.steps as step
import pipelib.main.pipeline as pipeline

# A pipeline to process a list of strings
steps = (

   # convert everything to lowercase
   step.AllLowercase(),

   # don't include anything with "two"
   ~step.HasFilter(filters=["two"])
)

# Strings to process
items = ['item-ONE', 'item-TWO', 'item-two-THREE']

p = pipeline.Pipeline(steps)

# The updated and transformed items
updated = p.run(items)
# ['item-one']
```

In the above, you can always use the `~` symbol to reverse the functionality of a step.
E.g., a step named `steps.HasMinLength()` will return True given that an item has a min length 
that you've provided, and the item will be kept for further processing in the pipeline. 
However, `~steps.HasMinLength()` will do the opposite, not including those same items that have
the min length (and keeping those that do not). 

### Pipeline Logic

Steps are composable, meaning that you can chain them together into logical statements.
As an example, let's say part of my processing needs to determine if a string has a commit
reference, where generally I want to check:

- the length is >= 10
- there are not all letters

It wouldn't work to check all of these separately (as their own steps) because I want them
grouped together as one condition, e.g.,

> Don't keep if the length is >= 10 AND there are not all letters

We can thus compose steps into this logic as follows:

```python
import pipelib.main.steps as step
import pipelib.main.pipeline as pipeline

# We want to keep those length >= 10 and not all letters
tags = [
 '0.9.24--ha87ae23_0',
 '0.9.19--1',
 '0.9.14--1',
 'ishouldberemoved',
 '0.9.10--hdbcaa40_3']

# A pipeline to process docker tags
steps = (
   # Example of chaining steps together
   step.HasMinLength(length=10) & ~step.HasAllLetters(),
)

p = pipeline.Pipeline(steps)

# The updated and transformed items
updated = p.run(tags)
# ['0.9.24--ha87ae23_0', '0.9.10--hdbcaa40_3']
```

As expected, the above returned have length >= 10 and aren't all letters! And
technically, the pipeline above only has one step, which is generated with out custom logic. Note
that for this to work, you need to chain together steps of the same type. All of the above are class `BooleanStep`
so they will return a True or False that can be combined (`&`), and an outcome that we can take the inverse of (`~`).


### Combining Pipelines

It might be the case that you want to re-use the same pipeline over again, or even include
it with another pipeline! We can actually do that by just using the pipeline as a step.
To start with our previous example, let's say we turn it into some kind of check for a commit,
because commits never have all letters and are usually >= 10. Maybe we want to run these preprocessing
steps, split the tag by the `--` to remove the remainder, and then turn it into a Version we can
sort.


```python
import pipelib.main.steps as step
import pipelib.main.pipeline as pipeline

fruits = ["Orange", "Melon", "Watermelon", "Fruit23"]
preprocess = pipeline.Pipeline(
    steps = (
        # Example of chaining steps together
        step.HasMaxLength(length=8) & step.HasAllLetters(),
    )
)

# Add this preprocess step alongside other steps (make lowercase)
steps = (
   step.AllLowercase(),
   preprocess,
)

# Createa a new pipeline and run
p = pipeline.Pipeline(steps)

# We should expect orange and melon!
updated = p.run(fruits)
['orange', 'melon']
```

We have plans to provide reasonable combinations of steps ready to go for different
processing needs. Stay tuned!

## TODO

 - add support for addition operator on steps that return string
 - better organize steps into submodules
 - real world example with docker tags
 - should be able to print pretty a pipeline / steps
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
