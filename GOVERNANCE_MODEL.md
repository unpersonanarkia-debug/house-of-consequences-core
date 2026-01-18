# House of Consequences Core  
## GOVERNANCE_MODEL.md  
*Version 1.0 | January 2026 | House of Consequences Core (AGPL-3.0)*

---

## 0. Purpose and Scope

This document defines the governance model of *House of Consequences Core* (“HoC Core”), an open, public-interest protocol designed to function as a permanent *watchdog over power, decisions, and institutional normalization*.

HoC Core belongs to the public commons. Commercial governance services, dashboards, and enterprise integrations operate separately under distinct agreements, without ownership or control over the core protocol.

This governance model ensures:
- Independence from institutional capture
- Structural transparency
- Legal and technical traceability
- Protection against authoritarian misuse
- Community stewardship over systemic power analysis

---

## 1. Foundational Principles and Red Lines

### 1.1 Core Principles

HoC Core is governed by the following immutable principles:

*Transparency*  
All audit logs, decision flows, and governance changes are publicly inspectable and cryptographically verifiable.

*Independence*  
No exclusive institutional control, licensing, or dependency structures are permitted.

*Accountability*  
The system exposes power, it does not conceal it. HoC Core exists to reveal consequences, not justify authority.

*Decentralization*  
Governance authority is distributed through a DAO-based and community-controlled model.

*Human Rights and Civil Protection*  
HoC Core must never be used for repression, surveillance, profiling, or political targeting.

---

### 1.2 Red Lines (Non-Negotiable Constraints)

Any modification violating these requires unanimous DAO approval and public constitutional review:

1. No features enabling surveillance, repression, or population profiling.
2. No exclusive access agreements with states or corporations.
3. No closed or proprietary forks of the core protocol.
4. No suppression, distortion, or hiding of core analytical outputs in commercial products.
5. No opaque or non-auditable AI/ML models.
6. No centralized control over data, logic, or governance.
7. No integration that enables discrimination, coercion, or manipulation of civic processes.

---

## 2. Governance Roles and Authority Boundaries

| Role | Description | Authority |
|------|-------------|-----------|
| *Core Maintainers* | Technical stewards (initially: unpersonanarkia-debug + contributors) | Merge PRs, publish releases, propose RFCs. No unilateral veto. |
| *DAO Members* | Reputation-based participants | Vote on governance, approve changes, audit logs. |
| *Citizen Nodes* | NGOs, journalists, civil groups | Operate mirror instances, submit reports, validate anomalies. |
| *Institutional Users* | Governments, enterprises | Access APIs under governance contracts. No control over core logic. |
| *Public Auditors* | Any individual | Inspect hashes, logs, governance records, and propose corrections. |

---

## 3. DAO Structure and Decision Process

HoC Core governance operates through a decentralized autonomous organization (DAO), initially deployed as a contractual governance layer, with the option to transition to a legal hybrid association or foundation.

### 3.1 Tooling Stack

- *Governance:* Aragon DAO
- *Voting:* Snapshot (off-chain, gas-free)
- *Treasury:* Gnosis Safe
- *Token Model:* Reputation-based ERC20Votes (non-transferable reputation layer + optional economic layer)

---

### 3.2 Governance Workflow (RFC → DAO → Implementation)

1. *Request for Comments (RFC)*  
   Open proposal in /rfc/YYYY-NN-title.md.

2. *Public Discussion*  
   Minimum 14-day review via GitHub + Snapshot forum.

3. *DAO Vote*  
   7-day Snapshot vote. Quorum: 10% DAO participation.  
   Voting model: conviction-weighted or reputation-weighted voting.

4. *Implementation*  
   Core Maintainers merge approved changes.

5. *Documentation*  
   Final decision archived in /governance/DECISIONS/DAO-YYYY-NN.md.

6. *Audit Anchoring*  
   Merkle root of decision + code state hashed to public blockchain (L2).

---

### 3.3 Delegation and Representation

Trusted delegates (e.g., NGOs, academic institutions, watchdog organizations) may represent members through opt-in delegation.

---

## 4. Licensing and Governance Layering

| Layer | License | Description |
|------|---------|-------------|
| *Core Protocol Code* | AGPL-3.0 | All modifications must be public and returned to the commons. |
| *Governance Documents* | CC-BY-SA-4.0 | Freely reusable, modifications must remain open. |
| *Enterprise Services* | Commercial License | Paid services built atop the core without owning or modifying it. |
| *Data* | Source-specific | Subject to GDPR, public data licenses, and national law. |

License changes require DAO approval.

No entity may distribute a closed fork, shadow fork, or proprietary derivative of the core protocol.

---

## 5. Auditability and Traceability

### 5.1 Cryptographic Audit Layer

All audit logs, governance decisions, and case records generate cryptographic hashes anchored to a public blockchain.

Minimum required endpoints:
- GET /audit/proof/{case_id}
- GET /cases
- GET /decisions
- GET /anomalies

No personal data is written to chain.

---

### 5.2 Whistleblower Protection Path

A secure, pseudonymous reporting channel is mandatory:
- Onion/Tor access
- IPFS-backed document storage
- Schema-validated submissions
- DAO-reviewed handling
- Immutable audit trail

The whistleblower pipeline is protected from institutional override.

---

### 5.3 Oversight Council

DAO elects 3–5 independent oversight members annually (academics, legal experts, civil society).  
Mandate:
- Quarterly audits
- Public compliance reports
- Governance integrity reviews

---

## 6. AI, Analytics, and Model Governance

All analytical models must:
- Be open-source
- Be explainable
- Be auditable
- Have documented training data sources
- Be versioned and hash-anchored

Black-box models are prohibited.

No automated decision outputs may be concealed from end-users.

---

## 7. Change Management and Constitutional Protection

This governance model functions as the *constitutional layer* of HoC Core.

Changes require:
- RFC process
- DAO approval
- Public documentation
- Blockchain anchoring

Historical versions are preserved under /governance/DECISIONS/.

---

## 8. Legal Positioning

HoC Core operates initially as a *contractual commons governance system*.

In Finland and comparable jurisdictions, it may be mirrored by:
- A registered association
- A foundation
- Or a cooperative structure
— whose bylaws must reflect this governance model exactly.

The DAO governs protocol evolution; any legal wrapper must follow DAO decisions.

---

## 9. Final Declaration

House of Consequences Core exists to prevent the normalization of harm, the invisibilization of power, and the erosion of accountability.

It is not a platform.
It is not a service.
It is a constitutional instrument for collective foresight.

---

*End of GOVERNANCE_MODEL.md v1.0*
