import os
import threading
import warnings
import speech_recognition as sr
import cohere
from gtts import gTTS
import whisper
import pygame
import customtkinter as ctk
from dotenv import load_dotenv


warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# 1. إعداد المتغيرات والتهيئة الأمنية
# ---------------------------------------------------------
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "*********")

# تهيئة Cohere و Pygame الصوتية
co = cohere.ClientV2(COHERE_API_KEY)
pygame.mixer.init()

# إعداد مظهر الواجهة الرسومية
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# تحميل نموذج Whisper
print("⏳ جاري تحميل نموذج Whisper...")
whisper_model = whisper.load_model("base")


# ---------------------------------------------------------
# 2. منطق التطبيق البرمجي (Backend Functions)
# ---------------------------------------------------------
def listen_and_convert(status_callback):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_callback("🎙️ جاري ضبط الضوضاء... اتكلم الآن")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            status_callback("🔴 جاري التسجيل...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            status_callback("⚙️ جاري تحويل الصوت إلى نص...")

            temp_audio_path = "temp_input.wav"
            with open(temp_audio_path, "wb") as f:
                f.write(audio.get_wav_data())

            result = whisper_model.transcribe(temp_audio_path, language="ar", fp16=False)
            text = result["text"].strip()

            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

            return text

        except sr.WaitTimeoutError:
            status_callback("⚠️ لم يتم التقاط صوت.")
            return None
        except Exception as e:
            status_callback(f"❌ خطأ في التسجيل: {e}")
            return None


def generate_response(prompt, status_callback):
    status_callback("🧠 Cohere يفكر في الرد...")
    try:
        response = co.chat(
            model="command-r-08-2024",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.message.content[0].text.strip()
        return reply
    except Exception as e:
        status_callback(f"❌ خطأ الاتصال بـ Cohere: {e}")
        return "عذراً، حدث خطأ أثناء معالجة الطلب."


def convert_and_play_audio(text, status_callback):
    status_callback("🔊 جاري توليد الصوت وتشغيله...")
    try:
        tts = gTTS(text=text, lang='ar')
        audio_file = "output_response.mp3"
        tts.save(audio_file)

        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        status_callback("✅ جاهز للاستماع مجدداً")
    except Exception as e:
        status_callback(f"❌ خطأ في تشغيل الصوت: {e}")


# ---------------------------------------------------------
# 3. الواجهة الرسومية والتفاعل (GUI Application)
# ---------------------------------------------------------
class VoiceAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Voice Assistant | المساعد الصوتي الذكي")
        self.geometry("550x650")
        self.resizable(False, False)

        # العنوان الرئيسي (محاذاة لليمين)
        self.title_label = ctk.CTkLabel(
            self,
            text="🤖 المساعد الصوتي الذكي",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=(20, 10))

        # شريط الحالة (محاذاة لليمين)
        self.status_label = ctk.CTkLabel(
            self,
            text="اضغط على الزر للبدء",
            font=("Arial", 14),
            text_color="#3B82F6"
        )
        self.status_label.pack(pady=10)

        # زر التحكم المباشر
        self.record_button = ctk.CTkButton(
            self,
            text="🎙️ ابدأ التحدث",
            font=("Arial", 16, "bold"),
            height=50,
            corner_radius=25,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.start_pipeline_thread
        )
        self.record_button.pack(pady=15)

        # صندوق عرض المحادثة بضبط المحاذاة لليمين (justify="right")
        self.chat_display = ctk.CTkTextbox(
            self,
            width=480,
            height=380,
            font=("Arial", 14),
            corner_radius=12,
            activate_scrollbars=True
        )
        self.chat_display.pack(pady=10)
        self.chat_display.configure(state="disabled")

    def update_status(self, text):
        self.status_label.configure(text=text)

    def append_chat(self, sender, message):
        self.chat_display.configure(state="normal")

        # إضافة النص مع تنسيق جهة اليمين
        formatted_entry = f"{sender}: {message}\n\n"
        self.chat_display.insert("end", formatted_entry)

        # تطبيق محاذاة جهة اليمين على النص المضاف
        self.chat_display.tag_add("right_align", "1.0", "end")
        self.chat_display.tag_config("right_align", justify="right")

        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def start_pipeline_thread(self):
        threading.Thread(target=self.run_pipeline, daemon=True).start()

    def run_pipeline(self):
        self.record_button.configure(state="disabled", fg_color="#DC2626")

        user_text = listen_and_convert(self.update_status)
        if user_text:
            self.append_chat("👤 أنت", user_text)

            ai_reply = generate_response(user_text, self.update_status)
            self.append_chat("🤖 الذكاء الاصطناعي", ai_reply)

            convert_and_play_audio(ai_reply, self.update_status)
        else:
            self.update_status("⚠️ حاول مرة أخرى.")

        self.record_button.configure(state="normal", fg_color="#2563EB")


# ---------------------------------------------------------
# 4. نقطة انطلاق التطبيق
# ---------------------------------------------------------
if __name__ == "__main__":
    app = VoiceAssistantGUI()
    app.mainloop()