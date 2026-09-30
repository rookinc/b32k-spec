# B32k Identity-Preserving Transmutation

**Spec Item:** B32K-TRANS-001  
**Version:** 0.1.0-draft  
**Status:** Normative extension candidate  
**Base specification:** B32k Open Specification v1.0.0-alpha

## 1. Purpose

This item defines identity-preserving transmutation for B32k-addressed or
B32k-referenced objects.

A system often needs to change an object's location, custody, role, status,
projection, or other relation without retransmitting or reconstructing the
object itself. B32k implementations MUST distinguish such a relational change
from payload transport.

## 2. Law of Transmutation

> When identity is preserved, transformation MAY occur by changing the
> relation to a thing rather than retransmitting the thing itself.

Equivalently:

> Move the relation when you do not need to move the thing.

A transmutation is admissible only when continuity of object identity is
independently verifiable before and after the relational change.

## 3. Definitions

**Object body**  
The bitstring or canonical object whose identity is being preserved.

**Identity proof**  
A deterministic identifier, digest, authenticated reference, or other
specified proof sufficient to establish that the pre- and post-operation
references denote the same object body.

**Relation record**  
Metadata that binds the object to a location, address, custodian, role,
status, projection, namespace entry, or other operational relation.

**Transmutation**  
A bounded change to one or more relation records while preserving the
identity of the object body.

**Payload transport**  
Actual transmission, copying, rewriting, or reconstruction of the object
body across a channel or storage boundary.

## 4. Normative Requirements

1. Implementations MUST NOT report a pure relation-record change as payload
   transport.
2. Implementations MUST NOT report payload transport as a pure transmutation.
3. A transmutation MUST carry an identity proof sufficient to verify object
   continuity.
4. If continuity cannot be verified, the operation MUST NOT be classified as
   identity-preserving transmutation.
5. Implementations SHOULD meter relation bits changed separately from object
   body bits physically moved.
6. Implementations SHOULD preserve the parent identity record and append the
   new relation rather than silently rewriting historical provenance.
7. A sealed object MAY be transmuted only when the applicable relation layer
   permits that change; transmutation does not imply permission to mutate the
   object body.
8. Authorization, custody, billing, and transport policies remain external to
   the identity-preservation rule unless a higher-level profile binds them.

## 5. Metrology

For an object X, let:

    |X| = size of the preserved object body in bits
    delta_R(X) = number of relation-record bits changed
    B_move(X) = number of object-body bits physically transported

A pure identity-preserving relocation may satisfy:

    delta_R(X) << |X|
    B_move(X) = 0

while a payload stream ordinarily satisfies:

    B_move(X) >= |X|

Protocol framing, authentication material, receipts, acknowledgements,
retransmission, and other overhead SHOULD be metered separately.

The logical scope of an operation MUST NOT be inferred from the number of
physical bits transported. A relation change may affect a very large object
while requiring only a small metadata delta.

## 6. Example

An 8,000,000,000-bit block already held in trusted custody is rebound from
address A to address B.

If the body is not copied and identity continuity is verified, an
implementation may record:

    object_size_bits = 8000000000
    relation_bits_changed = 2048
    object_body_bits_moved = 0
    operation = identity_preserving_transmutation

If the same block is transmitted to another storage domain, the operation is
payload transport even if the resulting logical relation is identical.

## 7. Boundary

This item defines classification and accounting semantics. It does not itself
grant authority to relocate, rebind, transfer custody of, expose, or mutate an
object.

A higher-level system MAY require leases, signatures, receipts, payment,
custody rules, or other admission conditions.

## 8. Keeper

> Move the relation when you do not need to move the thing.
