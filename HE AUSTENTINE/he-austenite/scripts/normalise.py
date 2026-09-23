"""Derived quantities and validation helpers for HE-Austenite."""
import json, sys, math
from jsonschema import Draft202012Validator  # pip install jsonschema

def ni_equivalent_hirayama(c):
    """Hirayama-Ogirima type Ni equivalent (wt%). Returns None if inputs missing."""
    need = ("Ni","Cr","Mo","Si","Mn","C","N")
    if any(c.get(k) is None for k in need):
        return None
    return (c["Ni"] + 0.65*c["Cr"] + 0.98*c["Mo"] + 1.05*c["Mn"]
            + 0.35*c["Si"] + 12.6*(c["C"] + c.get("N", 0.0)))

def md30(c):
    """Angel Md30 (degC): temperature for 50% martensite at 30% strain."""
    need = ("C","Si","Mn","Cr","Ni","Mo")
    if any(c.get(k) is None for k in need):
        return None
    n = c.get("N") or 0.0
    return (413 - 462*(c["C"] + n) - 9.2*c["Si"] - 8.1*c["Mn"]
            - 13.7*c["Cr"] - 9.5*c["Ni"] - 18.5*c["Mo"])

def relative_ratio(rec):
    a, h = rec.get("property_reference"), rec.get("property_h2")
    if a in (None, 0) or h is None:
        return None
    return round(h / a, 3)

def validate(records, schema_path="scripts/schema.json"):
    schema = json.load(open(schema_path))
    v = Draft202012Validator(schema)
    errs = []
    for r in records:
        for e in v.iter_errors(r):
            errs.append((r.get("record_id"), e.message))
    return errs

if __name__ == "__main__":
    recs = json.load(open(sys.argv[1]))
    for r in recs:
        c = r.get("composition_wt_pct") or {}
        derived = r.setdefault("derived_fields", [])
        if r.get("ni_equivalent") is None:
            nieq = ni_equivalent_hirayama(c)
            if nieq is not None:
                r["ni_equivalent"] = round(nieq, 2); derived.append("ni_equivalent")
        if r.get("relative_ratio") is None:
            rr = relative_ratio(r)
            if rr is not None:
                r["relative_ratio"] = rr; derived.append("relative_ratio")
    errs = validate(recs)
    print(f"{len(recs)} records, {len(errs)} schema errors")
    for rid, m in errs[:20]:
        print(" ", rid, m)
    json.dump(recs, open(sys.argv[1], "w"), indent=1)
