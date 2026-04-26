import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision.drawing_utils import DrawingSpec


class FaceNotFoundError(Exception):
    pass


class FaceMeshProcessor:
    def __init__(self, model_path, num_faces=2, debug=False):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(base_options=base_options, num_faces=num_faces)
        self.detector = vision.FaceLandmarker.create_from_options(options)

        self.debug = debug

    @staticmethod
    def draw_landmarks_on_image(rgb_img, detection_result, connections_thickness=1, contours_thickness=3,
                                circle_radius=1, landmark_color=(0, 255, 0), connection_color=(0, 255, 0),
                                contours_color=(255, 255, 0), draw_contours=False, draw_landmarks=True):
        """Функция возвращающая RGB изображению и результатам детекции RGB изображение с ключевыми точками"""
        face_landmarks_list = detection_result.face_landmarks

        for idx in range(len(face_landmarks_list)):
            face_landmarks = face_landmarks_list[idx]

            if draw_landmarks:
                drawing_utils.draw_landmarks(
                    image=rgb_img,
                    landmark_list=face_landmarks,
                    connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
                    landmark_drawing_spec=DrawingSpec(color=landmark_color, circle_radius=circle_radius),
                    connection_drawing_spec=DrawingSpec(color=connection_color, thickness=connections_thickness))

            if draw_contours:
                drawing_utils.draw_landmarks(
                    image=rgb_img,
                    landmark_list=face_landmarks,
                    connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=DrawingSpec(color=contours_color, thickness=contours_thickness))

        return rgb_img

    def process_image(self, img_path, **kwargs):
        """По пути картинки возвращает ее версию с отрисованными результатами детекции (BGR)"""
        img = cv2.imread(img_path)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        results = self.detector.detect(mp_image)

        if results.face_landmarks:
            img = self.draw_landmarks_on_image(img_rgb, results, **kwargs)
        else:
            raise FaceNotFoundError

        if self.debug:
            cv2.imshow("Image", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            cv2.waitKey(0)
        else:
            return img


if __name__ == '__main__':
    processor = FaceMeshProcessor('models/face_landmarker.task', debug=True)
    processor.process_image('imgs/1.png', draw_landmarks=False, draw_contours=True)
