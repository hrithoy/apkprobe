# APKprobe

![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/wadingporque/apkprobe/blob/main/LICENSE)

**APK decompiler and secrets scanner** for Android security research. Automatically extract **API keys**, **endpoints**, **tokens**, and other **leaked credentials** from Android applications.

Works with `.apk`, `.xapk`, `.dex`, `.jar`, `.class`, `.smali`, `.zip`, `.aar`, `.arsc`, `.aab` files.

Perfect for **apk2url** extraction, **apk leaks** detection, and **Android reverse engineering**. Used by security researchers, penetration testers, and bug bounty hunters.

---

## Table of Contents

- [Why APKprobe?](#why-apkprobe)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Supported Decompilers](#supported-decompilers)
- [Custom Rules](#custom-rules)
- [Performance](#performance)
- [Alternatives](#alternatives)
- [Contributing](#contributing)
- [FAQ](#faq)
- [License](#license)

---

## Why APKprobe?

### Extract Leaked API Keys & Secrets

Most Android apps contain hardcoded secrets. Developers often hide **AWS keys**, **Firebase tokens**, **API credentials** directly in the code, thinking obfuscation will protect them. It won't.

APKprobe decompiles the APK, runs deobfuscation, and scans everything with regex patterns to find:
- **Cloud credentials** (AWS, GCP, Azure)
- **API keys** (Stripe, Twilio, SendGrid, etc.)
- **OAuth tokens & secrets**
- **Database connection strings**
- **Private keys & certificates**

---

### Find Hidden Endpoints (apk2url)

Extract all **URLs**, **API endpoints**, and **backend routes** from any Android app. Perfect for:
- **Bug bounty** recon
- **Penetration testing** 
- **Attack surface mapping**

Discover forgotten dev/staging endpoints, internal APIs, and admin panels that shouldn’t be public.

---

### Reverse Engineering Made Easy

Quickly locate security-critical code:
- **SSL pinning** implementations
- **Root detection** functions  
- **Anti-tampering** checks
- **Encryption routines**

Speed up your Frida scripts by knowing exactly where to hook.

---

## Features

- **Multi-decompiler support** — JADX, APKTool, CFR, Procyon, Krakatau, Fernflower
- **Automatic deobfuscation** — better results on protected apps
- **250+ built-in patterns** — AWS, GCP, Azure, generic API keys, URLs
- **Custom rules** — JSON, YAML, TOML, gitleaks format
- **Batch processing** — scan hundreds of APKs at once
- **Fast** — parallel decompilation and scanning
- **Multiple output formats** — JSON, YAML, text

---

## Installation

```bash
git clone https://github.com/wadingporque/apkprobe.git
cd apkprobe
python setup.py install
```

Or install in development mode:
```bash
pip install -e .
```

---

## Quick Start

Scan an APK for secrets:
```bash
apkprobe target.apk
```

Extract URLs and endpoints:
```bash
apkprobe target.apk -r endpoints
```

Scan for AWS/cloud credentials:
```bash
apkprobe target.apk -r aws gcp azure
```

---

## Usage Examples

### Basic scan
```bash
apkprobe app.apk
```

### Scan multiple files
```bash
apkprobe app1.apk app2.apk app3.xapk
```

### Use multiple decompilers for better coverage
```bash
apkprobe --jadx --apktool --cfr app.apk
```

### Output to JSON
```bash
apkprobe app.apk -o results.json -f json
```

### Custom rules
```bash
apkprobe app.apk -r /path/to/rules.json
```

### Batch scan with cleanup
```bash
apkprobe -r aws endpoints -o output.yaml -f yaml -c *.apk
```

<details>
<summary><b>All CLI options</b></summary>

```
apkprobe [OPTIONS] FILES...

Options:
  -r, --rules FILES       Rule files or built-in sets (aws, gcp, azure, endpoints, etc.)
  -o, --output FILE       Output file path
  -f, --format FORMAT     Output format: json, yaml, text
  -g, --groupby TYPE      Group by: file, locator, both
  -c, --cleanup           Remove decompiled files after scan
  -q, --quiet             Suppress output

Decompilers:
  --jadx, -J              Use JADX (default)
  --apktool, -A           Use APKTool
  --cfr, -C               Use CFR
  --procyon, -P           Use Procyon
  --krakatau, -K          Use Krakatau
  --fernflower, -F        Use Fernflower

Advanced:
  -d, --deobfuscate       Enable deobfuscation
  -w, --working-dir DIR   Working directory
  --timeout SECONDS       Scan timeout
```

</details>

---

## Supported Decompilers

| Decompiler | Type | Notes |
|------------|------|-------|
| **JADX** | Java | Default, best for most APKs |
| **APKTool** | Smali | Resources + manifest |
| **CFR** | Java | Good for obfuscated code |
| **Procyon** | Java | Alternative decompiler |
| **Krakatau** | Java | Handles edge cases |
| **Fernflower** | Java | IntelliJ's decompiler |

Use multiple decompilers together for maximum coverage — different tools handle obfuscation differently.

---

## Custom Rules

APKprobe supports multiple rule formats. Create your own or use existing pattern databases.

### Supported formats

| Format | Extension |
|--------|-----------|
| APKprobe JSON | `.json` |
| Gitleaks | `.toml` |
| secret-patterns-db | `.yaml` |
| Simple key-value | `.json` |

### Example rule (JSON)

```json
{
    "id": "stripe-api-key",
    "name": "Stripe API Key",
    "pattern": "sk_live_[a-zA-Z0-9]{24}",
    "confidence": "high"
}
```

### Built-in rule sets

- `aws` — AWS credentials, S3 buckets, ARNs
- `gcp` — Google Cloud API keys, service accounts
- `azure` — Azure connection strings, keys
- `endpoints` — URLs, API routes, webhooks
- `generic` — Common API key patterns
- `gitleaks` — Full gitleaks ruleset

---

## Performance

APKprobe uses parallel processing for both decompilation and scanning.

```bash
# Use 8 workers for scanning
apkprobe app.apk -smw 8

# Use multiprocessing instead of threading
apkprobe app.apk -sct process
```

**Tips:**
- Decompilation is RAM-heavy — limit workers on low-memory systems
- Scanning is CPU-bound — more workers = faster results
- Use `--cleanup` to save disk space on batch jobs

---

## Alternatives

APKprobe is similar to these tools:

- [apkleaks](https://github.com/dwisiswant0/apkleaks) — Python, regex-based
- [jadx](https://github.com/skylot/jadx) — Java decompiler (no scanning)
- [apktool](https://github.com/iBotPeaches/Apktool) — Smali disassembler
- [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) — Full mobile security framework

APKprobe combines decompilation + scanning in one tool with support for multiple decompilers.

---

## Contributing

Found a bug? Have an idea? PRs welcome.

```bash
git clone https://github.com/wadingporque/apkprobe.git
cd apkprobe
python setup.py install
```

---

## FAQ

### How do I extract URLs from an APK file?

Use APKprobe with the `endpoints` ruleset to extract all URLs, API endpoints, and backend routes:
```bash
apkprobe app.apk -r endpoints -o urls.json
```
This performs **apk2url** extraction automatically after decompilation.

### How do I find leaked API keys in Android apps?

APKprobe scans decompiled code for hardcoded secrets using 250+ regex patterns:
```bash
apkprobe app.apk -r aws gcp azure
```
It detects **AWS keys**, **Firebase tokens**, **Stripe keys**, and other **leaked credentials**.

### What's the best APK decompiler for security research?

APKprobe supports multiple decompilers — use them together for best results:
```bash
apkprobe --jadx --apktool --cfr app.apk
```
Different decompilers handle obfuscation differently, so combining them increases coverage.

### Is APKprobe good for bug bounty?

Yes. APKprobe is designed for **Android penetration testing** and **bug bounty** recon. It quickly maps the attack surface by extracting endpoints, API keys, and hardcoded secrets from target apps.

---

## Resources

- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/) — comprehensive mobile app security testing
- [Android Security Documentation](https://developer.android.com/privacy-and-security/security-tips) — official security best practices
- [HackerOne Android Bug Bounty Programs](https://hackerone.com/opportunities/all/search?asset_types=GOOGLE_PLAY_APP_ID) — find Android targets

---

## Author

**wadingporque**

---

## License

MIT License. See [LICENSE](LICENSE) for details.
