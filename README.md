# Palm-Chat

Palm-Chat is a Python-based application that uses Vertex AI and its PaLM2 powered chat-bison model to generate responses. This interactive chat application provides a user-friendly interface for managing and deploying your chatbots.

## Features

- Customizable context input field
- Examples input fields
- Adjustable model parameters: Temperature, Max Output Tokens, Top P, Top K
- Interactive chat UI with clear and end chat options
- Uses Vertex AI's chat-bison model for advanced conversational AI

## Requirements

- A GCP project with Vertex AI API enabled (aiplatform.googleapis.com)
- A machine with python 3.6+ installed.

## IMPORTANT

This application uses Google's Vertex AI API and it may incur charges. Please check the [pricing information](https://cloud.google.com/vertex-ai/pricing) before you use this. At the time of writing, PaLM API was in preview and available for free. This will change when the API becomes generally available.

## Installation

To use Palm-Chat,

1. clone the repository and install the dependencies.

    ```bash
    git clone https://github.com/eaingaran/palm-chat.git
    cd palm-chat
    ```

2. setup virtual env

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. setup gcp default credentials

    ```bash
    gcloud auth login --update-adc
    gcloud config set project <gcp-project-id>  #Make sure the project has Vertex AI API (aiplatform.googleapis.com) enabled.
    ```

## Usage

1. Run the application:

    ```bash
    python3 main.py
    ```

2. You will see a form where you can input the context, examples, and parameters for the model. After setting these up, click the "Start Chat" button to start interacting with the chatbot.

3. Here is a brief description of the fields:

    `Context`: The initial conversation history or context for the chatbot.

    `Examples`: Demonstrative examples of the type of conversation you want the model to have. You can add more examples by clicking the "Add Example" button.

    `Temperature`: Controls the randomness of the model's output. A higher value makes the output more random, while a lower value makes it more deterministic.

    `Max Output Tokens`: The maximum length of the model's output.

    `Top P`: A parameter for nucleus sampling, which is a method for controlling the randomness of the model's output.

    `Top K`: A parameter for controlling the diversity of the model's output.

4. Once the chat starts, you can type your message in the bottom text field and click "Send" or press enter to send it. The model's responses will appear above. You can clear the chat or end the chat by clicking the corresponding buttons.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Contact

For any issues, questions, or feedback, please contact the repository owner.
