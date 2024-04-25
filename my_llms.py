def get_llama():
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 2000,
        "min_new_tokens": 10,
        "temperature": 0.01,
        #     "top_k": 50,
        #     "top_p": 1,
    }

    from langchain_ibm import WatsonxLLM

    llama = WatsonxLLM(
        model_id="meta-llama/llama-3-70b-instruct",
        url="https://us-south.ml.cloud.ibm.com",
        project_id="a92c8753-e724-4835-a415-ec0730333135",
        params=parameters,
        apikey="b9n-3HqQTRSMvFhUry-awqN3ZLVIr_UzddSht6OQ6CyV",
    )

    return llama


def get_openai():
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4-turbo")

    return llm
