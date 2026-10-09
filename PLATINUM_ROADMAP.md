# Home Assistant Platinum readiness work items

This backlog breaks the work toward the [Home Assistant Integration Quality
Scale](https://developers.home-assistant.io/docs/core/integration-quality-scale/checklist/)
into independently actionable items. It is a proposed work plan, not a claim
that the integration currently meets any particular quality tier. Recheck the
official checklist as work progresses because its requirements can change.

## Proposed work items

### 1. Add automated integration tests

Cover config and options flows, setup and unload, coordinator updates, entity
platforms, and registered services using mocked Redback API responses.

**Acceptance criteria**

- Tests run without Redback credentials or network access.
- Cover successful setup and updates, invalid credentials, expired
  authentication, unavailable API, and malformed or incomplete API responses.
- Test important service input and failure paths.
- Run the tests in CI alongside the existing HACS and hassfest validation.

### 2. Make API updates resilient to incomplete data

Handle absent, empty, and invalid optional fields without losing otherwise
usable inverter or battery data. Include the multiple-inverter and empty PV-size
failure reported in [issue #20](https://github.com/cabberley/HA_RedbackTech/issues/20).
Coordinate any required fix in `redbacktechpy` with that dependency's
maintainers.

**Acceptance criteria**

- A missing or invalid optional value does not crash setup or discard unrelated
  device data.
- Transient service failures and authentication failures are surfaced through
  Home Assistant's coordinator/config-entry mechanisms.
- Automated tests cover malformed payloads, multiple devices, recovery, and
  authentication expiry.

### 3. Complete config-entry flows and lifecycle

Finish the reconfigure flow and exercise initial setup, reauthentication,
options updates, reload, and removal as supported config-entry workflows.

**Acceptance criteria**

- Reconfigure validates and saves updated credentials instead of displaying an
  unimplemented form.
- Each flow preserves existing options and reports actionable connection or
  authentication errors.
- Reload and removal leave no stale integration data, entities, or services.
- Tests cover success, validation errors, and lifecycle cleanup.

### 4. Add safe diagnostics

Provide a diagnostics download with the device and integration state needed to
troubleshoot setup and update issues.

**Acceptance criteria**

- Diagnostics follow Home Assistant's diagnostics conventions and have tests.
- Passwords, client secrets, access/refresh tokens, and other credentials are
  redacted before data is returned.
- The output contains enough non-sensitive context to investigate device,
  coordinator, and API problems.

### 5. Audit entities, services, and translations

Review all platforms and user-facing controls against Home Assistant's entity,
device, service, and translation conventions.

**Acceptance criteria**

- Entity identifiers remain stable and entities expose correct device
  association, availability, units, and state metadata where applicable.
- Service schemas and descriptions match the accepted inputs and are covered
  by tests; user-facing service and flow strings are translated.
- Unsupported hardware capabilities and invalid control requests fail safely
  with useful feedback.

### 6. Complete user and maintainer documentation

Document setup, supported devices and capabilities, configuration options,
entities, services, control limitations, troubleshooting, and safe operation.

**Acceptance criteria**

- Instructions match the actual config flows, options, services, and entities.
- Explain known API and hardware limitations, recovery steps, and the data
  needed when reporting a problem.
- Update documentation together with future user-visible changes.

### 7. Verify Platinum readiness against the current checklist

After the implementation work is complete, review every applicable rule in the
official quality-scale checklist, including all lower-tier requirements.

**Acceptance criteria**

- Each applicable rule has evidence in code, tests, documentation, or CI.
- Remaining gaps are recorded as separate work items; do not mark the
  integration Platinum-ready until all applicable requirements are met.

## Existing feature backlog

The README's existing feature ideas remain separate from the quality-scale
readiness work:

- Add control for the relays on SI model inverters.
- Evaluate moving API authentication to Home Assistant-managed OAuth
  credentials.
- Add a service for bulk multi-day schedule and envelope creation.
