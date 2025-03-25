model_name = "ibm/granite-3-2-8b-instruct" #"ibm/Mixtral-8x7B-Instruct-v0.1"
model_parameters = {
        "max_new_tokens": 200,
        "decoding_method": "greedy",
        "temperature": 0.9,
        "repetition_penalty": 1.0,
        "top_k": 50,
        "top_p": 1.0,
        "stop_sequences": []
    }