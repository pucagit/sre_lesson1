# Bài tập số 1

# Đặc tả yêu cầu

## Yêu cầu kiến thức

- Hiểu về quy trình deploy một ứng dụng web hoàn chỉnh theo cách truyền thống
- Hiểu về Nginx reverse proxy, HTTPS, DNS

## Yêu cầu kỹ năng

- Viết được config Nginx hoàn chỉnh, trong đó đã bao gồm cấu hình HTTPS
- Biết cách trỏ DNS record, quản lý domain và subdomain

# Đề bài

## Yêu cầu đề bài

1. Viết 2 ứng dụng web đơn giản chạy trên cùng 1 server. Mỗi khi truy cập trang web thứ nhất sẽ hiển thị dòng chữ **Bạn là lượt truy cập thứ xxx;** trang web thứ hai chỉ đơn giản là in ra thông tin của request như IP, phương thức, URL,…
2. Tạo 2 DNS record (ví dụ [web1.example.com](http://web1.example.com) và [web2.example.com](http://web2.example.com) ) trỏ về server trên.
3. Cài đặt Nginx và viết file config sao cho khi truy cập vào [web1.example.com](http://web1.example.com) sẽ ra trang web thứ nhất, truy cập vào [web2.example.com](http://web2.example.com) sẽ ra trang web thứ hai. Giới hạn truy cập vào trang web thứ hai theo IP (ví dụ cho phép IP `192.168.1.14` truy cập nhưng chặn IP `192.168.1.15`) dùng config của Nginx.
4. Cấu hình HTTPS cho 2 domain trên.

## Thời gian làm bài: 7 ngày (tính từ ngày nhận bài tập)

## Yêu cầu bài làm

- Đối với project:
    - Trang web thứ nhất cần phải có database, trang thứ hai thì không cần.
    - Ngôn ngữ và database sử dụng: tùy chọn, khuyến khích dùng python.
    - Nếu không có sẵn server, không thích mua domain thì deploy local. Còn nếu muốn thử tự dùng server free thì đăng ký tài khoản AWS hoặc Azure với mail edu. Domain .xyz cũng rất rẻ, mua lần đầu tiên khoảng 1$/năm.
    - Cấu hình HTTPS cho 2 trang web (nếu mua domain thì dùng Lets Encrypt, local thì self signed là đủ)
    - Sau khi deploy, server không expose cổng nào ra công khai trừ 80 và 443.
    - Push bài tập lên Gitlab, sử dụng Git Terminal **(không sử dụng Git Desktop)**

## Yêu cầu và hướng dẫn nộp bài

- Sử dụng Gitlab để lưu trữ bài tập
    - Tạo 1 private group trên [Gitlab](https://gitlab.com/) có tên `cs_<your_name>`, chẳng hạn `cs_vu_hai_dang`
    - Nếu tên group bị trùng thì thêm một chữ số theo thứ tự Alphabet phía sau, chẳng hạn `cs_vu_hai_dang_1`
    - Nếu group đã được tạo trước đó thì không cần tạo lại
    - Thêm member cho group: @dangvu99 với role `Reporter`
    - Tạo 1 private project bên trong private group vừa được tạo, có tên `devops_week1`
    - Download [GIT client](https://git-scm.com/downloads/guis) và sử dụng nó để push kết quả bải tập lên Gitlab
    
- Thông báo hoàn thành bài tập và trao đổi với người hướng dẫn Vũ Hải Đăng theo địa chỉ email `dangvh@cystack.net` với tiêu đề là `HomeworkDevopsX-<Hoten>` (X là số thứ tự của tuần). Phần nội dung thư không để trống, có ghi một số thông tin vắn tắt liên quan. Ví dụ:

```
Chào anh,

Em là xxx, 
    
Bài tập tuần X đã được em push lên gitlab tại địa chỉ https://gitlab.com/cs_nguyen_huu_trung/weekX/
    
Rất mong nhận được sự phản hồi từ anh.
    
Em cảm ơn.
```

## Lưu ý

- Bài bị phát hiện copy từ người khác, không hiểu nội dung thì TTS sẽ chịu hình thức kỷ luật ở mức cao nhất.
- Mọi nguồn tham khảo đều phải được ghi chú rõ ràng trong báo cáo
- Bài nộp không theo chuẩn nêu trên sẽ không được công nhận.

# Tài liệu tham khảo

## Liên quan trực tiếp tới nội dung chính

### Lý thuyết

- [Nginx](http://www.nginx.com)
- [DNS record](https://www.cloudflare.com/learning/dns/dns-records/)

### Kỹ năng

- [Nginx reverse proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)

## Tham khảo thêm

- DM cho người hướng dẫn @Dang Vu