# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): abc
- Lớp: L3B
- Repo của bàn: https://github.com/czx04/K5-L3B-DAY10-abc-PoCtoPilotGate1
- Thẻ sự cố đã bốc (S1–S8): S7

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |   Dư Văn Hùng        |   2A202603975   |   Vận hành và pháp lý   |        x     |
|   2 |     Đinh Hoài Nam      |   2A202603762   | Sản phẩm và kinh doanh      |             |
|   3 |   Nguyễn Minh Quân        |   2A202603747   |  Kỹ sư cổng   |             |
| 4 | Nguyễn Minh Thành | 2A202603884 | Kỹ sư cổng |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

*Ghi chú chung về Git:* theo README bước 2a, cả bàn đặt danh tính Git là mã học viên của trưởng nhóm (`2A202603975`), nên tác giả commit không tách được theo người. Bằng chứng dưới đây dựa trên Pull request / nhánh của từng người và các commit trên máy của từng người.

## DuVanHung-2A202603975

### Phần việc phụ trách

Trưởng nhóm, vai **Vận hành và pháp lý**. Đề: câu 1.2, 1.4 (Phiếu A); 2.4, 2.10 (Phiếu B mục B4, B5, B7.5, B7.6); phần riêng thẻ S7 và câu 3.1–3.7 (Phiếu C mục C3.3, C4, C9, C10, C11). File: `config/operating_gates.json` mục `operations` và `legal`. Ngoài ra: tạo repo, ký tiêu chí, chạy `lab10.checkpoint`, nhận thẻ S7, gom và nộp bài.

### Đóng góp cụ thể

- Tạo repo, mời thành viên, điền TEAM.md; chép eval card và PRD v1.1 Lab 9 vào `docs/lab9/`.
- Phiếu A: mục tiêu nhìn từ chị Oanh và chị Hạnh (1.2), telemetry production cho lệnh `file_carrier_fault` (1.4); ký tiêu chí (`python3 -m lab10.criteria sign`).
- Phiếu B: HAZOP vòng 1 trên `file_carrier_fault` (B4), checklist 9 nhóm có PIC (B5), runbook phần 1–3 và giờ cao điểm (B7.5, B7.6).
- Config vòng 1: `operations` (PIC NV-TUNG, người duyệt NV-HANH, 5 điều kiện dừng, kênh báo tin, ghi chú giải thích, kiểm mẫu 10%) và `legal` (chặn `recipient_contact`, `customer_note`; bắt buộc nguyên nhân khi ghi lỗi hãng). Cổng `legal` này đã chặn trước sự cố S7: lộ PII 30 → 0 ở mốc prepared.
- Chạy `checkpoint` chốt cổng vòng 1, ghi quyết định v1 (B8).
- Vòng 2: nhận thẻ S7, giảm người trực 2 → 1 để hết vượt trần ROI, điền Phiếu C phần vận hành và pháp lý, điền `submission/submission.json`, chạy `check_submission --collect` tới `ĐỦ THÀNH PHẦN`.

### Bằng chứng

- Commit: `8c35a91` (CP1), `781adab` (CP2), `45a8375` (Sign acceptance criteria), `b1987ab` (operations/legal + runbook), `fa7b71a` (chốt cổng vòng 1), `7a189e8` (v1), `98431b3` (nhận thẻ S7), `14444df` (sửa S7 + Phiếu C), `576b593` (bài nộp). PR #4 (`A1.2+1.4`), #5 (`A1.5`), #8 (`B2.4+2.5`).
- Lần chạy: `R-base-prepared-20261119-172601-6bc9f6` (prepared, 9/9 ngưỡng đạt); `R-S7-grade-20261119-173947-1ff4c4` (PASS-VISIBLE).
- Hash chốt vòng 1 `8b8672b8`; hash tiêu chí `38a24e41`.
- Phiếu: A mục A1–A2 (cột telemetry), A5; B mục B4, B5, B7.5, B7.6, B8; C mục C0–C1, C3.3, C4, C9–C11.

### Dùng AI

Có dùng Claude (Claude Code) để đọc code `lab10/`, soạn nháp câu 1.2, 1.4, 1.5, câu 1.6 và `acceptance_criteria.json`, HAZOP B4, checklist B5, pre-mortem B6, runbook B7.5–B7.6, B8, phần lớn Phiếu C (C0–C12), cổng allowlist `notify_carrier` và monitor `carrier_contact_attempt_rate`, và `submission.json`. Mọi con số đã được chạy lại bằng `lab10.eval` / `lab10.grade` và bàn đã đọc, chốt trước khi đẩy.

### Exit ticket

Học được: một cổng đặt trước khi biết sự cố (config `legal` vòng 1) có thể đỡ được sự cố thật nếu xuất phát từ pre-mortem cụ thể; và danh sách cấm chỉ giảm, danh sách cho phép mới ngăn. Chưa chắc: 1 người trực có đủ khi lưu lượng thật dồn gấp ba hay không, vì hôm nay chưa đo giờ cao điểm.

## DinhHoaiNam-2A202603762

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh**. Đề: câu 1.1, 1.6 (Phiếu A mục A1, A4); 2.3 (Phiếu B mục B3); 2.9 (Phiếu B mục B7.4, `config/operating_gates.json` mục `business`); câu 3.2 và quyết định v2 (Phiếu C mục C5, C12).

### Đóng góp cụ thể

- Viết mục tiêu cấp hệ thống (1.1): giảm thiệt hại tài chính và vận hành ngoài ý muốn ở quy mô pilot.
- Viết bảng câu tiêu chí "Nếu … thì chúng tôi sẽ …" cho 6 chỉ số và chốt ngưỡng: pass_rate 0,95, pass_k 0,90, ba chỉ số an toàn 0, escalation 0,25, chi phí 7.000đ, ROI 0,40, ca ùn 0.
- Bản đồ dữ liệu (B3): nguồn sự thật / bản sao của từng trường then chốt và ví dụ drift chính sách REFUND-v3 → v4 ngày 01/12/2026.
- Lý do phạm vi pilot `all` · 100% và các số mục `business` (B7.4).

### Bằng chứng

- PR #2 / #3 (`namdh`, `DHN-SPKD`): commit `f6ff9a7` (câu 1.1), `a45e997` (ngưỡng và hành động câu 1.6).
- PR #9 (`dhn-B`): Phiếu B mục B3. PR #10 (`B75`): commit `c61756c` (pilot_scope ở B7.4).
- Phiếu: A mục A1 (1.1), A4; B mục B3, B7.4.

### Dùng AI

Bổ sung nếu đã dùng AI. (Bản đề xuất ngưỡng của bàn có được Claude review trước khi chép vào câu 1.6.)

### Exit ticket

Học được: ngưỡng phải ký trước khi xem số, và mỗi ngưỡng cần một câu lý do từ dữ liệu (`ops_facts`, `ops_limits`), không lấy từ điểm của bộ thử khác. Chưa chắc: ROI 0,40 có quá dễ đạt khi trần chi phí đã là 7.000đ hay không.

## NguyenMinhQuan-2A202603747

### Phần việc phụ trách

Vai **Kỹ sư cổng** (cổng code). Đề: câu 1.3 (Phiếu A mục A2, cột offline); 2.1 (Phiếu B mục B0, B1); 2.6 (B7.1, `lab10/guards.py`).

### Đóng góp cụ thể

- Đề xuất offline metric cho bước "tìm phê duyệt" (1.3) và một bộ ngưỡng tham khảo cho câu 1.6.
- Chạy lần đánh giá đầu tiên sau khi ký (mốc base), đọc `[CHƯA]`: hoàn sai 20.000đ và 1 lỗi oan ở `T-002@55`; khuyến nghị gate "kết hợp" (B1).
- Viết 3 cổng `write_gate` vòng 1 trong `lab10/guards.py`: tính lại tiền từ tracking DB và chính sách hiệu lực; chặn hoàn trùng theo sổ cái; số ngày trễ phải khớp DB, kiện phải có lỗi hãng theo chính sách, từ lỗi thứ 3 / hãng / ngày chuyển người. Kết quả: ba chỉ số an toàn về 0 trên bộ nền, không làm hỏng ca đang đúng.

### Bằng chứng

- PR #1 (`feature/quan-cp2-metric`): commit `29906c5` (`docs/cp2_quan_proposal.md`).
- PR #7 (`feature/quan-cp3-baseline`): commit `f68e736` (B0, B1). Lần chạy `R-base-before-20261119-161935-bde05c`.
- PR #11 (`feature/quan-cp3-guards`): commit `8faf06f` (`lab10/guards.py`, B7.1). Lần chạy `R-base-after-20261119-165633-104606` (legit_pass 110/110).
- Phiếu: A mục A2 (cột offline); B mục B0, B1, B7.1.

### Dùng AI

Bổ sung nếu đã dùng AI. (Logic `guards.py` có được Claude review; câu 1.3 trong phiếu được chép lại từ đề xuất trong PR #1.)

### Exit ticket

Học được: cổng ghi phải tính lại từ nguồn sự thật (tracking DB, chính sách hiệu lực) chứ không tin con số agent đưa vào. Chưa chắc: cổng chống hoàn trùng dùng `deny` có chặn nhầm đơn có hai claim hợp lệ khác nhau trong bộ test ẩn hay không.

## NguyenMinhThanh-2A202603884

### Phần việc phụ trách

Vai **Kỹ sư cổng** (dò lỗi và kiểm thử). Đề: câu 2.2 (Phiếu B mục B2, bảng soát lỗi `T-002@55`); 2.7, 2.8 (B7.2, B7.3); đề xuất ngưỡng hỗ trợ câu 1.6; số ban đầu mục `business` của `config/operating_gates.json`.

### Đóng góp cụ thể

- Trace `T-002@55`, xếp loại **lỗi chìm**: agent dùng 5 ngày khách khai thay vì 2 ngày theo tracking, hoàn sai 20.000đ; điền ba phần của bảng soát lỗi (B2).
- Hai bước tránh rò rỉ dữ liệu khi chỉnh cổng trên chính bộ dùng để chấm (B7.2).
- Behavioral test với ticket hiểm chạy bằng `--adhoc` để thử cổng của Quân (B7.3).
- Đề xuất bộ ngưỡng chấp nhận kèm lý do vận hành (chi phí, tỉ lệ chuyển người, hàng chờ).

### Bằng chứng

- PR #6: commit `4aeb76b` (B2, mục `business` trong config).
- PR #12: commit `6c38857` (B7.2, B7.3), `832ff78`.
- Phiếu: B mục B2, B7.2, B7.3.

### Dùng AI

Bổ sung nếu đã dùng AI. (Bản đề xuất ngưỡng được Claude viết lại một phiên bản để khớp với đề xuất của Quân.)

### Exit ticket

Học được: lỗi nguy hiểm nhất là lỗi chìm, khi khách vẫn được hoàn tiền nên không ai thấy, mà người chịu hại là bên thứ ba (hãng bị ghi lỗi oan). Chưa chắc: hai ticket hiểm của behavioral test có đủ đại diện cho cách viết khác trong bộ test ẩn hay không.
