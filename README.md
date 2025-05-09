# Nilean News API

This repository contains a web application that scrapes news websites and provides a unified API to access the scraped data. The app is built using the FastAPI framework and uses a Firebase Firestore database for data storage.

## Setting Up Firebase and Running the App

### Prerequisites
1. Ensure you have Python installed on your system.
2. Install `pip` and `virtualenv` if not already installed.
3. Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/).

### Setting Up Firebase
1. In your Firebase project, navigate to **Project Settings** and download the `google-services.json` file.
2. Place the downloaded file in the root directory of your project.
3. Enable the required Firebase services (e.g., Firestore, Authentication) in the Firebase Console.

### Running the App
1. Clone the repository:
  ```bash
  git clone https://github.com/your-username/news-api.git
  cd news-api
  ```
2. Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Start the Unicorn server:
  ```bash
  unicorn app:app
  ```

### Notes
- Ensure your Firebase configuration matches the app's requirements.
- Refer to the Firebase documentation for advanced setup and troubleshooting.
- Replace `app:app` with the appropriate module and application name if different.
- Use environment variables to securely manage Firebase credentials.
