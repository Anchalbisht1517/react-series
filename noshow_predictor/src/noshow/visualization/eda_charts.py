"""EDA chart generator for the no-show predictor.

Loads ``data/processed/cleaned_appointments_v3.csv`` and produces
static plots saved under ``outputs/plots/``.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from noshow.logger import get_logger
from noshow.exception import NoShowException
from noshow.config import project_config

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Aesthetics
# ---------------------------------------------------------------------------
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 11

PLOT_DIR = os.path.join(project_config.ROOT_DIR, "outputs", "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Data loader
# ---------------------------------------------------------------------------

def _load_processed() -> pd.DataFrame:
    path = os.path.join(
        project_config.ROOT_DIR,
        project_config.config.get("data", {}).get(
            "processed_path", "data/processed/cleaned_appointments_v3.csv"
        )
    )
    if not os.path.exists(path):
        raise NoShowException(
            f"Processed dataset not found at {path}. "
            "Run the data pipeline first (Phase 2)."
        )
    df = pd.read_csv(path)
    logger.info(f"Loaded processed data for EDA: {df.shape}")
    return df

# ---------------------------------------------------------------------------
# Individual chart builders
# ---------------------------------------------------------------------------

def plot_class_distribution(df: pd.DataFrame, save: bool = True):
    """Bar chart of NoShow class counts."""
    fig, ax = plt.subplots()
    order = [0, 1] if df["NoShow"].isin([0, 1]).all() else ["No", "Yes"]
    palette = ["#66c2a5", "#fc8d62"]
    sns.countplot(data=df, x="NoShow", order=order, hue="NoShow", palette=palette, ax=ax, legend=False)
    ax.set_title("No-Show Class Distribution")
    ax.set_xlabel("NoShow (0 = attended, 1 = missed)")
    ax.set_ylabel("Count")
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                    ha="center", va="bottom")
    plt.tight_layout()
    if save:
        out = os.path.join(PLOT_DIR, "class_distribution.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved: {out}")
        plt.close(fig)
    return fig


def plot_sms_received_distribution(df: pd.DataFrame, save: bool = True):
    """SMS reminder distribution."""
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="SMS_received", hue="SMS_received", palette="pastel", ax=ax, legend=False)
    ax.set_title("SMS Received Distribution")
    ax.set_xlabel("SMS_received (0 = no, 1 = yes)")
    ax.set_ylabel("Count")
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                    ha="center", va="bottom")
    plt.tight_layout()
    if save:
        out = os.path.join(PLOT_DIR, "sms_received_distribution.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved: {out}")
        plt.close(fig)
    return fig


def plot_wait_bucket_no_show(df: pd.DataFrame, save: bool = True):
    """No-show rate by wait bucket."""
    if "wait_bucket" not in df.columns:
        logger.warning("wait_bucket column missing — skipping plot.")
        return None

    fig, ax = plt.subplots()
    bucket_order = ["0-7", "8-14", "15-30", "31-60", "60+"]
    rate = (
        df.groupby("wait_bucket")["NoShow"]
        .mean()
        .reindex(bucket_order)
    )
    rate.plot(kind="bar", color="steelblue", ax=ax)
    ax.set_title("No-Show Rate by Wait Bucket")
    ax.set_xlabel("Wait Bucket (days)")
    ax.set_ylabel("No-Show Rate")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=0)
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height):
            ax.annotate(f"{height:.2%}", (p.get_x() + p.get_width() / 2., height),
                        ha="center", va="bottom")
    plt.tight_layout()
    if save:
        out = os.path.join(PLOT_DIR, "wait_bucket_no_show.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved: {out}")
        plt.close(fig)
    return fig


def plot_no_show_by_weekday(df: pd.DataFrame, save: bool = True):
    """No-show rate by appointment weekday."""
    if "appointment_weekday" not in df.columns:
        logger.warning("appointment_weekday column missing — skipping plot.")
        return None

    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    fig, ax = plt.subplots()
    rate = df.groupby("appointment_weekday")["NoShow"].mean()
    rate = rate.reindex(range(7))
    rate.index = weekday_labels[:len(rate)]
    rate.plot(kind="bar", color="coral", ax=ax)
    ax.set_title("No-Show Rate by Appointment Weekday")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("No-Show Rate")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=0)
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height):
            ax.annotate(f"{height:.2%}", (p.get_x() + p.get_width() / 2., height),
                        ha="center", va="bottom")
    plt.tight_layout()
    if save:
        out = os.path.join(PLOT_DIR, "no_show_by_weekday.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved: {out}")
        plt.close(fig)
    return fig


def plot_no_show_by_age_group(df: pd.DataFrame, save: bool = True):
    """No-show rate by age group."""
    if "age_group" not in df.columns:
        logger.warning("age_group column missing — skipping plot.")
        return None

    fig, ax = plt.subplots()
    age_order = ["Child", "Teen", "Adult", "Senior", "Elderly"]
    rate = df.groupby("age_group")["NoShow"].mean().reindex(age_order)
    rate.plot(kind="bar", color="mediumseagreen", ax=ax)
    ax.set_title("No-Show Rate by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("No-Show Rate")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=0)
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height):
            ax.annotate(f"{height:.2%}", (p.get_x() + p.get_width() / 2., height),
                        ha="center", va="bottom")
    plt.tight_layout()
    if save:
        out = os.path.join(PLOT_DIR, "no_show_by_age_group.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved: {out}")
        plt.close(fig)
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, save: bool = True):
    """Correlation heatmap on numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        logger.warning("No numeric columns found for heatmap.")
        return None

    fig, ax = plt.subplots(figsize=(12, 10))
    corr = numeric_df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
                vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap (Numeric Features)")
    plt.tight_layout()
    if save:
        out = os.path.join(PLOT_DIR, "correlation_heatmap.png")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        logger.info(f"Saved: {out}")
        plt.close(fig)
    return fig

# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def generate_all_eda_plots() -> None:
    """Run every EDA chart and save to ``outputs/plots/``."""
    try:
        df = _load_processed()
        plot_class_distribution(df)
        plot_sms_received_distribution(df)
        plot_wait_bucket_no_show(df)
        plot_no_show_by_weekday(df)
        plot_no_show_by_age_group(df)
        plot_correlation_heatmap(df)
        logger.info("All EDA plots generated successfully.")
    except Exception as e:
        logger.error(f"EDA plot generation failed: {e}")
        raise NoShowException("EDA plot generation failed", sys.exc_info()) from e


if __name__ == "__main__":
    generate_all_eda_plots()
