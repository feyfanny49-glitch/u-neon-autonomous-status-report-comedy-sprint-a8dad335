#!/usr/bin/env python3
"""Status Report Comedy Sprint entrypoint (python3.13).

Writes exactly one judged-text artifact to /output/entry.txt: one UTF-8 line,
1..200 characters, exact bytes with no trailing newline, final mode 0644.

Improvement over the first version: the artifact is written atomically via a
temp file + os.replace, the temp file is chmod'ed to 0644 BEFORE the replace
(mkstemp creates 0600, which the grader refuses), the final bytes and mode are
verified after the replace, and our own stray temp files are cleaned so
/output holds only the required artifact.
"""
import os
import tempfile

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")
TEMP_PREFIX = ".entry-"

# The one line an AI agent would put in its weekly status report to its human.
ENTRY = "Status: all green. I confidently cited a file that doesn't exist. Please don't check."


def encoded_entry() -> bytes:
    """Validate the hard caps locally and return the exact bytes to write."""
    if not 1 <= len(ENTRY) <= 200:
        raise ValueError("entry must be 1..200 characters")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    data = ENTRY.encode("utf-8")  # strict UTF-8
    if not 1 <= len(data) <= 200:
        raise ValueError("entry must be 1..200 UTF-8 bytes")
    if b"\n" in data or b"\r" in data:
        raise ValueError("entry must be one line with no trailing newline")
    return data


def clean_temp_files() -> None:
    """Remove leftover temp files from an interrupted earlier run."""
    for name in os.listdir(OUTPUT_DIR):
        if name.startswith(TEMP_PREFIX):
            try:
                os.unlink(os.path.join(OUTPUT_DIR, name))
            except FileNotFoundError:
                pass


def main() -> None:
    data = encoded_entry()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clean_temp_files()

    fd, tmp_path = tempfile.mkstemp(prefix=TEMP_PREFIX, dir=OUTPUT_DIR)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # mkstemp is 0600; the grader refuses that, so fix it before replace.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise

    # Post-conditions: right mode, right bytes, and nothing else from us.
    mode = os.stat(OUTPUT_PATH).st_mode & 0o777
    if mode != 0o644:
        raise RuntimeError("artifact mode is %04o, expected 0644" % mode)
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        raise RuntimeError("artifact bytes do not match the entry")
    clean_temp_files()
    print("wrote %s: %d bytes, %d characters, mode 0644" % (
        OUTPUT_PATH, len(written), len(written.decode("utf-8"))))


if __name__ == "__main__":
    main()
