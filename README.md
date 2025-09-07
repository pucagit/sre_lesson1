# Triển khai 2 Flask app với Gunicorn + Nginx + HTTPS + Giới hạn IP

## Mục tiêu

* `web1.pucavv.io.vn` → app **web\_1**
* `web2.pucavv.io.vn` → app **web\_2** (chỉ cho phép truy cập từ IP chỉ định)
* Chạy Gunicorn dưới systemd, Nginx reverse proxy qua **Unix socket**, cài Let’s Encrypt (HTTPS).

> Repo/đường dẫn (ví dụ):
>
> * `/home/ubuntu/sre_lesson1/web_1`
> * `/home/ubuntu/sre_lesson1/web_2`
> * Mỗi app có `wsgi.py` với `app` (tức **entrypoint** là `wsgi:app`) và venv là `.venv`.

---

## 0) Chuẩn bị

1. **DNS**: Tạo 2 bản ghi A trỏ về Public IP của EC2

   * `web1.pucavv.io.vn` → `<EC2 IPv4>`
   * `web2.pucavv.io.vn` → `<EC2 IPv4>`
2. **Security Group**: Cho phép inbound **TCP 80, 443** từ Internet, **TCP 22** với giới hạn IP để truy cập SSH.
3. **Packages**

   ```bash
   sudo apt update
   sudo apt install -y python3-venv python3-pip nginx certbot python3-certbot-nginx
   ```

---

## 1) Virtualenv & Dependencies (mỗi app)

```bash
# web_1
cd /home/ubuntu/sre_lesson1/web_1
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt

# web_2
cd /home/ubuntu/sre_lesson1/web_2
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

---

## 2) Tạo service systemd (Gunicorn → Unix socket dưới /run)

### `web_1`

`/etc/systemd/system/web_1.service`

```ini
[Unit]
Description=Gunicorn for web_1
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/sre_lesson1/web_1
Environment="PATH=/home/ubuntu/sre_lesson1/web_1/.venv/bin"

ExecStart=/home/ubuntu/sre_lesson1/web_1/.venv/bin/python -m gunicorn \
  --workers 3 \
  --bind unix:/run/web_1/web_1.sock -m 007\
  wsgi:app

[Install]
WantedBy=multi-user.target
```

### `web_2`

`/etc/systemd/system/web_2.service`

```ini
[Unit]
Description=Gunicorn for web_2
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/sre_lesson1/web_2
Environment="PATH=/home/ubuntu/sre_lesson1/web_2/.venv/bin"

ExecStart=/home/ubuntu/sre_lesson1/web_2/.venv/bin/python -m gunicorn \
  --workers 3 \
  --bind unix:/run/web_2/web_2.sock -m 007 \
  wsgi:app

[Install]
WantedBy=multi-user.target
```

Kích hoạt:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now web_1 web_2
systemctl --no-pager status web_1 web_2
```

---

## 3) Cấu hình Nginx (2 server blocks)

### `web1.pucavv.io.vn` → web\_1

`/etc/nginx/sites-available/web_1`

```nginx
server {
    listen 80;
    server_name web1.pucavv.io.vn;

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/web_1/web_1.sock;
        proxy_read_timeout 120s;
    }
}
```

### `web2.pucavv.io.vn` → web\_2 (giới hạn IP)

`/etc/nginx/sites-available/web_2`

```nginx
server {
    listen 80;
    server_name web2.pucavv.io.vn;

    # Cho ACME challenge
    location ^~ /.well-known/acme-challenge/ {
        default_type "text/plain";
        allow all;          # cho LetsEncrypt truy cập xác thực
        root /var/www/html;
    }

    # Giới hạn IP cho phần còn lại
    location / {
        allow 203.0.113.45;    
        deny  all;

        include proxy_params;
        proxy_pass http://unix:/run/web_2/web_2.sock;
        proxy_read_timeout 120s;
    }
}
```

Bật site & reload:

```bash
sudo ln -sf /etc/nginx/sites-available/web_1 /etc/nginx/sites-enabled/web_1
sudo ln -sf /etc/nginx/sites-available/web_2 /etc/nginx/sites-enabled/web_2
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

---

## 4) Bật HTTPS (Let’s Encrypt)
**Cấp cert cho cả 2 domain cùng lúc:**

```bash
sudo certbot --nginx \
  -d web1.pucavv.io.vn \
  -d web2.pucavv.io.vn \
  --redirect
```

> Với `web2` đang giới hạn IP: do đã mở `/.well-known/acme-challenge/` cho **allow all**, ACME sẽ xác thực được.

---

Tham khảo: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04