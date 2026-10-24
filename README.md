# 🎓 Software Design for Intelligent Systems (PPOIS)

Welcome to the repository! This project contains completed laboratory works for the PPOIS course (Student: Stanislav Tishchenko, FITiU BSUIR, Group 521702).

The project is engineered not merely as a set of academic scripts, but as a **production-grade software product** adhering to industrial engineering standards: from rigorous class architectures to an automated cross-platform CI/CD pipeline and 90–100% unit test coverage.

---

## 📂 Laboratory Work Directory & Navigation

In accordance with course requirements, all work is maintained within a single repository. Each laboratory assignment is isolated within its own dedicated directory and provides its own local `README.md` with complete specifications.

| № | Topic & Description | Tech Stack | Status |
|:---:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1** | **OOP Fundamentals:** [Cantor Set & Polynomials](./lab1)<br><sub>Introduction to OOP, Git, and collaborative clean-code development standards.</sub> | `C++` | ✅ |
| **2** | **Enterprise OOP Domain:** [Dean's Office Architecture](./lab2)<br><sub>Domain-driven design (50+ classes), inheritance, and polymorphism.</sub> | `Python` | ✅ |
| **3** | **Enterprise OOP Domain:** [Airport Operations System](./lab3)<br><sub>Advanced OOP, design patterns, abstract base classes, and polymorphic fleets.</sub> | `Python` | ✅ |
| **4** | **Generic Programming:** [Sorting Algorithms & Containers](./lab4)<br><sub>Heapsort & Stooge Sort, templates, directed graph (Wirth's structure), STL-compatible iterators.</sub> | `C++` | ✅ |

---

## 🛠 Technology Stack

The project is structured across two technology ecosystems, each utilizing modern best practices and tools:

### 🔵 C++ Ecosystem (Labs 1, 4)
- **Standard:** C++20
- **Build System:** CMake (with automatic dependency management via `FetchContent`)
- **Unit Testing Framework:** Google Test (GTest)
- **Coverage Analysis:** `lcov`
- **Static Analysis & Linter:** `cppcheck`

### 🟡 Python Ecosystem (Labs 2, 3)
- **Standard:** Python 3.11+
- **Unit Testing Framework:** `pytest` + `pytest-cov`
- **Static Analysis & Strict Typing:** `mypy`
- **Linter & Code Formatter:** `ruff`
- **Bundler:** `PyInstaller` (standalone executable generation)

---

## ⚙️ Engineering Practices & Architecture

Special emphasis is placed on code quality and repository infrastructure:

1. **Cross-Platform CI/CD (GitHub Actions):** Configured pipeline running parallel testing of C++ code on Ubuntu runners and Python code on Windows/macOS runners. Pushes to `main` and `feat/lab4` trigger automated binary packaging and publish artifacts to GitHub Releases.
2. **Comprehensive Test Coverage:** Each domain model is covered by automated unit tests to **over 90%** (100% for complex algorithms and graph iterators). CI builds fail (`fail-under`) if coverage drops below the required threshold.
3. **CLI & Domain Isolation:** Business domain logic is strictly decoupled from the console user interface. The domain cores can be reused in GUI or web frameworks without modifications.
4. **Git Flow:** Direct commits to `main` are restricted. Development is organized through feature branches (`feat/`) with code reviews and merges gated by passing CI/CD pipelines.
5. **Clean Repository (`.gitignore`):** Only source code, build scripts, and official configurations are tracked. Build directories (`cmake-build-debug`, `build/`), caches (`.pytest_cache`, `.mypy_cache`, `.ruff_cache`), and OS artifacts (`.DS_Store`) are excluded.

---

## 🚀 Execution & Verification

The project is fully decoupled from any specific IDE and is ready to run directly from the command line.

### Option 1: Standalone Binaries (GitHub Releases)
No compilers or Python runtimes are required. Download prebuilt standalone binaries for macOS, Windows (`.exe`), and Linux directly from [Releases](../../releases).

### Option 2: Local Source Execution
Detailed build instructions for `CMake` and interpreter commands for Python are provided in each directory's `README.md`. General commands from the repository root:
* **For C++:** `cmake -S labX -B labX/build && cmake --build labX/build`
* **For Python:** `python3 -m labX.cli`
