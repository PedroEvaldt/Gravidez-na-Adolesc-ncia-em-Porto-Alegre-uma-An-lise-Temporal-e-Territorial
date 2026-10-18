import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6.2, 2.5), dpi=220)

labels = ["Brasil", "Porto Alegre"]
valores = [11.3, 6.16]
cores = ["#9aa7b8", "#2f6f9f"]

bars = ax.bar(labels, valores, color=cores, width=0.45)

for b, v in zip(bars, valores):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.35,
            f"{v:.2f}".replace(".", ",") + "%",
            ha="center", va="bottom", fontsize=11, fontweight="bold",
            color="#1b3a52")

ax.set_ylim(0, 14)
ax.set_ylabel("% dos nascidos vivos", fontsize=9)
ax.set_title("Nascidos vivos de mães com até 19 anos – 2025",
             fontsize=10.5, fontweight="bold", color="#1b3a52", pad=8)
ax.tick_params(axis="x", labelsize=10)
ax.tick_params(axis="y", labelsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#c9d2db")
ax.spines["bottom"].set_color("#c9d2db")
ax.yaxis.grid(True, color="#e6ebf0", linewidth=0.8)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("/home/claude/grafico.png", transparent=False, facecolor="white")
print("ok")
