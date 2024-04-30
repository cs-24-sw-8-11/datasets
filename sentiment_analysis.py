import sys
import transformers

sentiment_pipeline = transformers.pipeline("sentiment-analysis")

res = sentiment_pipeline(sys.argv[1:])

for result in res:
    if result['label'] == "POSITIVE":
        print(result['score'])
    else:
        print(-result['score'])