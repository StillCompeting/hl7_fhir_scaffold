# HL7 v2.x → FHIR Mapping Scaffold

This scaffold provides **one script per HL7 message type**.  
Each script ships with:
* A *stub HL7 message* constant (`STUB_HL7_MESSAGE`)
* A placeholder `hl7_to_fhir()` function returning an empty FHIR `Bundle`
* A `__main__` section that prints the Bundle JSON

## Quick Start

```bash
cd hl7_fhir_scaffold/scripts
pip install -r ../requirements.txt
python map_adt_a01.py
```

## Extending the Mapping

1. Edit each `hl7_to_fhir` to add segment‑to‑resource logic.  
2. Use `hl7apy` to parse the message and `fhir.resources` to build resources.  
3. Add unit tests or sample messages as needed.

## Adding More Message Types

* Edit `generate_scaffold.py` and append to `message_types`, then run it again.

-- Generated on 2025-04-20T13:01:20.622838
