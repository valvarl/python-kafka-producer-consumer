# Kafka Image Processing Pipeline

This project demonstrates a Kafka pipeline for real-time image segmentation. It uses a producer-consumer model to process and display segmented images using the COCO 2017 dataset.

## Environment Setup

Before running the application, you need to set up your environment by installing the necessary Python packages and downloading the COCO dataset.

### Install Requirements

Install the Python packages required for this project:

```shell
pip install -r requirements.txt
```

### Download COCO Dataset

Download the COCO 2017 validation images dataset from the following link. After downloading, unzip the file into the `data/` directory of your project.

[Download COCO 2017 Validation Images](http://images.cocodataset.org/zips/val2017.zip)

Note: The dataset is sourced from the official COCO dataset. It is essential for the image segmentation tasks in this project.

## Running the Application

To run the application, you'll need to start Kafka services and then run both the producer and consumer scripts.

### Start Kafka Services

If you're using Docker, start your Kafka services with:

```shell
docker-compose up -d
```

### Activate Virtual Environment

Activate your Python virtual environment if you have one:

```shell
source venv/bin/activate
```

### Run Producer and Consumer

Run the producer script to process images and the consumer script to display the results. Execute these commands in your terminal:

```shell
python src/producer.py &
streamlit run consumer.py
```

## Stopping the Application

To stop the application, follow these steps:

### Stop Producer

To terminate the producer script, use the following command:

```shell
kill -9 $(pidof python src/producer.py)
```

### Shutdown Docker Containers
To stop all Docker containers used by the project:

```shell
docker-compose down
```

### Stop Consumer

Use Ctrl+C in the terminal running the consumer script to interrupt it.
