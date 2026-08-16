from transformers import pipeline

# 1. ჩავტვირთოთ მოდელი (შეგიძლია შეცვალო ნებისმიერი Open-Source მოდელით)
print("ტვირთება AI მოდელი, გთხოვთ დაელოდოთ...")
ai_bot = pipeline("text-generation", model="gpt2")

# 2. მივცეთ ტექსტის დასაწყისი (Prompt)
prompt = "Artificial Intelligence is"

print(f"\n[+] AI გენერირებს პასუხს ტექსტზე: '{prompt}'...\n")

# 3. AI-ს მიერ ტექსტის გაგრძელება
results = ai_bot(prompt, max_length=50, num_return_sequences=1)

print("--- AI-ს პასუხი ---")
print(results[0]['generated_text'])