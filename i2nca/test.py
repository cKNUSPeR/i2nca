import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



fig5 = plt.figure(figsize=[10, 10])#constrained_layout=True)
widths = [1, 1]
heights = [1, 6, 6]
spec5 = fig5.add_gridspec(ncols=2, nrows=3, width_ratios=widths,
                          height_ratios=heights)
# big box for text
axbig = fig5.add_subplot(spec5[0, 0:2])
axbig.xaxis.set_major_locator(ticker.NullLocator())
axbig.yaxis.set_major_locator(ticker.NullLocator())



axbig.text(0.5, 0.5, f'centroid spectrum of name)', ha="center", va="bottom", size="x-large")

axbig.text(0.025, 0.1, "Theo. m/z: value", ha="left", va="bottom", size="large", color="red")
axbig.text(0.5, 0.1, "most abun. signal: value", ha="center", va="bottom", size="large", color="green")
axbig.text(0.975, 0.1, "weighted avg.: value", ha="right", va="bottom", size="large", color="purple")


ax1 = fig5.add_subplot(spec5[1,0])

ax2 = fig5.add_subplot(spec5[1,1])
ax3 = fig5.add_subplot(spec5[2,0])
ax4 = fig5.add_subplot(spec5[2,1])

fig5.show()