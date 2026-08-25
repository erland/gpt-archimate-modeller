from pathlib import Path
import yaml

PARTITIONS=["motivation","strategy","business","application","technology","physical","implementation-migration","composite"]

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def write_yaml(path,data):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")

def migrate(root):
    root=Path(root)
    p=read_yaml(root/"project.yaml")
    p["format_version"]="0.1"
    p["package_layout_version"]="0.1"
    p.setdefault("project",{}).setdefault("archimate_version","3.2")
    write_yaml(root/"project.yaml",p)

    for part in PARTITIONS:
        f=root/"model"/"elements"/f"{part}.yaml"
        if not f.exists():
            write_yaml(f,{"elements":[]})

    defaults={
        "model/relationships.yaml":{"relationships":[]},
        "sources/sources.yaml":{"sources":[]},
        "sources/references.yaml":{"references":[]},
        "extensions/extensions.yaml":{"extensions":{}},
        "extensions/specializations.yaml":{"specializations":{}},
        "issues/issues.yaml":{"issues":[]},
        "identity/id-counters.yaml":{"counters":{}},
        "changes/index.yaml":{"changes":[]},
        "versioning/history.yaml":{"history":[]}
    }
    for rel,data in defaults.items():
        f=root/rel
        if not f.exists():
            write_yaml(f,data)

    for d in ["queries","reports","views","exports","changes","versioning","migrations"]:
        (root/d).mkdir(parents=True,exist_ok=True)

    if not (root/"CHANGELOG.md").exists():
        (root/"CHANGELOG.md").write_text("# Changelog\n",encoding="utf-8")
