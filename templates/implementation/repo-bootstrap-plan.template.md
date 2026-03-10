# [Scenario Name]: Repo Bootstrap Plan

## Summary

Use this document for the one-time bootstrap work that establishes the smallest
runnable local baseline for the current PoC slice.

This document owns scaffold, tooling, local runtime, and privacy-seam setup. It
does **not** own fixture-driven PoC behavior implementation; that belongs in
the acceptance-contract plan.

## Current Source Inputs

- Root tracker: `<root_tracker_path>`
- Slice anchor: `<slice_anchor_path>`
- Tree A code map: `<tree_a_code_map_path>`
- Repo patterns: `<repo_patterns_path>`

## Bootstrap Scope

Create the smallest runnable baseline for:

- `<project_config_file>`
- `<package_manager_or_env_tool>`
- `<formatter_or_linter>`
- `<type_checker>`
- `<env_example_file>`
- `<graph_runtime_config>`
- minimal app, driver, and test folders

Add thin local delivery scaffolding for:

- `<primary_ui_shell>`
- `<thin_api_shell>`
- `<dockerfile_path>`
- `<local_compose_path>`
- `<tiltfile_path>`

Add workspace bootstrap for:

- `<editor_extensions_path>`
- `<editor_settings_path>`
- `<editor_launch_path>`

## Out Of Scope

This document does not own:

- fixture creation or acceptance-case truth
- workflow behavior, routing logic, or graph-step implementation
- live external model integration beyond the explicit privacy seam contract
- broader platform structure, persistence, workers, or non-local deployment work
- demo rehearsal, presentation assets, or broader validation posture

## Local Runtime Defaults

Runtime development defaults:

- primary dev loop: `<primary_dev_command>`
- debug loop: `<debug_command>`
- tracing posture: `<initial_tracing_default>`

Standardized task runner targets should include:

- `<install_target>`
- `<dev_target>`
- `<debug_target>`
- `<api_target>`
- `<ui_target>`
- `<test_target>`
- `<local_runtime_target>`

## Privacy Seam Bootstrap

Define one explicit provider-agnostic privacy boundary before any external
model call:

- contract name: `<privacy_contract_name>`
- raw input in
- tokenized safe text and safe context out
- reversible token map out

Planned implementations behind the same contract:

- deterministic baseline implementation for the core slice
- optional stretch implementation: `<stretch_privacy_path>`

## Tooling Defaults

Recommended workspace or editor extensions:

- `<extension_1>`
- `<extension_2>`
- `<extension_3>`

Recommended workspace settings:

- `<setting_1>`
- `<setting_2>`
- `<setting_3>`

## Ordered Implementation Steps

1. Inspect the current repo first and extend existing files or structure instead
   of recreating them.
2. Establish the project baseline with the minimum config and tooling files.
3. Add only the minimum app, driver, and test folder scaffold needed for the
   current slice.
4. Add the task-runner targets that support install, local development,
   debugging, UI, API, tests, and local runtime helpers.
5. Add thin delivery shells, keeping the primary demo UI and the thin API shell
   aligned to the same future workflow path.
6. Add the thinnest viable local runtime and deploy scaffold.
7. Add the workspace bootstrap and ensure the debugger path lines up with the
   runtime debug command.
8. Define the explicit privacy seam as bootstrap structure only, without
   implementing the broader workflow or live-model path in this pass.

## Bootstrap Done Criteria

Bootstrap is complete when:

- the repo has a runnable local scaffold
- thin baseline tooling is in place
- the development loop can start locally
- the debugger attach path is ready for use
- the privacy seam is explicit before any live external model integration

## Verification

Verify the bootstrap pass with the smallest practical checks:

- confirm the new baseline files and folders exist and are internally consistent
- run the repo formatting or lint checks that apply to the files you changed
- run the install path that lands in the repo
- start the primary local development loop and confirm the baseline config is
  wired
- start the UI shell and API shell and confirm both boot as thin stubs
- confirm the debugger configuration targets the runtime debug command
- confirm the privacy seam is explicit in code structure before any live
  external model wiring exists

## Completion Report

Report the following at the end of a bootstrap pass:

- changed files
- which bootstrap scope items were completed
- checks run and their results
- any bootstrap gaps intentionally deferred
- any existing repo structure you reused instead of recreating
- anything that still blocks the acceptance-contract implementation pass

## Assumptions

- this document owns setup/bootstrap only, not fixture truth or PoC behavior
- broader platform structure is optional and should not be introduced unless it
  clearly strengthens the current slice
- the primary demo UI remains the main demo surface
- the API remains a thin ingress over the same future workflow path
