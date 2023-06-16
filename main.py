import streamlit as st
import cv2
from datetime import datetime


class PhotoAPP:
    def __init__(self):
        self.title = st.title("Student Project")
        self.camera = cv2.VideoCapture(0)
        self.current_image = st.image([])
        self.current_time = datetime.now()
        self.my_frame = None

    def show_image(self, image: bytes):
        if image is not None:
            self.current_image.image(image)
        else:
            pass

    @classmethod
    def show_time(cls, frame, text, org, color):
        cv2.putText(img=frame, text=text, org=org,
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=color,
                    thickness=2, lineType=cv2.LINE_AA)

    def download_image(self):
        if self.my_frame is not None:
            st.download_button(label="Download file", data=self.my_frame, file_name='picture.jpg', mime='image/jpeg')

    def main(self):
        self.title

        if st.button("Start"):
            st.selectbox("", options=("Enable date", "Disable date"), key="user_choice")
            take_picture = st.button("Snap")

            date_now = self.current_time.strftime("%d-%m-%Y")
            time_now = self.current_time.strftime("%H:%M:%S")
            day_of_week = self.current_time.strftime("%A")

            while True:
                check, frame = self.camera.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if st.session_state["user_choice"] == "Enable date":
                    self.show_time(frame=frame, text=date_now, org=(20, 50), color=(255, 255, 255))
                    self.show_time(frame=frame, text=time_now, org=(20, 100), color=(255, 255, 255))
                    self.show_time(frame=frame, text=day_of_week, org=(20, 150), color=(255, 0, 0))

                self.show_image(frame)

                if take_picture and check:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    _, buffer = cv2.imencode('.jpg', rgb_frame)
                    self.my_frame = buffer.tobytes()
                    break

            self.download_image()


if __name__ == '__main__':
    app = PhotoAPP()
    app.main()
