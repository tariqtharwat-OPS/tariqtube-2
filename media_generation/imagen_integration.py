import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

def test_imagen():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tariq-worker-key.json"
    project_id = "tariqtube-production"
    location = "us-central1"
    
    vertexai.init(project=project_id, location=location)
    
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
    
    prompt = "A cute brave kitten standing on top of a mountain, children's book illustration style, vibrant colors."
    
    print(f"Generating image with Imagen 3.0: {prompt}")
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        # Default safety level
    )
    
    output_path = "imagen_test.png"
    images[0].save(location=output_path, include_generation_parameters=False)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    try:
        test_imagen()
        print("Imagen test successful!")
    except Exception as e:
        print(f"Imagen test failed: {e}")
