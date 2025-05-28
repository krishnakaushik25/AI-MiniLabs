# KYC-Extraction-system-using-LLM and Vision-based models using  Fireworks-AI as the inference engine. 
It's a system to extract the KYC details from the document that you provide as input. It can accept US National passports and US state driving licenses as input. 
The way it works is as below 

1. Base encodes the image
2. Uses an OCR + Reasoning model approach to deliver the results
3. If there are any missing details, we seek the missing details from the Vision model + Reasoning model to complete the missing details using PyDantic validations.
4. Uses an exponential retry back-off strategy. 
