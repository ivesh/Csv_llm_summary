from transformers import pipeline

generator = pipeline('text-generation', model='distilgpt2', device=-1)

def get_description(header):
    prompt = (f"You are a helpful assistant. For each column header, write a short descriptive phrase "
              f"that explains what the column means.\n\n"
              "Example:\n"
              "Invoice_ID: a unique transaction identifier\n"
              "Vendor_Name: the supplier or vendor associated with the transaction\n"
              "Amount: monetary value of the transaction\n"
              "Payment_Date: date payment was made\n"
              f"Now describe this column:\n{header}:")
    results = generator(prompt, max_new_tokens=40, num_return_sequences=3)
    
    # Pick the first non-empty meaningful description
    for res in results:
        desc = res['generated_text'].split(f"{header}:")[-1].strip().split('\n')[0].split('.')[0]
        if desc and desc.lower() not in ['none', 'no description', 'unknown', '']:
            return desc
    return "No description available"

if __name__ == "__main__":
    headers = ["Invoice_ID", "Vendor_Name", "Amount", "Payment_Date"]
    descriptions = {h: get_description(h) for h in headers}

    with open('output.txt', 'w') as f:
        for header, desc in descriptions.items():
            f.write(f"{header}: {desc}\n")

    for header, desc in descriptions.items():
        print(f"{header}: {desc}")
