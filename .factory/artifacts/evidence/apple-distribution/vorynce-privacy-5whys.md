# Vorynce Privacy Finding Correction

The prior preflight treated microphone access as collected data. Source
requirements and `Resources/PrivacyInfo.xcprivacy` show local-only processing
with no collected data declaration.

1. Why was privacy reported as contradictory? The manifest put microphone access
   in `collected_data` and `declared_data`.
2. Why did that happen? Access and collection were represented by one field.
3. Why was the distinction absent? The product manifest schema was simplified
   before archive/source privacy inspection.
4. Why did validation accept it? The validator compared two fields without
   checking the shipped privacy manifest.
5. Why was the result treated as a blocker? The preflight lacked a source-backed
   distinction between local access and transmission/collection.

Correction: represent microphone as `accessed_data` and keep collected and
declared data empty, matching the product's local-only privacy manifest.

Recurrence guard: the Vorynce preflight test requires no privacy contradiction
when the manifest and product declaration both report no collected data.
