import sqlite3

conn = sqlite3.connect('instance/apsp.db')
cursor = conn.cursor()

cursor.execute('SELECT battalion_number, name, organizational_structure FROM battalion ORDER BY battalion_number')
rows = cursor.fetchall()

print(f'Total battalions: {len(rows)}\n')

for r in rows:
    print(f'=== Battalion {r[0]}: {r[1]} ===')
    if r[2]:
        # Show first 700 characters to see the pattern
        print(f'Org Structure:\n{r[2][:700]}')
        print('...\n')
    else:
        print('Org Structure: None\n')
    print('-' * 80)

conn.close()
