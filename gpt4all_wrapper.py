from gpt4all import GPT4All

# Initialize model once
model = GPT4All("E:/GPT4All/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf")  # or your model path

def generate_response(prompt, max_tokens=2048, temperature=0.7, top_p=0.9):
    response = model.generate(
        prompt=prompt,
        max_tokens=max_tokens,      # 🚀 Use extended token count
        temperature=temperature,
        top_p=top_p,
        repeat_penalty=1.1,
    )
    return response
