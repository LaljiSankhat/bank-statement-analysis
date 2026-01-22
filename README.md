docker build -t bank-statement-app .




docker run \
  --name bank-statement-container \
  -p 8000:8000 \
  -e GEMINI_API_KEY="AIzaSyCWc-7tJ3niIcm3TwzIQnDvF0748IJP6YQ" \
  bank-statement-app