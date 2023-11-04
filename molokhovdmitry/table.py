import argparse
from transformers import TapexTokenizer, BartForConditionalGeneration
import pandas as pd

def main():
    # Load the model and the tokenizer
    global model
    global tokenizer
    tokenizer = TapexTokenizer.from_pretrained("microsoft/tapex-base-finetuned-wikisql")
    model = BartForConditionalGeneration.from_pretrained("microsoft/tapex-base-finetuned-wikisql")

    if file_path != "example" and query != "example":
        table = pd.read_csv(file_path, encoding='ISO-8859-1')

        # Does not work with huge tables
        table = table.iloc[:20]

        # Does not work with floats and NaN values so we convert everythong to strings
        table.fillna(0, inplace=True)
        for col in table.columns:
            if table[col].dtype != str:
                table[col] = table[col].astype(str)
        print(table)

        # Get an answer
        encoding = tokenizer(table=table, query=query, return_tensors="pt")
        outputs = model.generate(**encoding)
        print(tokenizer.batch_decode(outputs, skip_special_tokens=True))

    else:
        print_example()

def print_example():
    """Example from Hugging Face."""

    data = {
    "year": [1896, 1900, 1904, 2004, 2008, 2012],
    "city": ["athens", "paris", "st. louis", "athens", "beijing", "london"]
    }
    table = pd.DataFrame.from_dict(data)
    print(table)

    query = "In which year did beijing host the Olympic Games?"
    encoding = tokenizer(table=table, query=query, return_tensors="pt")

    outputs = model.generate(**encoding)

    print(f"Query: {query}")
    print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
    # [' 2008.0']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get csv file name and query")

    parser.add_argument("file", default=None, help="Path to the CSV file")
    parser.add_argument("query", default=None, help="Question to answer")

    args = parser.parse_args()
    file_path = args.file
    query = args.query

    main()
