import model
import argparse


def main():
    pars = argparse.ArgumentParser()
    pars.add_argument('--input-dir', dest='filename')
    pars.add_argument('--model', dest='model')

    args = pars.parse_args()
    finalmodel = model.TxtGen()

    finalmodel.fit(args.model, args.filename)



if __name__ == "__main__":
    main()
