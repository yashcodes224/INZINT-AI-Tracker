# # aws_uploader.py
# import boto3
# from io import BytesIO
# from PIL import ImageGrab
# from time import gmtime
# import time
# import os
# from dotenv import load_dotenv

# # Load credentials from .env file
# load_dotenv()

# # Get AWS credentials and configuration from environment variables
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_REGION = os.getenv("AWS_REGION")
# BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


# class AWSScreenshotUploader:
#     def __init__(self):
#         self.s3_client = boto3.client(
#             "s3",
#             aws_access_key_id=AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#             region_name=AWS_REGION,
#         )

#     def capture_and_upload_screenshot(self, action):
#         """
#         Capture a screenshot and upload it to an S3 bucket.
#         action: 'start' or 'stop' to identify when the screenshot was taken.
#         """
#         timestamp = time.strftime("%A, %D %B %Y %r")
#         object_key = f"screenshots/screenshot_{action}_{timestamp}.png"

#         try:
#             # Capture screenshot
#             screenshot = ImageGrab.grab()
#             buffer = BytesIO()
#             screenshot.save(buffer, format="PNG")
#             buffer.seek(0)

#             # Upload to S3
#             self.s3_client.upload_fileobj(buffer, BUCKET_NAME, object_key)
#             print(f"Screenshot uploaded to S3: {object_key}")
#         except Exception as e:
#             print(f"Error uploading screenshot: {e}")

import os
import time
import boto3
from dotenv import load_dotenv
from pymongo import MongoClient
from PIL import ImageGrab
from io import BytesIO

# Load credentials from .env file
load_dotenv()

# AWS credentials and configuration from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB URI for your database (e.g., "mongodb://localhost:27017/")
DB_NAME = "screenshot_metadata"
COLLECTION_NAME = "screenshots"


# AWS Screenshot Upload Class with MongoDB Integration
class AWSScreenshotUploaderMongoDB:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
        )

        # Connect to MongoDB
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def capture_and_upload_screenshot(self, user_id, action):
        """
        Capture a screenshot, upload it to S3, and store metadata in MongoDB.
        Action: 'start' or 'stop' to identify when the screenshot was taken.
        """
        timestamp = time.strftime("%A, %D %B %Y %r")
        date = time.strftime("%Y-%m-%d")  # Use date as the category for grouping
        object_key = f"screenshots/screenshot_{action}_{timestamp}.png"

        try:
            # Capture screenshot
            screenshot = ImageGrab.grab()
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            buffer.seek(0)

            # Upload to S3
            self.s3_client.upload_fileobj(buffer, BUCKET_NAME, object_key)
            s3_url = f"https://{AWS_REGION}.amazonaws.com/{BUCKET_NAME}/{object_key}"

            print(f"Screenshot uploaded to S3: {s3_url}")

            # Insert metadata into MongoDB, categorizing by user and date
            self.store_metadata_in_mongo(user_id, date, s3_url)

        except Exception as e:
            print(f"Error uploading screenshot: {e}")

    def store_metadata_in_mongo(self, user_id, date, s3_url):
        """
        Store the screenshot metadata in MongoDB.
        If an entry for the user on the same date already exists, append the new URL.
        """
        existing_entry = self.collection.find_one({"userID": user_id, "date": date})

        if existing_entry:
            # If entry exists, update the list of URLs
            self.collection.update_one(
                {"userID": user_id, "date": date},
                {"$push": {"s3Urls": s3_url}},
            )
            print(f"Metadata updated for user {user_id} on {date}")
        else:
            # If no entry exists, create a new one
            new_entry = {
                "userID": user_id,
                "date": date,
                "s3Urls": [s3_url],
            }
            self.collection.insert_one(new_entry)
            print(f"Metadata inserted for user {user_id} on {date}")


