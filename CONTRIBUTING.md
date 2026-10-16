# Contributing to FloatPen

Thank you for your interest in contributing to **FloatPen**! We welcome all contributions, including bug reports, feature requests, documentation improvements, and code enhancements.

---

## 🛠️ Development Setup

### Prerequisites

- Linux OS with GTK 3 & Cairo libraries:
  ```bash
  # Debian / Ubuntu:
  sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 libcairo2-dev libx11-dev
  ```

### Clone and Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Khitishnayak/floatpen.git
   cd floatpen
   ```

2. Run directly in development mode:
   ```bash
   ./run.sh
   ```

3. Run the unit test suite:
   ```bash
   python3 -m unittest discover -s tests -v
   ```

---

## 📌 How to Contribute

### 1. Reporting Bugs
- Search existing issues to avoid duplicates.
- Provide your Linux distribution and desktop environment (`echo $XDG_CURRENT_DESKTOP`, `echo $XDG_SESSION_TYPE`).
- Include steps to reproduce the issue.

### 2. Suggesting Features
- Open an issue describing the feature, rationale, and how it improves desktop annotations or presentations.

### 3. Submitting Pull Requests
- Create a feature branch: `git checkout -b feature/my-new-feature`
- Follow existing code style and naming conventions.
- Ensure all unit tests pass before submitting.
- Submit a PR with a clear description of changes.

---

## 📜 Code of Conduct

Please adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all project interactions.
