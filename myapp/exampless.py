from textblob import TextBlob
text=input('enter a text : ')
blob=TextBlob(text)
result=blob.sentiment.polarity
if result>0:
    print('pos')
elif result==0:
    print('normal')
else:
    print('neg')