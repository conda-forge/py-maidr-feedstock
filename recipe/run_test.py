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
    "fetch_script",
    # #18: this seems kinda vibe-broken
    "test_pieplot",
    # #20: not sure
    "a_log_axis_answers_its_limits_and_its_ticks_in_different_spaces",
    "no_new_module_stashes_maidr_state_on_an_axes",
    # #21: missing test fixtures
    "gallery_examples",
    "every_classifier_is_tested",
    "every_tested_version_is_claimed",
    "contributing_names_the_ci_matrix",
    "every_documented_command_exists",
    "every_documented_key_is_unchanged",
    "a_ctrl_binding_says_cmd_in_the_mac_column",
    "every_maidr_id_a_selector_names_is_in_the_svg",
    "every_point_layer_selector_resolves_one_marker_per_point",
    # #21: maybe more dependency drift?
    "a_user_gid_survives_a_draw_and_keys_its_selector",
    "a_rendered_bar_chart_carries_one_selector_per_bar",
    "a_swarm_resolves_to_the_markers_seaborn_packed",
    # #23: unknown missing path layers?
    "inline_markers_resolve_to_the_points_they_draw",
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
    "--html=pytest.html",
    "--self-contained-html",
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
    # unlink(*[Path(f"src/tests/{p}") for p in UNLINK_TESTS])
    sys.exit(do(*TEST_ARGS) or do(*REPORT_ARGS))
