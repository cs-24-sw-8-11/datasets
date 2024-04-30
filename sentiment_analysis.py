import sys
import transformers

sentiment_pipeline = transformers.pipeline("sentiment-analysis")

res = sentiment_pipeline(sys.argv[1:])

for result in res:
    print(((1 if result['label'] == "POSITIVE" else 0) + result["score"])/2)