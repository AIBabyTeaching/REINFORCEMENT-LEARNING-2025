"""Plotting helpers for labs."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np


FIGURES_DIR = Path(__file__).resolve().parents[1] / "assets" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def save_curve(x: Sequence[float], y: Sequence[float], title: str, filename: str) -> Path:
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Value")
    fig.tight_layout()
    output_path = FIGURES_DIR / filename
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def save_heatmap(
    matrix: np.ndarray,
    title: str,
    filename: str,
    cmap: str = "viridis",
    annotations: bool = False,
) -> Path:
    fig, ax = plt.subplots()
    cax = ax.imshow(matrix, cmap=cmap, origin="upper")
    ax.set_title(title)
    fig.colorbar(cax, ax=ax)
    if annotations:
        for (y, x), value in np.ndenumerate(matrix):
            ax.text(x, y, f"{value:.2f}", ha="center", va="center", color="white")
    fig.tight_layout()
    output_path = FIGURES_DIR / filename
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def multi_curve(curves: Iterable[Sequence[float]], labels: Iterable[str], title: str, filename: str) -> Path:
    fig, ax = plt.subplots()
    for y, label in zip(curves, labels):
        ax.plot(y, label=label)
    ax.set_title(title)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.legend()
    fig.tight_layout()
    output_path = FIGURES_DIR / filename
    fig.savefig(output_path)
    plt.close(fig)
    return output_path
