import pytest
from vertex_ai import BisonChatApp

def test_chat():
    app = BisonChatApp(context="Write a response in a friendly and informative manner.", examples=[
        {
            "input": "What is Vertex AI?",
            "output": "Vertex AI is a suite of machine learning tools and services by Google Cloud for developing, deploying, and maintaining AI models."
        }
    ])

    response = app.chat("Tell me about Vertex AI.")
    assert "Vertex AI" in response['content']

def test_clear_messages():
    app = BisonChatApp()
    app.chat("Test message.")
    app.clear_messages()
    assert len(app.messages) == 0

def test_end_chat():
    app = BisonChatApp()
    app.end_chat()
    with pytest.raises(AttributeError):
        app.chat("Test message.")