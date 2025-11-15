---
tags:
  - prompt
  - prompt/technical
  - prompt/analytical
---
## Prompt Details

## The Results of Prompts

![[Pasted image 20251115084048.png | 600]]
![[Pasted image 20251115084244.png | 600]]
![[WhatsApp Image 2025-11-15 at 08.36.55_78b7564a.jpg | 300]]

### The Gradio Codes Generated 
```
"""
Gradio Web App for Bird Species Classification with ConvNeXt V2 Models
This application provides a user-friendly web interface for classifying bird species
using fine-tuned ConvNeXt V2 models (Tiny, Base, Large) trained with advanced techniques:
- ImageNet-22k pre-trained weights
- Hybrid class imbalance handling
- Advanced data augmentation (TrivialAugment, Mixup, CutMix)
- Cosine annealing scheduler with warmup
- Label smoothing and gradient clipping
- Automatic Mixed Precision (AMP)
The app allows users to:
- Upload bird images for classification
- Select from multiple ConvNeXt V2 models
- View Top-5 predictions with confidence scores
- See model performance metrics
Author: COS30082 Assignment 1
Deployed on: HuggingFace Spaces
"""

# Import necessary libraries
import gradio as gr
import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import json
import timm


# =============================================================================
# CONFIGURATION
# =============================================================================

# Model configurations
MODELS = {
    'ConvNeXt V2 Tiny': {
        'variant': 'convnextv2_tiny.fcmae_ft_in22k_in1k',
        'path': 'convnextv2_tiny.pth',
        'params': '28M',
        'expected_acc': '82-85%'
    },
    'ConvNeXt V2 Base': {
        'variant': 'convnextv2_base.fcmae_ft_in22k_in1k',
        'path': 'convnextv2_base.pth',
        'params': '89M',
        'expected_acc': '87-90%'
    },
    'ConvNeXt V2 Large': {
        'variant': 'convnextv2_large.fcmae_ft_in22k_in1k',
        'path': 'convnextv2_large.pth',
        'params': '198M',
        'expected_acc': '90-92%'
    }
}

# Paths
CLASSES_PATH = 'classes.txt'
METRICS_PATH = 'model_metrics.json'

# Image preprocessing parameters
IMG_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_class_names(class_file_path):
    """
    Read bird species names from text file
    Args:
        class_file_path (str): Path to classes.txt
    Returns:
        list: List of bird species names
    """
    try:
        with open(class_file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"ERROR: Classes file not found at {class_file_path}")
        return [f"Class_{i}" for i in range(200)]


def load_model_metrics(metrics_path):
    """
    Load model performance metrics
    Args:
        metrics_path (str): Path to metrics JSON file
    Returns:
        dict: Model metrics
    """
    try:
        with open(metrics_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"WARNING: Metrics file not found at {metrics_path}")
        return {}


def load_model(model_name, num_classes=200):
    """
    Load a ConvNeXt V2 model with trained weights
    Args:
        model_name (str): Name of the model (e.g., 'ConvNeXt V2 Tiny')
        num_classes (int): Number of output classes
    Returns:
        tuple: (model, device, model_info)
    """
    if model_name not in MODELS:
        raise ValueError(f"Unknown model: {model_name}")

    model_config = MODELS[model_name]
    model_path = model_config['path']

    # Determine device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    try:
        # Create model architecture
        model = timm.create_model(
            model_config['variant'],
            pretrained=False,
            num_classes=num_classes
        )

        # Load trained weights
        if os.path.exists(model_path):
            model.load_state_dict(torch.load(model_path, map_location=device))
            print(f"Loaded model: {model_name} from {model_path}")
        else:
            print(f"WARNING: Model weights not found at {model_path}. Using random weights.")

        # Move to device and set to evaluation mode
        model = model.to(device)
        model.eval()

        return model, device, model_config

    except Exception as e:
        print(f"ERROR loading model {model_name}: {e}")
        return None, device, model_config


# =============================================================================
# MODEL LOADING
# =============================================================================

# Load class names
class_names = load_class_names(CLASSES_PATH)
print(f"Loaded {len(class_names)} bird species names")

# Load model metrics
model_metrics = load_model_metrics(METRICS_PATH)

# Pre-load first model (default)
current_model_name = list(MODELS.keys())[0]
current_model, device, current_model_info = load_model(current_model_name, num_classes=len(class_names))

print(f"Default model loaded: {current_model_name}")
print(f"Device: {device}")


# =============================================================================
# PREDICTION FUNCTION
# =============================================================================

def predict(image, model_name):
    """
    Predict bird species from uploaded image
    Args:
        image (PIL.Image): Input bird image
        model_name (str): Selected model name
    Returns:
        tuple: (prediction_dict, model_info_html)
    """
    global current_model, current_model_name, current_model_info

    # Check if model needs to be changed
    if model_name != current_model_name:
        print(f"Switching model from {current_model_name} to {model_name}")
        current_model, _, current_model_info = load_model(model_name, num_classes=len(class_names))
        current_model_name = model_name

    if current_model is None:
        return {"Error": "Model not loaded"}, "Model loading error"

    try:
        # Preprocess image
        transform = transforms.Compose([
            transforms.Resize(IMG_SIZE + 32),
            transforms.CenterCrop(IMG_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=MEAN, std=STD)
        ])

        # Convert to RGB
        image = image.convert("RGB")

        # Transform and add batch dimension
        image_tensor = transform(image).unsqueeze(0).to(device)

        # Run inference
        with torch.no_grad():
            outputs = current_model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]

        # Get top-5 predictions
        top5_probs, top5_indices = torch.topk(probabilities, k=min(5, len(class_names)))

        # Create prediction dictionary with species names and class numbers
        predictions = {}
        for prob, idx in zip(top5_probs, top5_indices):
            class_id = idx.item()
            species_name = class_names[class_id]
            confidence = prob.item()

            # Format: "Species Name (Class ID)"
            label = f"{species_name} (Class {class_id})"
            predictions[label] = float(confidence)

        # Create model info HTML
        model_info_html = create_model_info_html(model_name)

        return predictions, model_info_html

    except Exception as e:
        print(f"Prediction error: {e}")
        return {"Error": str(e)}, "Prediction failed"


def create_model_info_html(model_name):
    """
    Create HTML for model information display
    Args:
        model_name (str): Name of current model
    Returns:
        str: HTML string with model information
    """
    model_config = MODELS[model_name]

    # Get metrics for this model if available
    metrics = model_metrics.get(model_name, {})
    top1_acc = metrics.get('top1_accuracy', 'N/A')
    avg_per_class = metrics.get('avg_per_class_accuracy', 'N/A')

    # Format accuracy values
    if isinstance(top1_acc, (int, float)):
        top1_acc = f"{top1_acc:.2f}%"
    if isinstance(avg_per_class, (int, float)):
        avg_per_class = f"{avg_per_class:.2f}%"

    html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h3 style="margin-top: 0; font-size: 1.3em;">📊 Model Performance</h3>
        <div style="background: rgba(255,255,255,0.1);
                    padding: 15px;
                    border-radius: 10px;
                    margin-top: 10px;">
            <p style="margin: 5px 0; font-size: 1.1em;">
                <strong>Model:</strong> {model_name}
            </p>
            <p style="margin: 5px 0; font-size: 1.1em;">
                <strong>Parameters:</strong> {model_config['params']}
            </p>
            <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 10px 0;">
            <p style="margin: 5px 0; font-size: 1.1em;">
                <strong>Top-1 Accuracy:</strong> {top1_acc}
            </p>
            <p style="margin: 5px 0; font-size: 1.1em;">
                <strong>Avg Per-Class Accuracy:</strong> {avg_per_class}
            </p>
            <p style="margin: 5px 0; font-size: 0.9em; color: #e0e0e0; margin-top: 10px;">
                Expected accuracy range: {model_config['expected_acc']}
            </p>
        </div>
    </div>
    """

    return html


# =============================================================================
# GRADIO INTERFACE
# =============================================================================

# Custom CSS for professional appearance
css = """
/* Main container styling */
.gradio-container {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}
/* Title section with glassmorphism */
.title {
    text-align: center;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
/* Description card */
.description {
    text-align: center;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    color: #2c3e50;
}
/* Button styling */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 25px !important;
    font-weight: 600 !important;
    padding: 12px 30px !important;
}
.btn-secondary {
    background: #6c757d !important;
    border: none !important;
    border-radius: 25px !important;
    font-weight: 600 !important;
}
/* Dropdown styling */
.dropdown {
    border-radius: 10px !important;
}
"""

# Create Gradio interface
with gr.Blocks(css=css, theme=gr.themes.Soft(), title="Bird Species Classifier") as iface:

    # Title section
    gr.HTML("""
    <div class="title">
        <h1 style="color: #3498db; font-size: 2.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🦅 Bird Species Classification
        </h1>
        <p style="color: white; font-size: 1.2em; margin: 10px 0 0 0; opacity: 0.9;">
            Powered by ConvNeXt V2 - CUB-200 Dataset
        </p>
        <p style="color: white; font-size: 0.9em; margin: 5px 0 0 0; opacity: 0.7;">
            COS30082 Applied Machine Learning - Assignment 1
        </p>
    </div>
    """)

    # Description section
    gr.HTML("""
    <div class="description">
        <p style="margin: 0; font-size: 1.1em; color: black;">
            Upload an image of a bird to classify its species using state-of-the-art ConvNeXt V2 models.
            Select your preferred model and view the top 5 predictions with confidence scores.
        </p>
    </div>
    """)

    # Main content area
    with gr.Row():
        # Left column: Input
        with gr.Column(scale=1):
            # Model selector dropdown
            model_dropdown = gr.Dropdown(
                choices=list(MODELS.keys()),
                value=list(MODELS.keys())[0],
                label="🔧 Select Model",
                info="Choose which ConvNeXt V2 model to use for classification"
            )

            # Image upload
            image_input = gr.Image(
                type="pil",
                label="📷 Upload Bird Image",
                height=400,
                show_label=True
            )

            # Buttons
            with gr.Row():
                submit_btn = gr.Button("🔍 Classify Bird", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", variant="secondary", size="lg")

        # Right column: Output
        with gr.Column(scale=1):
            # Model info display
            model_info_display = gr.HTML(
                value=create_model_info_html(list(MODELS.keys())[0]),
                label="Model Information"
            )

            # Predictions display
            output_label = gr.Label(
                num_top_classes=5,
                label="🏆 Top 5 Predictions",
                show_label=True
            )

    # Examples section
    gr.Markdown("### 📋 Try These Examples")
    gr.Examples(
        examples=[],  # Add example image paths here when deploying
        inputs=image_input,
        label="Example Images"
    )

    # Instructions
    gr.HTML("""
    <div style="background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                color: white;">
        <h4 style="margin-top: 0;">📖 How to Use:</h4>
        <ol style="margin-bottom: 0; padding-left: 20px;">
            <li>Select a ConvNeXt V2 model from the dropdown (larger models = higher accuracy)</li>
            <li>Upload or drag & drop a bird image</li>
            <li>Click "Classify Bird" to get predictions</li>
            <li>View the top 5 most likely species with confidence scores</li>
        </ol>
        <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
            <strong>Note:</strong> Results show species name and class ID in format: "Species Name (Class ID)"
        </p>
    </div>
    """)

    # Event handlers
    submit_btn.click(
        fn=predict,
        inputs=[image_input, model_dropdown],
        outputs=[output_label, model_info_display]
    )

    clear_btn.click(
        fn=lambda: (None, create_model_info_html(list(MODELS.keys())[0])),
        inputs=None,
        outputs=[image_input, model_info_display]
    )

    # Update model info when model is changed
    model_dropdown.change(
        fn=lambda x: create_model_info_html(x),
        inputs=model_dropdown,
        outputs=model_info_display
    )

    # Footer
    gr.HTML("""
    <div style="text-align: center;
                padding: 20px;
                margin-top: 30px;
                color: white;
                opacity: 0.7;">
        <p>Built with ❤️ using Gradio | Trained on CUB-200 Dataset (200 North American bird species)</p>
        <p style="font-size: 0.9em;">Models: ConvNeXt V2 (Tiny: 28M, Base: 89M, Large: 198M parameters)</p>
    </div>
    """)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    if current_model is not None:
        print("\n" + "="*80)
        print("Launching Gradio Interface...")
        print("="*80)
        print(f"Loaded models: {len(MODELS)}")
        print(f"Number of classes: {len(class_names)}")
        print(f"Device: {device}")
        print("="*80 + "\n")

        # Launch the interface
        iface.launch(
            share=True,  # Create public URL for sharing
            server_name="0.0.0.0",  # Allow external access
            server_port=7860  # Default Gradio port
        )
    else:
        print("\n" + "="*80)
        print("ERROR: Could not load model!")
        print("="*80)
        print("Please ensure model weights are available in the deployment directory.")
        print("\nRequired files:")
        for model_name, config in MODELS.items():
            print(f"  - {config['path']}")
        print(f"  - {CLASSES_PATH}")
        print("="*80)
```
## The Prompt
```bash
for this project, you are to refer to the assignemnt pdf and the check the marking rubric from time to time. 

For the dataset, my plan for u is to create a python file to balance out the number of images per class since the dataset are imbalanced in the training set. I also plan to have a validation set. Be creative on how u can eplore the data
OR
study the dataset in the zip file that i put in the project folder.

Basically what we gonna do is we gonna get the models from libraries like pytorch. For this assignment, I want to use a few DivoV2 model. For the models I want u to keep them in their own respective files like their results, visualisation of the accuracy, loss learning rate graph, overfitting analysis(train - val with the overfitting threshold)

For the models, I plan to use DinoV2 and the rest of its version. No need to take all the version. I only want one .pth which is the .pth after the model is trained

any more ideas to make it better and simpler would be nice. 


Also, when we fine tune the model, my other main goal of this assignment is to get a highest accuracy as much as possible from each of the model with the right techniques. implement the best fine tuning techniques to have all the models to the the highest accuracy as possible as they can


After training the models, use gradio to make a website to test the trained model by deploying it on HuggingFace so make sure the app.py is as simple as it can get, where the user can upload the image and then at the side, it tells the user some kind of metrics or numbers to tell the user how close the image that they upload is close to a species that the model are trained. Basically, give the user the top 5 predictions with the name of the species of the bird and the class number. It should also rank how close they are with other classes of the iamges as well. For the classes, make sure to put the acutal name for it. For example, it class 145 is Eagle, it should display the name of the bird when trying to classify it. So, it should display top 1 accruacry and avg per class The models they choose from the pulldown menu

here is the example of the app.py taht will be deployed on HuiggingFace:
"""
Gradio Web App for Bird Species Classification with ResNet-50 (Timm Recipe)
This application provides a user-friendly web interface for classifying bird species
using a fine-tuned ResNet-50 model trained with advanced techniques including:
- Timm's advanced training recipe
- Cosine annealing scheduler with warmup
- Dropout regularization
- Early stopping
- Aggressive data augmentation
The app loads a pre-trained model and allows users to upload bird images
for real-time species classification with confidence scores.
"""

# Import necessary libraries for the web application
import gradio as gr  # For creating the web interface
import torch  # PyTorch for deep learning operations
import torchvision.transforms as transforms  # Image preprocessing transforms
from PIL import Image  # Python Imaging Library for image handling
import os  # Operating system interface for file operations
import timm  # PyTorch Image Models library for advanced model architectures

# Configuration constants - file paths for model and class labels
MODEL_PATH = 'best_resnet50_TIMM_RECIPE_model.pth'  # Path to the trained model weights
CLASSES_PATH = 'classes.txt'  # Path to file containing bird species names

def get_class_names(class_file_path):
    """
    Read bird species names from a text file.
    
    Args:
        class_file_path (str): Path to the text file containing class names
        
    Returns:
        list: List of bird species names (one per line)
    """
    with open(class_file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def load_model(model_path, num_classes=200):
    """
    Load the pre-trained ResNet-50 model with the correct architecture.
    
    This function creates a ResNet-50 model using timm library with:
    - No pre-trained weights (since we're loading our custom trained weights)
    - Specified number of output classes (200 bird species)
    - Dropout rate of 0.5 for regularization
    
    Args:
        model_path (str): Path to the saved model weights (.pth file)
        num_classes (int): Number of output classes (default: 200)
        
    Returns:
        tuple: (model, device) - Loaded model and computation device
    """
    # Determine the best available device (GPU if available, otherwise CPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Create ResNet-50 model with timm (matches training architecture)
    model = timm.create_model('resnet50', pretrained=False, num_classes=num_classes, drop_rate=0.5)
    
    # Load the trained weights from the saved model file
    model.load_state_dict(torch.load(model_path, map_location=device))
    
    # Move model to the appropriate device (GPU/CPU)
    model.to(device)
    
    # Set model to evaluation mode (disables dropout, batch norm updates)
    model.eval()
    
    return model, device

# --- MODEL LOADING SECTION ---
# Attempt to load the model and class names at startup
# If loading fails, the app will still start but show an error message
try:
    # Load bird species names from text file
    class_names = get_class_names(CLASSES_PATH)
    
    # Load the trained ResNet-50 model
    model, device = load_model(MODEL_PATH, num_classes=len(class_names))
    
    print("ResNet-50 (Timm Recipe) model and classes loaded successfully.")
except Exception as e:
    # If model loading fails, set model to None and print error
    model = None
    print(f"FATAL ERROR loading model: {e}")

def predict(image):
    """
    Predict bird species from an uploaded image.
    
    This function processes the input image through the same preprocessing
    pipeline used during training, then runs inference to get predictions.
    
    Args:
        image (PIL.Image): Input bird image uploaded by user
        
    Returns:
        dict: Dictionary mapping bird species names to confidence scores
              If model not loaded, returns error message
    """
    # Check if model was successfully loaded
    if model is None: 
        return {"Error": "Model not loaded."}
    
    # Define image preprocessing pipeline (must match training preprocessing)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize to model's expected input size
        transforms.ToTensor(),  # Convert PIL image to PyTorch tensor
        # Normalize using ImageNet statistics (standard for pre-trained models)
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Convert image to RGB format (ensures 3 channels)
    image = image.convert("RGB")
    
    # Apply preprocessing and add batch dimension (unsqueeze adds dimension for batch)
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    # Run inference without computing gradients (faster, uses less memory)
    with torch.no_grad():
        # Forward pass through the model
        outputs = model(image_tensor)
        
        # Convert raw logits to probabilities using softmax
        probabilities = torch.softmax(outputs, dim=1)[0]
    
    # Create dictionary mapping class names to confidence scores
    confidences = {class_names[i]: float(prob) for i, prob in enumerate(probabilities)}
    
    return confidences

# --- GRADIO WEB INTERFACE ---
# Define custom CSS styles for a modern, professional appearance
css = """
/* Main container styling - dark gradient background for better visual appeal */
.gradio-container {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}
/* Title section with glassmorphism effect - semi-transparent with blur */
.title {
    text-align: center;
    background: rgba(255, 255, 255, 0.1);  /* Semi-transparent white background */
    backdrop-filter: blur(10px);  /* Blur effect for glassmorphism */
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
}
/* Description card styling - clean white background with shadow */
.description {
    text-align: center;
    background: rgba(255, 255, 255, 0.95);  /* Nearly opaque white background */
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);  /* Soft shadow */
    color: #2c3e50;  /* Dark gray text for good contrast */
}
/* Primary button styling - gradient background with rounded corners */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 25px !important;  /* Fully rounded corners */
    font-weight: 600 !important;  /* Bold text */
}
/* Secondary button styling - gray background for secondary actions */
.btn-secondary {
    background: #6c757d !important;  /* Bootstrap gray color */
    border: none !important;
    border-radius: 25px !important;
    font-weight: 600 !important;
}
"""

# Create the Gradio web interface with custom styling
with gr.Blocks(css=css, theme=gr.themes.Soft()) as iface:
    # Title section with glassmorphism effect
    gr.HTML("""
    <div class="title">
        <h1 style="color: #3498db; font-size: 2.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            Bird Species Classification
        </h1>
        <p style="color: white; font-size: 1.2em; margin: 10px 0 0 0; opacity: 0.9;">
            Powered by ResNet-50 
        </p>
    </div>
    """)
    
    # Description section explaining the application
    gr.HTML("""
    <div class="description">
        <p style="margin: 0; font-size: 1.1em; color: black;">
            Upload an image to classify the bird species using a fine-tuned ResNet-50 model trained with an advanced recipe.
        </p>
    </div>
    """)
    
    # Main content area with two columns
    with gr.Row():
        # Left column: Image upload and control buttons
        with gr.Column(scale=1):
            # Image upload component - accepts PIL images, shows label
            image_input = gr.Image(
                type="pil",  # Expect PIL Image objects
                label="Upload Bird Image",
                height=400,  # Fixed height for consistent layout
                show_label=True
            )
            
            # Button row for user actions
            with gr.Row():
                # Primary action button for classification
                submit_btn = gr.Button("Classify Bird", variant="primary", size="lg")
                # Secondary action button to clear the image
                clear_btn = gr.Button("Clear", variant="secondary", size="lg")
        
        # Right column: Results display
        with gr.Column(scale=1):
            # Label component to display top 5 predictions with confidence scores
            output_label = gr.Label(
                num_top_classes=5,  # Show top 5 most confident predictions
                label="Top 5 Predictions",
                show_label=True
            )
    
    # --- EVENT HANDLERS ---
    # Connect the classify button to the predict function
    submit_btn.click(fn=predict, inputs=image_input, outputs=output_label)
    
    # Connect the clear button to clear the image input (lambda returns None)
    clear_btn.click(fn=lambda: None, inputs=None, outputs=image_input)

# --- MAIN EXECUTION ---
# This block runs when the script is executed directly (not imported)
if __name__ == "__main__":
    # Check if model was successfully loaded before starting the web interface
    if model is not None:
        # Launch the Gradio web interface
        # share=True creates a public URL for easy sharing and testing
        iface.launch(share=True)
    else:
        # If model loading failed, print error message instead of starting the interface
        print("Could not start Gradio interface because the model failed to load.")
        
each of the model folder, as far as my knowledge can go, it should have the model from pytorch or tensorflow, the hyperparameters, the evaluation metric (expecially the top-1 accuracy and the Average accuracy per class is used to assess the performance of an individual class), u can use other metrics like accuracy, number of epoch, time taken, th train loss, train acc, val loss, val acc and mor eif u want to add. 

When the models are in training, make sure the models use the dataset taht are already balanced through python file to balance out the number of images per class since the dataset are imbalanced in the training set. Again, dont forget about the validation set. When the models are in training, i want to see the progress bar appear in the terminal and make sure the progress bar looks clean and professional


and small note,after training the models, ui have to make sure taht my pc does not run out of space or the mdoels trained should not use up a lot of space on my local disk.


```


