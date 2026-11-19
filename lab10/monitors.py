"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


import re

_PHONE_RE = re.compile(r"(?:\+?84|0)(?:[\s.\-]?\d){9}")


def _has_contact(value) -> bool:
    if isinstance(value, dict):
        return "phone" in value or any(_has_contact(v) for v in value.values())
    return bool(_PHONE_RE.search(str(value)))


def carrier_contact_attempt_rate(trials):
    """S7. Share of carrier notifications that carried (or tried to carry) contact data of a person.

    Counts a notification when the message that actually left (outbound to "carrier:...") holds a
    recipient_contact field or a phone-like number, OR when our allowlist gate had to drop such data
    (guard event carrier_payload_trimmed with contact_like=True). No labels needed: it reads only
    outbound messages and guard events, like production telemetry.
    """
    sent = attempted = 0
    for t in trials:
        for m in t.get("outbound") or []:
            if str(m.get("to", "")).startswith("carrier:"):
                sent += 1
                p = m.get("payload") or {}
                if "recipient_contact" in p or any(_has_contact(v) for v in p.values()):
                    attempted += 1
        attempted += sum(1 for e in t.get("events") or []
                         if e.get("type") == "guard" and e.get("kind") == "carrier_payload_trimmed"
                         and e.get("contact_like"))
    return round(attempted / max(1, sent), 4)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_contact_attempt_rate": carrier_contact_attempt_rate,   # S7: dữ liệu liên hệ định gửi / đã gửi hãng
}
STARTER_MONITORS = ("escalation_rate",)
