#!/usr/bin/env python3
# Copyright 2010-2025 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reader and solver of the single assembly line balancing problem.

from https://assembly-line-balancing.de/salbp/:

The simple assembly line balancing problem (SALBP) is the basic optimization
problem in assembly line balancing research. Given is a set of tasks each of
which has a deterministic task time. The tasks are partially ordered by
precedence relations defining a precedence graph as depicted below.

It reads .alb files:
    https://assembly-line-balancing.de/wp-content/uploads/2017/01/format-ALB.pdf

and solves the corresponding problem.
"""

import collections
import csv
import json
import os
import re
from typing import Dict, Sequence, Tuple

from absl import app
from absl import flags


from ortools.sat.python import cp_model

_INPUT = flags.DEFINE_string("input", "", "Input file to parse and solve.")
_PARAMS = flags.DEFINE_string("params", "", "Sat solver parameters.")
_OUTPUT_PROTO = flags.DEFINE_string(
    "output_proto", "", "Output file to write the cp_model proto to."
)
_MODEL = flags.DEFINE_string(
    "model", "boolean", "Model used: boolean, scheduling, greedy"
)
_OBJECTIVE = flags.DEFINE_string(
    "objective", "min_stations", "Objective: min_stations|min_manpower|min_idle"
)
_TARGET_TAKT = flags.DEFINE_integer(
    "target_takt", 0, "Target takt time (same unit as task times). Required for min_manpower"
)
_MAX_WORKERS = flags.DEFINE_integer(
    "max_workers_per_station", 8, "Upper bound for workers per station in min_manpower objective"
)
_FIXED_STATIONS = flags.DEFINE_integer(
    "fixed_stations", 0, "Fixed number of stations (for min_idle objective). 0=auto from greedy"
)
_MULTI_OBJECTIVE = flags.DEFINE_string(
    "multi_objective", "", "Multi-objective mode: 'stations_then_idle' | 'manpower_then_idle'"
)
_JSON_OUTPUT = flags.DEFINE_string(
    "json_output", "", "If set, write solution + KPIs JSON to this path"
)

# CSV input/output flags
# _INPUT_FORMAT = flags.DEFINE_string(
#     "input_format", "alb", "Input format: alb | csv"
# )
_TASKS_CSV = flags.DEFINE_string(
    "tasks_csv", "", "Tasks CSV file (for CSV input mode). If empty, uses --input"
)
_PRECEDENCES_CSV = flags.DEFINE_string(
    "precedences_csv", "", "Precedences CSV file (optional, can be in tasks CSV)"
)
_CONFIG_CSV = flags.DEFINE_string(
    "config_csv", "", "Config CSV file (optional, uses command line params if not provided)"
)
_CSV_OUTPUT = flags.DEFINE_string(
    "csv_output", "", "Write solution to CSV (task assignments)"
)
_KPI_CSV = flags.DEFINE_string(
    "kpi_csv", "", "Write KPI summary to CSV"
)
_STATION_CSV = flags.DEFINE_string(
    "station_csv", "", "Write station details to CSV"
)


class SectionInfo:
    """Store problem information for each section of the input file."""

    def __init__(self):
        self.value = None
        self.index_map = {}
        self.set_of_pairs = set()

    def __str__(self):
        if self.index_map:
            return f"SectionInfo(index_map={self.index_map})"
        elif self.set_of_pairs:
            return f"SectionInfo(set_of_pairs={self.set_of_pairs})"
        elif self.value is not None:
            return f"SectionInfo(value={self.value})"
        else:
            return "SectionInfo()"


# ALB format support commented out - CSV input only
# def read_problem(filename: str) -> Dict[str, SectionInfo]:
#     """Reads a .alb file and returns the problem."""
# 
#     current_info = SectionInfo()
# 
#     problem: Dict[str, SectionInfo] = {}
#     with open(filename, "r") as input_file:
#         print(f"Reading problem from '{filename}'")
# 
#         for line in input_file:
#             stripped_line = line.strip()
#             if not stripped_line:
#                 continue
# 
#             match_section_def = re.fullmatch(r"<([\w\s]+)>", stripped_line)
#             if match_section_def:
#                 section_name = match_section_def.group(1)
#                 if section_name == "end":
#                     continue
# 
#                 current_info = SectionInfo()
#                 problem[section_name] = current_info
#                 continue
# 
#             match_single_number = re.fullmatch(r"^([0-9]+)$", stripped_line)
#             if match_single_number:
#                 current_info.value = int(match_single_number.group(1))
#                 continue
# 
#             match_key_value = re.fullmatch(r"^([0-9]+)\s+([0-9]+)$", stripped_line)
#             if match_key_value:
#                 key = int(match_key_value.group(1))
#                 value = int(match_key_value.group(2))
#                 current_info.index_map[key] = value
#                 continue
# 
#             match_pair = re.fullmatch(r"^([0-9]+),([0-9]+)$", stripped_line)
#             if match_pair:
#                 left = int(match_pair.group(1))
#                 right = int(match_pair.group(2))
#                 current_info.set_of_pairs.add((left, right))
#                 continue
# 
#             print(f"Unrecognized line '{stripped_line}'")
# 
#     return problem


def read_problem_from_csv(
    tasks_file: str,
    precedences_file: str = "",
    config_file: str = ""
) -> Dict[str, SectionInfo]:
    """Reads CSV files and returns the problem in SectionInfo format.
    
    Args:
        tasks_file: Path to tasks.csv with columns: task_id, duration, [predecessors]
        precedences_file: Optional path to precedences.csv with: before_task, after_task
        config_file: Optional path to config.csv with: parameter, value
    
    Returns:
        Dict[str, SectionInfo] compatible with existing solvers
    """
    print(f"Reading problem from CSV: '{tasks_file}'")
    
    problem: Dict[str, SectionInfo] = {}
    
    # Initialize sections
    problem["number of tasks"] = SectionInfo()
    problem["task times"] = SectionInfo()
    problem["precedence relations"] = SectionInfo()
    problem["cycle time"] = SectionInfo()
    
    # Read tasks.csv
    task_ids = []
    predecessors_from_tasks = []
    
    with open(tasks_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task_id = int(row["task_id"])
            duration = int(row["duration"])
            task_ids.append(task_id)
            problem["task times"].index_map[task_id] = duration
            
            # Check for predecessors column
            if "predecessors" in row and row["predecessors"].strip():
                preds = [int(p.strip()) for p in row["predecessors"].split(",") if p.strip()]
                for pred in preds:
                    predecessors_from_tasks.append((pred, task_id))
    
    problem["number of tasks"].value = len(task_ids)
    
    # Read precedences.csv if provided, otherwise use predecessors from tasks
    if precedences_file and os.path.exists(precedences_file):
        print(f"  Reading precedences from '{precedences_file}'")
        with open(precedences_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                before = int(row["before_task"])
                after = int(row["after_task"])
                problem["precedence relations"].set_of_pairs.add((before, after))
    else:
        # Use predecessors from tasks.csv
        for before, after in predecessors_from_tasks:
            problem["precedence relations"].set_of_pairs.add((before, after))
    
    # Read config.csv if provided
    if config_file and os.path.exists(config_file):
        print(f"  Reading config from '{config_file}'")
        with open(config_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                param = row["parameter"].strip()
                value = row["value"].strip()
                if param == "cycle_time":
                    problem["cycle time"].value = int(value)
                # Other config params handled by flags, not here
    
    # Set default cycle_time if not provided
    if problem["cycle time"].value is None:
        # Use a reasonable default or sum of all durations / estimate
        total_duration = sum(problem["task times"].index_map.values())
        num_tasks = problem["number of tasks"].value
        problem["cycle time"].value = total_duration // max(1, num_tasks // 3)
        print(f"  Using estimated cycle_time: {problem['cycle time'].value}")
    
    return problem


def write_solution_csv(
    filename: str,
    assignment: Dict[int, int],
    durations: Dict[int, int],
    workers: Dict[int, int]
) -> None:
    """Write task assignment solution to CSV.
    
    Format: task_id, station_index, workers_assigned, task_duration, cumulative_load
    """
    # Group tasks by station
    station_tasks = collections.defaultdict(list)
    for task_id, station in assignment.items():
        station_tasks[station].append(task_id)
    
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["task_id", "station_index", "workers_assigned", "task_duration", "cumulative_load"])
        
        for station_idx in sorted(station_tasks.keys()):
            cumulative = 0
            w = workers.get(station_idx, 1) if workers else 1
            for task_id in sorted(station_tasks[station_idx]):
                duration = durations.get(task_id, 0)
                cumulative += duration
                writer.writerow([task_id, station_idx, w, duration, cumulative])
    
    print(f"Wrote solution CSV to {filename}")


def write_kpi_csv(filename: str, kpis: Dict[str, object], solve_time: float = 0.0) -> None:
    """Write KPI summary to CSV.
    
    Format: metric, value, unit
    """
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "unit"])
        
        writer.writerow(["total_stations", len(kpis.get("stations", [])), "stations"])
        writer.writerow(["total_workers", kpis.get("manpower_total", 0), "persons"])
        writer.writerow(["bottleneck_station", kpis.get("bottleneck_station", ""), ""])
        writer.writerow(["bottleneck_load", kpis.get("bottleneck_load", 0), "time_units"])
        writer.writerow(["calculated_takt", kpis.get("calculated_takt", 0), "time_units"])
        writer.writerow(["target_takt", kpis.get("target_takt", 0), "time_units"])
        writer.writerow(["cycle_time", kpis.get("cycle_time", 0), "time_units"])
        writer.writerow(["avg_utilization", kpis.get("avg_utilization_pct", 0), "percent"])
        writer.writerow(["total_idle_time", kpis.get("total_idle_time", 0), "time_units"])
        writer.writerow(["solve_time", round(solve_time, 3), "seconds"])
    
    print(f"Wrote KPI CSV to {filename}")


def write_station_csv(filename: str, kpis: Dict[str, object], assignment: Dict[int, int]) -> None:
    """Write per-station details to CSV.
    
    Format: station_index, total_load, idle_vs_bottleneck, workers, utilization_pct, assigned_tasks
    """
    # Group tasks by station
    station_tasks = collections.defaultdict(list)
    for task_id, station in assignment.items():
        station_tasks[station].append(task_id)
    
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["station_index", "total_load", "idle_vs_bottleneck", "workers", "utilization_pct", "assigned_tasks"])
        
        stations_info = kpis.get("stations", [])
        for station_info in stations_info:
            station_idx = station_info["station_index"]
            tasks = station_tasks.get(station_idx, [])
            tasks_str = ",".join(str(t) for t in sorted(tasks))
            
            writer.writerow([
                station_idx,
                station_info["load"],
                station_info["idle_vs_bottleneck"],
                station_info["workers"],
                station_info["utilization_pct"],
                tasks_str
            ])
    
    print(f"Wrote station CSV to {filename}")


def print_stats(problem: Dict[str, SectionInfo]) -> None:
    print("Problem Statistics")
    for key, value in problem.items():
        print(f"  - {key}: {value}")


def solve_problem_greedily(problem: Dict[str, SectionInfo]) -> Dict[int, int]:
    """Compute a greedy solution."""
    print("Solving using a Greedy heuristics")

    num_tasks = problem["number of tasks"].value
    if num_tasks is None:
        return {}
    all_tasks = range(1, num_tasks + 1)  # Tasks are 1 based in the data.
    precedences = problem["precedence relations"].set_of_pairs
    durations = problem["task times"].index_map
    cycle_time = problem["cycle time"].value

    weights = collections.defaultdict(int)
    successors = collections.defaultdict(list)

    candidates = set(all_tasks)

    for before, after in precedences:
        weights[after] += 1
        successors[before].append(after)
        if after in candidates:
            candidates.remove(after)

    assignment: Dict[int, int] = {}
    current_pod = 0
    residual_capacity = cycle_time

    while len(assignment) < num_tasks:
        if not candidates:
            print("error empty")
            break

        best = -1
        best_slack = cycle_time
        best_duration = 0

        for c in candidates:
            duration = durations[c]
            slack = residual_capacity - duration
            if slack < best_slack and slack >= 0:
                best_slack = slack
                best = c
                best_duration = duration

        if best == -1:
            current_pod += 1
            residual_capacity = cycle_time
            continue

        candidates.remove(best)
        assignment[best] = current_pod
        residual_capacity -= best_duration

        for succ in successors[best]:
            weights[succ] -= 1
            if weights[succ] == 0:
                candidates.add(succ)
                del weights[succ]

    print(f"  greedy solution uses {current_pod + 1} pods.")

    return assignment


def solve_problem_with_boolean_model(
    problem: Dict[str, SectionInfo], hint: Dict[int, int]
) -> Dict[int, int]:
    """Solve the given problem minimizing stations. Returns assignment (task->station)."""

    print("Solving using the Boolean model")
    # problem data
    num_tasks = problem["number of tasks"].value
    if num_tasks is None:
        return {}
    all_tasks = range(1, num_tasks + 1)  # Tasks are 1 based in the problem.
    durations = problem["task times"].index_map
    precedences = problem["precedence relations"].set_of_pairs
    cycle_time = problem["cycle time"].value

    num_pods = max(p for _, p in hint.items()) + 1 if hint else num_tasks - 1
    all_pods = range(num_pods)

    model = cp_model.CpModel()

    # assign[t, p] indicates if task t is done on pod p.
    assign = {}
    # possible[t, p] indicates if task t is possible on pod p.
    possible = {}

    # Create the variables
    for t in all_tasks:
        for p in all_pods:
            assign[t, p] = model.new_bool_var(f"assign_{t}_{p}")
            possible[t, p] = model.new_bool_var(f"possible_{t}_{p}")

    # active[p] indicates if pod p is active.
    active = [model.new_bool_var(f"active_{p}") for p in all_pods]

    # Each task is done on exactly one pod.
    for t in all_tasks:
        model.add_exactly_one([assign[t, p] for p in all_pods])

    # Total tasks assigned to one pod cannot exceed cycle time.
    for p in all_pods:
        model.add(sum(assign[t, p] * durations[t] for t in all_tasks) <= cycle_time)

    # Maintain the possible variables:
    #   possible at pod p -> possible at any pod after p
    for t in all_tasks:
        for p in range(num_pods - 1):
            model.add_implication(possible[t, p], possible[t, p + 1])

    # Link possible and active variables.
    for t in all_tasks:
        for p in all_pods:
            model.add_implication(assign[t, p], possible[t, p])
            if p > 1:
                model.add_implication(assign[t, p], ~possible[t, p - 1])

    # Precedences.
    for before, after in precedences:
        for p in range(1, num_pods):
            model.add_implication(assign[before, p], ~possible[after, p - 1])

    # Link active variables with the assign one.
    for p in all_pods:
        all_assign_vars = [assign[t, p] for t in all_tasks]
        for a in all_assign_vars:
            model.add_implication(a, active[p])
        model.add_bool_or(all_assign_vars + [~active[p]])

    # Force pods to be contiguous. This is critical to get good lower bounds
    # on the objective, even if it makes feasibility harder.
    for p in range(1, num_pods):
        model.add_implication(~active[p - 1], ~active[p])
        for t in all_tasks:
            model.add_implication(~active[p], possible[t, p - 1])

    # Objective.
    model.minimize(sum(active))

    # add search hinting from the greedy solution.
    for t in all_tasks:
        model.add_hint(assign[t, hint[t]], 1)

    if _OUTPUT_PROTO.value:
        print(f"Writing proto to {_OUTPUT_PROTO.value}")
        model.export_to_file(_OUTPUT_PROTO.value)

    # solve model.
    solver = cp_model.CpSolver()
    if _PARAMS.value:
        solver.parameters.parse_text_format(_PARAMS.value)
    solver.parameters.log_search_progress = True
    solver.solve(model)

    assignment: Dict[int, int] = {}
    for t in all_tasks:
        for p in all_pods:
            if solver.boolean_value(assign[t, p]):
                assignment[t] = p
                break
    if assignment:
        used = len(set(assignment.values()))
        print(f"  boolean model uses {used} stations")
    return assignment

def solve_problem_with_manpower_model(
    problem: Dict[str, SectionInfo], hint: Dict[int, int]
) -> Tuple[Dict[int, int], Dict[int, int]]:
    """Solve with objective = minimize total manpower (workers).

    Modeling approach:
    - Binary assign[t,p] => task t on station p.
    - Integer workers[p] in [0, max_workers].
    - Load_p = sum_t assign[t,p] * duration_t.
      Capacity constraint: Load_p <= workers[p] * target_takt.
    - station_of[t] linearized: sum_p assign[t,p]*p == station_of[t].
    - Precedence: station_of[after] >= station_of[before].
    - Objective: minimize sum(workers[p]). (Stations with workers=0 will be empty.)
    Upper bound on number of stations (num_pods): we take max(greedy_used*2, greedy_used+3) but not above num_tasks.
    """
    print("Solving using manpower minimization model")
    num_tasks = problem["number of tasks"].value
    if num_tasks is None:
        return {}, {}
    all_tasks = range(1, num_tasks + 1)
    durations = problem["task times"].index_map
    precedences = problem["precedence relations"].set_of_pairs
    cycle_time = problem["cycle time"].value

    if _TARGET_TAKT.value <= 0:
        raise ValueError("--target_takt must be > 0 for objective=min_manpower")
    takt = _TARGET_TAKT.value
    max_workers = _MAX_WORKERS.value if _MAX_WORKERS.value > 0 else 8

    greedy_used = max(hint.values()) + 1 if hint else num_tasks
    num_pods = min(num_tasks, max(greedy_used * 2, greedy_used + 3))
    all_pods = range(num_pods)

    model = cp_model.CpModel()

    # Variables
    assign = {}
    for t in all_tasks:
        for p in all_pods:
            assign[t, p] = model.new_bool_var(f"assign_{t}_{p}")

    # Each task exactly one station.
    for t in all_tasks:
        model.add_exactly_one([assign[t, p] for p in all_pods])

    # workers per station.
    workers = [model.new_int_var(0, max_workers, f"workers_{p}") for p in all_pods]

    # Station load capacity constraints.
    for p in all_pods:
        load_expr = sum(assign[t, p] * durations[t] for t in all_tasks)
        model.add(load_expr <= workers[p] * takt)

    # station_of task int vars.
    station_of = {}
    for t in all_tasks:
        station_var = model.new_int_var(0, num_pods - 1, f"station_{t}")
        station_of[t] = station_var
        # Linearization: sum(assign[t,p]*p) == station_var
        model.add(sum(assign[t, p] * p for p in all_pods) == station_var)

    # Precedence constraints.
    for before, after in precedences:
        model.add(station_of[after] >= station_of[before])

    # Optional: ensure ordering uses workers if any task assigned; if workers[p]==0 then no task.
    for p in all_pods:
        # If workers[p] == 0 then no tasks may be assigned: sum(assign[t,p]) == 0
        # This is automatically enforced by load <= 0, but load expression integer might allow tasks whose durations are 0.
        # Add explicit disallow: sum(assign[t,p]) <= workers[p] * num_tasks
        model.add(sum(assign[t, p] for t in all_tasks) <= workers[p] * num_tasks)

    # Hints from greedy solution.
    if hint:
        for t, p in hint.items():
            if p < num_pods:
                model.add_hint(assign[t, p], 1)

    # Objective: minimize total workers.
    model.minimize(sum(workers))

    solver = cp_model.CpSolver()
    if _PARAMS.value:
        solver.parameters.parse_text_format(_PARAMS.value)
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No feasible manpower solution")
        return {}, {}

    assignment: Dict[int, int] = {}
    workers_solution: Dict[int, int] = {}
    for p in all_pods:
        w = int(solver.value(workers[p]))
        if w > 0:
            workers_solution[p] = w
    for t in all_tasks:
        for p in all_pods:
            if solver.boolean_value(assign[t, p]):
                assignment[t] = p
                break

    print(
        f"  manpower model uses {len(workers_solution)} stations, total workers={sum(workers_solution.values())}."
    )
    return assignment, workers_solution

def solve_problem_with_idle_model(
    problem: Dict[str, SectionInfo], hint: Dict[int, int], fixed_stations: int = 0
) -> Dict[int, int]:
    """Solve with objective = minimize total idle time.
    
    Modeling approach:
    - Binary assign[t,p] => task t on station p.
    - Fixed number of stations (from --fixed_stations or greedy hint).
    - Load_p = sum_t assign[t,p] * duration_t.
    - idle[p] = cycle_time - load[p] (or bottleneck - load[p]).
    - Capacity: load[p] <= cycle_time.
    - Objective: minimize sum(idle[p]) = minimize (num_stations * cycle_time - total_duration).
      Since total_duration is constant, this is equivalent to minimizing max(load) if we use
      bottleneck-based idle, OR minimizing sum of squared deviations for balance.
    
    For simplicity: minimize sum of (cycle_time - load_p) = constant - sum(load_p).
    Better: minimize max_load (bottleneck) for fixed stations.
    """
    print("Solving using idle minimization model")
    num_tasks = problem["number of tasks"].value
    if num_tasks is None:
        return {}
    all_tasks = range(1, num_tasks + 1)
    durations = problem["task times"].index_map
    precedences = problem["precedence relations"].set_of_pairs
    cycle_time = problem["cycle time"].value

    # Determine fixed station count
    if fixed_stations <= 0:
        fixed_stations = max(hint.values()) + 1 if hint else num_tasks
        print(f"  Using {fixed_stations} stations (from greedy hint)")
    else:
        print(f"  Using {fixed_stations} fixed stations")
    
    num_pods = fixed_stations
    all_pods = range(num_pods)

    model = cp_model.CpModel()

    # Variables
    assign = {}
    for t in all_tasks:
        for p in all_pods:
            assign[t, p] = model.new_bool_var(f"assign_{t}_{p}")

    # Each task exactly one station
    for t in all_tasks:
        model.add_exactly_one([assign[t, p] for p in all_pods])

    # Load variables per station
    loads = []
    for p in all_pods:
        load_p = model.new_int_var(0, cycle_time, f"load_{p}")
        model.add(load_p == sum(assign[t, p] * durations[t] for t in all_tasks))
        loads.append(load_p)

    # station_of for precedence
    station_of = {}
    for t in all_tasks:
        station_var = model.new_int_var(0, num_pods - 1, f"station_{t}")
        station_of[t] = station_var
        model.add(sum(assign[t, p] * p for p in all_pods) == station_var)

    # Precedence constraints
    for before, after in precedences:
        model.add(station_of[after] >= station_of[before])

    # Objective: minimize bottleneck (max load) for better balance
    # Alternatively: minimize sum of idle = num_pods * max_load - total_duration (constant term)
    # We choose: minimize max_load (makespan-like for fixed stations)
    max_load = model.new_int_var(0, cycle_time, "max_load")
    for load_p in loads:
        model.add(max_load >= load_p)
    
    model.minimize(max_load)

    # Hints
    if hint:
        for t, p in hint.items():
            if p < num_pods:
                model.add_hint(assign[t, p], 1)

    solver = cp_model.CpSolver()
    if _PARAMS.value:
        solver.parameters.parse_text_format(_PARAMS.value)
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No feasible idle solution")
        return {}

    assignment: Dict[int, int] = {}
    for t in all_tasks:
        for p in all_pods:
            if solver.boolean_value(assign[t, p]):
                assignment[t] = p
                break
    
    bottleneck = int(solver.value(max_load))
    total_load = sum(durations.values())
    total_idle = num_pods * bottleneck - total_load
    print(f"  idle model: bottleneck={bottleneck}, total_idle={total_idle}")
    return assignment

def compute_kpis(
    assignment: Dict[int, int],
    durations: Dict[int, int],
    takt: int,
    workers: Dict[int, int] | None,
    cycle_time: int,
) -> Dict[str, object]:
    """Compute KPI dictionary for output."""
    loads = collections.defaultdict(int)
    for t, p in assignment.items():
        loads[p] += durations[t]
    if not loads:
        return {}
    bottleneck_p = max(loads, key=lambda k: loads[k])
    bottleneck_load = loads[bottleneck_p]
    effective_takt = bottleneck_load  # Derived takt from assignment
    stations_info = []
    for p in sorted(loads):
        load = loads[p]
        idle_vs_bottleneck = bottleneck_load - load
        w = workers.get(p, 1) if workers else 1
        utilization = (load / (w * takt)) * 100 if takt > 0 and w > 0 else 0.0
        stations_info.append(
            {
                "station_index": p,
                "load": load,
                "idle_vs_bottleneck": idle_vs_bottleneck,
                "workers": w,
                "utilization_pct": round(utilization, 2),
            }
        )
    manpower_total = sum(workers.values()) if workers else len(loads)
    avg_util = (
        sum(s["utilization_pct"] for s in stations_info) / len(stations_info)
        if stations_info
        else 0.0
    )
    
    # Calculate total idle time
    total_idle = sum(s["idle_vs_bottleneck"] for s in stations_info)
    
    return {
        "stations": stations_info,
        "bottleneck_station": bottleneck_p,
        "bottleneck_load": bottleneck_load,
        "calculated_takt": effective_takt,
        "target_takt": takt,
        "cycle_time": cycle_time,
        "manpower_total": manpower_total,
        "avg_utilization_pct": round(avg_util, 2),
        "total_idle_time": total_idle,
    }


def solve_problem_with_scheduling_model(
    problem: Dict[str, SectionInfo], hint: Dict[int, int]
) -> Dict[int, int]:
    """Solve using a cumulative model minimizing last station index. Returns assignment."""

    print("Solving using the scheduling model")
    # Problem data
    num_tasks = problem["number of tasks"].value
    if num_tasks is None:
        return {}
    all_tasks = range(1, num_tasks + 1)  # Tasks are 1 based in the data.
    durations = problem["task times"].index_map
    precedences = problem["precedence relations"].set_of_pairs
    cycle_time = problem["cycle time"].value

    num_pods = max(p for _, p in hint.items()) + 1 if hint else num_tasks

    model = cp_model.CpModel()

    # pod[t] indicates on which pod the task is performed.
    pods = {}
    for t in all_tasks:
        pods[t] = model.new_int_var(0, num_pods - 1, f"pod_{t}")

    # Create the variables
    intervals = []
    demands = []
    for t in all_tasks:
        interval = model.new_fixed_size_interval_var(pods[t], 1, "")
        intervals.append(interval)
        demands.append(durations[t])

    # add terminating interval as the objective.
    obj_var = model.new_int_var(1, num_pods, "obj_var")
    obj_size = model.new_int_var(1, num_pods, "obj_duration")
    obj_interval = model.new_interval_var(
        obj_var, obj_size, num_pods + 1, "obj_interval"
    )
    intervals.append(obj_interval)
    demands.append(cycle_time)

    # Cumulative constraint.
    model.add_cumulative(intervals, demands, cycle_time)

    # Precedences.
    for before, after in precedences:
        model.add(pods[after] >= pods[before])

    # Objective.
    model.minimize(obj_var)

    # add search hinting from the greedy solution.
    for t in all_tasks:
        model.add_hint(pods[t], hint[t])

    if _OUTPUT_PROTO.value:
        print(f"Writing proto to{_OUTPUT_PROTO.value}")
        model.export_to_file(_OUTPUT_PROTO.value)

    # solve model.
    solver = cp_model.CpSolver()
    if _PARAMS.value:
        solver.parameters.parse_text_format(_PARAMS.value)
    solver.parameters.log_search_progress = True
    solver.solve(model)

    assignment: Dict[int, int] = {}
    # Extract station from pods int var values using greedy hint as fallback
    for t in all_tasks:
        val = int(solver.value(pods[t]))
        assignment[t] = val
    used = len(set(assignment.values())) if assignment else 0
    print(f"  scheduling model uses {used} stations")
    return assignment


def main(argv: Sequence[str]) -> None:
    if len(argv) > 1:
        raise app.UsageError("Too many command-line arguments.")

    # Read problem from CSV format only
    import time
    start_time = time.time()
    
    # CSV input only
    tasks_file = _TASKS_CSV.value if _TASKS_CSV.value else _INPUT.value
    if not tasks_file:
        raise ValueError("Must provide --tasks_csv or --input for CSV input")
    problem = read_problem_from_csv(
        tasks_file,
        _PRECEDENCES_CSV.value,
        _CONFIG_CSV.value
    )
    
    # ALB format support commented out
    # if _INPUT_FORMAT.value.lower() == "csv":
    #     tasks_file = _TASKS_CSV.value if _TASKS_CSV.value else _INPUT.value
    #     if not tasks_file:
    #         raise ValueError("Must provide --tasks_csv or --input for CSV mode")
    #     problem = read_problem_from_csv(
    #         tasks_file,
    #         _PRECEDENCES_CSV.value,
    #         _CONFIG_CSV.value
    #     )
    # else:
    #     problem = read_problem(_INPUT.value)
    
    print_stats(problem)
    greedy_solution = solve_problem_greedily(problem)
    durations = problem["task times"].index_map if "task times" in problem else {}
    cycle_time = problem["cycle time"].value if "cycle time" in problem else 0

    assignment: Dict[int, int] = {}
    workers_solution: Dict[int, int] = {}

    # Multi-objective mode: two-phase optimization
    if _MULTI_OBJECTIVE.value:
        mode = _MULTI_OBJECTIVE.value.lower()
        print(f"\n=== Multi-objective mode: {mode} ===")
        
        if mode == "stations_then_idle":
            # Phase 1: minimize stations
            print("\nPhase 1: Minimizing stations...")
            assignment = solve_problem_with_boolean_model(problem, greedy_solution)
            if not assignment:
                print("Phase 1 failed, using greedy")
                assignment = greedy_solution
            
            # Phase 2: minimize idle with fixed stations
            num_stations = len(set(assignment.values()))
            print(f"\nPhase 2: Minimizing idle time with {num_stations} fixed stations...")
            assignment = solve_problem_with_idle_model(problem, assignment, num_stations)
            
        elif mode == "manpower_then_idle":
            # Phase 1: minimize manpower
            print("\nPhase 1: Minimizing manpower...")
            assignment, workers_solution = solve_problem_with_manpower_model(problem, greedy_solution)
            if not assignment:
                print("Phase 1 failed, using greedy")
                assignment = greedy_solution
            
            # Phase 2: minimize idle with fixed stations (and workers)
            num_stations = len(set(assignment.values()))
            print(f"\nPhase 2: Minimizing idle time with {num_stations} fixed stations...")
            assignment_idle = solve_problem_with_idle_model(problem, assignment, num_stations)
            if assignment_idle:
                assignment = assignment_idle
        else:
            raise ValueError(f"Unknown multi_objective mode: {mode}")
    
    # Single objective mode
    elif _OBJECTIVE.value == "min_manpower":
        assignment, workers_solution = solve_problem_with_manpower_model(problem, greedy_solution)
    elif _OBJECTIVE.value == "min_idle":
        fixed = _FIXED_STATIONS.value if _FIXED_STATIONS.value > 0 else 0
        assignment = solve_problem_with_idle_model(problem, greedy_solution, fixed)
    else:  # min_stations or default
        if _MODEL.value == "boolean":
            assignment = solve_problem_with_boolean_model(problem, greedy_solution)
        elif _MODEL.value == "scheduling":
            assignment = solve_problem_with_scheduling_model(problem, greedy_solution)
        else:  # greedy
            assignment = greedy_solution

    # KPI & JSON output
    solve_time = time.time() - start_time
    
    if _OBJECTIVE.value == "min_manpower" and _TARGET_TAKT.value > 0:
        kpis = compute_kpis(
            assignment, durations, _TARGET_TAKT.value, workers_solution, cycle_time
        )
    else:
        # default KPI uses cycle_time as takt reference
        kpis = compute_kpis(assignment, durations, cycle_time, workers_solution, cycle_time)

    # JSON output
    if _JSON_OUTPUT.value:
        output_obj = {
            "input_file": _INPUT.value,
            "objective": _OBJECTIVE.value,
            "multi_objective": _MULTI_OBJECTIVE.value,
            "model": _MODEL.value,
            "assignment": assignment,
            "workers": workers_solution,
            "kpis": kpis,
            "solve_time_seconds": round(solve_time, 3),
        }
        with open(_JSON_OUTPUT.value, "w", encoding="utf-8") as f:
            json.dump(output_obj, f, ensure_ascii=False, indent=2)
        print(f"Wrote JSON output to {_JSON_OUTPUT.value}")
    
    # CSV outputs
    if _CSV_OUTPUT.value:
        write_solution_csv(_CSV_OUTPUT.value, assignment, durations, workers_solution)
    
    if _KPI_CSV.value:
        write_kpi_csv(_KPI_CSV.value, kpis, solve_time)
    
    if _STATION_CSV.value:
        write_station_csv(_STATION_CSV.value, kpis, assignment)
        print(f"Wrote JSON output to {_JSON_OUTPUT.value}")


if __name__ == "__main__":
    app.run(main)