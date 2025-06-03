import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

def create_erd():
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set background color
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Set axis limits
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    
    # Create entity boxes
    crab_population = patches.Rectangle((1, 3.5), 3, 2, linewidth=2, edgecolor='#1e3a8a', facecolor='#dbeafe', alpha=0.7)
    settings = patches.Rectangle((6, 3.5), 3, 2, linewidth=2, edgecolor='#1e3a8a', facecolor='#dbeafe', alpha=0.7)
    
    # Add entity boxes to plot
    ax.add_patch(crab_population)
    ax.add_patch(settings)
    
    # Add entity titles
    ax.text(2.5, 5.2, 'crab_population', ha='center', fontsize=12, fontweight='bold', color='#1e3a8a')
    ax.text(7.5, 5.2, 'settings', ha='center', fontsize=12, fontweight='bold', color='#1e3a8a')
    
    # Add attributes to crab_population
    attributes_crab = [
        'id (PK)',
        'population',
        'latitude',
        'longitude',
        'timestamp'
    ]
    
    for i, attr in enumerate(attributes_crab):
        y_pos = 4.8 - i * 0.3
        if 'PK' in attr:
            ax.text(1.2, y_pos, attr, fontsize=10, fontweight='bold')
        else:
            ax.text(1.2, y_pos, attr, fontsize=10)
    
    # Add attributes to settings
    attributes_settings = [
        'key (PK)',
        'value',
        'category',
        'description'
    ]
    
    for i, attr in enumerate(attributes_settings):
        y_pos = 4.8 - i * 0.3
        if 'PK' in attr:
            ax.text(6.2, y_pos, attr, fontsize=10, fontweight='bold')
        else:
            ax.text(6.2, y_pos, attr, fontsize=10)
    
    # Add title
    ax.text(5, 5.8, 'Blue Crab GIS - Entity Relationship Diagram', ha='center', fontsize=14, fontweight='bold', color='#1e3a8a')
    
    # Save the ERD
    plt.savefig('assets/erd.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

if __name__ == "__main__":
    create_erd()
