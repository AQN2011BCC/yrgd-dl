# Yuri garden Downloader (yrgd-dl)

>**Được viết bởi người không chuyên, có thể có lỗi (chắc chắn có lỗi)**  
>**Có thể vài ngày nữa web cập nhật và nó không hoạt động nữa**  
Dự án sử dụng **[botasaurus](https://github.com/omkarcloud/botasaurus)**
## Miễn trừ trách nhiệm
- Dự án được tạo ra với mục đích học tập, nghiên cứu
- Tôi không sở hữu, lưu trữ, chịu trách nhiệm về bất kỳ nội dung nào được tải xuống bằng công cụ này, cũng như tài khoản của bạn khi sử dụng.
- Vui lòng tôn trọng điều khoản của **[yurigarden](https://yurigarden.moe/)**, không sử dụng cho mục đích thương mại, hoặc phát tán trái phép
## Tính năng?
- Giúp tải các truyện bạn muốn trên **[yurigarden](https://yurigarden.moe/)** về máy
- Có thể tải đơn chap hoặc nhiều chap
## Sử dụng
1. Clone kho lưu trữ này
```powershell
git clone https://github.com/AQN2011BCC/yrgd-dl.git
cd yrgd-dl
```
2. Tạo và kích hoạt môi trường ảo (tùy chọn)
- Nên tạo và sử dụng môi trường ảo
```powershell
python -m venv .venv
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)
```
3. Cài đặt các thư viện cần thiết
```powershell
pip install -r requirements.txt
```
4. Điều chỉnh các thông tin trong **[conf.py](https://github.com/AQN2011BCC/yrgd-dl/blob/main/conf.py)**
- Tôi đã ghi chú khá rõ ràng trong file **[conf.py](https://github.com/AQN2011BCC/yrgd-dl/blob/main/conf.py)**, bạn đọc rồi làm theo là được
5. Bắt đầu tải
- chạy file m.py để bắt đầu tải
```powershell
python m.py
```
- truyện sẽ được lưu trong **.\Downloads**
6. Dành cho việc trích xuất html của 1 trang yurigarden nào bạn muốn
- Để sử dụng cũng cần cài thư viện, sau đó chạy file **[dl-html.py](https://github.com/AQN2011BCC/yrgd-dl/blob/main/dl-html.py)**
```powershell
python dl-html.py
```
- Sau khi chạy terminal sẽ hiện lên yêu cầu nhập link trang cần trích xuất, nhập link vô đây và bấm enter
- Tiếp theo sẽ hiện lên trang đăng nhập nếu đây là lần đầu, hãy đăng nhập sau đó quay về terminal và bấm enter
- Chờ 1 lát và nó sẽ lưu thành file **"yrgd_c.html"**
## Không biết nên ghi gì
- vẫn còn nhiều lỗi, có lỗi gì tôi sẽ sửa dần
- cảm ơn vì dành thời gian đọc tới đây
- **by linh**
