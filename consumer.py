import streamlit as st
import json
from time import sleep
from confluent_kafka import Consumer
from PIL import Image

class ImageSegmentationConsumer:
    def __init__(self, bootstrap_servers='localhost:9095', topic='image_segmentation', group_id='my_consumers'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.conf = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe([self.topic])
        self.setup_streamlit()

    def setup_streamlit(self):
        st.set_page_config(
            page_title="Real-Time Segmentation Dashboard",
            layout="wide",
        )
        st.title("Segmented Images")

    def consume_data(self):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is not None and not msg.error():
                data = json.loads(msg.value().decode('utf-8'))
                self.display_images(data)
            else:
                print('Waiting for messages or got an error')
                sleep(1)

    def display_images(self, data):
        orig_image = Image.open(data['image_orig'])
        processed_image = Image.open(data['image_processed'])

        col1, col2 = st.columns(2)
        with col1:
            st.image(orig_image, caption='Original Image', use_column_width=True)
        with col2:
            st.image(processed_image, caption='Segmented Image', use_column_width=True)

if __name__ == "__main__":
    consumer = ImageSegmentationConsumer()
    consumer.consume_data()
