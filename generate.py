import argparse
import model


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', dest='model')
    parser.add_argument('--prefix', dest='prefix')
    parser.add_argument('--length', dest='length')

    args = parser.parse_args()
    newText = model.TxtGen()

    print(*newText.generate(args.model, args.prefix, int(args.length)))


if __name__ == "__main__":
    main()
