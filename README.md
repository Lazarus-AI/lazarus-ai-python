# lazarus-ai
Lazarus Forms API Python Library

## Setup instructions

```shell
pre-commit install
```

```shell
cd src && pip install -r requirements.txt
```

To run locally on the dev API URL, set an environment variable with the preview base URL. Otherwise all requests will post to the prod API URL.
```
os.environ["BASE_URL"] = "..."
```


## Testing instructions

In `tests/plugins/set_test_vars.py` replace the `ORG_ID`, `AUTH_KEY`, `BASE_URL` with the Lazarus test credentials and the preview API URL.
```shell
pytest
```


## Release instructions

Update the version number in `src/setup.py`. Run the following commands:
```shell
python3 -m pip install --upgrade build
cd src
python3 -m build
python3 -m pip install --upgrade twine
twine upload dist/*
```
Note that you may need to delete previous `dist/` files.
