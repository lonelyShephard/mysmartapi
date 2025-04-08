# My Web App

This project is a web application that provides a user interface for trading functionalities. It allows users to log in and access various features such as fetching historical data, placing orders, live streaming, and exiting the application.

## Project Structure

```
my-web-app
├── app
│   ├── __init__.py          # Initializes the app package
│   ├── login.py             # Contains the login functionality
│   ├── fetch_data_gui.py    # Handles fetching historical data
│   ├── place_order_gui.py    # Manages order placement functionality
│   ├── websocket_stream.py   # Implements live streaming functionality
│   ├── exit_smartapi.py     # Logic to exit the application
│   └── options.py           # Defines options available after login
├── templates
│   ├── login.html           # HTML structure for the login page
│   └── options.html         # HTML structure for the options page
├── static
│   └── css
│       └── styles.css       # CSS styles for the web application
├── run.py                   # Entry point for running the web application
├── requirements.txt         # Lists dependencies required for the project
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd my-web-app
   ```

2. **Install dependencies**:
   Make sure you have Python installed. Then, install the required packages using:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Start the web application by running:
   ```
   python run.py
   ```

4. **Access the application**:
   Open your web browser and go to `http://localhost:5000` to access the login page.

## Usage Guidelines

- **Login**: Enter your credentials and click the login button to access the trading functionalities.
- **Options**: After logging in, you will see options for:
  - Fetching historical data
  - Placing orders
  - Live streaming
  - Exiting the application

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.