"""
Report generator for Production Readiness Review results.
"""

from checklist import AuditResult

class ReportGenerator:
    @staticmethod
    def to_markdown(result: AuditResult) -> str:
        verdict = "APPROVED FOR PRODUCTION" if result.passed else "REJECTED - REMEDIATION REQUIRED"
        lines = [
            f"# Production Readiness Review Report",
            f"",
            f"**Verdict**: `{verdict}`",
            f"**Score**: {result.score}/{result.max_score} ({result.percentage}%)",
            f"",
            f"| Check Area | Status | Message |",
            f"| :--- | :--- | :--- |"
        ]
        for f in result.findings:
            lines.append(f"| {f['check']} | `{f['status']}` | {f['msg']} |")

        return "\n".join(lines)
