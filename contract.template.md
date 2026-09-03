# Idioca Box Contract: `[name]`

**Contract version:** `[version]`  
**Status:** Draft  
**Maintainers:** `[people or team]`  
**Implementation:** `[repository, image, package, or other reference]`

Start with what is known and keep the contract proportional to the box. Remove prompts that do not apply, and describe externally observable guarantees rather than internal implementation details.

AI may be used to draft and tighten this contract, identify missing information, and check it against the [Idioca Box Spec](IdiocaSpec.md). Humans remain responsible for approving its meaning, boundaries, and acceptance criteria.

## 1. Purpose and scope

**Purpose:** `[Why does this box exist?]`  
**Workload:** `[What bounded work does it perform?]`  
**Outside its scope:** `[What does it deliberately not do?]`

## 2. Interfaces

Describe each way that users or other components interact with the box.

| Direction | Name | Interface and format | Meaning or guarantee |
|---|---|---|---|
| Input | `[name]` | `[API, event, file, database, CLI, etc.]` | `[what it represents and requires]` |
| Output | `[name]` | `[API, event, file, database, CLI, etc.]` | `[what consumers may rely on]` |

**Errors and failures:** `[How are errors exposed, invalid inputs rejected, retries handled, and unavailable dependencies reported?]`

## 3. Semantic contract

**Meaning:** `[Define the domain meaning that consumers must preserve or may rely upon. Include units, time, provenance, authority, invariants, assumptions, or information preservation where relevant.]`

## 4. Dependencies and configuration

| Dependency or setting | Required version or value | Purpose | If unavailable or omitted |
|---|---|---|---|
| `[service, storage, dataset, setting, etc.]` | `[version, range, value, or externally supplied]` | `[why it is needed]` | `[failure, fallback, or default]` |

Record required networking, permissions, secrets, runtime limits, and infrastructure without including secret values.

## 5. State and storage

**Authoritative state:** `[What must survive replacement, where is it stored, and who owns it?]`  
**Access and coordination:** `[What may this box read or change, and how is shared access coordinated?]`  
**Transient state:** `[What caches or working data may be discarded?]`  
**Recovery:** `[How is authoritative information backed up and recovered?]`

## 6. Verification

List the smallest useful set of externally verifiable acceptance criteria.

| Acceptance criterion | Evidence |
|---|---|
| `[observable behaviour that must hold]` | `[test, fixture, schema, command, or other evidence]` |
| `[important failure or semantic invariant]` | `[how it is verified]` |

A replacement implementation must be able to satisfy substantially the same criteria.

## 7. Deployment and operation

**Deployment:** `[What is deployed, and how is it started, stopped, and identified?]`  
**Observation:** `[How are health, progress, results, logs, or metrics exposed?]`  
**Recovery and replacement:** `[How can a competent maintainer diagnose, recover, and replace the box without undocumented knowledge?]`

## 8. System composition and orchestration

**System role:** `[Who consumes this box, what triggers it, and where does it belong in the workflow?]`  
**Coordination:** `[Who coordinates the workflow, or why is orchestration unnecessary?]`  
**Coupling constraints:** `[Which relationships must remain stable or must not be introduced?]`

## Change history

| Contract version | Date | Change | Migration |
|---|---|---|---|
| `[version]` | `[YYYY-MM-DD]` | `[summary]` | `[not required, or instructions]` |
