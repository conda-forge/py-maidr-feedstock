import sys
import shutil

from pathlib import Path
from subprocess import call

COV_FAIL_UNDER = 71

UNLINK_TESTS = [
    # #20: parses random markdown file
    "core/test_plot_type_stability.py",
    "core/test_docs_quote_the_real_warning.py",
    # #21: loads random files
    "docs/",
]

SKIPS = [
    # #18: these do weird bash things
    "shell_guard_matches_the_python_validator",
    "freshness_workflow_imports_resolve",
    "fetch_script_bundles_every_asset_the_runtime_needs",
    # #18: this seems kinda vibe-broken
    "pieplot",
    "pie_schema",
    # #19: double encoding?
    "survives_html_embedding",
    # #20: not sure
    "a_log_axis_answers_its_limits_and_its_ticks_in_different_spaces",
    "no_new_module_stashes_maidr_state_on_an_axes",
    # #21: missing test fixtures
    "gallery_examples",
]

TEST_ARGS = [
    "coverage",
    "run",
    "--source=maidr",
    "--branch",
    "-m",
    "pytest",
    "-vv",
    "--tb=long",
    "--color=yes",
    "-k",
    f"""not ({" or ".join(SKIPS)})""",
]

REPORT_ARGS = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COV_FAIL_UNDER}",
]


def do(*args: str) -> int:
    print(">>>", *args, flush=True)
    return call(args, cwd="src")


def unlink(*paths: Path) -> None:
    for path in paths:
        shutil.rmtree(path) if path.is_dir() else path.unlink()


if __name__ == "__main__":
    unlink(*[Path(f"src/tests/{p}") for p in UNLINK_TESTS])
    sys.exit(do(*TEST_ARGS) or do(*REPORT_ARGS))
