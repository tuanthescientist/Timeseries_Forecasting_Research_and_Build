"""Stage A: explicit offline baseline run; default is synthetic demonstration."""
import argparse

from btcforecast.experiments import run_stage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=["DEMO", "BTC"], default="DEMO")
    args = parser.parse_args()
    print(run_stage("A", args.dataset))
