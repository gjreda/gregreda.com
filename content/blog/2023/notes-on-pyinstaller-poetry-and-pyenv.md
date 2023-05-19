title: Notes on using PyInstaller, poetry, and pyenv
slug: notes-on-using-pyinstaller-poetry-and-pyenv
date: 2023-05-18
tags: python, software, notes

In my all my years of working in Python, I don't think I've ever had to create a standalone executable. But, it finally happened.

It was a pretty seamless experience, but I did hit a minor hiccup, so I wanted to capture some notes for my future self (and others, too).

I was using [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://python-poetry.org/) to manage my Python environments and dependencies, and [PyInstaller](https://pyinstaller.org/en/stable/) to create the executable.

<hr>

Let's assume you have the following project setup:
```
$ ls -la
total 56
drwxr-xr-x@ 5 greg  staff    160 May 18 17:26 .
drwxr-xr-x@ 5 greg  staff    160 May 18 17:23 ..
-rw-r--r--@ 1 greg  staff  22220 May 18 17:28 poetry.lock
-rw-r--r--@ 1 greg  staff    381 May 18 17:28 pyproject.toml
drwxr-xr-x@ 3 greg  staff     96 May 18 17:24 src
```

Let's also assume you have a simple Python script at `src/main.py` that you want to turn into an executable.

```python
# src/main.py

from bs4 import BeautifulSoup
import requests

def get_data():
    response = requests.get('https://www.google.com')
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    print(f"Hi, the title element of Google's webpage is: {title.text}")

if __name__ == '__main__':
    get_data()
```

You can create the excutable via:
```bash
$ poetry run pyinstaller src/main.py
```

This should create a `dist` directory with the executable and all the necessary libraries. You can run the executable via:

```bash
$ ./dist/main/main
Hi, the title element of Google's webpage is: Google
```

But if you are using pyenv, you may run into the following error:
```
OSError: Python library not found: libpython3.9.dylib, Python, libpython3.9m.dylib, .Python, Python3
    This means your Python installation does not come with proper shared library files.
    This usually happens due to missing development package, or unsuitable build parameters of the Python installation.

    * On Debian/Ubuntu, you need to install Python development packages:
      * apt-get install python3-dev
      * apt-get install python-dev
    * If you are building Python by yourself, rebuild with `--enable-shared` (or, `--enable-framework` on macOS)
```

To fix this, you need to reinstall the appropriate version of Python with the `--enable-framework` flag.
```bash
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.10.11
```

You may have to reestablish your poetry environment to the newly built python version above:
```bash
$ pyenv local 3.10.11
$ poetry env use $(which python)
```

If you'd already installed your dependencies via poetry, you'll have to reinstall them:
```
$ poetry install
```

Now you should be able to create the executable:
```bash
$ poetry run pyinstaller src/main.py
```

Check that it worked
```bash
$ ls -la
total 64
drwxr-xr-x@ 8 greg  staff    256 May 18 17:51 .
drwxr-xr-x@ 5 greg  staff    160 May 18 17:23 ..
drwxr-xr-x@ 3 greg  staff     96 May 18 17:51 build
drwxr-xr-x@ 3 greg  staff     96 May 18 17:54 dist
-rw-r--r--@ 1 greg  staff    889 May 18 17:54 main.spec
-rw-r--r--@ 1 greg  staff  22220 May 18 17:28 poetry.lock
-rw-r--r--@ 1 greg  staff    381 May 18 17:28 pyproject.toml
drwxr-xr-x@ 3 greg  staff     96 May 18 17:24 src
```

And run the executable:
```bash
$ ./dist/main/main
Hi, the title element of Google's webpage is: Google
```

The end.