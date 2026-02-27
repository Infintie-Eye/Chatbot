# Contributing to Conrux AI

Thank you for your interest in contributing! We welcome all contributions — bug fixes, new features, documentation improvements, and more.

---

## 🚀 Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/Chatbot.git
   cd Chatbot
   ```
3. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
4. **Configure your environment:**
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY to .env
   ```

---

## 🌿 Branch Naming

| Type | Pattern | Example |
|---|---|---|
| Feature | `feature/short-description` | `feature/streaming-responses` |
| Bug fix | `fix/issue-description` | `fix/session-ttl-reset` |
| Docs | `docs/what-changed` | `docs/api-reference-update` |
| Refactor | `refactor/component` | `refactor/pipeline-stages` |

---

## ✅ Contribution Checklist

Before submitting a pull request:

- [ ] Code follows the existing style (PEP 8 for Python)
- [ ] New dependencies added to `requirements.txt`
- [ ] `.env.example` updated if new environment variables were added
- [ ] `README.md` updated if behaviour or setup changed
- [ ] No secrets, API keys, or `.env` files committed

---

## 📝 Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>

[optional body]
```

| Type | When to use |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructure without behaviour change |
| `chore` | Dependency updates, tooling |

**Examples:**
```
feat: add streaming chat endpoint
fix: handle empty Gemini response gracefully
docs: update API reference table in README
```

---

## 🐛 Reporting Bugs

Please open a [GitHub Issue](https://github.com/Infintie-Eye/Chatbot/issues) with:

- A clear title and description
- Steps to reproduce the bug
- Expected vs actual behaviour
- Environment details (OS, Python version, model used)
- Relevant error messages or logs

---

## 💡 Suggesting Features

Open a [GitHub Issue](https://github.com/Infintie-Eye/Chatbot/issues) with the label `enhancement` and describe:

- The problem you're trying to solve
- Your proposed solution
- Any alternatives you considered

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
