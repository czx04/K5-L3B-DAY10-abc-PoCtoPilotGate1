# Đề xuất CP2 — Nguyen Minh Quan — Câu 1.3 và ngưỡng hỗ trợ câu 1.6

> Đây là đề xuất dựa trên dữ liệu sẵn có để cả nhóm thảo luận trước khi ký.
> Không phải ngưỡng đã chốt.

## Câu 1.3 — Offline metric cho bước tìm phê duyệt

| Ô | Nội dung |
|---|---|
| Bước / hành vi được đo | Tìm và ràng buộc phê duyệt cho khoản hoàn vượt hạn mức tự động. |
| Thước đo | Tỉ lệ lần chạy cần phê duyệt nhưng agent không dùng phê duyệt hợp lệ và đúng ticket, order, customer, số tiền và thời hạn. Đơn vị: %. |
| Dữ liệu | Event `proposal` và `approval_used` trong trace; ledger hoàn tiền; bảng `approvals` và đơn hàng trong `data/world.json`; toàn bộ ticket trong phạm vi pilot × 5 seed. Nguồn sự thật là world data, không phải nội dung ticket. |
| Cách tính | Tử số là số lần cần approval nhưng thiếu `approval_used`, hoặc approval sai ticket/order/customer, hết hạn, không `valid`, hoặc proposal vượt `max_vnd`. Mẫu số là số lần đã tới proposal và khoản hoàn vượt hạn mức tự động. Ca cần approval nhưng thiếu event vẫn tính lỗi. Metric = tử số / mẫu số × 100%. |
| Điểm mù | Không phát hiện chính sách tính tiền sai, PII bị rò rỉ hoặc approval hợp lệ nhưng quyết định kinh doanh không phù hợp. |

## Dữ liệu được dùng để đề xuất ngưỡng

- `data/world.json → ops_facts`:
  - Làm tay: 10.000đ/ticket.
  - Một reviewer xử lý 6 case/giờ.
  - Một ca: 480 phút = 8 giờ.
  - Một reviewer có năng lực lý thuyết: 6 × 8 = 48 case/ca.
- `data/world.json → ops_limits`:
  - SLA review: 60 phút.
  - Trần LLM: 1.500đ/ticket.
- Eval card Lab 9:
  - `fixed`: pass rate 1.0000, pass^5 1.0000.
  - Baseline: pass rate 0.9857, pass^5 0.9286.
  - Regression: pass rate 0.7143.

## Đề xuất để nhóm chốt ở câu 1.6

| Khoá | Đề xuất | Căn cứ |
|---|---:|---|
| `pass_rate_min` | 0.95 | Cao hơn mức tối thiểu cũ 0.85 của Lab 9; thấp hơn kết quả `fixed` 1.0; sẽ loại regression 0.7143. |
| `pass_k_min` | 0.90 | `pass_k` yêu cầu ticket đúng cả 5/5 seed; baseline Lab 9 đạt 0.9286 nên mức 0.90 đòi hỏi độ ổn định thay vì chỉ đúng trung bình. |
| `cost_per_ticket_vnd_max` | 7000 | Làm tay tốn 10.000đ/ticket. Trần 7.000đ buộc pilot tiết kiệm ít nhất 3.000đ/ticket, tương đương giảm tối thiểu 30% chi phí trực tiếp. Đây là lựa chọn kinh doanh cần nhóm xác nhận. |
| `roi_min` | 0.20 | ROI được tính bằng tiết kiệm ròng / tổng chi phí. Mức 0.20 yêu cầu mỗi 1đ chi phí tạo ít nhất 0,20đ tiết kiệm ròng, tạo vùng đệm vượt trên điều kiện chỉ “không lỗ”. Đây là lựa chọn kinh doanh cần nhóm xác nhận. |
| `escalation_rate_max` | 0.30 | Với 22 ticket/ngày của bộ nền, 30% tương đương khoảng 6–7 case cần người duyệt/ngày; thấp hơn nhiều năng lực một reviewer là 48 case/ca. Con số cần được xem lại nếu pilot có lưu lượng cao hơn bộ nền. |
| `queue_stuck_max` | 0 | `ops_limits` quy định SLA review là 60 phút; một case vượt SLA là case bị ùn, nên không chấp nhận case nào bị stuck. |

## Lưu ý cho nhóm

- Ba metric an toàn `wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max` nên được nhóm cân nhắc đặt 0, vì một lỗi có thể gây thiệt hại tiền, uy tín hoặc dữ liệu cá nhân.
- `cost_per_ticket_vnd_max` và `roi_min` là lựa chọn kinh doanh, không phải “sự thật” suy ra duy nhất từ dữ liệu.
- Chỉ sau khi cả nhóm chấp thuận mới chép ngưỡng vào `config/acceptance_criteria.json` và chạy lệnh ký.