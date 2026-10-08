"""Stage B is intentionally gated: no audited attention prediction export exists yet."""
if __name__ == "__main__":
    raise SystemExit(
        "Stage B pending. Export attention forecasts with observable cutoffs and protocol hash; "
        "validate using btcforecast.models.load_attention_predictions before comparison. "
        "The archived 3.40% MAPE is rolling one-step evidence only."
    )
