# Concept Registry Schema

Architecture completely separates knowledge from feature mapping scoring.
```python
@dataclass
class Concept:
  canonical_name: str
  aliases: list[Alias]
  family: str
  category: str
  confidence: str
  rejection_reason: str = None
```
Registry Version: 1.0.0
Registry Hash: 9c71ee88a1f7dc7a32a9d0e7883b642277e794ad38e2f2fcfa26625aa9d3a497
