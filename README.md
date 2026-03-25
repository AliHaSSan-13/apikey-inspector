# apikey-inspector 🔍

**One package, zero fluff, maximum insight.**

apikey-inspector is a universal, privacy-first API key inspector. It allows you to identify, validate, and inspect API keys from major AI providers without risking leakage.

[![PyPI version](https://img.shields.io/pypi/v/apikey-inspector.svg)](https://pypi.org/project/apikey-inspector/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- 🔒 **Privacy-First**: Pure regex detection *before* any network calls.
- 🎭 **Auto-Masking**: Sensitive keys are always masked in terminal output and redacted in JSON.
- 🚀 **Async-First**: Batch inspect hundreds of keys concurrently with per-provider rate-limiting.
- 📡 **Deep Inspection**: Fetches available models, usage, costs, and rate limits where available.
- 🛠️ **CI/CD Ready**: Exit codes optimized for security pipelines (`--scan` flag).

## 📦 Supported Providers

| Provider | Key Detection | Validation | Usage/Costs | Models List |
|---|---|---|---|---|
| **OpenAI** | ✅ | ✅ | ✅ | ✅ |
| **Anthropic** | ✅ | ✅ | 🚧 | ✅ |
| **Google Gemini**| ✅ | ✅ | 🚧 | ✅ |
| **HuggingFace** | ✅ | ✅ | ✅ | ✅ |
| **Cohere** | ✅ | ✅ | 🚧 | ✅ |

---

## 🚀 Quick Start

### Installation

```bash
pip install apikey-inspector
```

### Usage

```bash
# Basic inspection (masks key automatically)
apikey inspect sk-proj-1234...

# Offline mode (detection only, no network calls)
apikey inspect sk-proj-1234... --offline

# Batch inspection from a file or stdin
cat keys.txt | apikey inspect --json > results.json

# Security scanning mode (exit 1 if valid keys are found)
apikey inspect sk-proj-1234... --scan
```

## 🛠️ CLI Reference

| Option | Description |
|---|---|
| `inspect [KEY]` | The main command to inspect a key. |
| `--offline` | Skip network checks, only perform local regex detection. |
| `--json` | Output raw JSON instead of the rich table. |
| `--no-redact` | Disable automatic redaction of secrets in JSON output. |
| `--from-env VAR` | Read the API key from an environment variable. |
| `--scan` | Return exit code 1 if any valid keys are detected (for CI). |
| `version` | Show the current version. |

---

## 🧪 Development & Testing

```bash
# Clone the repo
git clone https://github.com/alihassan/apikey-inspector.git
cd apikey-inspector

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## 📜 License

MIT © [Ali Hassan](mailto:alihassan.shahzadmughal@gmail.com)
