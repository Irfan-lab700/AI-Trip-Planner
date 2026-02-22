import os
from huggingface_hub import InferenceClient
client = InferenceClient(
    model = "Qwen/Qwen2.5-7B-Instruct",
    token=os.getenv("HF_TOKEN")
)
def generate_output(user_data):
    prompt = f"""
    Generate a {user_data['day']}-day itinerary for a trip from {user_data['source']} 
    to {user_data['destination']}. Interests: {', '.join(user_data['interests'])}. 
    Budget: {user_data['budget']} INR.
    Return the result in a simple list for each day.
    """
    response = client.chat.completions.create(
        messages = [{"role":"user", "content": prompt,}],
        max_tokens = 500
    )
    ai_text = response.choices[0].message.content
    return ai_text
if __name__ == "__main__":
    from user_input import get_user_input 
    user_data = get_user_input() 
    itinerary = generate_output(user_data) 
    print("\nAI-generated Itinerary:\n", itinerary)
    