# Health Assistant

Health Assistant is a Python-based application that provides personalized health advice by calculating BMI, offering health goal recommendations, and returning medical advice based on user input. The project uses machine learning models (via scikit-learn) for symptom classification and BMI prediction.

## Features

- **BMI Calculation:** Calculates BMI and categorizes it according to WHO guidelines.
- **Health Goal Advice:** Provides basic advice on weight loss, muscle gain, or general fitness.
- **Medical Advice:** Uses direct matching and an ML-based approach to offer medical advice.
- **Model Persistence:** Supports saving and loading of trained models.

## Technologies Used

- Python 3.x
- NumPy
- scikit-learn
- joblib
- OS

## Project Structure

- `src/health_assistant.py`: Contains the main application code.
- `requirements.txt`: Lists the project dependencies.
- `README.md`: Project documentation.
- `.gitignore`: Specifies files and folders to ignore in the repository.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/health-assistant.git
   cd health-assistant
