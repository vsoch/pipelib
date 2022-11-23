.. _getting_started-user-guide:

==========
User Guide
==========

Pipelib is a library for creating pipelines. You can parse, compare, and order iterables. With Pipelib you can:

1. Create a custom pipeline to parse and compare version strings
2. Use a collection of provided sorting functions for custom sorts.
3. Assemble different processing blocks to pre-process inputs first.

If you have a question, find a bug, or want to request a feature!
This is an open source project and we are eager for your contribution. 🎉️

.. _getting_started-user-guide-concepts:

Concepts
========

Pipelib has a few concepts:

- a *pipeline* is a collection of steps that take, as input, a listing of items and return a parser and filtered list
- a *step* is some action in a pipeline. There are different kinds of steps
  - *filter* steps are boolean steps, meaning functions that return True/False to indicate if the item should be kept.
  - *transform* steps take the initial input and return a different version. If the resulting item is empty or None, is it not included.
  - *sort* performs some kind of specialized sort or ordering, usually expecting a list with something sortable.
  - *custom* a custom step usually can perform any kind of operation (or more than one), as an example a step to filter and sort container tags.
- a *wrapper* is (exactly that) - an internal wrapper class to an item. Wrappers are used inside steps and allow for things like sorting and comparison. You probably don't need to worry about wrappers unless you want to develop for pipelib.

Pipelines are composeable, meaning that you can insert an entire pipeline into another pipeline as a step.

.. _getting_started-user-guide-usage:

Usage
=====

Once you have ``pipelib`` installed (:ref:`getting_started-installation`) you
can parse your errors fairly easily, either using ohno as a wrapper or post-run
log parser.

.. _getting_started-user-guide-usage-simple-example:


A Simple Example
----------------


Here is a simple example to process and filter a list of strings:

.. code-block:: python

    import pipelib.steps as step
    import pipelib.pipeline as pipeline

    # A pipeline to process a list of strings
    steps = (

       # convert everything to lowercase
       step.transform.ToLowercase(),

       # don't include anything with "two"
       ~step.filters.HasPatterns(filters=["two"])
    )

    # Strings to process
    items = ['item-ONE', 'item-TWO', 'item-two-THREE']

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(items)
    # ['item-one']

In the above, you can always use the `~` symbol to reverse the functionality of a step.
E.g., a step named `steps.HasMinLength()` will return True given that an item has a min length
that you've provided, and the item will be kept for further processing in the pipeline.
However, `~steps.HasMinLength()` will do the opposite, not including those same items that have
the min length (and keeping those that do not).


.. _getting_started-user-guide-usage-pipeline-logic:

Pipeline Logic
--------------

Steps are composable, meaning that you can chain them together into logical statements.
As an example, let's say part of my processing needs to determine if a string has a commit
reference, where generally I want to check:

- the length is >= 10
- there are not all letters

It wouldn't work to check all of these separately (as their own steps) because I want them
grouped together as one condition, e.g.,

> Don't keep if the length is >= 10 AND there are not all letters

We can thus compose steps into this logic as follows:

.. code-block:: python

    import pipelib.steps as step
    import pipelib.pipeline as pipeline

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
       step.filters.HasMinLength(length=10) & ~step.filters.HasAllLetters(),
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)
    # ['0.9.24--ha87ae23_0', '0.9.10--hdbcaa40_3']

As expected, the above returned have length >= 10 and aren't all letters! And
technically, the pipeline above only has one step, which is generated with out custom logic. Note
that for this to work, you need to chain together steps of the same type. All of the above are class `BooleanStep`
so they will return a True or False that can be combined (`&`), and an outcome that we can take the inverse of (`~`).

.. _getting_started-user-guide-usage-combining-pipelines:


Combining Pipelines
-------------------

It might be the case that you want to re-use the same pipeline over again, or even include
it with another pipeline! We can actually do that by just using the pipeline as a step.
To start with our previous example, let's say we turn it into some kind of check for a commit,
because commits never have all letters and are usually >= 10. Maybe we want to run these preprocessing
steps, split the tag by the `--` to remove the remainder, and then turn it into a Version we can
sort.


.. code-block:: python

    import pipelib.steps as step
    import pipelib.pipeline as pipeline

    fruits = ["Orange", "Melon", "Watermelon", "Fruit23"]
    preprocess = pipeline.Pipeline(
        steps = (
            # Example of chaining steps together
            step.filters.HasMaxLength(length=8) & step.filters.HasAllLetters(),
        )
    )

    # Add this preprocess step alongside other steps (make lowercase)
    steps = (
       step.transform.ToLowercase(),
       preprocess,
    )

    # Createa a new pipeline and run
    p = pipeline.Pipeline(steps)

    # We should expect orange and melon!
    updated = p.run(fruits)
    ['orange', 'melon']


.. _getting_started-user-guide-usage-docker-tags:


A Real World Example - Docker Tags
----------------------------------

A more real world example might be starting with a list of tags and then both filtering
and sorting. For example, if you look at tags for [biocontainers/diamond](https://crane.ggcr.dev/ls/quay.io/biocontainers/diamond)
you see a lot of duplicate versions, and things like:

.. code-block:: console

    ...
    0.9.14--1
    0.9.14--0
    0.8.22--boost1.60_1
    0.7.12--boost1.61_0
    ...

It could be that we want to filter out boost (or keep it) and that we want to only preserve ``0.9.14--1`` as the "latest"
version of ``0.9.14``. To support this, you might do the following:

.. code-block:: python

    import pipelib.steps as step
    import pipelib.pipeline as pipeline

    # Pre-generated sets of steps we can use
    import pipelib.pipelines as pipelines
    import requests

    # Docker tags for biocontainers/diamond
    tags = [x for x in requests.get("https://crane.ggcr.dev/ls/quay.io/biocontainers/diamond").text.split('\n') if x]

    # A pipeline to process docker tags
    steps = (

       # don't include tags with boost
       ~step.filters.HasPatterns(filters=["boost"]),

       # Filter out those that look like commits
       pipelines.git.RemoveCommits,

       # Scrub commits from version string
       step.filters.CleanCommit(),

       # Parse versions, return sorted ascending, and taking version major.minor.patch into account
       step.container.ContainerTagSort()
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)


By default, all pipelines turn the items as strings, meaning the processed ones. For this reason,
the result we get back is:

.. code-block:: python

    ['0.9.36.0',
     '0.9.35.0',
     '0.9.34.0',
     '0.9.32.0',
     '0.9.30.0',
     '0.9.29.0',
     '0.9.28.0',
     '0.9.26.0',
     '0.9.25.0',
     '0.9.24.1',
     '0.9.21.1',
     '0.9.19.4',
     '0.9.14.1',
     '0.9.10.4',
     '0.8.36.4',
     '0.8.31.1',
     '0.8.30.3',
     '0.8.29.4',
     '0.8.28.3',
     '0.8.27.4',
     '0.8.26.3',
     '0.8.22.4']

Do you see a problem with this? These are the filtered and reduced original tags, but they aren't
super useful to us if we actually need to pull the containers! Although it's neat to see that N=50 has been
reduced to N=22, and that the parser is honoring our request to consider patches as unique, we can't really do
anything with this. Let's try again, but asking pipelib to not "unwrap" the result:

.. code-block:: python

    updated = p.run(tags, unwrap=False)

The list may look the same, but we are actually looking at wrapped results, each of which has an `_original`
attribute that contains the original tab!


.. code-block:: python

    > [x._original for x in updated]
    ['0.9.36--h56fc30b_0',
     '0.9.35--h56fc30b_0',
     '0.9.34--h56fc30b_0',
     '0.9.32--h56fc30b_0',
     '0.9.30--h56fc30b_0',
     '0.9.29--h56fc30b_0',
     '0.9.28--h56fc30b_0',
     '0.9.26--hfb76ee0_0',
     '0.9.25--hfb76ee0_0',
     '0.9.24--ha888412_1',
     '0.9.21--1',
     '0.9.19--h8b12597_4',
     '0.9.14--1',
     '0.9.10--h8b12597_4',
     '0.8.36--h8b12597_4',
     '0.8.31--1',
     '0.8.30--h8b12597_3',
     '0.8.29--h8b12597_4',
     '0.8.28--h8b12597_3',
     '0.8.27--h8b12597_4',
     '0.8.26--h8b12597_3',
     '0.8.22--hdbcaa40_4']


Note that this particular pipeline also supports different variations of the container
parsing step to ask for unique versions on the level of major, minor, or patch (default, above):
Here we ask for just minor versions:

.. code-block:: python

    # A pipeline to process docker tags
    steps = (

       # don't include tags with boost
       ~step.filters.HasPatterns(filters=["boost"]),

       # Filter out those that look like commits
       pipelines.git.RemoveCommits,

       # Scrub commits from version string
       step.filters.CleanCommit(),

       # Parse versions, return sorted ascending, and taking version major.minor.patch into account
       step.container.ContainerTagSort(unique_minor=True)
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)
    ['0.9.36.0', '0.8.36.4']


And finally, just major.


.. code-block:: python

    # A pipeline to process docker tags
    steps = (

       # don't include tags with boost
       ~step.filters.HasPatterns(filters=["boost"]),

       # Filter out those that look like commits
       pipelines.git.RemoveCommits,

       # Scrub commits from version string
       step.filters.CleanCommit(),

       # Parse versions, return sorted ascending, and taking version major.minor.patch into account
       step.container.ContainerTagSort(unique_major=True)
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)
    ['0.9.36.0']


.. _getting_started-user-guide-usage-github-tags:


A Real World Example - GitHub Tags
----------------------------------

If you want to filter down GitHub tags to semantic versions, you're best off using
the ``ContainerTagSort`` described previously. However, for some trusted actions,
we want to stick with a major tag or release like ``v3``. This is what this
step is intended for.

.. code-block:: python

    import pipelib.steps as step
    import pipelib.pipeline as pipeline

    # Pre-generated sets of steps we can use
    import pipelib.pipelines as pipelines

    # Example GitHub release tags
    tags = ['v3', 'v2', 'v2.5.1']

    # A pipeline to process docker tags
    steps = (

       # Parse versions, return sorted ascending, and taking version major.minor.patch into account
       step.release.MajorTagSort()
    )

    p = pipeline.Pipeline(steps)
    # The updated and transformed items
    updated = p.run(tags)


Steps
-----

The following steps are available


.. include:: ../steps.inc

You can easily look at the steps that are provided:

.. code-block:: python

    from pipelib.steps import all_steps
    In [1]: all_steps
    Out[1]:
    {'filter': {'HasMaxLength': pipelib.steps.filters.numeric.HasMaxLength,
      'HasMinLength': pipelib.steps.filters.numeric.HasMinLength,
      'HasAllLetters': pipelib.steps.filters.strings.HasAllLetters,
      'HasAllLowerLettersNumbers': pipelib.steps.filters.strings.HasAllLowerLettersNumbers,
      'HasPatterns': pipelib.steps.filters.strings.HasPatterns,
      'CleanCommit': pipelib.steps.filters.git.CleanCommit},
     'transform': {'ToInteger': pipelib.steps.transform.numeric.ToInteger,
      'SplitAndJoinN': pipelib.steps.transform.strings.SplitAndJoinN,
      'ToLowercase': pipelib.steps.transform.strings.ToLowercase,
      'ToString': pipelib.steps.transform.strings.ToString},
     'container': {'ContainerTagSort': pipelib.steps.container.tags.ContainerTagSort},
     'sort': {'BasicSort': pipelib.steps.sort.basic.BasicSort},
     'release': {'MajorTagSort': pipelib.steps.release.tags.MajorTagSort}}

This library is under development and we will have more documentation coming soon!
