import sys
import transformers

sentiment_pipeline = transformers.pipeline("sentiment-analysis")

res = sentiment_pipeline(sys.argv[1:])

for result in res:
    if result['score'] < .5:
        if result["label"] == "POSITIVE":
            print(result['score']+1.5) # low score should be neutral between 1 to 2, positive neutrals should be between 1.5 to 2
        else:
            print(result['score']+1) # low score should be neutral between 1 to 2, negative neutrals should be between 1 to 1.5
    else:
        if result["score"] == "POSITIVE":
            print(result['score']+2) # positive should be between 2 to 3
        else:
            print(result['score']) # negative should be between 0 to 1