# Tải Fshare trên linux bằng Python 2.7 + Centos 7 ( chưa test với phiên bản python và OS khác )

# Cài đặt các thư viện ( có thể cài bằng yum  hoặc pip )

pip install beautifulsoup4 wget requests pycurl ptyprocess wand blinker

# Thông tin đăng nhập tài khoản Fshare thay đổi trong tập tin account.json, trong trường hợp không có thông tin đăng nhập hoặc thông tin đăng nhập với tài khoản thường sẽ tải về với tốc độ giới hạn

## Cách sử dụng ./Fshare link_file_Fshare ( tải bằng folder sẽ tiếp tục phát triển )

./Fshare.py https://www.fshare.vn/file/YJHMDQ9U6Z9Z

# Để download nhiều file có thể tạo file download.sh và chạy sh download.sh ( xem file mẫu đi kèm hoặc như bên dưới )
./Fshare https://www.fshare.vn/file/YJHMDQ9U6Z9Z
./Fshare https://www.fshare.vn/file/96TEAU89CMU3
./Fshare https://www.fshare.vn/file/Q7IPQC5GMH9L
