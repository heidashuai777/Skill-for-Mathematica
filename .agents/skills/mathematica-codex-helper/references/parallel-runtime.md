# Parallel runtime: use the machine without overwhelming it

Read this for expensive stages, independent tasks or memory-heavy computations. These are execution instructions, not a request to build a scheduling framework. Use the existing local evaluator, process tools or job scheduler. Keep one sectioned scientific source where practical. Thresholds below are adjustable project defaults, not Wolfram requirements or guaranteed safe limits.

## Always seek acceleration; do not parallelise blindly

First remove avoidable work: reuse unchanged expensive results, factor common computations, use a targeted algebraic transformation, exploit established symmetries and process only required terms. Then consider parallel kernels, concurrent independent programs, numerical compilation, sparse/packed representations or another documented method. Preserve precision, assumptions, regulator orders and analytic branches.

Use an already-observed timing or a small representative pilot. Compare useful wall-clock work, including startup, package loading, data transfer and collection. Do not rerun a complete hours-long calculation merely to benchmark it. Reuse valid pilot results. Cheap work or a strongly sequential dependency may remain serial; briefly record a non-obvious reason in an existing comment, not a new report. Do not add parallel infrastructure to a millisecond calculation.

For similar independent inputs, [ParallelMap](https://reference.wolfram.com/language/ref/ParallelMap.html) or ParallelTable may fit. Wolfram documents a trade-off between scheduling overhead and load balancing: coarse batches suit comparable work; variable-duration jobs need smaller, still useful batches. Parallel execution can differ when there are side effects. Check the actual workload rather than decorating arbitrary code with Parallelize.

## Preflight: one resource owner for all tasks

Before launching expensive work, inspect the actual execution host, not the chat container or remembered hardware. Determine effective CPU availability, current free memory headroom, relevant kernel licence limits, active task-owned processes and any scheduler/container caps. Never infer available RAM or kernel licences from GPU model or physical core count.

On Linux/Fedora, use CPU affinity and effective cgroup CPU quotas; read /proc/meminfo and resolve the process's actual cgroup and its limiting ancestors. Do not assume /sys/fs/cgroup itself is the workload's cgroup. memory.current includes descendants; a finite memory.max can be inherited from an ancestor. cpu.max can limit usable CPU bandwidth below the number of visible cores. See the [kernel cgroup documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html). On other systems use the corresponding available process/scheduler metrics and limits. Unknown limits are not unlimited resources.

Keep a small in-memory job list: task ID, dependencies, process/evaluation handle, allocated CPU, estimated peak RAM, observed status and result handle. One coordinator admits work across all Codex agents; each agent must not independently allocate the whole machine. No extra agents are needed merely to launch several Mathematica processes.

## A shared CPU and memory budget

Let C be this workload's approved CPU capacity, after reserving capacity for other active work. Count each job's master, all its subkernels and native-library/external-program threads in its allocation c_i. Enforce sum(c_i) <= C across simultaneous jobs. The actual accounting can reserve coordinator capacity separately; never count a master and its pool as one CPU. Disable unplanned nested parallelism through documented task-local settings, and verify observed process/thread activity. A thread-count environment variable is not a universal guarantee. Do not change machine-wide settings or shut down unrelated user sessions.

Prefer one level of parallelism initially: several single-worker jobs, or one job with a bounded pool. A mixed allocation is allowed only after it fits the same budget. Honour separate main-kernel and subkernel licence limits; if launch fails, read the message and reduce concurrency rather than repeatedly spawning. [LaunchKernels](https://reference.wolfram.com/language/ref/LaunchKernels.html) supports an explicit local worker count, subject to licence/configuration constraints. LaunchKernels[n] adds workers to ones already running; it is not a total-pool cap. Inspect the existing count and ownership first, and read back the actual count after launch.

For memory, select a conservative workload cap B and reserve R for host responsiveness and unexpected growth. As a starting policy, preserve roughly 25% of effective RAM and target no more than the remainder for the *whole* workload, lowering B further when other programs need memory. A user-specified lower cap wins. Never treat this fraction as evidence that an unknown symbolic job fits.

Estimate each active job's peak p_i from relevant observed cases, including its entire process tree, loaded data, temporary algebra, transfers and returned results. Inflate uncertain estimates and start with one pilot when the peak is unknown. Do not infer the peak from the final expression's ByteCount or one easy diagram. Reserve master/result-assembly memory separately when it is not already in p_i.

At admission, enforce both the total peak budget and current headroom:

    sum(p_i for active jobs) + p_next + collection_reserve <= B

    sum(max(0, p_i - m_i) for active jobs)
        + p_next + remaining_collection_growth <= H - R

Here m_i is each active job's current measured usage on a consistent accounting basis. H is the smallest current headroom among host MemAvailable and all applicable finite cgroup limit-minus-current values. Omit nonexistent caps; do not double-count memory already included in an ancestor or master allocation. Reject admission if either side cannot be established conservatively. If one job cannot fit by itself, reduce its batch/problem size, change method or report the resource blocker; do not queue forever.

These equations are admission heuristics, not hard protection against a sudden allocation or another program consuming RAM. Keep an independent monitor and use available task-scoped operating-system limits for risky jobs.

## Inside one Mathematica calculation

Use a bounded existing subkernel pool for independent parameter points, diagram subsets or integrals only after their input/output contracts are established. Explore an unfamiliar package call on a representative case first. Keep the evaluate -> inspect -> decide gate inside each dependency chain; parallelism does not permit guessing later-stage results.

Load the documented package on each worker, including required initialisation and external executables. [ParallelNeeds](https://reference.wolfram.com/language/ref/ParallelNeeds.html) evaluates Needs on parallel kernels; it is not a guarantee that a stateful package or every external link is parallel-safe. Use [DistributeDefinitions](https://reference.wolfram.com/language/ref/DistributeDefinitions.html) for selected user definitions. Its recursive distribution can pull in dependencies: avoid broadcasting all of Global` or a huge amplitude merely for convenience. Do not share live links, open file handles or mutable package state by assumption.

Use pure per-task transformations where possible, stable task IDs and deterministic per-task random seeds when needed. Match serial and parallel results with appropriate exact or numerical checks on representative distinct cases. A changed floating-point reduction order needs a precision/tolerance check, not automatic rejection or assumed equivalence.

Bound queued inputs and collected outputs as well as running workers. For unequal long jobs, [ParallelSubmit](https://reference.wolfram.com/language/ref/ParallelSubmit.html) with [WaitNext](https://reference.wolfram.com/language/ref/WaitNext.html) can collect completed results incrementally. WaitNext returns a result, its evaluation ID and the remaining evaluations; preserve the ID-to-input association and inspect status before dependent work. Submit the next admitted task only after checking current capacity. Avoid building an unbounded list of pending jobs or retaining all huge intermediate results. Keep the OS monitor alive while the main kernel is blocked waiting.

## Multiple independent Mathematica programs

Run independent ready programs at the same time when their combined budgets fit; do not wait for program A merely because it was listed before unrelated B. Use separate processes when tasks already have separate programs, incompatible package state, or genuinely independent expensive computations. Reuse a common parameterised source rather than cloning it into job1.wl, job2.wl and so on. Within one calculation, prefer the pool over inventing many program files.

Give each job isolated mutable scratch paths when the package writes files. Share immutable inputs read-only; use distinct result keys and one controlled writer for a shared final artifact. Temporary process I/O is not a reason to retain every cheap result. Consolidate useful outputs into the authoritative calculation/checkpoint and remove only your disposable scratch files after checks pass.

Track every launched process, its descendants, completion status and nonzero exit. Do not discard stderr, treat an existing result file as success, or combine incomplete outputs. Native external-program workers count in both budgets. An input change invalidates affected running/pending dependants; cancel or ignore stale results safely. An unrelated branch may continue while the first failing branch is diagnosed.

## Monitor during execution, not only afterwards

Start or attach to a real local supervisor before expensive concurrent work. It must run independently of a busy Mathematica kernel and of the model's next message. Use existing process/scheduler facilities; do not generate a permanent daemon, kernel service or logging framework. When no supervisor is available, use a smaller contained pilot and be explicit that live whole-workload protection is unavailable. Do not claim monitoring from a comment or an end-of-job memory printout.

A practical initial sampling period is about two seconds while jobs are active, adjusted to allocation speed. Keep samples local in a bounded in-memory buffer and surface only a failure, pressure transition, completion needing inspection or requested status. Do not spend a model call per sample or save a high-frequency CSV by default.

Measure host headroom and the total task-owned workload, including descendants and native helpers. Where possible, use a dedicated job cgroup's accounting; otherwise inspect the full process tree and use RSS conservatively, noting shared-page double counting. PSS can refine accounting when available and affordable. Linux [MemAvailable](https://docs.kernel.org/filesystems/proc.html) estimates memory usable without swapping; RSS/PSS describe process mappings. Do not add swap space to the RAM budget or confuse virtual address space with resident RAM.

Use three responses:

- **Normal:** admit ready jobs only when CPU, licence, peak and live-headroom checks pass. Increase concurrency gradually after credible measurements.
- **Pressure:** stop new submissions; shrink future batches; release only known-dead task-owned intermediates or idle workers after preserving necessary expensive state. If usage approaches B (an initial warning point is about 90% of B), headroom falls below R, or swapping/pressure rises, prefer fewer concurrent jobs. Resume admissions only after sustained recovery, not a single good sample.
- **Critical:** use an already-prepared checkpoint/abort boundary or gracefully cancel a selected task-owned job before exhaustion. Emergency termination is limited to identifiable processes launched for this task under the agreed safety policy, after graceful handling is insufficient. Do not kill another notebook or write an enormous checkpoint during an allocation crisis. Mark aborted output invalid and block dependants. Suspending a process does not release its RAM.

Polling can miss short spikes. Use permitted task-scoped cgroup/scheduler limits where available, without raising privileges or changing unrelated groups. Linux memory.high throttles/reclaims; memory.max is a backstop that can trigger an OOM kill within the group, not a promise of graceful checkpointing. Account for the parent and children together. See [memory controls](https://docs.kernel.org/admin-guide/cgroup-v2.html). State clearly whether protection is advisory monitoring or enforced containment.

## Local Wolfram measurements are supplementary

[MemoryInUse](https://reference.wolfram.com/language/ref/MemoryInUse.html) and [MaxMemoryUsed](https://reference.wolfram.com/language/ref/MaxMemoryUsed.html) help inspect a kernel. They are not a whole-machine or all-descendants memory monitor. MaxMemoryUsed does not typically account for code space, stack space or heap fragmentation. [MemoryConstrained](https://reference.wolfram.com/language/ref/MemoryConstrained.html) limits additional memory requested during an evaluation, not the total RAM of all concurrent kernels and external programs; its abort may also be protected. Never use it as the sole machine-memory guard.

The following is a measurement pattern, not an executable package example. Replace nextCalculation[input] with the actual unevaluated next operation; the assignment evaluates it once. Read the result and messages before using it. The memory observation is kernel-local, not OS peak RSS:

```wolfram
elapsed = First[
  AbsoluteTiming[
    extraMemory = MaxMemoryUsed[
      result = nextCalculation[input];
    ];
  ]
];
{elapsed, extraMemory, Head[result]}
```

Do not subtract two session-wide historical maxima and call the difference this job's peak. If profiling requires re-executing an expensive result already computed, use existing OS observations instead.

## Further acceleration without more clutter

Prefer appropriate built-ins, sparse structure, factorisation, selected simplification and avoiding repeated work before adding workers. Use temporary memoisation only for reused arguments and release disposable caches at known boundaries. Compilation or GPU work needs supported operations, compatible data/precision and a measured benefit; a GPU does not automatically accelerate arbitrary symbolic package calls. Consult the installed version's documentation before using specialised acceleration.

Keep scientific sections, actual-output gates, minimal source files and selective persistence. Success is faster *validated* work within resource limits, not maximum worker count or prettier parallel syntax. No final Summary section or performance report unless requested; retain only a useful observed timing/limit in an existing note when needed for the next run.
