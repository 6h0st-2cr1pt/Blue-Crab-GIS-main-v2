import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

def create_erd():
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Set background color
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Set axis limits
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    
    # Create entity boxes
    observer_table = patches.Rectangle((1, 7), 3.5, 2.5, linewidth=2, edgecolor='#1e3a8a', facecolor='#dbeafe', alpha=0.7)
    location_table = patches.Rectangle((9.5, 7), 3.5, 2.5, linewidth=2, edgecolor='#1e3a8a', facecolor='#dbeafe', alpha=0.7)
    crab_data_table = patches.Rectangle((5, 3), 4, 3.5, linewidth=2, edgecolor='#1e3a8a', facecolor='#dbeafe', alpha=0.7)
    
    # Add entity boxes to plot
    ax.add_patch(observer_table)
    ax.add_patch(location_table)
    ax.add_patch(crab_data_table)
    
    # Add entity titles
    ax.text(2.75, 9.2, 'observers', ha='center', fontsize=12, fontweight='bold', color='#1e3a8a')
    ax.text(11.25, 9.2, 'locations', ha='center', fontsize=12, fontweight='bold', color='#1e3a8a')
    ax.text(7, 6.2, 'crab_data', ha='center', fontsize=12, fontweight='bold', color='#1e3a8a')
    
    # Add attributes to observers table
    attributes_observer = [
        'id (PK)',
        'name',
        'email',
        'organization'
    ]
    
    for i, attr in enumerate(attributes_observer):
        y_pos = 8.8 - i * 0.3
        if 'PK' in attr:
            ax.text(1.2, y_pos, attr, fontsize=10, fontweight='bold', color='#dc2626')
        else:
            ax.text(1.2, y_pos, attr, fontsize=10)
    
    # Add attributes to locations table
    attributes_location = [
        'id (PK)',
        'latitude',
        'longitude',
        'location_name',
        'region'
    ]
    
    for i, attr in enumerate(attributes_location):
        y_pos = 8.8 - i * 0.3
        if 'PK' in attr:
            ax.text(9.7, y_pos, attr, fontsize=10, fontweight='bold', color='#dc2626')
        else:
            ax.text(9.7, y_pos, attr, fontsize=10)
    
    # Add attributes to crab_data table
    attributes_crab = [
        'id (PK)',
        'date_month',
        'date_year',
        'juvenile_counts',
        'adult_counts',
        'male_counts',
        'female_counts',
        'population',
        'observer_id (FK)',
        'location_id (FK)',
        'created_at'
    ]
    
    for i, attr in enumerate(attributes_crab):
        y_pos = 5.8 - i * 0.25
        if 'PK' in attr:
            ax.text(5.2, y_pos, attr, fontsize=10, fontweight='bold', color='#dc2626')
        elif 'FK' in attr:
            ax.text(5.2, y_pos, attr, fontsize=10, fontweight='bold', color='#2563eb')
        else:
            ax.text(5.2, y_pos, attr, fontsize=10)
    
    # Draw relationships
    # Observer to Crab Data (One-to-Many)
    ax.annotate('', xy=(5, 5), xytext=(4.5, 8),
                arrowprops=dict(arrowstyle='->', lw=2, color='#2563eb'))
    ax.text(4, 6.5, '1:N', fontsize=10, fontweight='bold', color='#2563eb')
    
    # Location to Crab Data (One-to-Many)
    ax.annotate('', xy=(9, 5), xytext=(9.5, 8),
                arrowprops=dict(arrowstyle='->', lw=2, color='#2563eb'))
    ax.text(9.5, 6.5, '1:N', fontsize=10, fontweight='bold', color='#2563eb')
    
    # Add title
    ax.text(7, 9.5, 'Blue Crab GIS - Entity Relationship Diagram', ha='center', fontsize=16, fontweight='bold', color='#1e3a8a')
    
    # Add constraints note
    ax.text(7, 1.5, 'Constraints:', ha='center', fontsize=12, fontweight='bold', color='#dc2626')
    ax.text(7, 1.2, '• juvenile_counts + adult_counts = population', ha='center', fontsize=10, color='#dc2626')
    ax.text(7, 0.9, '• male_counts + female_counts = population', ha='center', fontsize=10, color='#dc2626')
    ax.text(7, 0.6, '• All count fields must be non-negative integers', ha='center', fontsize=10, color='#dc2626')
    
    # Add legend
    ax.text(1, 0.5, 'Legend:', fontsize=10, fontweight='bold')
    ax.text(1, 0.2, 'PK = Primary Key', fontsize=9, color='#dc2626')
    ax.text(3, 0.2, 'FK = Foreign Key', fontsize=9, color='#2563eb')
    
    # Save the ERD
    plt.savefig('assets/erd_new.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

if __name__ == "__main__":
    create_erd()
    print("ERD created successfully!")
