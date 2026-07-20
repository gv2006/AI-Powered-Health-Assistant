# Import necessary libraries
import numpy as np  # for math operations
from sklearn.feature_extraction.text import TfidfVectorizer  # text processing
from sklearn.naive_bayes import MultinomialNB  # for symptom classification
from sklearn.tree import DecisionTreeClassifier  # for BMI predictions
import joblib  # for saving/loading models
import os  # for file operations

class HealthAssistant:
    def __init__(self):
        # Medical advice database - collected from various sources
        self.medical_advice = {
            'fever': {  # Most common condition
                'symptoms': ['high temperature', 'chills', 'body aches'],  # main symptoms
                'medicines': 'Paracetamol or Ibuprofen',  # basic medications
                'lifestyle': 'Rest, stay hydrated, wear light clothing',  # lifestyle advice
                'warning': 'Seek immediate medical help if fever exceeds 103°F (39.4°C).'  # critical warning
            }
        }
        
        # Initialize ML components
        self.vectorizer = TfidfVectorizer()  # works well for text data
        self.symptom_classifier = MultinomialNB()  # text classification model
        self.bmi_classifier = DecisionTreeClassifier()  # simple model for BMI predictions
        
        # Training data for symptom classifier (example data)
        self.symptom_data = [
            "I have a high temperature and chills", 
            "My body is aching and I feel hot", 
            "I'm feeling feverish with body pain", 
            "Having chills and fever", 
            "High temperature with body aches", 
            "Feeling cold and shivering with fever"
        ]
        self.symptom_labels = ['fever'] * len(self.symptom_data)  # all labeled as 'fever'
        
        # BMI training data - based on standard ranges
        self.bmi_features = np.array([[18], [19], [23], [24], [27], [28], [32], [33]])
        self.bmi_labels = ['underweight', 'underweight', 'normal', 'normal', 
                           'overweight', 'overweight', 'obese', 'obese']
        
        # Train the ML models
        self._train_models()

    def _train_models(self):
        # Train the symptom classification model
        X_symptoms = self.vectorizer.fit_transform(self.symptom_data)
        self.symptom_classifier.fit(X_symptoms, self.symptom_labels)
        
        # Train the BMI classifier
        self.bmi_classifier.fit(self.bmi_features, self.bmi_labels)

    def calculate_bmi(self, weight, height):
        """
        Calculates BMI using the formula: BMI = weight / (height^2)
        Returns the BMI value and the corresponding category based on WHO guidelines.
        """
        bmi = weight / (height * height)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        return bmi, category

    def get_health_goal_advice(self, choice):
        """
        Returns basic advice based on the chosen health goal.
        """
        if choice == '1':
            return "Create a calorie deficit with a balanced diet and regular exercise."
        elif choice == '2':
            return "Increase protein intake and follow a progressive resistance training program."
        elif choice == '3':
            return "Maintain regular exercise and balanced nutrition for overall well-being."
        else:
            return "Invalid choice. Please select a valid option from the menu."

    def get_medical_advice(self, condition):
        """
        Returns medical advice based on the input condition.
        First, tries a direct match; if not found, uses the ML model for prediction.
        """
        condition = condition.lower()
        if condition in self.medical_advice:
            return self.medical_advice[condition]
        
        # If not directly found, predict using the ML model
        condition_vector = self.vectorizer.transform([condition])
        predicted_condition = self.symptom_classifier.predict(condition_vector)
        if predicted_condition[0] in self.medical_advice:
            return self.medical_advice[predicted_condition[0]]
        return None  # No advice found

    def predict_bmi_category(self, bmi):
        """
        Predicts BMI category using the trained ML model.
        """
        prediction = self.bmi_classifier.predict([[bmi]])
        return prediction[0].capitalize()

    def save_models(self):
        """
        Saves the trained models and vectorizer to the disk.
        """
        if not os.path.exists('models'):
            os.makedirs('models')
        joblib.dump(self.symptom_classifier, 'models/symptom_classifier.pkl')
        joblib.dump(self.vectorizer, 'models/vectorizer.pkl')
        joblib.dump(self.bmi_classifier, 'models/bmi_classifier.pkl')

    def load_models(self):
        """
        Loads saved models from disk.
        """
        try:
            self.symptom_classifier = joblib.load('models/symptom_classifier.pkl')
            self.vectorizer = joblib.load('models/vectorizer.pkl')
            self.bmi_classifier = joblib.load('models/bmi_classifier.pkl')
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False

def get_numeric_input(prompt, datatype=float):
    """
    Prompts the user for input until a valid numeric value is entered.
    """
    while True:
        try:
            value = datatype(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")

def main():
    # Initialize the assistant
    assistant = HealthAssistant()
    
    print("=== Welcome to Your Health Assistant ===\n")
    
    # Get user details with input validation
    name = input("Enter your name: ").strip()
    age = get_numeric_input("Enter your age: ", float)
    weight = get_numeric_input("Enter your weight (kg): ", float)
    height = get_numeric_input("Enter your height (m): ", float)

    # Calculate BMI and display results
    bmi, category = assistant.calculate_bmi(weight, height)
    print(f"\n{name}, your BMI is {bmi:.2f} ({category}).")
    
    # Health goal advice menu with validation
    while True:
        print("\nChoose a health goal:")
        print("1. Weight Loss")
        print("2. Muscle Gain")
        print("3. General Fitness")
        choice = input("Enter choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    advice = assistant.get_health_goal_advice(choice)
    print(f"\nHealth Advice: {advice}")
    
    # Loop for medical advice if needed
    while True:
        need_medical = input("\nDo you need medical advice? (y/n): ").strip().lower()
        if need_medical == 'y':
            condition = input("Enter condition (e.g., cold, fever): ").strip()
            medical_info = assistant.get_medical_advice(condition)
            if medical_info:
                print("\nMedical Advice:")
                print(f"Symptoms: {', '.join(medical_info['symptoms'])}")
                print(f"Medicines: {medical_info['medicines']}")
                print(f"Lifestyle: {medical_info['lifestyle']}")
                print(f"Warning: {medical_info['warning']}")
            else:
                print("Sorry, no medical advice is available for that condition.")
        elif need_medical == 'n':
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
    
    print("\nSession logged. Stay healthy!")

if __name__ == "__main__":
    main()
