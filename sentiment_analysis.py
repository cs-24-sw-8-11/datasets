import sys
import transformers

sentiment_pipeline = transformers.pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

res = sentiment_pipeline(sys.argv[1:])

print(res)

for result in res:
    if result['score'] < .5:
        if result["label"].lower() == "positive":
            # low score should be neutral between 1 to 2, positive neutrals should be between 1.5 to 2
            print(result['score']+1.5) 
        else:
            # low score should be neutral between 1 to 2, negative neutrals should be between 1 to 1.5
            print(1-(result['score']+1)) 
    else:
        if result["label"].lower() == "positive":
            # positive should be between 2 to 3
            print(result['score']+2) 
        else:
            # negative should be between 0 to 1
            print(1-result['score']) 