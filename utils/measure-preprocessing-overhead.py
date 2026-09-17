#!/usr/bin/env python3
"""measure-preprocessing-overhead.py -- The time the preprocessor adds when config1 of the umljava
case study is derived, built and tested (M1.5).

Usage: measure-preprocessing-overhead.py <Vitruv-DSLs checkout> <Vitruv-CaseStudies checkout>

Needs JAVA_HOME pointing at a JDK 21 and bash on the PATH (Git Bash on Windows), which runs the
Maven wrappers of both checkouts. A run takes about 20 minutes.

Setup, not timed: the preprocessor of the Vitruv-DSLs checkout is built and its classpath resolved,
the pcmumlclass rules are derived from their annotated reactions, and the modules the umljava tests
depend on are installed against those rules.

Timed on the wall clock: the preprocessor derives config1 from the annotated umljava reactions 100
times, each run in a JVM of its own, and `mvnw -pl umljava clean test` builds and tests the case
study against the derived rules 10 times. Configurations, derived rules and Maven logs go to a
scratch folder, whose path the output names.

The output starts with the git state of both checkouts, the Java version and the processor. It lists
every preprocessing time, the size of the derived rules as count-loc.sh counts it, and the duration,
result and test counts of every build, and it ends with mean, median, minimum and maximum of both
series and the share of preprocessing in preprocessing plus build and test.
"""

import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PREPROCESSOR_RUNS = 100
TEST_RUNS = 10
MAIN_CLASS = "tools.vitruv.reactions.preprocessor.Main"
PREPROCESSOR = "reactions/preprocessor"
CONFIGS = PREPROCESSOR + "/src/main/resources/configs"
UMLJAVA_REACTIONS = "umljava/src/main/reactions/tools/vitruv/applications/umljava"
PCMUMLCLASS_REACTIONS = "pcmumlclass/src/main/reactions/tools/vitruv/applications/pcmumlclass"
UMLJAVA_DEPENDENCIES = "util.temporary,testutility,testutility.integration"
COUNT_LOC = Path(__file__).resolve().parent / "count-loc.sh"

TEST_COUNTS = re.compile(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)\s*$")
MAVEN_TOTAL_TIME = re.compile(r"Total time:\s+(.+?)\s*$")


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def git_state(checkout):
    head = subprocess.run(["git", "-C", str(checkout), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    changed = subprocess.run(["git", "-C", str(checkout), "status", "--porcelain", "--untracked-files=no"],
                             capture_output=True, text=True).stdout.splitlines()
    return head + (" (clean)" if not changed else f" ({len(changed)} changed tracked files)")


def processor_name():
    if os.name == "nt":
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
            return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    return platform.processor()


def maven(bash, env, checkout, arguments, log):
    started = time.perf_counter()
    with open(log, "w", encoding="utf-8", errors="replace") as out:
        code = subprocess.run([bash, "./mvnw", "-B", *arguments], cwd=checkout, env=env,
                              stdout=out, stderr=subprocess.STDOUT).returncode
    return code, time.perf_counter() - started


def setup_step(what, bash, env, checkout, arguments, log):
    code, seconds = maven(bash, env, checkout, arguments, log)
    if code != 0:
        fail(f"{what} failed, see {log}")
    print(f"  {what}: {seconds:.1f} s")


def preprocess(java, classpath, env, config, reactions):
    output = config.with_name(config.stem + "-reactions")
    started = time.perf_counter()
    result = subprocess.run([str(java), "-cp", classpath, MAIN_CLASS, "--config", str(config),
                             "--reactions", str(reactions)], env=env, capture_output=True, text=True)
    seconds = time.perf_counter() - started
    console = result.stdout + result.stderr
    if result.returncode != 0 or "ERROR" in console or not any(output.rglob("*.reactions")):
        fail(f"Preprocessing {config.name} failed:\n{console}")
    return seconds


def main():
    sys.stdout.reconfigure(line_buffering=True)
    if len(sys.argv) != 3:
        fail("Usage: measure-preprocessing-overhead.py <Vitruv-DSLs checkout> <Vitruv-CaseStudies checkout>")
    dsls = Path(sys.argv[1]).resolve()
    cases = Path(sys.argv[2]).resolve()
    if not (dsls / CONFIGS / "config1.json").is_file():
        fail(f"{dsls} holds no {CONFIGS}/config1.json")
    if not (cases / UMLJAVA_REACTIONS).is_dir():
        fail(f"{cases} holds no {UMLJAVA_REACTIONS}")
    if not os.environ.get("JAVA_HOME"):
        fail("JAVA_HOME is not set; it has to point at a JDK 21.")
    java_home = Path(os.environ["JAVA_HOME"])
    java = java_home / "bin" / ("java.exe" if os.name == "nt" else "java")
    if not java.is_file():
        fail(f"No java in {java_home / 'bin'}")
    bash = shutil.which("bash")
    if not bash:
        fail("No bash on the PATH; the Maven wrappers need one (Git Bash on Windows).")
    env = dict(os.environ)
    env["PATH"] = str(java_home / "bin") + os.pathsep + env.get("PATH", "")
    scratch = Path(tempfile.mkdtemp(prefix="preprocessing-overhead-"))
    java_version = subprocess.run([str(java), "-version"], capture_output=True, text=True).stderr.splitlines()[0]

    print("Preprocessing overhead of config1 (M1.5)")
    print()
    print(f"Vitruv-DSLs          {git_state(dsls)}  {dsls.as_posix()}")
    print(f"Vitruv-CaseStudies   {git_state(cases)}  {cases.as_posix()}")
    print(f"Java                 {java_version}")
    print(f"Processor            {processor_name()}, {os.cpu_count()} logical processors, "
          f"{platform.system()} {platform.release()}")
    print(f"Scratch folder       {scratch.as_posix()}")
    print(f"Started              {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("Setup, not timed")
    setup_step("build the preprocessor", bash, env, dsls,
               ["-q", "-pl", PREPROCESSOR, "-am", "install", "-DskipTests"], scratch / "setup-preprocessor.log")
    classpath_file = scratch / "preprocessor-classpath.txt"
    setup_step("resolve its classpath", bash, env, dsls,
               ["-q", "-pl", PREPROCESSOR, "dependency:build-classpath",
                "-Dmdep.outputFile=" + classpath_file.as_posix()], scratch / "setup-classpath.log")
    classpath = str(dsls / PREPROCESSOR / "target" / "classes") + os.pathsep + classpath_file.read_text().strip()
    for name in ("config1.json", "pcmumlclass.json"):
        shutil.copy(dsls / CONFIGS / name, scratch / name)
    seconds = preprocess(java, classpath, env, scratch / "pcmumlclass.json", cases / PCMUMLCLASS_REACTIONS)
    print(f"  derive pcmumlclass: {seconds:.1f} s")
    setup_step("install " + UMLJAVA_DEPENDENCIES, bash, env, cases,
               ["-q", "-pl", UMLJAVA_DEPENDENCIES, "-am", "install", "-DskipTests",
                "-Dpcmumlclass.reactions.dir=" + (scratch / "pcmumlclass-reactions").as_posix()],
               scratch / "setup-dependencies.log")
    print()

    config = scratch / "config1.json"
    derived = scratch / "config1-reactions"
    print(f"Preprocessing config1, {PREPROCESSOR_RUNS} runs, one JVM each, seconds")
    preprocessing = [preprocess(java, classpath, env, config, cases / UMLJAVA_REACTIONS)
                     for _ in range(PREPROCESSOR_RUNS)]
    for start in range(0, PREPROCESSOR_RUNS, 10):
        row = preprocessing[start:start + 10]
        print(f"  {start + 1:3d}-{start + len(row):3d}  " + "  ".join(f"{t:.3f}" for t in row))
    files = len(list(derived.rglob("*.reactions")))
    loc = subprocess.run([bash, COUNT_LOC.as_posix(), derived.as_posix(), "-e", "reactions", "-q"],
                         capture_output=True, text=True).stdout.strip()
    print(f"  derived config1: {files} files, {loc} lines of code")
    print()

    print(f"Building and testing umljava against config1, {TEST_RUNS} runs of mvnw -pl umljava clean test")
    builds = []
    for run in range(1, TEST_RUNS + 1):
        log = scratch / f"build-and-test-{run:02d}.log"
        code, seconds = maven(bash, env, cases,
                              ["-pl", "umljava", "clean", "test", "-Dumljava.reactions.dir=" + derived.as_posix()], log)
        lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
        counts = [match.groups() for match in map(TEST_COUNTS.search, lines) if match]
        tests, failures, errors, skipped = counts[-1] if counts else ("?", "?", "?", "?")
        totals = [match.group(1) for match in map(MAVEN_TOTAL_TIME.search, lines) if match]
        result = "BUILD SUCCESS" if code == 0 else "BUILD FAILURE"
        print(f"  {run:2d}  {seconds:6.1f}  {result}  tests {tests}, failures {failures}, errors {errors}, "
              f"skipped {skipped}  (Maven total time {totals[-1] if totals else '?'})")
        if code != 0:
            print(f"Build {run} failed, see {log}", file=sys.stderr)
        builds.append(seconds)
    print()

    print("Summary, seconds")
    print(f"  {'':24}{'runs':>6}{'mean':>10}{'median':>10}{'min':>10}{'max':>10}")
    for name, values, digits in (("preprocessing config1", preprocessing, 3), ("build and test umljava", builds, 1)):
        numbers = (statistics.mean(values), statistics.median(values), min(values), max(values))
        print(f"  {name:24}{len(values):6d}" + "".join(f"{number:10.{digits}f}" for number in numbers))
    by_mean = statistics.mean(preprocessing) / (statistics.mean(preprocessing) + statistics.mean(builds))
    by_median = statistics.median(preprocessing) / (statistics.median(preprocessing) + statistics.median(builds))
    print(f"  share of preprocessing in preprocessing plus build and test: {by_mean:.2%} of the means, "
          f"{by_median:.2%} of the medians")
    print()
    print(f"Finished             {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
