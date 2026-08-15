from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .claims import get_claims
from .compare import compare_text
from .models import ScanReport
from .scanner import scan_text


def _read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def _print_scan(report: ScanReport, path: str) -> None:
    counts = report.counts
    print(f"file: {path}")
    print(f"sha256: {report.sha256}")
    print(
        "summary: "
        f"{report.characters} chars, {report.words} words, "
        f"{counts['critical']} critical, {counts['warning']} warning, "
        f"{counts['info']} info"
    )
    if not report.findings:
        print("findings: none")
        return
    print("findings:")
    for finding in report.findings:
        print(
            f"  {finding.line}:{finding.column} "
            f"[{finding.severity}] {finding.category} "
            f"{finding.codepoint} {finding.escaped} — {finding.message}"
        )


def _scan_command(args: argparse.Namespace) -> int:
    report = scan_text(_read_text(args.path))
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_scan(report, args.path)

    threshold = {"none": 99, "warning": 1, "critical": 2}[args.fail_on]
    levels = {"info": 0, "warning": 1, "critical": 2}
    return int(any(levels[finding.severity] >= threshold for finding in report.findings))


def _compare_command(args: argparse.Namespace) -> int:
    result = compare_text(_read_text(args.before), _read_text(args.after))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"identical: {str(result['identical']).lower()}")
        print(f"similarity: {result['similarity']:.2%}")
        print(f"canonical equivalent: {str(result['canonical_equivalent']).lower()}")
        print(
            "changes: "
            f"+{result['inserted']} -{result['deleted']} "
            f"~{result['replaced_before']}→{result['replaced_after']} chars"
        )
        print(f"findings before: {result['findings_before']}")
        print(f"findings after: {result['findings_after']}")
    return 0


def _claims_command(args: argparse.Namespace) -> int:
    claims = get_claims()
    if args.json:
        print(json.dumps(claims, ensure_ascii=False, indent=2))
    else:
        for claim in claims:
            print(f"{claim['provider']} {claim['system']}: {claim['status']}")
            print(f"  {claim['summary']}")
            print(f"  detector: {claim['official_detector']}")
            print(f"  source: {claim['source']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="textmark",
        description="Audit machine-readable signals and watermark claims in text.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="scan UTF-8 text for hidden Unicode signals")
    scan.add_argument("path", help="UTF-8 file path, or - for standard input")
    scan.add_argument("--json", action="store_true", help="emit a machine-readable report")
    scan.add_argument(
        "--fail-on",
        choices=("none", "warning", "critical"),
        default="none",
        help="return exit status 1 when a finding meets the threshold",
    )
    scan.set_defaults(handler=_scan_command)

    compare = subparsers.add_parser("compare", help="compare two versions of a text")
    compare.add_argument("before")
    compare.add_argument("after")
    compare.add_argument("--json", action="store_true")
    compare.set_defaults(handler=_compare_command)

    claims = subparsers.add_parser("claims", help="show sourced vendor watermark claims")
    claims.add_argument("--json", action="store_true")
    claims.set_defaults(handler=_claims_command)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    return 2
