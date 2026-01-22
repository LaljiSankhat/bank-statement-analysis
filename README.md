docker build -t bank-statement-app .




docker run \
  --name bank-statement-container \
  -p 8000:8000 \
  -e GEMINI_API_KEY="Your API key" \
  bank-statement-app
