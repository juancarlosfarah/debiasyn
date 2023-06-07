# The DebiaSyn Toolbox

Pushing the Boundaries of Information-Theoretic Estimators for Neuroimaging Data
---

## Installing Dependencies

We recommend you create a virtual environment within the repository.

```
python -m venv venv
```

You can then use this `venv` to install the dependencies.

```
source ./venv/bin/activate
pip install -r requirements.txt
```

Then install the PySamba module.

```
python -m pip install -e ./src
```

To stop the `venv` session, just execute `deactivate`.

If you add any dependencies to the code, please update the `requirements.txt` file.

```
pip freeze > requirements.txt
```

## Flags

export LDFLAGS=-L/usr/local/lib
export CPPFLAGS=-I/usr/local/include
