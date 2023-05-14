import requests
from google.auth import default
from google.auth.transport.requests import Request

class BisonChatApp:
    def __init__(
        self,
        project_id=None,
        context='',
        examples=[],
        temperature=0.2,
        max_output_tokens=100,
        top_p=0.95,
        top_k=40,
    ):
        """
        Initializes the VertexChatApp instance.

        :param project_id: Google Cloud project ID. If not provided, it will use the project ID from the default credentials.
        :param context: Context for the AI model to consider when generating responses.
        :param examples: A list of example input-output pairs to guide the AI model.
        :param temperature: Controls the degree of randomness in token selection. Lower values make the output more deterministic and less creative.
        :param max_output_tokens: Maximum number of tokens in the generated response.
        :param top_p: Probability threshold for token selection. Lower values make the output less random.
        :param top_k: Number of most probable tokens to consider for selection. Lower values make the output less random.
        """
        if not project_id:
            _, project_id = default()

        self.project_id = project_id
        self.model_endpoint = f'https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/chat-bison:predict'
        self.credentials, _ = default()
        self.credentials.refresh(Request())
        self.headers = {'Authorization': 'Bearer ' + self.credentials.token}

        self.context = context
        self.examples = examples
        self.parameters = {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
            "topP": top_p,
            "topK": top_k,
        }
        self.messages = []

    async def chat(self, message):
        self.messages.append({"author": "User", "content": message})

        request_body = {
            "instances": [{
                "context":  self.context,
                "examples": [
                    {
                        "input": example["input"],
                        "output": example["output"]
                    } for example in self.examples
                ],
                "messages": self.messages,
            }],
            "parameters": self.parameters
        }

        try:
            response = requests.post(self.model_endpoint, headers=self.headers, json=request_body)
            response.raise_for_status()
            generated_text = response.json()['predictions'][0]['candidates'][0]['content']
            message = {"author": "AI", "content": generated_text}
        except Exception as e:
            generated_text = f"Unable to get a response from the AI model. ({str(e)})"
            message = {"author": "System", "content": generated_text}

        self.messages.append(message)
        return message

    def clear_messages(self):
        self.messages = []

    def end_chat(self):
        del self


async def print_chat(message):
    print(await app.chat(message))


if __name__ == '__main__':
    app = BisonChatApp(context="Write a response in a friendly and informative manner.", examples=[
        {
            "input": "What is Vertex AI?",
            "output": "Vertex AI is a suite of machine learning tools and services by Google Cloud for developing, deploying, and maintaining AI models."
        }
    ])

    import asyncio

    asyncio.run(print_chat("Tell me about Vertex AI."))
    asyncio.run(print_chat("How many tokens have been used so far?"))
