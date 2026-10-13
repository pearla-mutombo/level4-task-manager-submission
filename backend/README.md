# Student backend starter

This folder intentionally contains **no completed Flask application**. Start Day 1 by opening `app.py` and building it with the guide. Running Flask before that work is complete will report that it cannot find an application; that is expected.

Copy this folder into the student's **separate application repository** as `backend`. Do not include instructor-reference folders in the student's initial handout.

## First setup on macOS

From the student's `backend` directory:

```zsh
python3.13 --version
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

A virtual environment gives this project its own Python and installed packages. A successful installation finishes without an error. Confirm the interpreter belongs to the project:

```zsh
python -c 'import sys; print(sys.executable)'
```

The printed path should end in `backend/.venv/bin/python`.

After completing the Day 1 app.py, start it:

```zsh
python -m flask --app app run --debug --host 127.0.0.1 --port 5001
```

Keep this terminal running. Control-C stops Flask. `deactivate` leaves the virtual environment after class. On another day, activate the environment again before starting Flask. No dependency reinstall is needed unless requirements change.

The fixed backend address is **http://127.0.0.1:5001**. Use a second terminal for React on **http://127.0.0.1:5173**.

## Included files

- `app.py`: construction prompts, with no route answers.
- `requirements.txt`: pinned application packages.
- `requirements-dev.txt`: application packages plus pytest for Thursday.
- `.gitignore`: excludes local environments, caches, and private configuration.
- `.env.example`: the public example origin, used starting Thursday. Create a local `.env` then; it is not committed.

Follow the daily guides to add task behavior, then `store.py`, `validation.py`, and tests. Business data stays in memory throughout Week 1. The JSON-file exercise is separate.
