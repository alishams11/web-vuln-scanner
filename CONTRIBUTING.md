# Contributing

Thanks for contributing! Please follow these steps.

## Process
1. (Optional for solo work) Open an Issue describing the change/bug before heavy work.
2. Create a branch: `git checkout -b feat/short-desc`.
3. Make small, focused commits. Run tests & linters locally.
4. Open a PR if you want code review; otherwise merge to main.

## Coding style
- Python: Black + Flake8. Target Python >= 3.11.
- Go: gofmt, go vet. Target Go >= 1.20.

## Tests
- Add unit tests under `tests/`.
- Run: `pytest -q`

## PR checklist
- [ ] Tests added/updated
- [ ] Linted (`black .`, `gofmt -w .`)
- [ ] CHANGELOG updated if needed

