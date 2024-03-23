import torch
from torchvision import models
from torchvision.transforms import functional as F

import numpy as np
from PIL import Image

class FCNResNet50:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.load_model()

    def load_model(self):
        # Загружаем предобученную модель FCN с backbone ResNet50
        model = models.segmentation.fcn_resnet50(pretrained=True)
        model = model.to(self.device)
        model.eval()  # Переключаем модель в режим оценки
        return model

    def predict(self, image):
        # Преобразование изображения для подачи в модель
        image = F.to_tensor(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(image)['out'][0]
        return output

    # def decode_segmentation(self, output, threshold=0.5):
    #     # Применяем порог для определения маски сегментации
    #     output = torch.sigmoid(output)
    #     output[output <= threshold] = 0
    #     output[output > threshold] = 1
    #     # Преобразовываем тензор обратно в PIL Image для визуализации
    #     return F.to_pil_image(output.cpu().byte())
    
    def decode_segmentation(self, output, n_classes=21):
        # Преобразование выходных данных модели в предсказанные классы для каждого пикселя       
        _, pred = torch.max(output, 0)
        pred = pred.byte().cpu().numpy()

        # Создаем карту цветов для n_classes классов
        # Пример: 3 класса -> [(255,0,0), (0,255,0), (0,0,255)]
        np.random.seed(42)  # Для воспроизводимости цветов
        colors = np.random.randint(0, 255, (n_classes, 3), dtype=np.uint8)

        # Применяем цвета к предсказаниям
        # Инициализация RGB изображения
        seg_img = np.zeros((pred.shape[0], pred.shape[1], 3), dtype=np.uint8)

        for cls in range(n_classes):
            seg_img[pred == cls] = colors[cls]

        # Преобразуем numpy массив в PIL Image
        return Image.fromarray(seg_img)