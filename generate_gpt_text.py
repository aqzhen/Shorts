from openai import OpenAI

def gen_gpt_output(input_text):
    # Call GPT API and get generated text (implementation required)
    client = OpenAI(
        api_key="Rqx3ei8i.fSVxHdim3OBDWGLX4h17iFGIcv7gLGT4",
        base_url="https://bridge.baseten.co/jwd196mw/v1"
    )

    response = client.chat.completions.create(
        model="Mistral 7B Chat",
        messages=[
            {"role":"user", "content": "You are a helpful assistant that, when given a large text input prompt, converts the prompt into a number of digestible, bite-sized, TikTok-type video scripts. Return the output in json format, with key values denoting whether the description describes a scene, or if it represents the narrator. The values will be the content."},
            {"role":"assistant","content":"Okay, got it! I'll output something like this: \n\n [Scene 1]: You are sitting in school, seated at a desk.\n\n Narrator: imagine you are a student at the university of pennsylvania. \n\n"},
            {"role":"user","content":input_text}]
    )

    return(response.choices[0].message.content)