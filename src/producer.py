import os
from confluent_kafka import Producer
import json
import time
from PIL import Image
from model import FCNResNet50  # Импортируем нашу модель сегментации

class ImageSegmentationProducer:
    def __init__(self, bootstrap_servers='localhost:9095', topic='image_segmentation'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.conf = {'bootstrap.servers': self.bootstrap_servers}
        self.producer = Producer(self.conf)
        self.folder_to_store_processed = './data/processed_data/'
        self.base_dir_originals = './data/val2017/'
        self.check_dataset_exists()

    def check_dataset_exists(self):
        if not os.path.exists(self.base_dir_originals):
            raise FileNotFoundError(
                "COCO dataset not found. Please download the COCO 'val2017' dataset and place it in the './data/val2017/' directory."
            )

    def get_processed_image(self, image_id, data, processor):
        image_path = os.path.join(self.base_dir_originals, data[image_id])
        image = Image.open(image_path).convert("RGB")
        output = processor.predict(image)
        segmentation_mask = processor.decode_segmentation(output)
        processed_image_path = os.path.join(self.folder_to_store_processed, f'processed_{image_id}.png')
        segmentation_mask.save(processed_image_path)

    def make_json(self, data, image_id):
        image = data[image_id]
        image_data = {
            'image_id': image_id,
            'image_orig': os.path.join(self.base_dir_originals, image),
            'image_processed': os.path.join(self.folder_to_store_processed, f'processed_{image_id}.png')
        }
        return image_data

    def produce_data(self):
        data_to_be_produced = sorted(os.listdir(self.base_dir_originals))
        print(f'Found {len(data_to_be_produced)} images in stream. Processing...')
        processor = FCNResNet50()
        if not os.path.isdir(self.folder_to_store_processed):
            os.makedirs(self.folder_to_store_processed)
        for image_id, image_name in enumerate(data_to_be_produced):
            self.get_processed_image(image_id=image_id, data=data_to_be_produced, processor=processor)
            image_data = self.make_json(data=data_to_be_produced, image_id=image_id)
            self.producer.produce(self.topic, key=str(image_id), value=json.dumps(image_data))
            self.producer.flush()
            print(f'Produced: {image_data}')
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        producer = ImageSegmentationProducer()
        producer.produce_data()
    except FileNotFoundError as e:
        print(e)