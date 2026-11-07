import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'serif'
import matplotlib.pyplot as plt
import fitz

fig, ax = plt.subplots(figsize=(4.82, 2.21), dpi=300)
fig.subplots_adjust(left=0.10, right=0.96, top=0.88, bottom=0.25)

categories = ['Blocked under\ndefault policy', 'Advisory anomaly\n(default policy)']
counts = [6, 1]
colors = ['#dc2626', '#f59e0b']

bars = ax.bar(categories, counts, color=colors, width=0.45, edgecolor='#1e293b', linewidth=0.8)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.18, str(int(yval)), ha='center', va='bottom', fontsize=9.5, fontweight='bold')

ax.set_ylim(0, 7.5)
ax.set_yticks(range(8))
ax.set_ylabel('Documented scenarios', fontsize=8.8, fontweight='bold')
ax.set_title('Reported adversarial scenario outcomes', fontsize=9.5, fontweight='bold', pad=8)
ax.grid(axis='y', linestyle='--', alpha=0.5, color='#e2e8f0')
ax.tick_params(axis='both', which='major', labelsize=8.2)

out_pdf = r'c:\Users\Ram\Documents\pipejack-platform\Research Paper\PIC2026\scenario_outcomes.pdf'
fig.savefig(out_pdf, format='pdf')
plt.close(fig)

doc = fitz.open(out_pdf)
words = doc[0].get_text('words')
rects = [fitz.Rect(w[:4]) for w in words]
coll = 0
for a in range(len(rects)):
    for b in range(a + 1, len(rects)):
        r_int = rects[a] & rects[b]
        if not r_int.is_empty and r_int.width > 0.5 and r_int.height > 0.5:
            coll += 1
print('scenario_outcomes words:', len(words), 'collisions:', coll)
