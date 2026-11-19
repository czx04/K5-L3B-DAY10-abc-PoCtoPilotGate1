# Đề xuất ngưỡng chấp nhận

Các ngưỡng dưới đây dùng cho `config/acceptance_criteria.json`. Ngưỡng chất lượng tham chiếu eval card Lab 9; ngưỡng vận hành đối chiếu `data/world.json` và giữ thêm điều kiện hàng chờ để tránh một tỉ lệ trung bình che khuất giờ cao điểm.

| Khoá | Đề xuất | Lý do |
|---|---:|---|
| `cost_per_ticket_vnd_max` | `10000` | Giới hạn ở mức chi phí làm tay 10.000đ/ticket trong `ops_facts`; nếu hệ thống đắt hơn mốc này thì chưa có lợi thế chi phí so với quy trình hiện tại. |
| `escalation_rate_max` | `0.30` | Mức 30% tạo khoảng đệm 7,27 điểm phần trăm so với tỉ lệ mẫu 22,73%; trên 22 ticket/ngày tương đương khoảng 6,6 lượt chuyển người, trong khi một người duyệt xử lý được tối đa 48 lượt/ca 8 giờ, và `queue_stuck_max = 0` vẫn bắt tình trạng dồn cục. |
| `queue_stuck_max` | `0` | Không chấp nhận ca ùn nào: ticket phải được nhận trong SLA 60 phút đã thống nhất với Ops, không quá SLA hoặc trôi qua hết ca. |
| `pass_rate_min` | `0.85` | Dùng sàn blocking 85% của `pass_rate` trong eval card Lab 9; card cũng cho thấy sàn này chặn được hồi quy nghiêm trọng (kết quả seeded regression 0,7143). |
| `pass_k_min` | `0.80` | Dùng sàn 80% cho tỉ lệ ticket đúng cả 5/5 lần, tương ứng mốc `pass_hat_5` trong Lab 9 v2; mốc này dưới baseline A/A 0,8929 nhưng vẫn chặn hồi quy thiếu ổn định ở 0,5714. |

## Cách áp dụng và giới hạn

- Các con số `pass_rate_min` và `pass_k_min` là sàn tối thiểu, không thay thế yêu cầu Lab 9 về không giảm có ý nghĩa so với baseline cùng phiên bản eval set.
- `cost_per_ticket_vnd_max` là chi phí vận hành tổng hợp trên mỗi ticket, không phải trần tiền LLM riêng. `ops_limits.max_llm_cost_per_ticket_vnd` vẫn là trần độc lập 1.500đ cho mỗi ticket.
- `escalation_rate_max` là ngưỡng trung bình; nó không bảo đảm an toàn khi ticket dồn vào một giờ. Vì vậy cần chặn riêng mọi lượt ùn bằng `queue_stuck_max = 0` và theo dõi thời gian chờ tối đa theo SLA 60 phút.
- Eval card Lab 9 ghi nhận bộ mẫu nhỏ và dùng MockLLM. Trước khi coi các sàn chất lượng là chuẩn production, nên đo A/A trên mô hình và lưu lượng pilot thực tế; nếu đổi eval set thì chạy lại baseline, không nới ngưỡng trên cùng một phiên bản.

## Nguồn

- [Dữ liệu vận hành](../data/world.json) — `ops_limits` và `ops_facts`.
- [Eval card Lab 9](./lab9/eval_card.md) — sàn `pass_rate`, `pass_hat_5`, kết quả hồi quy và giới hạn cỡ mẫu.
- [Hướng dẫn Lab 10](./guide.md) — định nghĩa `pass_k`, cách tính chi phí/vận hành và ví dụ bộ nền 22 ticket/ngày.
