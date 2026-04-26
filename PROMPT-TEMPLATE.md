# Prompt Template - Đăng bài sản phẩm JOMOO lên thichboncau.com

## Cách sử dụng

Copy prompt bên dưới và thay thế `[TÊN SẢN PHẨM]` bằng model sản phẩm muốn đăng (ví dụ: ZS860, ZS860-1, 74120, ZS021...).

---

## Prompt

```
Đăng bài sản phẩm JOMOO [TÊN SẢN PHẨM] lên website thichboncau.com theo quy trình sau:

1. Đọc file products/[TÊN SẢN PHẨM]/product_data.json và products/[TÊN SẢN PHẨM]/PRODUCT_VI.md trong workspace jomoo/
2. Chọn 10 ảnh tốt nhất từ products/[TÊN SẢN PHẨM]/images/ (ưu tiên ảnh show ngoại hình + selling points)
3. Đổi tên ảnh theo chuẩn SEO: bon-cau-thong-minh-jomoo-[ten-san-pham]-01.jpg → -10.jpg (tiếng Việt không dấu, ngăn cách bởi dấu -)
4. Upload ảnh lên WordPress qua REST API:
   - Endpoint: POST https://thichboncau.com/wp-json/wp/v2/media
   - Auth: thichboncau_wp:6o3V WqNH ulhz Xmgj 4UTB lgQj
   - Header: Content-Disposition: attachment; filename="ten-anh.jpg"
5. Tạo sản phẩm WooCommerce qua REST API:
   - Endpoint: POST https://thichboncau.com/wp-json/wc/v3/products
   - Auth: thichboncau_wp:6o3V WqNH ulhz Xmgj 4UTB lgQj
   - Categories: {"id": 17} (Bồn Cầu) + {"id": 19} (Bồn Cầu Thông Minh)
   - Nếu là phụ kiện thì dùng category khác phù hợp
6. Viết nội dung theo phong cách thichboncau.com:
   - Giới thiệu ngắn gọn, súc tích
   - Bullet điểm ✅ highlight tính năng chính
   - Ảnh minh họa xen kẽ
   - Phần "Ai nên mua?"
   - Bảng tóm tắt tính năng ở cuối
   - Bảng thông số kỹ thuật
   - Danh sách phụ kiện đi kèm

QUAN TRỌNG:
- KHÔNG sử dụng bất kỳ từ tiếng Trung nào trong bài viết
- Tất cả thuật ngữ phải dịch sang tiếng Việt:
  + 净界Air → Dòng Air
  + 微波 → Sóng siêu âm
  + 人体工学 → Công thái học
  + NFC一键 → NFC một chạm
  + 脉冲 → Xung mạnh
  + 静音 → Yên tĩnh
  + 普通 → Thông thường
- Slug sản phẩm: bon-cau-thong-minh-jomoo-[ten-san-pham] (không dấu, ngăn cách -)
- Giá sản phẩm: để trống (không set price, không set regular_price, không set sale_price)
- Nếu cần update sản phẩm đã có: dùng PUT /wp-json/wc/v3/products/{id}

🚫 TUYỆT ĐỐI KHÔNG ĐỀ CẬP (cả trong nội dung bài lẫn footer):
- Giá bán / giá niêm yết / giá khuyến mãi / "Giá tham khảo"
- Bảo hành / thời hạn bảo hành / chính sách bảo hành
- Hotline / số điện thoại / liên hệ
- Lắp đặt / dịch vụ lắp đặt / hỗ trợ lắp đặt
- Bất kỳ thông tin nào liên quan đến giá cả, liên hệ, bảo hành, lắp đặt


Categories WooCommerce có sẵn:
- ID 17: Bồn Cầu
- ID 18: Bồn Cầu 1 Khối
- ID 19: Bồn Cầu Thông Minh
- ID 37: Chậu Rửa
- ID 85: Bathrooms
```

---

## Ví dụ sử dụng

### Đăng 1 sản phẩm:
```
Đăng bài sản phẩm JOMOO ZS860 lên website thichboncau.com theo quy trình trong PROMPT-TEMPLATE.md
```

### Đăng nhiều sản phẩm:
```
Đăng bài cho 3 sản phẩm JOMOO: ZS860, ZS860-1, ZS021 lên website thichboncau.com theo quy trình trong PROMPT-TEMPLATE.md
```

### Đăng phụ kiện:
```
Đăng bài phụ kiện JOMOO 74120 (vòi xịt tăng áp) lên website thichboncau.com. Category: Phụ Kiện Phòng Tắm. Theo quy trình trong PROMPT-TEMPLATE.md
```

### Sửa bài đã đăng:
```
Cập nhật bài sản phẩm JOMOO ZS800I trên thichboncau.com (ID: 543), thêm phần so sánh với ZS700P
```

---

## Danh sách sản phẩm đã có dữ liệu

### Bồn cầu thông minh (có PRODUCT_VI.md + ảnh đã trim):
| Model | Tên | Giá (NDT) | Trạng thái |
|---|---|---|---|
| ZS860 | 净界 Ultra | ¥4,923 | ✅ Đã đăng (ID: 817) |
| ZS860-1 | 净界 Ultra (Nâng cấp) | ¥5,532 | ✅ Đã đăng (ID: 818) |
| ZS800I | 净界 Air | ¥4,224 | ✅ Đã đăng (ID: 543) |
| ZS800J | 净界 Pro | - | Chưa đăng |
| ZS780 | - | - | Chưa đăng |
| ZS780P | - | - | Chưa đăng |
| ZS760J | - | - | Chưa đăng |
| ZS711J | - | - | Chưa đăng |
| ZS710J | - | - | Chưa đăng |
| ZS700P | - | - | Chưa đăng |
| ZS690P | - | - | Chưa đăng |
| ZS690I | - | - | Chưa đăng |
| ZS680U | - | - | Chưa đăng |
| ZS680I | - | - | Chưa đăng |
| ZS680 | - | - | Chưa đăng |
| ZS520I-S2 | Khử mùi bạch kim | ¥2,293 | ✅ Đã đăng (ID: 816) |
| ZS300P | Không cần áp lực nước | ¥1,909 | ✅ Đã đăng (ID: 815) |
| ZD8611 | P50 treo tường UV | ¥11,349 | ✅ Đã đăng (ID: 761) |
| ZD8920 | i90 flagship 3 tầng bảo vệ | ¥13,349 | ✅ Đã đăng (ID: 772) |

### Phụ kiện (có PRODUCT_VI.md + ảnh đã trim):
| Model | Tên | Giá (NDT) | Trạng thái |
|---|---|---|---|
| 13D900 | Dung dịch tạo bọt Magic Foam | ¥22 | Chưa đăng |
| 13D900-2065 | Lõi lọc chống cặn tích hợp | ¥34 | Chưa đăng |
| 74120 | Vòi xịt tăng áp đa năng | ¥141 | Chưa đăng |
| KD903-1073 | Lõi lọc nước chống cặn | ¥198 | Chưa đăng |
| X74107 | Bộ vòi xịt vệ sinh âm tường | ¥222 | Chưa đăng |
| ZS021 | Nắp bồn cầu thông minh | ¥902 | Chưa đăng |
