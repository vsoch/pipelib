#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

import pipelib.steps as step
import pipelib.pipelines as pipelines
import pipelib.pipeline as pipeline
import pipelib.utils


def test_basic_pipeline():
    """
    Test a basic pipeline
    """
    # A pipeline to process a list of strings
    steps = (
        # convert everything to lowercase
        step.transform.ToLowercase(),
        # don't include anything with "two"
        ~step.filters.HasPatterns(filters=["two"]),
    )

    # Strings to process
    items = ["item-ONE", "item-TWO", "item-two-THREE"]

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(items)
    assert len(updated) == 1
    assert "item-one" in updated


def test_composeable_pipeline():
    """
    Test a composeable pipeline
    """
    # We want to keep those length >= 10 and not all letters
    tags = [
        "0.9.24--ha87ae23_0",
        "0.9.19--1",
        "0.9.14--1",
        "ishouldberemoved",
        "0.9.10--hdbcaa40_3",
    ]

    # A pipeline to process docker tags
    steps = (
        # Example of chaining steps together
        step.filters.HasMinLength(length=10)
        & ~step.filters.HasAllLetters(),
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)
    assert len(updated) == 2
    for item in ["0.9.24--ha87ae23_0", "0.9.10--hdbcaa40_3"]:
        assert item in updated


def test_combined_pipeline():
    """
    Test a combined pipeline
    """
    fruits = ["Orange", "Melon", "Watermelon", "Fruit23"]
    preprocess = pipeline.Pipeline(
        steps=(
            # Example of chaining steps together
            step.filters.HasMaxLength(length=8)
            & step.filters.HasAllLetters(),
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
    assert len(updated) == 2
    for item in ["orange", "melon"]:
        assert item in updated


def test_docker_tags_pipeline():
    """
    Test a manual docker tags pipeline
    """
    # Pre-generated sets of steps we can use
    import pipelib.pipelines as pipelines

    # Docker tags for biocontainers/diamond
    tags = [
        "0.9.24--ha87ae23_0",
        "0.9.19--1",
        "0.9.14--1",
        "0.9.14--0",
        "0.8.22--boost1.60_1",
        "0.7.12--boost1.61_0",
        "0.8.30--0",
        "0.8.27--0",
        "0.8.29--0",
        "0.8.28--0",
        "0.8.26--0",
        "0.8.31--0",
        "0.8.36--0",
        "0.8.27--1",
        "0.9.10--1",
        "0.8.26--1",
        "0.8.36--1",
        "0.8.28--1",
        "0.9.21--1",
        "0.8.31--1",
        "0.8.30--1",
        "0.7.12--boost1.60_0",
        "0.8.29--1",
        "0.8.9--boost1.60_1",
        "0.7.12--boost1.64_0",
        "0.9.10--0",
        "0.9.10--hdbcaa40_3",
        "0.8.36--hdbcaa40_3",
        "0.8.29--hdbcaa40_3",
        "0.9.19--hdbcaa40_3",
        "0.8.27--hdbcaa40_3",
        "0.8.22--hdbcaa40_4",
        "0.9.24--ha888412_1",
        "0.9.25--hfb76ee0_0",
        "0.9.26--hfb76ee0_0",
        "0.8.29--h8b12597_4",
        "0.8.36--h8b12597_4",
        "0.9.28--h56fc30b_0",
        "0.9.29--h56fc30b_0",
        "0.9.30--h56fc30b_0",
        "0.9.32--h56fc30b_0",
        "0.9.34--h56fc30b_0",
        "0.9.35--h56fc30b_0",
        "0.9.36--h56fc30b_0",
        "0.9.19--h8b12597_4",
        "0.9.10--h8b12597_4",
        "0.8.27--h8b12597_4",
        "0.8.30--h8b12597_3",
        "0.8.26--h8b12597_3",
        "0.8.28--h8b12597_3",
    ]

    # A pipeline to process docker tags
    steps = (
        # don't include tags with boost
        ~step.filters.HasPatterns(filters=["boost"]),
        # Filter out those that look like commits
        pipelines.git.RemoveCommits,
        # Scrub commits from version string
        step.filters.CleanCommit(),
        # Parse versions, return sorted ascending, and taking version major.minor.patch into account
        step.container.ContainerTagSort(),
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)
    assert len(updated) == 22
    for item in [
        "0.9.36.0",
        "0.9.35.0",
        "0.9.34.0",
        "0.9.32.0",
        "0.9.30.0",
        "0.9.29.0",
        "0.9.28.0",
        "0.9.26.0",
        "0.9.25.0",
        "0.9.24.1",
        "0.9.21.1",
        "0.9.19.4",
        "0.9.14.1",
        "0.9.10.4",
        "0.8.36.4",
        "0.8.31.1",
        "0.8.30.3",
        "0.8.29.4",
        "0.8.28.3",
        "0.8.27.4",
        "0.8.26.3",
        "0.8.22.4",
    ]:
        assert item in updated

    updated = p.run(tags, unwrap=False)
    assert len(updated) == 22
    originals = [x._original for x in updated]
    for item in [
        "0.9.36--h56fc30b_0",
        "0.9.35--h56fc30b_0",
        "0.9.34--h56fc30b_0",
        "0.9.32--h56fc30b_0",
        "0.9.30--h56fc30b_0",
        "0.9.29--h56fc30b_0",
        "0.9.28--h56fc30b_0",
        "0.9.26--hfb76ee0_0",
        "0.9.25--hfb76ee0_0",
        "0.9.24--ha888412_1",
        "0.9.21--1",
        "0.9.19--h8b12597_4",
        "0.9.14--1",
        "0.9.10--h8b12597_4",
        "0.8.36--h8b12597_4",
        "0.8.31--1",
        "0.8.30--h8b12597_3",
        "0.8.29--h8b12597_4",
        "0.8.28--h8b12597_3",
        "0.8.27--h8b12597_4",
        "0.8.26--h8b12597_3",
        "0.8.22--hdbcaa40_4",
    ]:
        assert item in originals

    # A pipeline to process docker tags
    steps = (
        # don't include tags with boost
        ~step.filters.HasPatterns(filters=["boost"]),
        # Filter out those that look like commits
        pipelines.git.RemoveCommits,
        # Scrub commits from version string
        step.filters.CleanCommit(),
        # Parse versions, return sorted ascending, and taking version major.minor.patch into account
        step.container.ContainerTagSort(unique_minor=True),
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)
    assert len(updated) == 2
    for item in ["0.9.36.0", "0.8.36.4"]:
        assert item in updated

    # A pipeline to process docker tags
    steps = (
        # don't include tags with boost
        ~step.filters.HasPatterns(filters=["boost"]),
        # Filter out those that look like commits
        pipelines.git.RemoveCommits,
        # Scrub commits from version string
        step.filters.CleanCommit(),
        # Parse versions, return sorted ascending, and taking version major.minor.patch into account
        step.container.ContainerTagSort(unique_major=True),
    )

    p = pipeline.Pipeline(steps)

    # The updated and transformed items
    updated = p.run(tags)
    assert len(updated) == 1
    assert "0.9.36.0" in updated
