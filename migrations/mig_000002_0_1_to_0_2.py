from pathlib import Path
import yaml

DEFAULT_IMPACT_THEME_PATH="extensions/impact-themes.yaml"

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def write_yaml(path,data):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")

def migrate(root):
    root=Path(root)
    descriptor=read_yaml(root/"project.yaml") or {}
    if str(descriptor.get("format_version"))!="0.1":
        raise ValueError("MIG-000002 requires source format 0.1")

    files=descriptor.setdefault("files",{})
    theme_rel=files.get("impact_themes")
    if not theme_rel:
        theme_rel=DEFAULT_IMPACT_THEME_PATH
        files["impact_themes"]=theme_rel

    theme_path=root/theme_rel
    if theme_path.exists():
        theme_doc=read_yaml(theme_path) or {}
        themes=theme_doc.get("impact_themes")
        if themes is None:
            themes=[]
        if not isinstance(themes,list):
            raise ValueError(f"{theme_rel} impact_themes must be a list")
        theme_doc={"format_version":"0.2","impact_themes":themes}
    else:
        theme_doc={"format_version":"0.2","impact_themes":[]}
    write_yaml(theme_path,theme_doc)

    descriptor["format_version"]="0.2"
    descriptor.setdefault("package_layout_version","0.1")
    write_yaml(root/"project.yaml",descriptor)

    # These are derived transport/cache artifacts. Leaving old copies would make the
    # migrated workspace appear checksummed/indexed when the source files have changed.
    (root/"PACKAGE-MANIFEST.yaml").unlink(missing_ok=True)
    (root/"MODEL-INDEX.json").unlink(missing_ok=True)
