def write_run_log(entries: List[Tuple[str, ModelResponse]]) -> None:
    ensure_reports_dir()
    path = REPORTS_DIR / "run_log.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["prompt", "output", "latency_ms", "tokens_in", "tokens_out"])
        for prompt, resp in entries:
            w.writerow([
                prompt,
                resp.text,
                f"{resp.latency_ms:.3f}",
                resp.tokens_in,
                resp.tokens_out,
            ])
