class QualityEngine:
    @staticmethod
    def check_not_null(records, field):
        return all(r.get(field) is not None and str(r.get(field)).strip() != "" for r in records)
    @staticmethod
    def check_unique(records, field):
        seen = set()
        for r in records:
            val = r.get(field)
            if val in seen: return False
            seen.add(val)
        return True
