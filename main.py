import sys
import subprocess

# Tự động cài đặt yt-dlp nếu chưa có trên Android
try:
    import yt_dlp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import yt_dlp

class DownloaderLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Ô nhập link video
        self.url_input = TextInput(
            hint_text='Dán URL video tại đây...',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.url_input)

        # Nút tải
        self.download_btn = Button(
            text='Tải Video',
            size_hint_y=None,
            height=50
        )
        self.download_btn.bind(on_press=self.start_download_thread)
        self.add_widget(self.download_btn)

        # Nhãn hiển thị trạng thái
        self.status_label = Label(text='Sẵn sàng')
        self.add_widget(self.status_label)

    def update_status(self, text):
        self.status_label.text = text

    def start_download_thread(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "Vui lòng nhập URL!"
            return

        self.status_label.text = "Đang tải..."
        self.download_btn.disabled = True
        
        # Chạy tải video ở background thread để không bị treo giao diện
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url):
        ydl_opts = {
            'outtmpl': '/sdcard/Download/%(title)s.%(ext)s',  # <--- Đã sửa thành đường dẫn Android
            'quiet': True,
            'no_warnings': True,
            # Thêm User-Agent để tránh bị Facebook chặn tải video
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: self.on_success())
        except Exception as e:
            error_msg = str(e)
            Clock.schedule_once(lambda dt: self.on_error(error_msg))

    def on_success(self):
        self.status_label.text = "Tải thành công! Kiểm tra thư mục Download."
        self.download_btn.disabled = False

    def on_error(self, error_msg):
        self.status_label.text = f"Lỗi: {error_msg}"
        self.download_btn.disabled = False


class VideoDownloaderApp(App):
    def build(self):
        return DownloaderLayout()

if __name__ == '__main__':
    VideoDownloaderApp().run()
