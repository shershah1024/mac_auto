import json
import requests
from submit_quiz import submit_spanish_quiz

def generate_spanish_quiz(user_message):
    url = 'https://api.anthropic.com/v1/messages'
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': "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",
        'anthropic-version': '2023-06-01'
    }

    body = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 3000,
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "tools": [
            {
                "name": "submit_spanish_quiz",
                "description": "Submit a new Spanish reading exercise quiz with various question types",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the quiz"
                        },
                        "lessonText": {
                            "type": "string",
                            "description": "The lesson text in Spanish"
                        },
                        "questions": {
                            "type": "array",
                            "description": "An array of questions for the quiz",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["multipleChoice", "fillInTheBlank", "checkbox", "essay"],
                                        "description": "The type of question"
                                    },
                                    "question": {
                                        "type": "string",
                                        "description": "The question text"
                                    },
                                    "options": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Answer options for multiple choice or checkbox questions"
                                    },
                                    "correctAnswer": {
                                        "type": "string",
                                        "description": "The correct answer for multiple choice or fill in the blank questions"
                                    },
                                    "correctAnswers": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "The correct answers for checkbox questions"
                                    },
                                    "minWords": {
                                        "type": "integer",
                                        "description": "Minimum word count for essay questions (optional)"
                                    },
                                    "maxWords": {
                                        "type": "integer",
                                        "description": "Maximum word count for essay questions (optional)"
                                    }
                                },
                                "required": ["type", "question"]
                            }
                        }
                    },
                    "required": ["title", "lessonText", "questions"]
                }
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        # Check for tool use in the response
        for content in data.get('content', []):
            if content.get('type') == 'tool_use':
                quiz_data = content.get('input')
                if quiz_data:
                    return quiz_data

        print('No valid tool use found in the response')
        raise ValueError('No valid tool use found in the response')

    except requests.RequestException as e:
        print(f'Error generating quiz: {e}')
        raise
    except json.JSONDecodeError as e:
        print(f'Error parsing JSON: {e}')
        raise


def generate_quiz(message):
    quiz_data = generate_spanish_quiz(message)
    link= submit_spanish_quiz(quiz_data)
    print(link)



message= "Please create a spanish quiz about a mad king. The text should be about 150 words, and I need 10 questions. This is for beginners in Spanish"
generate_quiz(message)