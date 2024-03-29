import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import firebase_admin
from firebase_admin import firestore


def generate_text(project_id: str, location: str, file: str) -> str:
    # Initiate Git Actions
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    multimodal_model = GenerativeModel("gemini-pro-vision")
    # Query the model
    response = multimodal_model.generate_content(
        [
            # Add an example image
            Part.from_uri(
                file, mime_type="image/jpeg"
            ),
            # Add an example query
            "Let's play pictionary. I will show you a drawing I drew and you guess what it is! I will be drawing common nouns like animals, vehicles, and household objects. Please guess even if you are unsure. Do not respond with a question.",
        ]
    )
    return response.text


def save_results(uuid, time, desc, url):
    # import firebase_admin

    # Application Default credentials are automatically created.
    # app = firebase_admin.initialize_app()

    if not firebase_admin._apps:
        firebase_admin.initialize_app()

    db = firestore.client()

    doc_ref = db.collection("gemini-demo-images").document(uuid)
    doc_ref.set({"timeStamp": time, "imageDescription": desc, "imageUrl": url})
