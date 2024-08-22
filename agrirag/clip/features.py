from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

class CLIPFeatureExtractor:
    """
    A class to load the CLIP model from Hugging Face's Transformers library and extract
    text and image features for downstream tasks such as Retrieval-Augmented Generation (RAG).

    Attributes:
    -----------
    model : CLIPModel
        The CLIP model instance loaded from pretrained weights.
    processor : CLIPProcessor
        The processor instance used to preprocess text and image inputs for the model.
    
    Methods:
    --------
    extract_text_features(text: list[str]) -> torch.Tensor
        Extracts text features from the input text list.
        
    extract_image_features(image_path: str) -> torch.Tensor
        Extracts image features from the image at the provided file path.
    """

    def __init__(self, model_name='openai/clip-vit-base-patch32'):
        """
        Initializes the CLIPFeatureExtractor with a specified model.

        Parameters:
        -----------
        model_name : str
            The name or path of the pretrained CLIP model to load. Defaults to 'openai/clip-vit-base-patch32'.
        """
        # Load the CLIP model and processor
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def extract_text_features(self, text):
        """
        Extracts text features from the provided text inputs.

        Parameters:
        -----------
        text : list[str]
            A list of text strings from which to extract features.

        Returns:
        --------
        torch.Tensor
            A tensor containing the extracted text features.
        """
        # Tokenize the text input and get the embeddings
        inputs = self.processor(text=text, return_tensors="pt", padding=True)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        return text_features

    def extract_image_features(self, image_path):
        """
        Extracts image features from the image located at the provided file path.

        Parameters:
        -----------
        image_path : str
            The file path to the image from which to extract features.

        Returns:
        --------
        torch.Tensor
            A tensor containing the extracted image features.
        """
        # Load and preprocess the image
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        return image_features

# test
if __name__ == "__main__":
    feature_extractor = CLIPFeatureExtractor()
    text_features = feature_extractor.extract_text_features(["A photo of a cat","A photo of a dog","A photo of a pig"])
    image_features = feature_extractor.extract_image_features("cat.jpg")
    # print(image_features.shape) # (1, 512)
    # normalize features
    text_features /= text_features.norm(dim=-1, keepdim=True)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    # compute similarity
    similarity = text_features @ image_features.transpose(0,1)
    print(similarity) # 这里还没有进行归一化