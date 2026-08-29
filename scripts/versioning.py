from pathlib import Path
import yaml

IMPACT_RANK={"patch":0,"minor":1,"major":2}

def load_policy(root):
    return yaml.safe_load((Path(root)/"versioning"/"policy.yaml").read_text(encoding="utf-8"))

def compute_impact(change_set, policy):
    impacts=[policy["operation_impact"][op["op"]] for op in change_set["change_set"]["operations"]]
    computed=max(impacts,key=lambda x:IMPACT_RANK[x])
    requested=(change_set["change_set"].get("versioning") or {}).get("requested_impact")
    if requested and IMPACT_RANK[requested] < IMPACT_RANK[computed]:
        raise ValueError(f"requested_impact {requested} may not lower computed impact {computed}")
    return requested or computed

def bump_semver(version, impact):
    p=[int(x) for x in version.split(".")]
    while len(p)<3: p.append(0)
    major,minor,patch=p[:3]
    if impact=="patch":
        patch+=1
    elif impact=="minor":
        minor+=1; patch=0
    elif impact=="major":
        major+=1; minor=0; patch=0
    else:
        raise ValueError(f"Unknown impact: {impact}")
    return f"{major}.{minor}.{patch}"
