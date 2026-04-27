import os
import cv2
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from face_mesh_tools import FaceMeshProcessor, FaceNotFoundError

BASE_DIRECTION = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIRECTION, 'models', 'face_landmarker.task')
REAL_IMAGE_PATH = os.path.join(BASE_DIRECTION, 'imgs', '1.png')


class TestFaceMeshProcessor:
    def __init__(self):
        pass

    @pytest.fixture
    def mock_processor(self):
        """Фикстура с моком для быстрой проверки логики"""
        with patch('mediapipe.tasks.python.vision.FaceLandmarker.create_from_options') as mocked_create:
            mock_detector = MagicMock()
            mocked_create.return_value = mock_detector

            processor = FaceMeshProcessor(MODEL_PATH)
            return processor, mock_detector

    def test_initialization(self, mock_processor):
        """Проверка инициализации"""
        processor, _ = mock_processor
        assert processor.detector is not None

    def test_process_image_face_not_found(self, mock_processor, tmp_path):
        """Тест лицо не найдено"""
        processor, mock_detector = mock_processor

        mock_detector.detect.return_value.face_landmarks = []

        img_file = tmp_path / "blank.png"
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(str(img_file), test_img)

        with pytest.raises(FaceNotFoundError):
            processor.process_image(str(img_file))

    def test_draw_landmarks_on_image_format(self):
        """Проверка отрисовки на пустых данных"""
        img_input = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_result = MagicMock()
        mock_result.face_landmarks = [[]]

        result = FaceMeshProcessor.draw_landmarks_on_image(img_input, mock_result)
        assert result.shape == (100, 100, 3)

    @pytest.mark.skipif(not os.path.exists(MODEL_PATH), reason="Файл модели не найден")
    @pytest.mark.skipif(not os.path.exists(REAL_IMAGE_PATH), reason="Тестовое фото 1.png не найдено")
    def test_integration_real_process(self):
        """Тест на реальных данных"""
        processor = FaceMeshProcessor(MODEL_PATH)

        result = processor.process_image(REAL_IMAGE_PATH)
        assert isinstance(result, np.ndarray)
        assert result.size > 0

    def test_process_invalid_file_format(self, mock_processor, tmp_path):
        """Тест: передача не изображения"""
        processor, _ = mock_processor

        fake_img = tmp_path / "test.txt"
        fake_img.write_text("This is not an image")

        with pytest.raises(ValueError, match="не является корректным изображением"):
            processor.process_image(str(fake_img))

    def test_process_empty_image(self, mock_processor, tmp_path):
        """Тест: передача пустого файла"""
        processor, _ = mock_processor

        empty_file = tmp_path / "empty.jpg"
        empty_file.write_bytes(b"")

        with pytest.raises(ValueError, match="не является корректным изображением"):
            processor.process_image(str(empty_file))
