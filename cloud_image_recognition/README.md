# Cloud Image Recognition System

A comprehensive GUI application built with Python and Tkinter that performs image recognition using Google Cloud Vision API, with Firebase authentication and Google Cloud Storage for persistent storage.

## Features

### 🔐 User Authentication
- Firebase email/password authentication
- Secure login and signup functionality
- User-specific data storage

### 🖼️ Image Recognition
- **Label Detection**: Identifies objects and concepts in images
- **Object Localization**: Detects and locates specific objects
- **Text Detection (OCR)**: Extracts text from images
- **Face Detection**: Identifies faces and emotions
- **Landmark Detection**: Recognizes famous landmarks
- **Dominant Color Analysis**: Analyzes color composition

### ☁️ Cloud Storage
- Automatic upload of analyzed images to Google Cloud Storage
- Results saved as JSON files
- User-specific storage paths: `{UID}/images/` and `{UID}/results/`

### 📜 History Management
- View all previous analyses
- Detailed view of analysis results
- Delete unwanted history items
- Automatic cleanup of associated files

## Requirements

- Python 3.7+
- Google Cloud Platform account with:
  - Vision API enabled
  - Cloud Storage bucket created
  - Service account credentials
- Firebase project with Authentication enabled

## Installation

1. Clone or download the project

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Google Cloud Setup

1. **Create a GCP Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable APIs**:
   - Enable Cloud Vision API
   - Enable Cloud Storage API

3. **Create Service Account**:
   - Go to IAM & Admin > Service Accounts
   - Create a service account with appropriate permissions
   - Download the JSON key file
   - Rename it to match the one in the code or update the path in `main.py`

4. **Create Storage Bucket**:
   - Go to Cloud Storage
   - Create a bucket (e.g., `image-recognition-storage-project`)
   - Update the bucket name in `main.py` if different

### Firebase Setup

1. **Create Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project

2. **Enable Authentication**:
   - In Firebase Console, go to Authentication
   - Enable Email/Password sign-in method

3. **Get Configuration**:
   - Go to Project Settings
   - Copy your Web API Key and Project ID
   - Update the Firebase configuration in `main.py`:
   ```python
   firebase_config = {
       "apiKey": "YOUR_API_KEY",
       "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
       "projectId": "YOUR_PROJECT_ID",
       "storageBucket": "YOUR_PROJECT_ID.appspot.com",
       "messagingSenderId": "YOUR_MESSAGING_ID",
       "appId": "YOUR_APP_ID",
       "databaseURL": ""
   }
   ```

## Usage

1. **Run the application**:
```bash
python main.py
```

2. **First Time Users**:
   - Click "Sign Up" to create an account
   - Enter your email and password (minimum 6 characters)
   - Click "Sign Up" to create your account

3. **Returning Users**:
   - Enter your email and password
   - Click "Login" to access the application

4. **Analyze Images**:
   - Click "📁 Upload Image" to select an image
   - Click "🔍 Analyze & Save" to perform analysis
   - Results will be displayed and automatically saved to cloud

5. **View History**:
   - Click "📜 View History" to see all your previous analyses
   - Select an item and click "View Details" to see full results
   - Click "Delete" to remove unwanted items
   - Click "Refresh" to reload the history list

6. **Logout**:
   - Click "Logout" button in the top-right corner

## Project Structure

```
cloud_image_recognition/
├── main.py                          # Main application file
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── python-project-476206-*.json    # GCP service account credentials
```

## Data Storage Format

### Images
- Path: `{UID}/images/{timestamp}_{filename}`
- Example: `abc123/images/20250125_143022_photo.jpg`

### Analysis Results
- Path: `{UID}/results/{timestamp}_{filename}.json`
- Example: `abc123/results/20250125_143022_photo.json`

### JSON Structure
```json
{
  "timestamp": "20250125_143022",
  "original_filename": "photo.jpg",
  "image_path": "abc123/images/20250125_143022_photo.jpg",
  "labels": [
    {"description": "Cat", "score": 0.95},
    {"description": "Pet", "score": 0.92}
  ],
  "objects": [
    {"name": "Cat", "score": 0.89}
  ],
  "text": "Detected text from image",
  "faces": 0
}
```

## Features Overview

### Authentication Flow
1. Login/Signup screen on startup
2. Credentials validated through Firebase
3. User session maintained throughout app usage
4. Secure logout functionality

### Analysis Workflow
1. User uploads an image
2. Image is analyzed using Google Cloud Vision API
3. Results are displayed in real-time
4. Both image and results are saved to GCS
5. Files organized by user UID

### History Management
1. List all user's previous analyses
2. View detailed results for any analysis
3. Delete analyses (removes both image and JSON)
4. Real-time list updates

## Troubleshooting

### API Errors
- **"API not initialized"**: Check your GCP credentials file path
- **"Permission denied"**: Ensure service account has proper permissions
- **"Bucket not found"**: Verify bucket name and existence

### Authentication Errors
- **"Invalid email or password"**: Check credentials
- **"Email already exists"**: Use login instead of signup
- **"Weak password"**: Use at least 6 characters

### Storage Errors
- **"Failed to upload"**: Check internet connection and GCS permissions
- **"Failed to load history"**: Verify bucket access permissions

## Security Notes

- Never commit your service account JSON file to version control
- Keep your Firebase API key secure
- Use environment variables for sensitive configuration in production
- Implement proper IAM policies for GCS bucket access

## Development

### Adding New Features
1. Image filters and preprocessing
2. Batch image processing
3. Export reports as PDF
4. Image comparison features
5. Custom model integration

### Customization
- Modify UI colors and layout in the respective setup functions
- Add new Vision API features (SafeSearch, Web Detection, etc.)
- Customize storage paths in the analysis function
- Extend JSON structure for additional metadata

## License

This project is provided as-is for educational purposes.

## Support

For issues related to:
- Google Cloud: [GCP Documentation](https://cloud.google.com/docs)
- Firebase: [Firebase Documentation](https://firebase.google.com/docs)
- Python/Tkinter: [Python Documentation](https://docs.python.org/)

## Version History

- **v2.0** (Current): Added Firebase authentication and GCS storage with history management
- **v1.0**: Basic image recognition with Google Cloud Vision API

---

**Note**: Make sure to replace placeholder values in the configuration with your actual Firebase and GCP credentials before running the application.
