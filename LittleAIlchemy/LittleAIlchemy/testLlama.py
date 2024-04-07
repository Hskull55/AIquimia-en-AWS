import replicate

def combinarAPI(elemento1, elemento2):
    model_version = "meta/llama-2-7b-chat"
    prompt = f"Tell me the result of combining {elemento1} and {elemento2}"

    for event in replicate.stream(
        model_version,
        input={
            "prompt": prompt,
            "system_prompt": "You are an AI that combines elements as if we were playing the videogame Little Alchemy.You need to come up with the result of combining both an as output, write in a single word said result. Do not say anything else in the output. Just one single word.",
        },
    ):
        print(str(event), end="")
        return str(event)
