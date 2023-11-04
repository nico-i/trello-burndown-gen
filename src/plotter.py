import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_burn_down(logger, df):
    # Set 'sprint day' as the index
    df.set_index('sprint day', inplace=True)

    # Plot the lines
    plt.figure(figsize=(10, 6))
    plt.plot([df.index[0], df.index[-1]],
             [df['actual work'][0], 0],
             label='Ideal Work', color='blue', linestyle='--')
    plt.plot(df.index, df['actual work'],
             label='Actual Work', color='red', marker='o')

    # Annotate the points on the 'actual work' line
    for index, row in df.iterrows():
        if row['label']:  # Check if there is a label for the row
            # Join multiple labels with a new line
            label = "\n".join(row['label'])
            plt.annotate(label,  # this is the text
                         # this is the point to label
                         (index, row['actual work']),
                         textcoords="offset points",  # how to position the text
                         xytext=(0, 10),  # distance from text to points (x,y)
                         ha='center')  # horizontal alignment can be left, right or center

    # Set the title and labels
    plt.title('Sprint Burndown Chart')
    plt.xlabel('Sprint Day')
    plt.ylabel('Story Points')

    # Show legend
    plt.legend()

    # Rotate dates on x-axis
    plt.xticks(rotation=45)
    # Set x-axis to show every day
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))

    # Set y-axis ticks
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    max_y_value = df['actual work'].max()
    top_margin = 2  # you can change this to whatever margin you want
    plt.ylim(top=max_y_value + top_margin)

    # Add a grid with transparency
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Adjust layout to prevent clipping of tick-labels
    plt.tight_layout()

    # Add margins to the plot
    plt.margins(x=0.075)

    # Show the plot
    plt.show()
