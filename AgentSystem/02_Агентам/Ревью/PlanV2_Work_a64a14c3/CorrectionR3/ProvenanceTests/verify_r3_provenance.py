#!/usr/bin/env python3
"""Read-only validator and real isolated mutation suite for R3 C2 provenance."""

from __future__ import annotations

import copy
import hashlib
import json
import struct
import sys
import unicodedata
from pathlib import Path


REQUIRED_IDS = [
    "P1-01",
    "P1-02",
    "P1-03",
    "P1-04",
    "P1-05",
    "P1-06",
    "P1-07",
    "P1-08",
    "P2-01",
    "NEW-P1-01",
    "NEW-P1-02",
    "NEW-P1-03",
    "NEW-P1-04",
]
RAW_PATH = (
    "N8NAgents/02_Агентам/Ревью/PlanV2_Work_a64a14c3/"
    "CorrectionR2/C2_PREFREEZE_AUDIT_R2_RAW.md"
)
PROHIBITED_SOURCES = [
    "19_PREFREEZE_CORRECTION_R1.json",
    "19A_PREFREEZE_CORRECTION_R1_METADATA_R3.json",
]
ITEM_DOMAIN = b"N8NAGENTS-C2-PROSPECTIVE-AUDIT-ITEM-R3\0"
SET_DOMAIN = b"N8NAGENTS-C2-PROSPECTIVE-AUDIT-SET-R3\0"


class StopValidation(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def stop(condition: bool, code: str) -> None:
    if condition:
        raise StopValidation(code)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def frame(text: str) -> bytes:
    data = text.encode("utf-8")
    return struct.pack(">I", len(data)) + data


def exact_text(text: object, field: str) -> str:
    stop(not isinstance(text, str), f"STOP_{field}_TYPE")
    assert isinstance(text, str)
    stop("\r" in text or "\0" in text, f"STOP_{field}_CONTROL")
    stop(unicodedata.normalize("NFC", text) != text, f"STOP_{field}_NOT_NFC")
    return text


def item_hash(item: dict, raw_digest: bytes, span: bytes) -> str:
    audit_id = exact_text(item.get("audit_id"), "AUDIT_ID")
    severity = exact_text(item.get("severity"), "SEVERITY")
    assessment = exact_text(item.get("original_assessment"), "ASSESSMENT")
    claim = exact_text(item.get("claim"), "CLAIM")
    source_span = item.get("source_span")
    stop(not isinstance(source_span, dict), "STOP_SOURCE_SPAN_TYPE")
    offset = source_span.get("offset")
    length = source_span.get("bytes")
    stop(not isinstance(offset, int) or isinstance(offset, bool) or offset < 0, "STOP_SPAN_OFFSET")
    stop(not isinstance(length, int) or isinstance(length, bool) or length <= 0, "STOP_SPAN_LENGTH")
    payload = (
        ITEM_DOMAIN
        + frame(audit_id)
        + frame(severity)
        + frame(assessment)
        + frame(claim)
        + struct.pack(">Q", offset)
        + struct.pack(">Q", length)
        + hashlib.sha256(span).digest()
        + hashlib.sha256(claim.encode("utf-8")).digest()
        + raw_digest
    )
    return sha(payload)


def validate(baseline: dict, raw: bytes) -> dict:
    stop(baseline.get("schema_version") != 3, "STOP_SCHEMA_VERSION")
    source = baseline.get("source")
    stop(not isinstance(source, dict), "STOP_SOURCE_TYPE")
    raw_record = source.get("raw")
    stop(not isinstance(raw_record, dict), "STOP_RAW_RECORD_TYPE")
    stop(raw_record.get("path") != RAW_PATH, "STOP_RAW_PATH")
    stop(source.get("prohibited_as_source") != PROHIBITED_SOURCES, "STOP_PROHIBITED_SOURCE_SET")
    stop(raw_record.get("bytes") != len(raw), "STOP_RAW_BYTES")
    stop(raw_record.get("sha256") != sha(raw), "STOP_RAW_SHA256")
    stop(raw.startswith(b"\xef\xbb\xbf"), "STOP_RAW_BOM")
    stop(b"\r" in raw, "STOP_RAW_CR")
    stop(not raw.endswith(b"\n") or raw.endswith(b"\n\n"), "STOP_RAW_FINAL_LF")
    try:
        raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise StopValidation("STOP_RAW_UTF8") from exc

    ids = baseline.get("required_ids")
    stop(ids != REQUIRED_IDS, "STOP_REQUIRED_IDS_EXACT_ORDER")
    stop(baseline.get("item_count") != len(REQUIRED_IDS), "STOP_ITEM_COUNT")
    items = baseline.get("items")
    stop(not isinstance(items, dict), "STOP_ITEMS_TYPE")
    stop(list(items.keys()) != REQUIRED_IDS, "STOP_ITEM_KEYS_EXACT_ORDER")

    raw_digest = hashlib.sha256(raw).digest()
    recomputed: dict[str, str] = {}
    for audit_id in REQUIRED_IDS:
        item = items[audit_id]
        stop(not isinstance(item, dict), "STOP_ITEM_TYPE")
        stop(item.get("audit_id") != audit_id, "STOP_ITEM_AUDIT_ID")
        span_record = item.get("source_span")
        stop(not isinstance(span_record, dict), "STOP_SOURCE_SPAN_TYPE")
        offset = span_record.get("offset")
        length = span_record.get("bytes")
        stop(not isinstance(offset, int) or isinstance(offset, bool) or offset < 0, "STOP_SPAN_OFFSET")
        stop(not isinstance(length, int) or isinstance(length, bool) or length <= 0, "STOP_SPAN_LENGTH")
        stop(offset + length > len(raw), "STOP_SPAN_BOUNDS")
        span = raw[offset : offset + length]
        stop(span_record.get("sha256") != sha(span), "STOP_SPAN_SHA256")
        try:
            decoded = span.decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise StopValidation("STOP_SPAN_UTF8") from exc
        claim = exact_text(item.get("claim"), "CLAIM")
        stop(decoded != claim, "STOP_SPAN_DECODED_CLAIM_MISMATCH")
        stop(span_record.get("decoded_utf8_exact_claim") is not True, "STOP_DECODED_CLAIM_ATTESTATION")
        stop(item.get("claim_utf8_sha256") != sha(claim.encode("utf-8")), "STOP_CLAIM_UTF8_SHA256")
        line = raw[:offset].count(b"\n") + 1
        stop(span_record.get("line") != line, "STOP_SPAN_LINE")
        calculated = item_hash(item, raw_digest, span)
        stop(item.get("source_item_sha256") != calculated, "STOP_ITEM_HASH")
        recomputed[audit_id] = calculated

    aggregate = SET_DOMAIN + struct.pack(">I", len(REQUIRED_IDS))
    for audit_id in REQUIRED_IDS:
        aggregate += frame(audit_id) + bytes.fromhex(recomputed[audit_id])
    aggregate_sha256 = sha(aggregate)
    stop(baseline.get("items_aggregate_sha256") != aggregate_sha256, "STOP_AGGREGATE_HASH")
    return {
        "status": "PASS",
        "rc": 0,
        "raw_bytes": len(raw),
        "raw_sha256": sha(raw),
        "item_count": len(REQUIRED_IDS),
        "items_aggregate_sha256": aggregate_sha256,
    }


def expect_reject(case_id: str, expected: str, baseline: dict, raw: bytes) -> dict:
    try:
        validate(baseline, raw)
    except StopValidation as exc:
        return {
            "case_id": case_id,
            "mutation_applied": True,
            "validator_invoked": True,
            "expected_status": expected,
            "actual_status": exc.code,
            "result": "PASS" if exc.code == expected else "FAIL",
        }
    return {
        "case_id": case_id,
        "mutation_applied": True,
        "validator_invoked": True,
        "expected_status": expected,
        "actual_status": "ACCEPTED",
        "result": "FAIL",
    }


def mutation_suite(baseline: dict, raw: bytes) -> list[dict]:
    cases: list[dict] = []

    mutated = copy.deepcopy(baseline)
    mutated["items"]["P1-01"]["source_span"]["offset"] += 1
    cases.append(expect_reject("M01_SPAN_OFFSET_PLUS_ONE", "STOP_SPAN_SHA256", mutated, raw))

    mutated = copy.deepcopy(baseline)
    mutated["items"]["P1-01"]["claim"] += "."
    cases.append(
        expect_reject(
            "M02_CLAIM_APPEND_ONE_CODEPOINT",
            "STOP_SPAN_DECODED_CLAIM_MISMATCH",
            mutated,
            raw,
        )
    )

    mutated = copy.deepcopy(baseline)
    mutated["items"]["P1-01"]["source_item_sha256"] = "0" * 64
    cases.append(expect_reject("M03_ITEM_HASH_ZEROED", "STOP_ITEM_HASH", mutated, raw))

    mutated = copy.deepcopy(baseline)
    mutated["required_ids"][0], mutated["required_ids"][1] = (
        mutated["required_ids"][1],
        mutated["required_ids"][0],
    )
    cases.append(
        expect_reject(
            "M04_REQUIRED_ORDER_SWAP_FIRST_TWO",
            "STOP_REQUIRED_IDS_EXACT_ORDER",
            mutated,
            raw,
        )
    )

    mutated = copy.deepcopy(baseline)
    mutated["items_aggregate_sha256"] = "0" * 64
    cases.append(expect_reject("M05_AGGREGATE_HASH_ZEROED", "STOP_AGGREGATE_HASH", mutated, raw))

    raw_mutated = bytearray(raw)
    raw_mutated[baseline["items"]["P1-01"]["source_span"]["offset"]] ^= 1
    cases.append(expect_reject("M06_RAW_CLAIM_BYTE_FLIPPED", "STOP_RAW_SHA256", baseline, bytes(raw_mutated)))

    mutated = copy.deepcopy(baseline)
    mutated["source"]["raw"]["path"] = "19_PREFREEZE_CORRECTION_R1.json"
    cases.append(expect_reject("M07_HISTORICAL_19_AS_SOURCE", "STOP_RAW_PATH", mutated, raw))

    return cases


def main() -> int:
    test_dir = Path(__file__).resolve().parent
    correction_dir = test_dir.parent
    work_dir = correction_dir.parent
    baseline_path = correction_dir / "24_PROSPECTIVE_AUDIT_R3_BASELINE.json"
    raw_path = work_dir / "CorrectionR2" / "C2_PREFREEZE_AUDIT_R2_RAW.md"
    baseline_bytes = baseline_path.read_bytes()
    stop(baseline_bytes.startswith(b"\xef\xbb\xbf"), "STOP_BASELINE_BOM")
    stop(b"\r" in baseline_bytes, "STOP_BASELINE_CR")
    stop(not baseline_bytes.endswith(b"\n") or baseline_bytes.endswith(b"\n\n"), "STOP_BASELINE_FINAL_LF")
    baseline = json.loads(baseline_bytes.decode("utf-8", "strict"))
    raw = raw_path.read_bytes()
    validator_bytes = Path(__file__).read_bytes()
    positive = validate(baseline, raw)
    mutations = mutation_suite(baseline, raw)
    all_rejected_as_expected = all(case["result"] == "PASS" for case in mutations)
    report = {
        "schema_version": 1,
        "record_kind": "N8NAGENTS_R3_PROVENANCE_MUTATION_RUN",
        "validator": Path(__file__).name,
        "validator_bytes": len(validator_bytes),
        "validator_sha256": sha(validator_bytes),
        "command": "py -3 -X utf8 ProvenanceTests/verify_r3_provenance.py",
        "cwd_contract": "CorrectionR3; validator also accepts any cwd because all paths derive from __file__",
        "python": sys.version.split()[0],
        "baseline": {
            "path": baseline_path.name,
            "bytes": len(baseline_bytes),
            "sha256": sha(baseline_bytes),
        },
        "positive": positive,
        "mutation_count": len(mutations),
        "mutations": mutations,
        "all_mutations_rejected_as_expected": all_rejected_as_expected,
        "result": "PASS" if all_rejected_as_expected else "FAIL",
        "runtime_state": "LOCAL_READ_ONLY_TEST_ONLY",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all_rejected_as_expected else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StopValidation as exc:
        print(json.dumps({"result": "FAIL", "status": exc.code}, indent=2))
        raise SystemExit(2)
