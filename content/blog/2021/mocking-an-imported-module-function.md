title: Mocking an imported module-level function in Python
slug: mocking-imported-module-function-python
date: 2021-06-28
tags: testing, python

The other day I spent far too much time trying to figure out how to mock a module-level function that was being used inside of my class's method in Python. My googling didn't lead to obvious answers, so I figured it'd be good to document here for future reference.

Imagine we have some module-level function like the following:
```python
# file: project/some_module/functions.py

def fetch_thing():
    # query some database
    return data
```

And that we use it inside of a class within a different module:
```python
# file: project/other_module/thing.py

from some_module.functions import fetch_thing

class Thing:
    def run(self):
        try:
            data = fetch_thing()
        except:
            self.fail_gracefully()
```

In this example, I want to test that a failure fetching from the db will fail gracefully, so I need to mock `fetch_thing` and have it raise an exception.

I kept trying to mock the function at its module path, like so:
```python
from other_module.thing import Thing

thing = Thing()

with patch.object('some_module.functions.fetch_thing') as mocked:
    mocked.side_effect = Exception('mocked error')
    data = thing.run()
```

But this isn't right. It turns out that you need to mock/patch the function **within the module it's being imported into.**

```python
from other_module.thing import Thing

thing = Thing()

with patch.object('other_module.fetch_thing') as mocked:
    mocked.side_effect = Exception('mocked error')
    data = thing.run()
```

Note the very subtle difference in the string path we are passing to `patch.object`. Because we are importing the function into `other_module` where our class uses it, **that** is what we need to mock.