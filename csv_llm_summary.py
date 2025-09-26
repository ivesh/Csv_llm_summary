# filename: describe_headers.py

from transformers import pipeline

def generate_descriptions(headers):
    # Select a small offline model; distilbert is lightweight and fast.
    # For descriptive text generation, some models like 'distilgpt2' can be used.
    generator = pipeline('text-generation', model='distilgpt2')
    
    descriptions = {}
    for header in headers:
        # Prompt engineering for better description
        prompt = f"The column '{header}' in a dataset typically means:"
        # Set max_length to avoid long rambling outputs
        output = generator(prompt, max_length=40, num_return_sequences=1)[0]['generated_text']
        # Extract only generated description after the colon
        desc = output.split(':', 1)[-1].strip()
        descriptions[header] = desc

    return descriptions

def save_output(descriptions, filename='output.txt'):
    with open(filename, 'w') as f:
        for header, desc in descriptions.items():
            f.write(f"{header}: {desc}\n")
    print(f"Output saved to {filename}")

if __name__ == "__main__":
    # Hardcoded list based on example
    headers = ["Invoice_ID", "Vendor_Name", "Amount", "Payment_Date"]
    descriptions = generate_descriptions(headers)
    for header, desc in descriptions.items():
        print(f"{header}: {desc}")
    save_output(descriptions)
