# ANX-Bench v0.1 Event Registries

This directory contains versioned event registries for ANX-Bench v0.1 longitudinal and event-study analyses. Each registry is a frozen exposure contract, not an analysis note. It records the eligible `event_id` values for a wave, the externally sourced event timestamp, exposure and comparison windows, affected domains, competing events, lock date, and amendment history.

Event registries must be frozen before any ANX-Bench response outcomes, score distributions, subgroup estimates, or item-level summaries from the relevant wave are inspected. Freezing the registry before outcome inspection prevents analysts from adding, removing, retiming, or reclassifying events after seeing whether anxiety scores moved.

For confirmatory event-study work, the registry is the source of truth for wave `event_id` fields. Every response row, preregistration, analysis script, and public report must use an `event_id` present in the frozen registry for that wave. The row-level `event_exposure_window`, `baseline_or_followup`, and `fielding_time_relative_to_event_hours` values must be derived from the frozen timestamp and windows in the registry, not recomputed from ad hoc event definitions.

Non-event calibration waves must still use an explicit registry record. The reserved `event_id` is `no_event`, with `category` set to `no_event` and event timestamp fields marked not applicable by the schema. This makes calibration waves auditable while preserving a clear distinction between absence of an event and missing event metadata.

Amendments after registry lock must be recorded in `amendment_history`. Clerical corrections may preserve confirmatory status only when they do not change event inclusion, classification, timing, affected domains, or window assignment. Any amendment made after outcome inspection that changes a substantive event-study exposure definition makes the affected analysis exploratory.
