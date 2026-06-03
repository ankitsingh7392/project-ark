import os

VERSION = "0.1.0"
MODEL_PATH = os.getenv("W2V_MODEL_PATH", "data/word2vec.kv")


def main():
    from matcher import ATSMatcher

    ATSMatcher(model_path=MODEL_PATH)
    print(f"ATS v{VERSION} ready. Model: {MODEL_PATH}")


if __name__ == "__main__":
    main()
