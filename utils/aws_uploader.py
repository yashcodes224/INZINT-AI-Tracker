import os
import sys
import time
from PIL import ImageGrab
from io import BytesIO
import boto3
from pymongo import MongoClient
from dotenv import load_dotenv

# Determine correct path for .env file and load environment variables
def load_environment():
    # When bundled as exe, use embedded .env file
    if getattr(sys, 'frozen', False):
        # Path to the extracted resources in the bundled app
        env_path = os.path.join(sys._MEIPASS, '.env')
    else:
        # Regular development environment
        env_path = '.env'
    
    # Load the .env file
    load_dotenv(env_path)
    
    # Return config dict with all necessary credentials
    return {
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "AWS_REGION": os.getenv("AWS_REGION"),
        "BUCKET_NAME": os.getenv("AWS_BUCKET_NAME"),
        "MONGO_URI": os.getenv("MONGO_URI")
    }

class AWSScreenshotUploaderMongoDB:
    def __init__(self, user_name):
        """
        Initializes the AWS S3 client, MongoDB client, and stores the logged-in user dynamically.
        :param user_name: The logged-in user's name (passed dynamically).
        """
        # Load configuration
        config = load_environment()
        
        # Initialize AWS client with credentials from the embedded .env
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
            region_name=config["AWS_REGION"],
        )
        self.bucket_name = config["BUCKET_NAME"]
        self.region = config["AWS_REGION"]
        
        # Initialize MongoDB client
        self.mongo_client = MongoClient(config["MONGO_URI"])
        self.db = self.mongo_client["screenshot_metadata"]
        self.collection = self.db["screenshots"]
        
        # Store logged-in user
        self.user_name = user_name or "unknown_user"
    
    def capture_and_upload_screenshot(self, action):
        """
        Captures a screenshot, uploads it to AWS S3, and stores metadata in MongoDB.
        The action parameter differentiates between 'start', 'stop', and 'random'.
        """
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        date = time.strftime("%Y-%m-%d")
        object_key = f"screenshots/{self.user_name}/{date}/screenshot_{action}_{timestamp}.png"
        
        try:
            # Capture the screenshot
            screenshot = ImageGrab.grab()
            buffer = BytesIO()
            screenshot.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Upload to S3
            self.s3_client.upload_fileobj(buffer, self.bucket_name, object_key)
            s3_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{object_key}"
            
            # Store metadata in MongoDB
            self.store_metadata(date, s3_url)
            print(f"Screenshot uploaded and metadata stored: {s3_url}")
            
            return s3_url
        except Exception as e:
            print(f"Error during upload or metadata storage: {e}")
            return None
    
    def store_metadata(self, date, s3_url):
        """
        Stores screenshot metadata in MongoDB by appending S3 URLs to a single document per day.
        """
        try:
            existing_entry = self.collection.find_one({"userName": self.user_name, "date": date})
            
            if existing_entry:
                # Append the new URL to the existing document
                self.collection.update_one(
                    {"userName": self.user_name, "date": date},
                    {"$push": {"s3Urls": s3_url}},
                )
            else:
                # Create a new document for the day
                self.collection.insert_one(
                    {
                        "userName": self.user_name,
                        "date": date,
                        "s3Urls": [s3_url],
                    }
                )
        except Exception as e:
            print(f"Error storing metadata in MongoDB: {e}")