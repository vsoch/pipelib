# Pipelib


[![PyPI version](https://badge.fury.io/py/pipelib.svg)](https://badge.fury.io/py/pipelib)

Pipelib is a library for creating pipelines. You can parse, compare, and order iterables. With Pipelib you can:

1. Create a custom pipeline to parse and compare version strings
2. Use a collection of provided sorting functions for custom sorts.
3. Assemble different processing blocks to pre-process inputs first.

The initial ideas came from [Singularity Registry HPC (shpc)](https://github.com/singularityhub/singularity-hpc/blob/main/shpc/main/container/update/versions.py) that had a need to parse and compare version strings from docker container tags.

⭐️ [Documentation](https://vsoch.github.io/pipelib/) ⭐️


## TODO

 - add tests for wrappers and pipelines
 - automated detection / docs for pipelines too
 - should be able to print pretty a pipeline / steps
 - ToInteger doesn't work because we choose an int wrapper - we need to be able to detect output and apply a different wrapper type given int.
 - pipeline steps will need a way to sort / compare / filter

## Contributors

We use the [all-contributors](https://github.com/all-contributors/all-contributors) 
tool to generate a contributors graphic below.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://vsoch.github.io"><img src="https://avatars.githubusercontent.com/u/814322?v=4?s=100" width="100px;" alt="Vanessasaurus"/><br /><sub><b>Vanessasaurus</b></sub></a><br /><a href="https://github.com/vsoch/pipelib/commits?author=vsoch" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
