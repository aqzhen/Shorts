from openai import OpenAI

def gen_gpt_output(input_text):
    # Call GPT API and get generated text (implementation required)
    client = OpenAI(
        api_key="v1ansFR6.sCFTwu9SNXRIOlUkCuxBM6CBhpZKec4K",
        base_url="https://bridge.baseten.co/jwd196mw/v1"
    )

    prompt = '''
    {
        "Scene 1": {
            "Content": "Hey TikTok fam! Today, I'm going to show you how to whip up a delicious and super easy meal in just a few minutes. Get ready to impress your friends and family with your cooking skills! Let's dive in!"
        },
        "Scene 2": {
            "Content": "First up, we've got some fresh veggies, pasta, and chicken breasts. It's time to turn these simple ingredients into something extraordinary!"
        },
        "Scene 3": {
        
        }
        ... and so on
    }
    '''

    response = client.chat.completions.create(
        model="Mixtral 8x7B Instruct TRT-LLM Weights Only Quantized",
        messages=[
            {"role":"user", "content": "You are a helpful assistant that, when given a large text input prompt, converts the prompt into a number of digestible, bite-sized, TikTok-type video script scenes with enthusiasm and wit, summarizing at a high level. Make each scene at most two sentences. Return the output in json format. Here's an example, you must follow it strictly in json structure using Scenes as keys and the content as values:" + prompt 
    },
            {"role":"assistant","content":""},
            {"role":"user","content":input_text}]
    )

    return(response.choices[0].message.content)