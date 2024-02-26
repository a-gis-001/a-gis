# A_GIS Python Package

```python
pip install A_GIS
```

Pronounced with a long "a" like AEGIS, this is a package for functional python. 

## Distill and recompose

Checkout out notebooks/roundtrip.ipynb for an example of round-tripping. 

In the `__A_GIS__` directory we can have the segmented data
so that AI can operate on different parts more efficiently. 

The basic sequence is

1. raw function only (8 lines or less ideally) 
2. add comments and spacing
3. add docstring
4. send through formatter
5. this is now a complete function like someone would want to see in a code base

To split it up again we go in reverse.

6. remove docstring
7. remove comments and spacing (save in file)
8. save raw function

Now you can see easily if the raw function changed. Once this iteration
converges, the diff should be zero.

This process has advantages in that we can isolate the docstring and
work on making that beautiful. 

It could get examples, and all kinds of crazy awesome reformatting
as its own document. Then we can reapply comments to the raw source,
THEN the docstring, then format. We could send this to an AI now to
create better comments and then ONLY update the comments file. I think
the comments are somewhat dependent on the
docstring so it's nice to have this flow of regenerating comments
assuming a certain docstring and visibility of the whole file. 

After splitting back out and saving the raw function, you can see (with
git diff for example), if the AI changed the execution of the code. One
could imagine asking the AI to split a function into several that don't
exceed e.g. 9 lines for example.

This scheme gives us a way to then split those functions and send them
to their place on the file system.

By going to such small granularity, we should be able to fit in many AIs
token counts and they should be able to design tests and examples much
easier. 

We could also, based on similarity metrics for the raw functions, make
sure AI aren't creating a bunch of extra functions. I.e. if they create
a new one that has high similarity to an existing one, we could ask it
to use the existing one instead, or propose modifications to the existing 
one, e.g. optional arguments, that would make it work. 

It would be interesting to see what an AI would generate in terms of a
code base with this approach. It should arrive at lots of small
functions that are basically idioms, like A_GIS.File.read().

You should be able to apply this approach hierarchically to handle tests
for example, each test a function. This should be a totally functional
based system. Inside the functions we may want helper classes,
especially for testing. We should start
these names with an `_` to make sure they do not appear in the public
API.

Finally, it should be possible to hash the raw function content like
IPFS and provide these in a distributed computing framework, where you
basically call a function by the hash, `output = A_GIS.<hash>(input)`
which ensures you get a specific version of that function even across
different versions of `A_GIS`. All `A_GIS` functions should require
keywords which may help with handling serialized data in dictionaries
and such.


## Nice Tree Output

```
tree -I *.pyc -I __A_GIS__ -I __init__.py -I __pycache__ -I tests A_GIS/
```
