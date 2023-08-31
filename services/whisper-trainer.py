from datasets import load_dataset, DatasetDict, concatenate_datasets

if __name__ == '__main__':
    common_voice = DatasetDict()

    common_voice["train"] = concatenate_datasets([
        load_dataset("google/fleurs", "he_il", split="train+validation"),
        load_dataset("google/fleurs", "en_us", split="train+validation"),
        load_dataset("google/fleurs", "ru_ru", split="train+validation")
    ])
    common_voice["test"] = concatenate_datasets([
        load_dataset("google/fleurs", "he_il", split="test"),
        load_dataset("google/fleurs", "en_us", split="test"),
        load_dataset("google/fleurs", "ru_ru", split="test")
    ])

    print(common_voice)