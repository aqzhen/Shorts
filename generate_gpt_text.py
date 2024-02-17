from openai import OpenAI

def gen_gpt_output(input_text):
    # Call GPT API and get generated text (implementation required)
    client = OpenAI(
        api_key="",
        base_url="https://bridge.baseten.co/jwd196mw/v1"
    )

    response = client.chat.completions.create(
        model="Mistral 7B Chat",
        messages=[
            {"role":"user", "content": "You are a helpful assistant that, when given a large text input prompt, converts the prompt into a number of digestible, bite-sized, TikTok-type video scripts. "},
            {"role":"assistant","content":"Okay, got it!"},
            {"role":"user","content":input_text}]
    )

    return(response.choices[0].message.content)