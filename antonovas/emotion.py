from transformers import pipeline
model = pipeline(model="seara/rubert-tiny2-cedr-russian-emotion")
model("Привет, ты мне нравишься!")
# [{'label': 'joy', 'score': 0.9605025053024292}]
