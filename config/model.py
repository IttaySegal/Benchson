model_name =  "mistralai/mistral-large"
model_parameters = {
        "max_new_tokens": 500,
        "decoding_method": "greedy",
        "temperature": 0.9,
        "repetition_penalty": 1.0,
        "top_k": 50,
        "top_p": 1.0,
        "random_seed": 42,
        "stop_sequences": []
    }