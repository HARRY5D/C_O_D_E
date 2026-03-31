"""
test_quick.py
=============
Quick integration test for the Voice Converter microservice.

Tests every endpoint with the generated sample audio files.

Usage (from Voice_converter/ root):
    # Step 1 – start the server in another terminal:
    uvicorn api.main:app --port 8002

    # Step 2 – run (samples are auto-generated if missing):
    python tests/test_quick.py

    # Or run against a different host:
    python tests/test_quick.py --base-url http://localhost:8002
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

BASE_URL = "http://localhost:8002"
TESTS_DIR = os.path.dirname(__file__)
SAMPLES_DIR = os.path.join(TESTS_DIR, "sample_audios")


# ─── Colour helpers ───────────────────────────────────────────────────────────

def _c(code: int, msg: str) -> str:
    return f"\033[{code}m{msg}\033[0m"

ok   = lambda s: print(_c(32, f"  ✓  {s}"))
fail = lambda s: print(_c(31, f"  ✗  {s}"))
info = lambda s: print(_c(36, f"     {s}"))
head = lambda s: print(_c(1,  f"\n{'─'*56}\n  {s}\n{'─'*56}"))


# ─── HTTP helpers (stdlib only) ───────────────────────────────────────────────

def _get(url: str) -> tuple[int, dict]:
    import urllib.request
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.status, json.loads(r.read())
    except Exception as exc:
        return 0, {"error": str(exc)}


def _post_multipart(url: str, fields: dict, files: dict,
                    timeout: int = 60) -> tuple[int, bytes]:
    """
    Submit multipart/form-data using only stdlib (no requests/httpx).
    fields: {name: value}
    files:  {name: (filename, bytes, content_type)}
    """
    import urllib.request
    import uuid

    boundary = uuid.uuid4().hex
    body_parts: list[bytes] = []

    for name, value in fields.items():
        body_parts.append(
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n".encode()
        )
    for name, (filename, data, ct) in files.items():
        body_parts.append(
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
            f"Content-Type: {ct}\r\n\r\n".encode()
            + data
            + b"\r\n"
        )
    body_parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(body_parts)

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode()


def _delete(url: str) -> tuple[int, dict]:
    import urllib.request
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())
    except Exception as exc:
        return 0, {"error": str(exc)}


# ─── Test runner ──────────────────────────────────────────────────────────────

class Results:
    passed = 0
    failed = 0

    def check(self, cond: bool, msg: str) -> bool:
        if cond:
            ok(msg)
            self.passed += 1
        else:
            fail(msg)
            self.failed += 1
        return cond


R = Results()


def _read(name: str) -> bytes:
    path = os.path.join(SAMPLES_DIR, name)
    with open(path, "rb") as f:
        return f.read()


def _ensure_samples() -> bool:
    needed = [
        "reference_voice_A.wav",
        "source_audio_B.wav",
        "short_source_5s.wav",
    ]
    missing = [n for n in needed if not os.path.exists(os.path.join(SAMPLES_DIR, n))]
    if not missing:
        return True
    print("  Generating sample audio files first…")
    script = os.path.join(TESTS_DIR, "generate_samples.py")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        return False
    return True


# ─── Individual tests ─────────────────────────────────────────────────────────

def test_health(base: str) -> None:
    head("1 / 5  Health Check")
    status, data = _get(f"{base}/api/health")
    R.check(status == 200, f"GET /api/health  →  {status}")
    info(f"Response: {data}")
    R.check(data.get("status") == "healthy", "status == 'healthy'")


def test_create_profile(base: str) -> str | None:
    head("2 / 5  Create Voice Profile")
    ref_audio = _read("reference_voice_A.wav")
    status, body = _post_multipart(
        f"{base}/api/create-voice-profile",
        fields={"profile_name": "Test_Female_Voice"},
        files={"reference_audio": ("reference_voice_A.wav", ref_audio, "audio/wav")},
        timeout=120,
    )
    R.check(status == 200, f"POST /api/create-voice-profile  →  {status}")
    try:
        data = json.loads(body)
    except Exception:
        R.check(False, "response is valid JSON")
        info(f"Raw body: {body[:200]}")
        return None
    info(f"Profile ID  : {data.get('profile_id', '—')}")
    info(f"Profile name: {data.get('profile_name', '—')}")
    chars = data.get("characteristics", {})
    pitch = (chars.get("pitch") or {}).get("mean", None)
    if pitch:
        info(f"Mean pitch  : {pitch:.1f} Hz")
    R.check("profile_id" in data, "response contains 'profile_id'")
    return data.get("profile_id")


def test_list_profiles(base: str, expected_id: str | None) -> None:
    head("3 / 5  List Profiles")
    status, data = _get(f"{base}/api/voice-profiles")
    R.check(status == 200, f"GET /api/voice-profiles  →  {status}")
    profiles = data.get("profiles", [])
    info(f"Total profiles: {len(profiles)}")
    if expected_id:
        ids = [p.get("profile_id") for p in profiles]
        R.check(expected_id in ids, f"created profile appears in list")


def test_convert(base: str, profile_id: str | None) -> None:
    head("4 / 5  Convert Audio (saved profile)")
    if not profile_id:
        fail("Skipped – no profile id available")
        R.failed += 1
        return
    src_audio = _read("source_audio_B.wav")
    status, body = _post_multipart(
        f"{base}/api/convert",
        fields={"target_profile_id": profile_id, "quality": "fast"},
        files={"source_audio": ("source_audio_B.wav", src_audio, "audio/wav")},
        timeout=180,
    )
    R.check(status == 200, f"POST /api/convert  →  {status}")
    if status == 200:
        R.check(len(body) > 1000, f"response is audio data ({len(body)} bytes)")
        out_path = os.path.join(SAMPLES_DIR, "converted_output.wav")
        with open(out_path, "wb") as f:
            f.write(body)
        ok(f"Saved converted audio → {out_path}")
    else:
        try:
            info(f"Error: {json.loads(body).get('detail', body[:200])}")
        except Exception:
            info(f"Body: {body[:200]}")


def test_convert_new_voice(base: str) -> None:
    head("5 / 5  Convert With New Voice (no saved profile)")
    src_audio = _read("short_source_5s.wav")
    ref_audio = _read("reference_voice_A.wav")
    status, body = _post_multipart(
        f"{base}/api/convert-with-new-voice",
        fields={"quality": "fast"},
        files={
            "source_audio": ("short_source_5s.wav", src_audio, "audio/wav"),
            "target_reference_audio": ("reference_voice_A.wav", ref_audio, "audio/wav"),
        },
        timeout=180,
    )
    R.check(status == 200, f"POST /api/convert-with-new-voice  →  {status}")
    if status == 200:
        R.check(len(body) > 1000, f"response is audio data ({len(body)} bytes)")
        out_path = os.path.join(SAMPLES_DIR, "converted_new_voice.wav")
        with open(out_path, "wb") as f:
            f.write(body)
        ok(f"Saved converted audio → {out_path}")
    else:
        try:
            info(f"Error: {json.loads(body).get('detail', body[:200])}")
        except Exception:
            info(f"Body: {body[:200]}")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Voice Converter quick test")
    parser.add_argument("--base-url", default=BASE_URL,
                        help=f"Converter base URL (default: {BASE_URL})")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")

    print(f"\n🔬  Voice Converter Integration Test")
    print(f"    Target: {base}\n")

    # Check server is reachable
    print("  Checking server…")
    status, _ = _get(f"{base}/api/health")
    if status == 0:
        print(f"\n  ⚠️  Cannot reach {base}/api/health")
        print("  Start the converter first:")
        print("    cd D:\\JAVA\\CODE\\Projects\\VoiceAPI\\Voice_converter")
        print("    uvicorn api.main:app --port 8002\n")
        sys.exit(1)

    # Generate samples if needed
    if not _ensure_samples():
        print("  Failed to generate sample audio files.")
        sys.exit(1)

    # Run tests
    test_health(base)
    profile_id = test_create_profile(base)
    test_list_profiles(base, profile_id)
    test_convert(base, profile_id)
    test_convert_new_voice(base)

    # Summary
    total = R.passed + R.failed
    colour = 32 if R.failed == 0 else 31
    print(_c(colour, f"\n{'═'*56}"))
    print(_c(colour, f"  Result: {R.passed}/{total} tests passed"
             + (f"  ({R.failed} failed)" if R.failed else "  ✅")))
    print(_c(colour, f"{'═'*56}\n"))
    if R.failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
