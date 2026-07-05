from pathlib import Path
from pytest_bdd import scenarios
from steps.juraregel_steps import *  # noqa: F401,F403
scenarios(str(Path(__file__).parent / "participatiewet.feature"))
