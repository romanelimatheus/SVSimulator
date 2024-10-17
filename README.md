# SV Simulator

Implementation of Sampled Values IEC61850 packet fuzzer.

### Recommendation

```bash
# install dependencies
make install-dev

# validate code
make pytest
make ruff
make mypy

# fix code
make ruff-fix
```

## Conventions

The following sections describe the naming conventions for branches and commits.

References:
 - https://dev.to/varbsan/a-simplified-convention-for-naming-branches-and-commits-in-git-il4
 - https://dev.to/couchcamote/git-branching-name-convention-cch

### Branch

`<category/description-here/issue-optional>`

Category:
- feature: adding, refactoring or removing a feature
- bugfix: bug fixing
- hotfix: temporary solution, emergency

#### Examples

```
feature/add-new-mms-service/123
bugfix/old-mms-service-not-working
hotfix/new-mms-service-bug/124
```

### Commit

`<category: commit description>`

category:
- feat: is for adding a new feature
- fix: is for fixing a bug
- refactor: is for changing code for peformance or convenience purpose (e.g. readibility)
- chore: is for everything else (writing documentation, formatting, adding tests, cleaning useless code etc.)

#### Examples

```
feature: add new mms service
fix, matheus: old mms service not working
refactor: old mms service
chore: pep8/ruff, docs and tests
```


