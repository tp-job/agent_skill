# Phase 1 — File System Inspection

Paths, folder structure, file content, and dependency/import trace — run first for missing-module, wrong-path, and encoding errors.

## PHASE 1 — File System Inspection

Run this phase when the error involves a path, import, missing file, wrong type, permission denied, module not found, or directory mismatch.

### 1-A Path Validation Checklist

For every path mentioned in the error or provided by the user:

|Check|Tool / Command|What to look for|
|---|---|---|
|**Exists**|`os.path.exists()` / `ls` / `stat`|FileNotFoundError, None|
|**Type**|`os.path.isfile()` / `os.path.isdir()`|Confusion between dir and file|
|**Extension**|`pathlib.Path.suffix` / `file -b`|`.py` vs `.txt`, missing ext|
|**Absolute vs relative**|`os.path.abspath()`|CWD assumption bug|
|**Symlink**|`os.path.islink()` / `readlink`|Dangling symlinks|
|**Permissions**|`os.access(R_OK/W_OK/X_OK)`|PermissionError|
|**Encoding**|`chardet` / `file -i`|UTF-8 vs Latin-1|

**Diagnostic template (Python):**

```python
import os, pathlib, stat

def inspect_path(p: str) -> dict:
    path = pathlib.Path(p)
    return {
        "raw":        str(path),
        "absolute":   str(path.resolve()),
        "exists":     path.exists(),
        "is_file":    path.is_file(),
        "is_dir":     path.is_dir(),
        "is_symlink": path.is_symlink(),
        "suffix":     path.suffix,
        "size_bytes": path.stat().st_size if path.exists() else None,
        "permissions": oct(path.stat().st_mode) if path.exists() else None,
    }
```

**Diagnostic template (Bash):**

```bash
p="$1"
echo "--- Path Inspection: $p ---"
[ -e "$p" ]  && echo "EXISTS"    || echo "MISSING"
[ -f "$p" ]  && echo "FILE"      || true
[ -d "$p" ]  && echo "DIR"       || true
[ -L "$p" ]  && echo "SYMLINK → $(readlink -f $p)" || true
[ -r "$p" ]  && echo "READABLE"  || echo "NOT READABLE"
[ -w "$p" ]  && echo "WRITABLE"  || echo "NOT WRITABLE"
[ -x "$p" ]  && echo "EXECABLE"  || echo "NOT EXECABLE"
ls -la "$p" 2>/dev/null || true
file "$p"    2>/dev/null || true
```

### 1-B Folder Structure Scan

When the error is "module not found", "file missing", or "wrong directory":

```bash
# Print full tree (depth 3), sizes, hidden files
find . -maxdepth 3 -not -path '*/\.*' | sort | \
  awk '{depth=split($0,a,"/"); printf "%*s%s\n", depth*2,"", a[depth]}'
```

Map what the code **expects** vs what **actually exists**:

```
Expected layout (from imports/config)     Actual layout (from scan)
──────────────────────────────────        ──────────────────────────
src/
  utils/
    helpers.py          ◄────── MISSING   src/util/helper.py  ← wrong name
  agents/
    coordinator.py      ◄────── OK        agents/coordinator.py
config/
  settings.yaml         ◄────── MISSING   (not found anywhere)
```

Common mismatches to flag:

- Singular vs plural (`util/` vs `utils/`)
- Case sensitivity (`Helper.py` vs `helper.py`)
- Nested vs flat (`agents/coordinator.py` vs `coordinator.py`)
- Wrong working directory at runtime

### 1-C File Content Quick-Check

When the file exists but behaves wrong:

```python
# Detect encoding issues, empty files, truncated content
with open(path, "rb") as f:
    raw = f.read(512)

print(f"First 512 bytes (hex): {raw.hex()}")
print(f"BOM detected: {raw.startswith((b'\xef\xbb\xbf', b'\xff\xfe', b'\xfe\xff'))}")
print(f"File size: {os.path.getsize(path)} bytes")
print(f"Line count: {sum(1 for _ in open(path))}")
```

For config files (YAML/JSON/TOML/env):

```python
# Validate parse-ability
import json, yaml, tomllib

try:
    with open(path) as f:
        data = json.load(f)   # or yaml.safe_load / tomllib.load
    print("Parses OK:", data)
except Exception as e:
    print(f"PARSE ERROR at {e}")
```

### 1-D Dependency & Import Trace

When the error is `ImportError`, `ModuleNotFoundError`, or missing package:

```bash
# Which Python is running?
which python3 && python3 --version

# Is the package installed in THIS env?
pip show <package-name>
pip list | grep -i <package-name>

# Is __init__.py present where expected?
find . -name "__init__.py" | sort

# Check sys.path at runtime
python3 -c "import sys; [print(p) for p in sys.path]"
```

For Node.js:

```bash
node -e "console.log(require.resolve('<module>'))"
ls node_modules/<module>/package.json
cat package.json | jq '.dependencies, .devDependencies'
```
