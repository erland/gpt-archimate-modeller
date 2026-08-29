#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import yaml
import unicodedata

ID_RE = re.compile(r"^[A-Z]{3}-[0-9]{6}$")

TYPE_PREFIX = {
    # Motivation
    "Stakeholder":"MOT","Driver":"MOT","Assessment":"MOT","Goal":"MOT","Outcome":"MOT",
    "Principle":"MOT","Requirement":"MOT","Constraint":"MOT","Meaning":"MOT","Value":"MOT",
    # Strategy
    "Resource":"STR","Capability":"STR","ValueStream":"STR","CourseOfAction":"STR",
    # Business
    "BusinessActor":"BUS","BusinessRole":"BUS","BusinessCollaboration":"BUS",
    "BusinessInterface":"BUS","BusinessProcess":"BUS","BusinessFunction":"BUS",
    "BusinessInteraction":"BUS","BusinessEvent":"BUS","BusinessService":"BUS",
    "BusinessObject":"BUS","Contract":"BUS","Representation":"BUS","Product":"BUS",
    # Application
    "ApplicationComponent":"APP","ApplicationCollaboration":"APP","ApplicationInterface":"APP",
    "ApplicationFunction":"APP","ApplicationProcess":"APP","ApplicationInteraction":"APP",
    "ApplicationEvent":"APP","ApplicationService":"APP","DataObject":"APP",
    # Technology
    "Node":"TEC","Device":"TEC","SystemSoftware":"TEC","TechnologyCollaboration":"TEC",
    "TechnologyInterface":"TEC","Path":"TEC","CommunicationNetwork":"TEC",
    "TechnologyFunction":"TEC","TechnologyProcess":"TEC","TechnologyInteraction":"TEC",
    "TechnologyEvent":"TEC","TechnologyService":"TEC","Artifact":"TEC",
    # Physical
    "Equipment":"PHY","Facility":"PHY","DistributionNetwork":"PHY","Material":"PHY",
    # Implementation
    "WorkPackage":"IMP","ImplementationEvent":"IMP","Deliverable":"IMP","Plateau":"IMP","Gap":"IMP",
    # Composite
    "Grouping":"CMP","Location":"CMP"
}

def normalize_name(value):
    value = unicodedata.normalize("NFKC", value or "")
    value = value.casefold().strip()
    value = re.sub(r"[\W_]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())

def expected_prefix_for_type(type_name):
    return TYPE_PREFIX.get(type_name)

def next_id(counters, prefix):
    current = int(counters.get(prefix, 0))
    new_value = current + 1
    counters[prefix] = new_value
    return f"{prefix}-{new_value:06d}"

def load_counters(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return data

def save_counters(path, data):
    Path(path).write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8"
    )
