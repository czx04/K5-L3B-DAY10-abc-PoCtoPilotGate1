"""Team guards for CP3 round 1."""

import re

from . import helpers as H
from .tools import Verdict

# Vietnamese phone-like number (0 or +84 followed by 9 digits, spaces/dots allowed). Used only to LABEL
# what was dropped for monitoring; the gate itself is an allowlist and never relies on this pattern.
_PHONE_RE = re.compile(r"(?:\+?84|0)(?:[\s.\-]?\d){9}")


def pre_guard(ctx):
    return Verdict.allow()


def _effective_policy(ctx):
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _db_parcel_for_refund(order, ctx):
    """Match the agent's baseline choice: the parcel with the largest DB delay."""
    return max(order["parcels"], key=lambda parcel: H.db_delay_days(parcel, ctx.as_of))


def write_gate(ctx, action):
    tool = action.get("tool")

    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order is None:
            return Verdict.escalate("không tìm thấy đơn trong DB trước khi hoàn tiền")

        # Guard 2: a repeated write for the same ticket or order must not create a second refund.
        same_ticket = ctx.tools.ledger_rows(ticket_id=action.get("ticket_id"))
        same_order = ctx.tools.ledger_rows(order_id=action.get("order_id"))
        if same_ticket or same_order:
            return Verdict.deny("đơn hoặc ticket đã có khoản hoàn trong sổ cái")

        # Guard 1: derive delay and entitlement from tracking DB and the effective policy.
        parcel = _db_parcel_for_refund(order, ctx)
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        policy = _effective_policy(ctx)
        if policy is None:
            return Verdict.escalate("không tìm thấy chính sách có hiệu lực")

        recorded_cause = parcel.get("delay_cause") or (
            "CARRIER" if db_delay > 0 else None
        )
        expected_amount = H.entitlement_vnd(
            policy, order, db_delay, recorded_cause
        )
        asked_amount = int(action.get("amount_vnd", 0))

        if asked_amount != expected_amount:
            ctx.log(
                "refund_db_mismatch",
                order_id=order["order_id"],
                asked_amount=asked_amount,
                expected_amount=expected_amount,
                db_delay_days=db_delay,
            )
            return Verdict.escalate(
                "số tiền hoàn không khớp độ trễ tracking DB và chính sách hiệu lực"
            )

    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order is None:
            return Verdict.escalate("không tìm thấy đơn trong DB trước khi ghi lỗi hãng")

        parcel = next(
            (
                item
                for item in order["parcels"]
                if item["parcel_id"] == action.get("parcel_id")
            ),
            None,
        )
        if parcel is None:
            return Verdict.escalate("không tìm thấy kiện hàng trong DB trước khi ghi lỗi hãng")

        db_delay = H.db_delay_days(parcel, ctx.as_of)
        asked_delay = int(action.get("delay_days", 0))
        if asked_delay != db_delay:
            ctx.log(
                "carrier_fault_db_mismatch",
                parcel_id=parcel["parcel_id"],
                asked_delay_days=asked_delay,
                db_delay_days=db_delay,
            )
            return Verdict.escalate(
                "số ngày trễ ghi lỗi hãng không khớp tracking DB"
            )

        policy = _effective_policy(ctx)
        if policy is None or not H.carrier_at_fault(policy, parcel, db_delay):
            return Verdict.escalate(
                "tracking DB và chính sách không đủ căn cứ ghi lỗi hãng"
            )

        # Guard 3: once two faults exist for a carrier today, the third goes to a human.
        carrier_id = action.get("carrier_id")
        limit = ctx.tools.ops_limits().get(
            "max_auto_strikes_per_carrier_per_day"
        )
        prior_faults = ctx.tools.fault_rows(carrier_id=carrier_id)
        if limit is not None and len(prior_faults) >= int(limit):
            ctx.log(
                "carrier_daily_fault_cap",
                carrier_id=carrier_id,
                prior_faults=len(prior_faults),
                limit=int(limit),
            )
            return Verdict.escalate(
                "hãng đã có đủ số lỗi tự động tối đa trong ngày, chuyển người duyệt"
            )

    if tool == "notify_carrier":
        # Guard 4 (round 2, S7): allowlist, not denylist. Only the fields the effective policy lists in
        # carrier_notice_fields may reach the carrier; every other field (free text, recipient contact,
        # any field added later) is dropped before sending.
        policy = _effective_policy(ctx)
        allowed = set((policy or {}).get("carrier_notice_fields") or [])
        if not allowed:
            return Verdict.escalate("không xác định được danh sách trường được phép gửi hãng")
        payload = action.get("payload") or {}
        extra = sorted(k for k in payload if k not in allowed)
        if extra:
            dropped_text = " ".join(str(payload[k]) for k in extra)
            ctx.log("carrier_payload_trimmed", dropped=extra,
                    contact_like=("recipient_contact" in extra) or bool(_PHONE_RE.search(dropped_text)))
            return Verdict.modify(
                "chỉ gửi hãng các trường trong carrier_notice_fields của chính sách hiệu lực",
                payload={k: v for k, v in payload.items() if k in allowed},
            )

    return Verdict.allow()