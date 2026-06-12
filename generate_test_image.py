from PIL import Image, ImageDraw

# Sheet settings
WIDTH, HEIGHT = 800, 1200
MARGIN_LEFT = 150
MARGIN_TOP = 100
ROW_SPACING = 100
COL_SPACING = 100
RADIUS = 30

# Answers we want to fill (Q1:A, Q2:B, Q3:C, Q4:D, Q5:A, Q6:B, Q7:C, Q8:D, Q9:A, Q10:B)
filled_answers = ['A','B','C','D','A','B','C','D','A','B']
options = ['A','B','C','D']

img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
draw = ImageDraw.Draw(img)

for q_num in range(10):
    y = MARGIN_TOP + q_num * ROW_SPACING
    # Draw question number
    draw.text((20, y - 10), f"Q{q_num+1}", fill='black')
    for i, opt in enumerate(options):
        x = MARGIN_LEFT + i * COL_SPACING
        # Draw circle outline
        draw.ellipse([x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS], outline='black', width=3)
        # Fill circle if it matches the answer for this question
        if opt == filled_answers[q_num]:
            draw.ellipse([x - RADIUS+5, y - RADIUS+5, x + RADIUS-5, y + RADIUS-5], fill='black')

img.save('test_sheet.png')
print("test_sheet.png created.")