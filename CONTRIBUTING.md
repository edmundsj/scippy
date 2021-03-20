# How to contribute
First of all, thank you for taking the time to contribute to this project! I've tried to make a stable project and to fix bugs and add features as I am able. :)

## Getting started

### Writing some code!

Contributing to a project on Github is pretty straight forward. If this is you're first time, these are the steps you should take.

- Fork this repo.

And that's it! Read the code available and change the part you don't like! You're change should not break the existing code and should pass the tests.

If you're adding a new functionality, start from the branch **master**. It would be a better practice to create a new branch and work in there. The **develop** branch contains features in-progress which are locally stable, so you may want to check that out to see what is being worked on. Other feature-specific branches may exist as well.

When you're done, submit a pull request and I will check it out. I'll let you know if there is any problem or any changes that should be considered. My main comments will probably have to do with testing and documentation (see below).

### Tests

I always try to write comprehensive test suites, and you can run it to assure the stability of the code, located in the 'test' directory.

### Documentation

Every chunk of code that may be hard to understand has some comments above it. If you write some new code or change some part of the existing code in a way that it would not be functional without changing it's usages, it needs to be documented.
