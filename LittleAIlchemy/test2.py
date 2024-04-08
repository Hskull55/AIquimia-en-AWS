import replicate

input = {
    "top_p": 1,
    "prompt": "Tell me the result of combining Fire and Water",
    "temperature": 0.75,
    "system_prompt": "You are an AI that combines elements as if we were playing the videogame Little Alchemy.You need to come up with the result of combining both an as output, write in a single word said result. Do not say anything else in the output. Just one single word.",
    "max_new_tokens": 800,
    "repetition_penalty": 1
}

output = replicate.run(
    "meta/llama-2-7b-chat",
    input=input
)
print(output)
#print("".join(output))
