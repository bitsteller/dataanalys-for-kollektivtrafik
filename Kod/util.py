from __future__ import annotations

from typing import Iterable

import pandas as pd
from IPython.display import Markdown, display
from plotnine import (
    aes,
    coord_flip,
    geom_boxplot,
    geom_density,
    geom_histogram,
    geom_vline,
    ggplot,
    labs,
    stat_ecdf,
    theme_minimal,
)


def plot_distribution_grid(title: str, data_sample: Iterable[float]):
    """Plot histogram, density, ECDF, and boxplot in a 2x2 grid with plotnine."""
    values = pd.Series(data_sample, dtype="float64").dropna()
    if values.empty:
        raise ValueError("data_sample must contain at least one non-null numeric value.")

    plot_df = pd.DataFrame({"value": values})
    plot_df["group"] = "sample"
    mean_value = float(values.mean())
    median_value = float(values.median())
    std_value = float(values.std(ddof=1))
    quantile_df = pd.DataFrame(
        {"q": values.quantile([0.25, 0.5, 0.75]).to_numpy()}
    )

    p_hist = (
        ggplot(plot_df, aes(x="value"))
        + geom_histogram(bins=30, fill="#4C72B0", color="white")
        + geom_vline(xintercept=mean_value, color="#D55E00", linetype="dashed")
        + geom_vline(xintercept=median_value, color="#009E73", linetype="dotted")
        + labs(title="Histogram", x="Värde", y="Antal")
        + theme_minimal()
    )
    p_density = (
        ggplot(plot_df, aes(x="value"))
        + geom_density(fill="#C44E52", alpha=0.6)
        + geom_vline(xintercept=mean_value, color="#D55E00", linetype="dashed")
        + geom_vline(xintercept=median_value, color="#009E73", linetype="dotted")
        + labs(title="Densitet", x="Värde", y="Densitet")
        + theme_minimal()
    )
    p_ecdf = (
        ggplot(plot_df, aes(x="value"))
        + stat_ecdf(geom="step", color="#55A868")
        + geom_vline(
            quantile_df,
            aes(xintercept="q"),
            linetype="dashed",
            color="#8172B3",
            alpha=0.8,
        )
        + labs(title="Kumulativ fördelning", x="Värde", y="Andel")
        + theme_minimal()
    )
    p_box = (
        ggplot(plot_df, aes(x="group", y="value"))
        + geom_boxplot(fill="#8172B3", outlier_alpha=0, width=0.25)
        + coord_flip()
        + labs(title="Boxplot", x="", y="Värde")
        + theme_minimal()
    )

    combined_plot = (p_hist | p_ecdf) / (p_density | p_box)
    print(f"* Medelvärde: {mean_value:.3f}, Median: {median_value:.3f}")
    print(f"* Standardavvikelse: {std_value:.3f}")
    display(Markdown(f"### {title}"))
    display(combined_plot)
