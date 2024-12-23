import os
import time
from PIL import ImageGrab
from io import BytesIO
import boto3
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB URI


class AWSScreenshotUploaderMongoDB:
    def __init__(self):
        # Initialize AWS S3 client
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )
        # Initialize MongoDB client
        self.mongo_client = MongoClient(MONGO_URI)
        self.db = self.mongo_client["screenshot_metadata"]
        self.collection = self.db["screenshots"]

        # Dummy user ID
        self.user_id = "anjali"

    def capture_and_upload_screenshot(self, action):
        """
        Captures a screenshot, uploads it to AWS S3, and stores metadata in MongoDB.
        The action parameter differentiates between 'start', 'stop', and 'random'.
        """
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        date = time.strftime("%Y-%m-%d")
        object_key = f"screenshots/{self.user_id}/{date}/screenshot_{action}_{timestamp}.png"

        try:
            # Capture the screenshot
            screenshot = ImageGrab.grab()
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            buffer.seek(0)

            # Upload to S3
            self.s3_client.upload_fileobj(buffer, BUCKET_NAME, object_key)
            s3_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_key}"

            # Store metadata in MongoDB
            self.store_metadata(date, s3_url)

            print(f"Screenshot uploaded and metadata stored: {s3_url}")
        except Exception as e:
            print(f"Error during upload or metadata storage: {e}")

    def store_metadata(self, date, s3_url):
        """
        Stores screenshot metadata in MongoDB by appending S3 URLs to a single document per day.
        """
        try:
            existing_entry = self.collection.find_one({"userID": self.user_id, "date": date})
            if existing_entry:
                # Append the new URL to the existing document
                self.collection.update_one(
                    {"userID": self.user_id, "date": date},
                    {"$push": {"s3Urls": s3_url}},
                )
            else:
                # Create a new document for the day
                self.collection.insert_one(
                    {
                        "userID": self.user_id,
                        "date": date,
                        "s3Urls": [s3_url],
                    }
                )
        except Exception as e:
            print(f"Error storing metadata in MongoDB: {e}")
