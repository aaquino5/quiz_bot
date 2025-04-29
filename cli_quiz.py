import json
import random
import time

# Load questions from JSON file
QUESTION_FILE = "fortisase_questions.json"

def load_questions():
    """Loads the questions from the JSON dataset."""
    try:
        with open(QUESTION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{QUESTION_FILE}' not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error: Failed to parse JSON file - {e}")
        return []

def run_exam(num_questions):
    """Runs the exam with the specified number of questions."""
    questions = load_questions()
    if not questions:
        print("❌ No questions available to run the exam.")
        return
    
    random.shuffle(questions)  # Shuffle questions for randomness
    selected_questions = questions[:num_questions]
    
    score = 0
    for i, question in enumerate(selected_questions, start=1):
        print(f"\n📝 Question {i}/{num_questions}")
        print(f"\n📌 {question['question']}")
        
        # Shuffle answer choices
        options = list(question["options"].items())
        random.shuffle(options)
        option_map = {chr(97 + i): key for i, (key, _) in enumerate(options)}  # Map a, b, c, d to answer keys
        
        for letter, (key, value) in zip(option_map.keys(), options):
            print(f"{letter}) {value}")
        
        user_answer = input("📝 Your answer (a, b, c, d): ").strip().lower()
        correct_key = question["correct_answer"]
        correct_letter = next((letter for letter, key in option_map.items() if key == correct_key), None)

        if user_answer in option_map:
            if option_map[user_answer] == correct_key:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. The correct answer is: {correct_letter}) {question['options'][correct_key]}")
        else:
            print("⚠️ Invalid input. Please enter a valid option (a, b, c, d).")
        
        print(f"📖 Explanation: {question['explanation']}")
        print(f"🔗 Reference: {question['source']}")
        time.sleep(1)  # Small delay for readability
    
    print(f"\n🎯 Your final score: {score}/{num_questions}")

if __name__ == "__main__":
    try:
        num_questions = int(input("Enter the number of questions for the exam: "))
        run_exam(num_questions)
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")

