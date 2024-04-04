import replicate

# https://replicate.com/meta/llama-2-70b-chat
model_version = "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"

for event in replicate.stream(
    model_version,
    input={
        "prompt": "What would be the result of combining water and fire? Answer in just one word",
    },
):
    print(str(event), end="")
