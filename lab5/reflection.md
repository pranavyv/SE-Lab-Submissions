# Reflection

**1. Which tool did you find most useful, and why?**
Bandit surfaced the findings that matter most (`eval` allowing arbitrary code, a weak-hash call, a hardcoded password), and it ranks them by severity and confidence, so it tells you what to fix first. Pylint gave the broadest coverage, taking the score from 4.48 to 10.00, and caught the mutable default argument and the leaking file handles. Flake8 is the quickest to act on, since almost everything it reports is mechanical.

**2. Did you encounter any false positives, or findings you disagreed with?**
Yes, two. Bandit rated `hashlib.md5` as High, but here it only makes a short fingerprint for bin labels, so the right response was `usedforsecurity=False` and a comment, not a new hash that would change every printed label. After I introduced a constant named `PASSWORD_ENV_VAR`, Bandit's B105 flagged it as a hardcoded password even though it only holds an environment variable's name; renaming it was cleaner than adding a `# nosec`. Pylint's `eval-used` also overlaps with Bandit's B307, so one root problem produced two warnings.

**3. How could you integrate these tools into your workflow?**
Run Flake8 and Pylint in a pre-commit hook for fast feedback, and run all three in CI on every pull request, failing the build on any Bandit High/Medium finding and on a Pylint score below a threshold (for example 9.5). Editor integration shows issues as I type. Keep the config (`.pylintrc`, `setup.cfg`/`.flake8`, a Bandit config) in the repo so everyone gets the same rules.

**4. What tangible improvements did you see in the code?**
Security: arbitrary-code execution through `eval` is gone, the password is no longer in source, and failed logins are logged. Robustness: no more silent `except: pass`, files are closed reliably, and the mutable default no longer leaks state. Correctness: the program no longer accepts negative quantities or integer SKUs, and it refuses to remove more stock than exists. Readability: snake_case names, docstrings and PEP 8 layout. The score went from 4.48 to 10.00, Bandit from 5 findings to 0, and Flake8 from 19 to 0. The tools did not catch the three behavioural bugs (negative stock, int SKU, over-removal); I found those by reading the program's own output, so static analysis complements testing and review rather than replacing them.
