from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

with app.app_context():
    battalions = Battalion.query.all()
    print(f'Total battalions: {len(battalions)}\n')
    
    for b in battalions:
        print(f'=== Battalion {b.battalion_number}: {b.name} ===')
        print(f'Location: {b.district}')
        print(f'Commandant: {b.commandant_name} ({b.commandant_rank})')
        if b.organizational_structure:
            print(f'Org Structure:\n{b.organizational_structure[:600]}...\n')
        else:
            print('Org Structure: None\n')
        print('-' * 80)
