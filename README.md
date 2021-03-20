# Template Github Repository
[![Build](https://github.com/edmundsj/template/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/edmundsj/template/actions/workflows/python-package-conda.yml) [![docs](https://github.com/edmundsj/template/actions/workflows/build-docs.yml/badge.svg)](https://github.com/edmundsj/template/actions/workflows/build-docs.yml ) [![codecov](https://codecov.io/gh/edmundsj/tabularasa/branch/main/graph/badge.svg?token=7L4PK4K0P3)](https://codecov.io/gh/edmundsj/tabularasa)

This is a template repository for python projects which use sphinx for
documentation, github actions for building, pytest and codecov for test
coverage.


## Getting Started
0. Choose a name for the new repository. Make sure it's available as a name on [testPyPi](https://test.pypi.org/)
  and [PyPi](https://pypi.org/). Create a new directory with that chosen module name.

1. Create a new repository on github by clicking "Use this template"


2. Clone this repository into your new directory

    ```git clone https://github.com/edmundsj/<MODULE_NAME>.git <MODULE_NAME>```

2. Set github pages to use the ``docs/`` folder for github pages at the bottom of the "Settings" page

3. Add this repositry to codecov: https://app.codecov.io/gh/edmundsj, and add the CODECOV_TOKEN secret to the github repository. You may need to login to codecov to refresh the repositories.

4. Create a new authentication token on testPyPi and add it as a github secret named ``test_pypi_token``\*

5. Create a new authentication token on PyPi and add it as a github secret named ``pypi_token``\*

6. Navigate into the cloned repository, and run the setup script. This will change all the names in the relevant setup files. If this does not work, see the end of the tutorial.:

    ```python repo_setup.py```

7. If desired, once the build on the remote server finishes, replace the tokens from testPyPi and pyPi with ones that are restricted to this pyPi project. Delete the old ones.
8. Create a status badge from the '... -> Create Status Badge' in the github actions area separately for docs and build, and paste them in the README, as well as from codecov. Add a project description in "SETUP.py" and fill out the sections of the downloaded README.


Done! Your repository should be viewable on github pages: 
https://edmundsj.github.io/REPO_NAME/

* Note - since the package does not already exist on pyPi or testPyPi you will need to create a token that has access to all your projects. This obviously isn't an optimal way of doing things, and this should really be changed. I may want to add a setup script which does all the renaming, changes github hooks, and does an initial deploy to pypi and testpypi. If you want after the first push, you can create a new token restricted to the newly-pushed project.

If step 6 does not work, you may need to do a git pull before execution. If that doesn't work, you can execute the following manually:

6a. Change the git hooks location:

    ```git config core.hooksPath .hooks```
6b. Change this repository's name with 

   ```git remote set-url origin <NEW_REPO_URL>```
6c. In the ``setup.py``, ``.hooks/pre-commit``, and ``.github/workflows/python-package-conda`` files, change all instances of "pytemplate" to "MODULE_NAME". 

6d. Push to the new repository 

    ```git push -u origin main```

## Features

- Github actions unit test integration via pytest
- Github actions package management with conda
- Github actions documentation build using sphinx and reST/markdown, with auto
self-push to repository after successful build
- Github pages documentation hosting/integration
- Local commits hooks run full test suite
- Coverage uploaded automatically to codecov after successful build
- [FUTURE] Auto-deploy to pyPi/testpyPi after successful build

## Common Issues
- Re-running builds on github actions will cause them to fail, as the build number deployed to PyPi depends on the github run number, which does not change if you restart a build.
- Pypi deploy is a little slower than test pypi, so it may not always be downloading the latest version.


## How to Use
### Adding Additional Unit Tests
- Any time you want to add additional unit tests just add them to those in the
``tests/`` directory and prepend with the name ``test``. These will be
automatically found by pytest and run during local commits and remote builds.

### Writing the Documentation
- The documentation source is located in ``docs/source`` and is written in
restructured text (markdown is also available).

### Building the Documentation
Simply run ``make html`` from the ``docs/`` directory. This will compile the
files in the ``docs/source/`` directory, and place them in the main ``docs/``
directory where github pages can find them.

## Dependencies / Technologies Used
- [Sphinx](http://www.sphinx-doc.org/)
- [pytest](https://docs.pytest.org/en/stable/index.html)
- [Github Actions](https://github.com/features/actions)
- [Codecov](https://codecov.io/)
- [Github Pages](https://pages.github.com/)

## Acknowledgements
Thanks to all the great people on stack overflow and github, for their
seemingly boundless tolerance to my and others' questions. 
